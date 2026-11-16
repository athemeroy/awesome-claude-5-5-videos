"""Markdown rendering for directory, collection analysis, and README summary blocks."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from .config import END_MARKER, MODEL_GROUPS, ROOT, START_MARKER
from .loader import read_rows, resolve_detail_page


def clean_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_library(entries: list[dict[str, str]], zh: bool) -> str:
    title = "按模型浏览全部来源" if zh else "Browse all sources by model"
    lines = [
        f"# {title}",
        "",
        "[首页](../README.zh-CN.md) · [English](library.md)" if zh else "[Home](../README.md) · [中文](library.zh-CN.md)",
        "",
        (
            f"合并全部日期批次，共 **{len(entries)} 条去重来源帖**。案例说明沿用来源语言。"
            if zh
            else f"All dated batches in one directory: **{len(entries)} distinct source posts**. Older case titles retain their source language."
        ),
        "",
        (
            "模型分组按来源标签整理，多模型对照会出现在多个分组。`Fable 5.2` 为 2026-11-09 正式发布后的作者披露案例；10 月早期疑似 Fable 5.5 路由归入 `Fable（早期灰度）`。路由讨论另列。"
            if zh
            else "Groups follow source labels; multi-model comparisons appear in several groups. `Fable 5.2` covers creator-reported works since the November 9, 2026 launch; earlier suspected 5.5 routing reports remain under `Fable (pre-release)`. Routing discussions are listed separately."
        ),
        "",
        (
            "[收录与证据分析](collection-analysis.zh-CN.md) · [Fable 5.2 专题报告](fable-5-2.zh-CN.md) · [完整 CSV](../data/collection-index.csv)"
            if zh
            else "[Collection / evidence analysis](collection-analysis.md) · [Fable 5.2 report](fable-5-2.md) · [Complete CSV](../data/collection-index.csv)"
        ),
        "",
    ]

    for group in MODEL_GROUPS:
        subset = [e for e in entries if group.key in e["model_tags"].split(";")]
        label = group.label_zh if zh else group.label_en
        lines.append(f"- [{label} ({len(subset)})](#{group.slug})")
    context_rows = [e for e in entries if not e["model_tags"]]
    lines.append(
        f"- [{'背景与其他对照' if zh else 'Context and other comparisons'} ({len(context_rows)})](#context)"
    )
    lines.append("")

    sections = [(g.slug, g.label_zh if zh else g.label_en, [e for e in entries if g.key in e["model_tags"].split(";")]) for g in MODEL_GROUPS]
    sections.append(("context", "背景与其他对照" if zh else "Context and other comparisons", context_rows))

    for slug, heading, subset in sections:
        lines += [
            f'<a id="{slug}"></a>',
            "",
            f"## {heading} ({len(subset)})",
            "",
            "| 原帖 | 分类 / 模型标签 | 证据 | 收录日期 |" if zh else "| Original post | Category / model label | Evidence | First listed |",
            "|---|---|---|---|",
        ]
        for e in subset:
            sampled = e["media_evidence"] == "sampled_preview"
            evidence = ("九帧取样" if sampled else "仅来源") if zh else ("9-frame sample" if sampled else "Source only")
            page, _, anchor = e["detail_page"].partition("#")
            if zh and page.endswith(".md") and (ROOT / (page[:-3] + ".zh-CN.md")).exists():
                page = page[:-3] + ".zh-CN.md"
            label_parts = [e["category"]] if e["category"] else []
            if e["model_attribution"] and e["model_attribution"] != e["category"]:
                label_parts.append(e["model_attribution"])
            cat_cell = clean_cell(" · ".join(label_parts))
            title_cell = clean_cell(e["title_zh" if zh else "title_en"])
            detail_ref = Path(page).name + ("#" + anchor if anchor else "")
            lines.append(
                f"| [{title_cell}]({e['source_url']}) | {cat_cell} | [{evidence}]({detail_ref}) | {e['first_listed_date']} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_analysis(entries: list[dict[str, str]], groups: list[dict[str, object]], zh: bool) -> str:
    latest_file = str(groups[-1]["source"])
    latest_row = read_rows(ROOT / latest_file)[0]
    latest_page = resolve_detail_page(latest_file, latest_row.get("detail_page", ""))
    if zh and (ROOT / (latest_page[:-3] + ".zh-CN.md")).is_file():
        latest_page = latest_page[:-3] + ".zh-CN.md"
    latest_link = Path(latest_page).name

    total = len(entries)
    sampled = sum(e["media_evidence"] == "sampled_preview" for e in entries)
    context = sum(e["entry_kind"] == "routing_context" for e in entries)
    later = [e for e in entries if e["first_listed_date"] >= "2026-10-02" and e["entry_kind"] != "routing_context"]
    creators = Counter(e["creator"].lower() for e in entries)
    top = creators.most_common(5)
    top_count = sum(n for _, n in top)

    lines = [
        "# 收录与证据分析" if zh else "# Collection and evidence analysis",
        "",
        "[首页](../README.zh-CN.md) · [目录](library.zh-CN.md) · [English](collection-analysis.md)" if zh else "[Home](../README.md) · [Directory](library.md) · [中文](collection-analysis.zh-CN.md)",
        "",
        (
            "这些统计描述本仓库选中的来源帖，不估计 X 全站比例，也不评价模型优劣。全部数字来自[统一来源索引](../data/collection-index.csv)，由 `scripts/generate_collection_summary.py` 生成。"
            if zh
            else "These statistics describe selected source posts in this repository. They do not estimate X-wide prevalence or rank models. All figures derive from [the unified source index](../data/collection-index.csv), generated by `scripts/generate_collection_summary.py`."
        ),
        "",
        "## 证据覆盖" if zh else "## Evidence coverage",
        "",
        "![按收录批次统计有九帧取样的来源帖比例](../assets/collection-coverage.svg)" if zh else "![Nine-frame preview sampling coverage by listing batch](../assets/collection-coverage.svg)",
        "",
        "| 单位 | 数量 | 解释 |" if zh else "| Unit | Count | Meaning |",
        "|---|---:|---|",
        f"| {'去重来源帖' if zh else 'Distinct source posts'} | {total} | {'含回复、对照与版本变体' if zh else 'Includes replies, comparisons and variants'} |",
        f"| {'有九帧预览取样' if zh else 'Posts with nine-frame preview sampling'} | {sampled} ({sampled / total:.1%}) | {'按帖子计数，不是附件数或完整播放验收' if zh else 'Posts, not attachments or full-playback acceptance'} |",
        f"| {'尚无媒体取样' if zh else 'Posts without preview sampling'} | {total - sampled} | {'来源披露，含背景讨论' if zh else 'Source disclosures, including context discussion'} |",
        f"| {'路由背景讨论' if zh else 'Routing-context posts'} | {context} | {'属于总来源数；单列，不当作作品' if zh else 'Included in total sources; kept separate from examples'} |",
        "",
        "## 增量批次的模型标签分布" if zh else "## Model labels in incremental batches",
        "",
        (
            f"统计 10 月 2 日起的 **{len(later)} 条非路由讨论来源**，避免把早期专搜 Opus 5.5 的 168 条深读样本当成跨模型分布。"
            if zh
            else f"Use the **{len(later)} non-routing-context sources listed since October 2**, avoiding the 168 older Opus-focused cases as a cross-model denominator."
        ),
        "",
        "| 模型标签 | 来源帖 | 有取样 |" if zh else "| Model label | Source posts | With sampling |",
        "|---|---:|---:|",
    ]
    for group in MODEL_GROUPS:
        subset = [e for e in later if group.key in e["model_tags"].split(";")]
        label = group.label_zh if zh else group.label_en
        lines.append(
            f"| {label} | {len(subset)} | {sum(e['media_evidence'] == 'sampled_preview' for e in subset)} |"
        )
    multi = sum(len(e["model_tags"].split(";")) > 1 for e in later if e["model_tags"])
    unlabeled = sum(not e["model_tags"] for e in later)
    lines += [
        "",
        (
            f"其中 {multi} 条同时提到多个模型（多为同题对比），{unlabeled} 条未匹配明确的版本标签。因此表格行不能相加。"
            if zh
            else f"{multi} sources mention multiple models (mostly side-by-side comparisons); {unlabeled} match no explicit versioned label. Rows therefore cannot be summed."
        ),
        "",
        "## 来源作者分布" if zh else "## Source-account concentration",
        "",
        (
            f"总来源涉及 **{len(creators)} 个不区分大小写的发布账号**。帖数最多的五个账号占 {top_count}/{total}（{top_count / total:.1%}）。发布账号不一定是原创作者。"
            if zh
            else f"The collection contains **{len(creators)} case-insensitive publishing handles**. The five most represented accounts contribute {top_count}/{total} ({top_count / total:.1%}). A publishing handle is not necessarily an original creator."
        ),
        "",
        "| 发布账号 | 来源帖 |" if zh else "| Publishing handle | Source posts |",
        "|---|---:|",
    ]
    lines += [f"| @{name} | {count} |" for name, count in top]
    lines += [
        "",
        "## 各批次与历史快照边界" if zh else "## Batches and snapshot boundary",
        "",
        "| 批次 | 来源帖 | 比此前新增 |" if zh else "| Batch | Source posts | New to earlier batches |",
        "|---|---:|---:|",
    ]
    lines += [
        f"| [{g['label']}](../{g['source']}) | {g['unique_source_posts']} | {g['newly_listed_source_posts']} |"
        for g in groups
    ]
    lines += [
        "",
        (
            f"批次按首次收录日期组织，不是作品发布趋势。最新批次说明见[本轮专题]({latest_link})。9 月 26 日逐文件领域、画风、片长和配色分析保留在[冻结快照分析](snapshot-analysis.zh-CN.md)。两套单位不混算。"
            if zh
            else f"Batches use first-listing dates, not a publication trend. See [the latest update]({latest_link}) for details. September 26 file-level domain, style, duration and color results remain in [frozen snapshot analysis](snapshot-analysis.md); the units are not merged."
        ),
        "",
    ]
    return "\n".join(lines)


def render_readme_summary(
    entries: list[dict[str, str]],
    summary: dict[str, object],
    zh: bool,
) -> list[str]:
    suffix = ".zh-CN" if zh else ""
    total = int(summary["unique_source_posts"])  # type: ignore[arg-type]
    sampled = int(summary["sampled_source_posts"])  # type: ignore[arg-type]
    as_of = str(summary["as_of"])

    model_rows = []
    for group in MODEL_GROUPS:
        count = sum(group.key in e["model_tags"].split(";") for e in entries)
        label = group.label_zh if zh else group.label_en
        model_rows.append(f"| [{label}](docs/library{suffix}.md#{group.slug}) | {count} |")

    if zh:
        return [
            f"截至 {as_of}：**{total} 条去重来源帖**（其中 **{sampled} 条有九帧预览取样**）。",
            "",
            "| 模型浏览入口 | 来源帖 |",
            "|---|---:|",
            *model_rows,
            "",
            "[完整目录](docs/library.zh-CN.md) · [Fable 5.2 专题报告](docs/fable-5-2.zh-CN.md) · [证据与作者分布](docs/collection-analysis.zh-CN.md) · [批次汇总](data/collection-summary.json)",
        ]
    return [
        f"As of {as_of}: **{total} distinct source posts** (**{sampled} with nine-frame preview sampling**).",
        "",
        "| Browse by model | Source posts |",
        "|---|---:|",
        *model_rows,
        "",
        "[Complete directory](docs/library.md) · [Fable 5.2 report](docs/fable-5-2.md) · [Evidence and account coverage](docs/collection-analysis.md) · [Batch totals](data/collection-summary.json)",
    ]


def inject_readme_block(path: Path, block_lines: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    if text.count(START_MARKER) != 1 or text.count(END_MARKER) != 1:
        raise ValueError(f"Expected exactly one summary marker pair in {path}")
    before, rest = text.split(START_MARKER)
    _, after = rest.split(END_MARKER)
    return before + START_MARKER + "\n\n" + "\n".join(block_lines) + "\n\n" + END_MARKER + after
