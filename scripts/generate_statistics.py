#!/usr/bin/env python3
"""Generate bilingual descriptive statistics from the public, frozen data.

The public CSVs can verify row-level counts and summaries. They cannot
reconstruct the search receipts, the MP4 bytes, or the SHA-256 deduplication.
Run with --check to detect stale pages without changing files.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "corpus-snapshot.json"
CASES = ROOT / "data" / "cases.csv"
CLASSIFIED = ROOT / "data" / "domain-style.csv"
OUTPUTS = (ROOT / "docs" / "statistics.md", ROOT / "docs" / "statistics.zh-CN.md")
POST_URL = re.compile(r"^https://x\.com/[^/]+/status/(\d+)$")
LABELS = {"yes", "likely", "no"}
CASE_COLUMNS = (
    "source_url", "primary_path", "label", "creator_disclosure",
    "hypit_observation", "review_note", "duration_s", "hypit_status",
)
CLASSIFIED_COLUMNS = (
    "post_url", "author", "opus_made", "domain", "style", "style2",
    "topic_en", "duration_s",
)
PATHS = (
    ("procedural_2d", "Code-drawn 2D", "程序二维逐帧绘图"),
    ("educational_explainer", "Educational explainer", "知识讲解"),
    ("3d_or_realtime_graphics", "3D or real-time graphics", "三维或实时图形"),
    ("existing_source_transformation", "Existing-source transformation", "现有素材改编"),
    ("external_video_model", "External video-model pipeline", "外部视频模型编排"),
    ("app_or_game_capture", "App or game capture", "应用或游戏录屏"),
    ("mixed_or_not_established", "Mixed or unestablished pipeline", "混合或流程未确定"),
)
DOMAINS = {
    "ai_self_meta": ("AI about AI", "AI 讲 AI"),
    "art_abstract": ("Art / abstract", "艺术／抽象"),
    "data_viz": ("Data visualization", "数据可视化"),
    "education_science": ("Education / science", "科普／教育"),
    "game_interactive": ("Games / interactive", "游戏／交互"),
    "history_culture": ("History / culture", "历史／文化"),
    "humor_meme": ("Humor / meme", "幽默／梗"),
    "music_video": ("Music video", "音乐视频"),
    "other": ("Other", "其他"),
    "product_ad": ("Ads / launches", "广告／发布片"),
    "story_short": ("Short story", "故事短片"),
}
STYLES = {
    "3d_render": ("3D render", "三维渲染"),
    "anime": ("Anime", "动漫"),
    "flat_vector_cartoon": ("Flat cartoon", "扁平卡通"),
    "generative_abstract": ("Generative abstract", "生成艺术"),
    "hand_drawn_sketch": ("Hand-drawn", "手绘"),
    "live_action": ("Live action", "真人"),
    "math_diagram": ("Math diagram", "数学图解"),
    "motion_graphics_ui": ("Motion graphics / UI", "动态图形／界面"),
    "painterly_ink_sand": ("Ink / sand / paint", "水墨／沙画／油彩"),
    "paper_cutout_collage": ("Paper cut-out", "纸片拼贴"),
    "photoreal": ("Photoreal", "写实"),
    "pixel_art": ("Pixel art", "像素"),
    "retro_terminal_ascii": ("Retro terminal / ASCII", "复古终端／ASCII"),
}

# These links illustrate evidence boundaries, not a random sample of a cell.
EXAMPLES = (
    (
        "https://x.com/Aurelien_Gz/status/2102786378282987591",
        "Clearwater", "Clearwater 水面",
        "A matching public WebGL source project supports the rendering route; the X preview does not reveal the full model conversation.",
        "匹配的公开 WebGL 工程可佐证渲染路径；X 预览不能还原完整模型对话。",
    ),
    (
        "https://x.com/ng169onX/status/2103183904563998809",
        "VAE explainer", "VAE 数学讲解",
        "The sampled frames show diagrams, while the training run, mathematical accuracy, and audio still require separate checks.",
        "九帧可见图解；训练过程、数学准确性和声音仍需另行核验。",
    ),
    (
        "https://x.com/jantijssen/status/2102861462461124755",
        "Externally rendered music video", "外部工具制作的音乐视频",
        "The creator assigns song, video clips, and editing to different tools; the classifier says `no`, so role and label must be read separately.",
        "作者把歌曲、视频片段和剪辑交给不同工具；分类器标为 `no`，应分别看模型分工与标签。",
    ),
    (
        "https://x.com/leogao25/status/2102544078927741369",
        "Two-model comparison", "双模型对照片",
        "The posted MP4 compares two outputs; it is not a full inspection of either underlying production run.",
        "帖子 MP4 并列展示两种输出，不等于验收任一模型的完整生产过程。",
    ),
    (
        "https://x.com/pradeepXkapoor/status/2102782449478668290",
        "Unfinished ink-film attempt", "未完成的水墨短片",
        "The creator calls the work unfinished despite a visible MP4; attachment presence is not a success measure.",
        "作者明确标为未完成，尽管有可见 MP4；有附件不等于成功交付。",
    ),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_csv(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == list(columns), f"Unexpected columns in {path.name}")
        rows = list(reader)
    require(bool(rows), f"Empty data file: {path.name}")
    return rows


def post_id(url: str) -> str:
    match = POST_URL.fullmatch(url)
    require(match is not None, f"Invalid X post URL: {url}")
    return match.group(1)


def duration(row: dict[str, str], name: str) -> float:
    try:
        value = float(row["duration_s"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid duration in {name}: {row.get('duration_s')!r}") from exc
    require(math.isfinite(value) and value > 0, f"Invalid duration in {name}: {value!r}")
    return value


def quartiles(values: list[float]) -> tuple[float, float, float]:
    require(len(values) > 1, "Quartiles require at least two values")
    q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
    return q1, statistics.median(values), q3


def percent(count: int, denominator: int) -> str:
    return f"{count / denominator * 100:.1f}%"


def example_cell(url: str, label: str, chinese: bool) -> str:
    """Link a single sampled preview still to its creator's original post."""
    identifier = post_id(url)
    thumbnail = ROOT / "assets" / "case-thumbnails" / f"{identifier}.webp"
    require(thumbnail.is_file(), f"Missing preview still for {identifier}")
    author = url.split("/")[3]
    alt = "X 预览取样截图" if chinese else "Sampled X preview frame"
    return (
        f'<a href="{url}"><img src="../assets/case-thumbnails/{identifier}.webp" '
        f'width="160" alt="{alt}"></a><br>@{html.escape(author)} · {html.escape(label)}'
    )


def summary() -> dict:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    cases = read_csv(CASES, CASE_COLUMNS)
    classified = read_csv(CLASSIFIED, CLASSIFIED_COLUMNS)

    for key in (
        "candidate_posts", "candidate_posts_with_mp4", "mp4_attachments",
        "sha256_distinct", "sha256_duplicate_groups",
        "sha256_duplicate_extra_attachments", "curated_cases",
        "domain_style_classified_files", "search_queries_saved",
        "search_queries_ok_or_cached",
    ):
        require(type(snapshot.get(key)) is int and snapshot[key] >= 0, f"Bad snapshot field: {key}")
    require(
        snapshot["candidate_posts_with_mp4"] <= snapshot["candidate_posts"],
        "Posts with MP4 exceed candidate posts",
    )
    require(
        snapshot["candidate_posts_with_mp4"] <= snapshot["mp4_attachments"],
        "Attachments fewer than posts with MP4",
    )
    require(
        snapshot["sha256_distinct"] + snapshot["sha256_duplicate_extra_attachments"]
        == snapshot["mp4_attachments"],
        "SHA distinct + exact duplicate extras do not equal attachments",
    )
    require(
        snapshot["search_queries_ok_or_cached"] <= snapshot["search_queries_saved"],
        "Successful queries exceed saved queries",
    )
    require(
        snapshot.get("hypit_status", {}).get("tile_ok") == snapshot["mp4_attachments"],
        "Snapshot media check count disagrees with attachments",
    )
    require(len(cases) == snapshot["curated_cases"], "Curated-case denominator mismatch")
    require(
        snapshot.get("curated_case_hypit_status", {}).get("tile_ok") == len(cases),
        "Curated tile count mismatch",
    )
    require(
        len(classified) == snapshot["domain_style_classified_files"] == snapshot["sha256_distinct"],
        "Classified-file denominator mismatch",
    )

    case_ids: set[str] = set()
    for row in cases:
        require(all(row.get(key, "").strip() for key in CASE_COLUMNS), "Blank required case field")
        identifier = post_id(row["source_url"])
        require(identifier not in case_ids, f"Duplicate curated post ID: {identifier}")
        case_ids.add(identifier)
        require(row["hypit_status"] == "tile_ok", f"Case lacks media check: {identifier}")
        duration(row, "cases.csv")
    require(
        {row["primary_path"] for row in cases} == {key for key, _, _ in PATHS},
        "Unrecognized or absent curated path",
    )

    files_by_post: dict[str, list[dict[str, str]]] = defaultdict(list)
    labels: Counter[str] = Counter()
    for row in classified:
        require(
            all(row.get(key, "").strip() for key in CLASSIFIED_COLUMNS if key != "style2"),
            "Blank required classifier field",
        )
        identifier = post_id(row["post_url"])
        require(row["opus_made"] in LABELS, f"Unknown classifier label: {row['opus_made']}")
        require(row["domain"] in DOMAINS, f"Unknown domain: {row['domain']}")
        require(row["style"] in STYLES, f"Unknown style: {row['style']}")
        duration(row, "domain-style.csv")
        files_by_post[identifier].append(row)
        labels[row["opus_made"]] += 1
    require(
        dict(labels) == snapshot.get("classifier_opus_made_labels"),
        "Classifier label counts disagree with the snapshot",
    )

    matched_labels: Counter[str] = Counter()
    for row in cases:
        matches = [
            file for file in files_by_post[post_id(row["source_url"])]
            if abs(duration(file, "domain-style.csv") - duration(row, "cases.csv")) <= 0.05
        ]
        require(
            len(matches) == 1,
            f"Expected exactly one post-and-duration match for {row['source_url']}; found {len(matches)}",
        )
        matched_labels[matches[0]["opus_made"]] += 1
    require(sum(matched_labels.values()) == len(cases), "Case-classifier join lost rows")
    for url, *_ in EXAMPLES:
        require(post_id(url) in case_ids, f"Illustrative case missing from CSV: {url}")

    strict = [row for row in classified if row["opus_made"] == "yes"]
    inclusive = [row for row in classified if row["opus_made"] in {"yes", "likely"}]
    strict_domains = Counter(row["domain"] for row in strict)
    inclusive_domains = Counter(row["domain"] for row in inclusive)
    strict_styles = Counter(row["style"] for row in strict)
    inclusive_styles = Counter(row["style"] for row in inclusive)
    cells = Counter((row["domain"], row["style"]) for row in inclusive)
    require(sum(strict_domains.values()) == len(strict), "Strict domain denominator mismatch")
    require(sum(inclusive_domains.values()) == len(inclusive), "Inclusive domain denominator mismatch")
    require(sum(strict_styles.values()) == len(strict), "Strict style denominator mismatch")
    require(sum(inclusive_styles.values()) == len(inclusive), "Inclusive style denominator mismatch")
    require(sum(cells.values()) == len(inclusive), "Cross-tab denominator mismatch")

    multi_posts = [rows for rows in files_by_post.values() if len(rows) > 1]
    return {
        "snapshot": snapshot, "cases": cases, "classified": classified,
        "labels": labels, "matched_labels": matched_labels,
        "strict": strict, "inclusive": inclusive,
        "strict_domains": strict_domains, "inclusive_domains": inclusive_domains,
        "strict_styles": strict_styles, "inclusive_styles": inclusive_styles,
        "cells": cells, "post_count": len(files_by_post),
        "multi_post_count": len(multi_posts),
        "multi_post_rows": sum(map(len, multi_posts)),
        "discordant_multi_posts": sum(
            len({row["opus_made"] for row in rows}) > 1 for rows in multi_posts
        ),
        "secondary_style_blank": sum(not row["style2"].strip() for row in classified),
    }


def render(data: dict, chinese: bool) -> str:
    lang = 1 if chinese else 0
    snapshot = data["snapshot"]
    cases = data["cases"]
    classified = data["classified"]
    strict = data["strict"]
    inclusive = data["inclusive"]
    sd = data["strict_domains"]
    idom = data["inclusive_domains"]
    ss = data["strict_styles"]
    istyle = data["inclusive_styles"]
    labels = data["labels"]
    matched = data["matched_labels"]
    top_cells = sorted(data["cells"].items(), key=lambda item: (-item[1], item[0]))[:10]
    path_data = [
        (en, zh, [duration(row, "cases.csv") for row in cases if row["primary_path"] == key])
        for key, en, zh in PATHS
    ]
    file_q = quartiles([duration(row, "domain-style.csv") for row in classified])
    case_q = quartiles([duration(row, "cases.csv") for row in cases])
    strict_top_domain = sorted(sd.items(), key=lambda item: (-item[1], item[0]))[0][0]
    inclusive_top_domain = sorted(idom.items(), key=lambda item: (-item[1], item[0]))[0][0]
    require(strict_top_domain != inclusive_top_domain, "Expected current-snapshot domain rank reversal is absent")
    require(
        {strict_top_domain, inclusive_top_domain} == {"product_ad", "game_interactive"},
        "Expected current-snapshot ad/game top ranks changed",
    )

    if chinese:
        lines = [
            "# 统计快照：单位、分母与敏感性", "",
            "[English](statistics.md) · 此页由 [`scripts/generate_statistics.py`](../scripts/generate_statistics.py) "
            "从公开 CSV 和[冻结快照](../data/corpus-snapshot.json)生成。运行 "
            "`python3 scripts/generate_statistics.py --check` 可检查页面是否与数据一致。", "",
            f"数据截点：{snapshot['snapshot_utc']}。以下是**检索样本的描述统计**，不是 X 全站作品普查、质量评分或模型成功率。", "",
            "图表由 [`scripts/generate_stat_charts.py`](../scripts/generate_stat_charts.py) 从相同公开数据生成；"
            "运行 `python3 scripts/generate_stat_charts.py --check` 可检查图表是否过期。", "",
            "## 先分清统计单位", "",
            "| 数字 | 单位 | 公开文件能否复算 |", "|---|---|---|",
            f"| {snapshot['search_queries_saved']:,}；其中成功或命中缓存 {snapshot['search_queries_ok_or_cached']:,} | 保存的检索查询 | 仅有汇总和[查询覆盖说明](search-coverage.zh-CN.md)，原始回执未公开。查询成功不等于覆盖全部作品。 |",
            f"| {snapshot['candidate_posts']:,} | 去重候选帖子 | 仅由冻结快照记录；候选原始表未公开。 |",
            f"| {snapshot['candidate_posts_with_mp4']:,} | 有 MP4 的候选帖子 | 仅由冻结快照记录。 |",
            f"| {snapshot['mp4_attachments']:,} | 取得并完成九帧抽样的 MP4 附件 | 仅由冻结快照记录；一个帖子可以有多个附件。 |",
            f"| {snapshot['sha256_distinct']:,} | 声称按 SHA-256 去重的 MP4 文件 | [分类 CSV](../data/domain-style.csv)可核对有 {len(classified):,} 行；未公开文件哈希或逐附件 ID，无法独立复算去重。 |",
            f"| {snapshot['curated_cases']:,} | 人工整理的原帖案例 | [案例 CSV](../data/cases.csv)可核对 {len(cases):,} 个唯一原帖 ID，均标为九帧抽样完成。 |",
            "", f"冻结快照还报告 {snapshot['sha256_duplicate_groups']} 个完全相同文件组、"
            f"{snapshot['sha256_duplicate_extra_attachments']} 个组内额外附件；"
            f"{snapshot['sha256_distinct']:,} + {snapshot['sha256_duplicate_extra_attachments']} = {snapshot['mp4_attachments']:,}。"
            "这项算术可核对，文件哈希本身不能从公开 CSV 重算。", "",
            "## 分类阈值会改变第一名", "",
            "视觉分类器根据帖文和九帧，为每个文件给出一个 `opus_made` 标签、一个主领域和一个主画风。"
            "这是模型判断，不是作者身份、模型调用或完整成片的独立验证。", "",
            "![分类器给出的各领域文件数；深蓝为 yes，橙色为 likely](../assets/domain-labels.svg)", "",
            "| 纳入口径 | 文件分母 | 游戏／交互 | 广告／发布片 | 第一名 |", "|---|---:|---:|---:|---|",
            f"| 只计 `yes` | {len(strict):,} | {sd['game_interactive']} ({percent(sd['game_interactive'], len(strict))}) | {sd['product_ad']} ({percent(sd['product_ad'], len(strict))}) | {DOMAINS[strict_top_domain][lang]} |",
            f"| 计 `yes` 和 `likely` | {len(inclusive):,} | {idom['game_interactive']} ({percent(idom['game_interactive'], len(inclusive))}) | {idom['product_ad']} ({percent(idom['product_ad'], len(inclusive))}) | {DOMAINS[inclusive_top_domain][lang]} |",
            "", f"全部 {len(classified):,} 个分类文件中：`yes` {labels['yes']:,}，"
            f"`likely` {labels['likely']:,}，`no` {labels['no']:,}。"
            f"严格与宽松口径分别占本次分类文件的 {percent(len(strict), len(classified))} 和 "
            f"{percent(len(inclusive), len(classified))}；**这两个百分数不是实际使用 Opus 的上下界**。"
            "第一名从广告变成游戏，表明领域排名对是否纳入 `likely` 敏感。"
            f"主画风前两名在两种口径下仍是动态图形／界面（{ss['motion_graphics_ui']} → {istyle['motion_graphics_ui']}）"
            f"与三维渲染（{ss['3d_render']} → {istyle['3d_render']}）。", "",
            "下面的画风图同样以**去重文件**为单位，将 `yes` 和新增的 `likely` 分段显示。", "",
            "![十三种主画风的分类文件数；深蓝为 yes，橙色为 likely](../assets/style-labels.svg)", "",
            "## 领域 × 主画风：前十个组合", "",
            f"下表只统计 `yes`＋`likely` 的 {len(inclusive):,} 个**文件**；每个文件只进入一个组合。"
            "百分比以该口径文件数为分母，表中仅列前十项，不能将十项相加当作总数。", "",
            "![按领域和主画风交叉计数的热力图，格子显示文件数](../assets/domain-style-heatmap.svg)", "",
            "| 领域 | 主画风 | 文件数 | 占该口径 |", "|---|---|---:|---:|",
        ]
        lines.extend(
            f"| {DOMAINS[domain][lang]} | {STYLES[style][lang]} | {count} | {percent(count, len(inclusive))} |"
            for (domain, style), count in top_cells
        )
        lines.extend([
            "", f"分类 CSV 对应 {data['post_count']:,} 个不同原帖 ID，而不是 {len(classified):,} 个不同帖子。"
            f"其中 {data['multi_post_count']} 帖有多个分类文件，共 {data['multi_post_rows']} 行；"
            f"{data['discordant_multi_posts']} 帖的多个附件甚至有不同 `opus_made` 标签。"
            f"可选的第二画风 `style2` 有 {data['secondary_style_blank']} 行留空，本表不使用它。"
            "同一作品经重新编码仍可能保留为多个不同文件，因此这些行不能当作独立创作者。", "",
            "## 人工案例的片长分布", "",
            "片长来自可取得的 X 预览 MP4，不保证是上传母版；少数旧观察文字与数值列的片长尚未逐项核对。"
            "下表用中位数和第 25–75 百分位描述右偏分布。四分位采用 Python "
            "`statistics.quantiles(n=4, method='inclusive')`；只描述被选入的案例，不能比较路径成功率。", "",
            "![七种人工案例路径的预览片长分布；点为中位数，横线为第 25 至 75 百分位](../assets/preview-duration.svg)", "",
            "| 单位 | n | 中位数（秒） | 第 25–75 百分位（秒） |", "|---|---:|---:|---:|",
            f"| 分类文件 | {len(classified):,} | {file_q[1]:.2f} | {file_q[0]:.2f}–{file_q[2]:.2f} |",
            f"| 人工案例主帖 MP4 | {len(cases):,} | {case_q[1]:.2f} | {case_q[0]:.2f}–{case_q[2]:.2f} |",
            "", "两行的抽样与单位不同；差异不能归因于某条制作路径或模型性能。", "",
            "| 人工案例的主制作路径 | 案例数 | 中位数（秒） | 第 25–75 百分位（秒） |",
            "|---|---:|---:|---:|",
        ])
        lines.extend(
            f"| {zh} | {len(values)} | {quartiles(values)[1]:.2f} | "
            f"{quartiles(values)[0]:.2f}–{quartiles(values)[2]:.2f} |"
            for _, zh, values in path_data
        )
        lines.extend([
            "", "## 为什么人工案例不等于分类真值", "",
            f"按原帖 ID 加预览片长（误差 ≤0.05 秒）与分类 CSV 对应后，{len(cases)} 条案例中"
            f"分类器为 `yes` {matched['yes']}、`likely` {matched['likely']}、`no` {matched['no']}。"
            "`no` 不能直接称为“模型误判”，案例入选也不能称为“人工证实 Opus 调用”。"
            "例如[双模型对照](https://x.com/leogao25/status/2102544078927741369)是比较片，"
            "[游戏录屏](https://x.com/The_Alex/status/2102440678282412195)的交付物是游戏，"
            "[Social SDK 广告](https://x.com/leodev/status/2102781872107659270)的模型分工在作者后续帖里说明。"
            "这些都是研究路径与证据范围问题，需要逐案读原帖和披露。", "",
            "## 用原帖检验数字的含义", "",
            "以下例子是有意挑选的证据对照，**不是**从任何统计单元随机抽出的代表作。", "",
            "| 原帖 | 它说明的证据边界 |", "|---|---|",
        ])
        lines.extend(
            f"| {example_cell(url, zh, True)} | {zh_note} |"
            for url, _, zh, _, zh_note in EXAMPLES
        )
        lines.extend([
            "", "## 可以与不可以推断什么", "",
            "X 搜索受关键词、语言、排序、每次返回上限、账号可见性与限流影响；案例又按路径和证据条件人工挑选。"
            "因此这里不给 X 全站的工艺比例、趋势、总体置信区间或 p 值，也不以播放片长推断成本、质量、独立创意量或模型优劣。"
            "九帧不能验收连续动作、音频、事实正确性或隐藏工具调用。"
            "详情见[调查方法](methodology.zh-CN.md)与[字段说明](case-index-guide.zh-CN.md)。", "",
            "[AAPOR 的透明度倡议](https://aapor.org/standards-and-ethics/transparency-initiative/)"
            "强调公开研究方法本身不等于方法质量认证；此页按同一透明原则说明统计边界。", "",
        ])
    else:
        lines = [
            "# Statistical snapshot: units, denominators, and sensitivity", "",
            "[中文](statistics.zh-CN.md) · Generated from the public CSVs and "
            "[frozen snapshot](../data/corpus-snapshot.json) by "
            "[`scripts/generate_statistics.py`](../scripts/generate_statistics.py). "
            "Run `python3 scripts/generate_statistics.py --check` to detect drift.", "",
            f"Snapshot: {snapshot['snapshot_utc']}. These are **descriptive statistics for the retrieved corpus**, "
            "not a census of X, a quality score, or a model success rate.", "",
            "Charts are generated from the same public data by "
            "[`scripts/generate_stat_charts.py`](../scripts/generate_stat_charts.py); "
            "run `python3 scripts/generate_stat_charts.py --check` to detect chart drift.", "",
            "## Count the right unit", "",
            "| Count | Unit | Reproducible from public files? |", "|---|---|---|",
            f"| {snapshot['search_queries_saved']:,}; {snapshot['search_queries_ok_or_cached']:,} succeeded or used cache | Saved search queries | Only the summary and [coverage notes](search-coverage.zh-CN.md) are public; raw receipts are not. A successful query does not imply full coverage. |",
            f"| {snapshot['candidate_posts']:,} | Deduplicated candidate posts | Recorded only in the snapshot; raw candidate rows are private. |",
            f"| {snapshot['candidate_posts_with_mp4']:,} | Candidate posts with MP4 | Recorded only in the snapshot. |",
            f"| {snapshot['mp4_attachments']:,} | Retrieved MP4 attachments with nine-frame samples | Recorded only in the snapshot; a post can have several attachments. |",
            f"| {snapshot['sha256_distinct']:,} | MP4 files reported as SHA-256 distinct | The [classifier CSV](../data/domain-style.csv) has {len(classified):,} rows, but no public file hashes or per-attachment IDs to independently repeat deduplication. |",
            f"| {snapshot['curated_cases']:,} | Manually reviewed source-post cases | The [case CSV](../data/cases.csv) has {len(cases):,} unique post IDs, each marked as sampled. |",
            "", f"The snapshot also reports {snapshot['sha256_duplicate_groups']} byte-identical groups and "
            f"{snapshot['sha256_duplicate_extra_attachments']} extra attachments in those groups; "
            f"{snapshot['sha256_distinct']:,} + {snapshot['sha256_duplicate_extra_attachments']} = {snapshot['mp4_attachments']:,}. "
            "That arithmetic is checkable; the underlying hashes are not public.", "",
            "## The classifier threshold changes first place", "",
            "A vision classifier assigned one `opus_made` label, one primary domain, and one primary style per file "
            "from the post text and nine sampled frames. Its labels do not independently establish authorship, "
            "model calls, or finished-video quality.", "",
            "![Classifier-assigned domain file counts, with yes in blue and likely in orange](../assets/domain-labels.svg)", "",
            "| Included labels | File denominator | Games / interactive | Ads / launches | First place |",
            "|---|---:|---:|---:|---|",
            f"| `yes` only | {len(strict):,} | {sd['game_interactive']} ({percent(sd['game_interactive'], len(strict))}) | {sd['product_ad']} ({percent(sd['product_ad'], len(strict))}) | {DOMAINS[strict_top_domain][lang]} |",
            f"| `yes` + `likely` | {len(inclusive):,} | {idom['game_interactive']} ({percent(idom['game_interactive'], len(inclusive))}) | {idom['product_ad']} ({percent(idom['product_ad'], len(inclusive))}) | {DOMAINS[inclusive_top_domain][lang]} |",
            "", f"Across all {len(classified):,} classified files, there are {labels['yes']:,} `yes`, "
            f"{labels['likely']:,} `likely`, and {labels['no']:,} `no` labels. The two thresholds include "
            f"{percent(len(strict), len(classified))} and {percent(len(inclusive), len(classified))} of these files; "
            "**these are not lower and upper bounds on actual Opus use**. The leading domain flips from "
            "ads to games, so that ranking depends on how `likely` is handled. The two leading primary styles "
            f"remain motion graphics / UI ({ss['motion_graphics_ui']} → {istyle['motion_graphics_ui']}) "
            f"and 3D render ({ss['3d_render']} → {istyle['3d_render']}).", "",
            "The style chart likewise counts **distinct files**, splitting the `yes` and added `likely` rows. "
            "These are classifier labels, not verified model use.", "",
            "![Thirteen primary visual styles by classified file count, split into yes and likely](../assets/style-labels.svg)", "",
            "## Domain × primary style: ten largest cells", "",
            f"This table uses only the {len(inclusive):,} **files** labeled `yes` or `likely`. "
            "Each file contributes to one cell; percentages use that file denominator. "
            "Only ten cells are shown, so their counts do not sum to the denominator.", "",
            "![Heatmap of classifier-assigned primary domain by primary style; each cell prints its file count](../assets/domain-style-heatmap.svg)", "",
            "| Domain | Primary style | Files | Share of included files |",
            "|---|---|---:|---:|",
        ]
        lines.extend(
            f"| {DOMAINS[domain][lang]} | {STYLES[style][lang]} | {count} | {percent(count, len(inclusive))} |"
            for (domain, style), count in top_cells
        )
        lines.extend([
            "", f"The classifier CSV has {data['post_count']:,} distinct post IDs, not {len(classified):,} distinct posts. "
            f"{data['multi_post_count']} posts have multiple classified files ({data['multi_post_rows']} rows), "
            f"and {data['discordant_multi_posts']} have differing `opus_made` labels across attachments. "
            f"The optional secondary style `style2` is blank on {data['secondary_style_blank']} rows and is excluded here. "
            "Re-encoded copies of one work can also remain distinct files; these rows are not independent creators.", "",
            "## Preview-duration distribution", "",
            "Durations describe accessible X preview MP4s, not necessarily the uploaded masters. Some older prose "
            "notes differ from the numeric duration and remain unreconciled. The median and 25th–75th percentiles "
            "describe skewed distributions. Quartiles use Python "
            "`statistics.quantiles(n=4, method='inclusive')`. These selected cases cannot rank production-path success.", "",
            "![Preview duration across seven manually reviewed production paths, showing medians and 25th–75th percentiles](../assets/preview-duration.svg)", "",
            "| Unit | n | Median (s) | 25th–75th percentile (s) |", "|---|---:|---:|---:|",
            f"| Classified file | {len(classified):,} | {file_q[1]:.2f} | {file_q[0]:.2f}–{file_q[2]:.2f} |",
            f"| Curated case's main-post MP4 | {len(cases):,} | {case_q[1]:.2f} | {case_q[0]:.2f}–{case_q[2]:.2f} |",
            "", "These rows have different units and selection rules; their difference cannot be attributed to a production route or model performance.", "",
            "| Curated case's primary path | Cases | Median (s) | 25th–75th percentile (s) |",
            "|---|---:|---:|---:|",
        ])
        lines.extend(
            f"| {en} | {len(values)} | {quartiles(values)[1]:.2f} | "
            f"{quartiles(values)[0]:.2f}–{quartiles(values)[2]:.2f} |"
            for en, _, values in path_data
        )
        lines.extend([
            "", "## Curated cases are not classifier ground truth", "",
            f"Matching original post ID and preview duration (tolerance ≤0.05 s) gives {matched['yes']} `yes`, "
            f"{matched['likely']} `likely`, and {matched['no']} `no` labels among the {len(cases)} curated cases. "
            "A `no` label is not automatically a classifier error, and inclusion in the case index does not prove "
            "an Opus call. For example, [one MP4 compares two models](https://x.com/leogao25/status/2102544078927741369), "
            "[one records a game](https://x.com/The_Alex/status/2102440678282412195), and "
            "[one creator describes the workflow later](https://x.com/leodev/status/2102781872107659270). "
            "These require case-level reading of the original and follow-up disclosures.", "",
            "## Examples that test what the counts mean", "",
            "These are deliberately chosen evidence contrasts, **not** randomly sampled representatives of statistical cells.", "",
            "| Original post | Evidence boundary |", "|---|---|",
        ])
        lines.extend(
            f"| {example_cell(url, en, False)} | {en_note} |"
            for url, en, _, en_note, _ in EXAMPLES
        )
        lines.extend([
            "", "## Limits on inference", "",
            "X search depends on terms, languages, ranking, per-query limits, account visibility, and rate limits. "
            "The case index was then chosen deliberately for production routes and evidence conditions. "
            "We therefore report no X-wide technique shares, time trends, population confidence intervals, or p-values. "
            "Preview length cannot establish cost, quality, creative independence, or model superiority. "
            "Nine frames cannot verify continuous motion, audio, factual accuracy, or hidden tool calls. "
            "See the [methodology](methodology.zh-CN.md) and [case-field guide](case-index-guide.zh-CN.md).", "",
            "[AAPOR's Transparency Initiative](https://aapor.org/standards-and-ethics/transparency-initiative/) "
            "distinguishes disclosure of methods from certification of their quality; this page likewise states the limits of its statistics.", "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="检查统计页面是否需要更新")
    args = parser.parse_args()
    try:
        data = summary()
        expected = (render(data, chinese=False), render(data, chinese=True))
        if args.check:
            stale = False
            for path, output in zip(OUTPUTS, expected):
                current = path.read_text(encoding="utf-8") if path.exists() else ""
                if current != output:
                    stale = True
                    sys.stderr.writelines(difflib.unified_diff(
                        current.splitlines(keepends=True), output.splitlines(keepends=True),
                        fromfile=str(path), tofile="generated from public CSVs",
                    ))
            if stale:
                print("统计页面与公开数据不一致；请运行 scripts/generate_statistics.py", file=sys.stderr)
                return 1
            print("中英文统计页面与公开数据一致")
            return 0
        for path, output in zip(OUTPUTS, expected):
            path.write_text(output, encoding="utf-8")
            print(f"已更新 {path.relative_to(ROOT)}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"统计页面生成失败：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
