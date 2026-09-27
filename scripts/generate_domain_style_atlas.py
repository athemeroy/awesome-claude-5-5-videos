#!/usr/bin/env python3
"""Generate the bilingual domain/style atlas from frozen public data.

The optional --export-engagement-from argument reconstructs a dated engagement
file from the maintainers' saved X search results. It never contacts X. Public
readers can run --check using only files in this repository.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import html
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from email.utils import parsedate_to_datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CASES = DATA / "cases.csv"
CLASSIFIED = DATA / "domain-style.csv"
SNAPSHOT = DATA / "corpus-snapshot.json"
ENGAGEMENT = DATA / "case-engagement-observed.csv"
ENGLISH_NOTES = DATA / "atlas-case-notes-en.csv"
OUTPUTS = (ROOT / "docs/domain-style-atlas.md", ROOT / "docs/domain-style-atlas.zh-CN.md")
THUMBNAILS = ROOT / "assets/case-thumbnails"
POST_ID = re.compile(r"^https://x\.com/[^/]+/status/(\d+)$")

DOMAINS = (
    ("game_interactive", "Games / interactive", "游戏／交互"),
    ("product_ad", "Ads / launches", "广告／发布片"),
    ("ai_self_meta", "AI about AI", "AI 讲 AI"),
    ("education_science", "Education / science", "科普／教育"),
    ("story_short", "Short story", "故事短片"),
    ("music_video", "Music video", "音乐视频"),
    ("history_culture", "History / culture", "历史／文化"),
    ("art_abstract", "Art / abstract", "艺术／抽象"),
    ("humor_meme", "Humor / meme", "幽默／梗"),
    ("data_viz", "Data visualization", "数据可视化"),
    ("other", "Other", "其他"),
)
STYLES = (
    ("motion_graphics_ui", "Motion / UI", "动态图形／界面"),
    ("3d_render", "3D render", "三维渲染"),
    ("flat_vector_cartoon", "Flat cartoon", "扁平卡通"),
    ("pixel_art", "Pixel art", "像素"),
    ("hand_drawn_sketch", "Hand-drawn", "手绘"),
    ("paper_cutout_collage", "Paper cut-out", "纸片拼贴"),
    ("painterly_ink_sand", "Ink / paint", "水墨／油彩"),
    ("generative_abstract", "Generative", "生成艺术"),
    ("anime", "Anime", "动漫"),
    ("math_diagram", "Math diagram", "数学图解"),
    ("photoreal", "Photoreal", "写实"),
    ("live_action", "Live action", "真人"),
    ("retro_terminal_ascii", "Terminal / ASCII", "终端／ASCII"),
)
ENGAGEMENT_FIELDS = (
    "post_id", "source_url", "post_created_at_utc", "likes", "views",
    "observed_at_utc", "hours_after_post", "observed_before_utc",
    "source_quality", "source_ref",
)
CASE_FIELDS = (
    "source_url", "primary_path", "label", "creator_disclosure",
    "hypit_observation", "review_note", "duration_s", "hypit_status",
)
CLASSIFIED_FIELDS = (
    "post_url", "author", "opus_made", "domain", "style", "style2",
    "topic_en", "duration_s",
)
ENGLISH_NOTE_FIELDS = ("post_id", "title_en", "creator_account_en", "review_limit_en")
CJK = re.compile(r"[\u3400-\u9fff]")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_csv(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == list(fields), f"Unexpected columns in {path.name}")
        rows = list(reader)
    require(bool(rows), f"Empty data file: {path.name}")
    return rows


def identifier(url: str) -> str:
    match = POST_ID.fullmatch(url)
    require(match is not None, f"Unexpected post URL: {url}")
    return match.group(1)


def parse_utc(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, f"Timestamp lacks timezone: {value}")
    return parsed.astimezone(dt.timezone.utc)


def utc_file_write(path: Path) -> str:
    """A saved-query file's write time is a bound, not X's exact read time."""
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat(timespec="seconds")


def export_engagement(private_root: Path, cases: list[dict[str, str]], snapshot: dict) -> None:
    """Reconstruct latest saved observation per case, without network requests."""
    raw_dir = private_root / "data/x-search-raw"
    posts_path = private_root / "data/x-posts.json"
    receipts_path = private_root / "data/x-search-receipts.json"
    require(raw_dir.is_dir() and posts_path.is_file() and receipts_path.is_file(),
            "Private root needs data/x-search-raw, data/x-posts.json, and data/x-search-receipts.json")
    receipt_names = {row["query"] for row in json.loads(receipts_path.read_text(encoding="utf-8"))}
    posts = {str(row["id"]): row for row in json.loads(posts_path.read_text(encoding="utf-8"))}
    wanted = {identifier(case["source_url"]): case["source_url"] for case in cases}
    observations: dict[str, list[tuple[str, str, dict]]] = defaultdict(list)
    for path in raw_dir.glob("*.json"):
        require(path.stem in receipt_names, f"Raw query lacks receipt: {path.name}")
        rows = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(rows, list), f"Raw query is not a list: {path.name}")
        saved_at = utc_file_write(path)
        for row in rows:
            post_id = str(row.get("id") or "")
            if post_id in wanted:
                observations[post_id].append((saved_at, path.stem, row))

    exported = []
    for case in cases:
        post_id = identifier(case["source_url"])
        require(post_id in posts, f"No merged post for case {post_id}")
        created = parsedate_to_datetime(posts[post_id]["created_at"]).astimezone(dt.timezone.utc)
        if observations[post_id]:
            saved_at, query, source = max(observations[post_id], key=lambda item: (item[0], item[1]))
            hours_after_post = (parse_utc(saved_at) - created).total_seconds() / 3600
            require(hours_after_post >= 0, f"Saved query predates post {post_id}")
            record = {
                "observed_at_utc": saved_at,
                "hours_after_post": f"{hours_after_post:.2f}",
                "observed_before_utc": "",
                "source_quality": "saved_raw_search",
                "source_ref": query,
            }
        else:
            source = posts[post_id]
            record = {
                "observed_at_utc": "",
                "hours_after_post": "",
                "observed_before_utc": snapshot["snapshot_utc"],
                "source_quality": "merged_cache_time_unknown",
                "source_ref": "x-posts.json",
            }
        exported.append({
            "post_id": post_id,
            "source_url": case["source_url"],
            "post_created_at_utc": created.isoformat(timespec="seconds"),
            "likes": "" if source.get("likes") is None else str(source["likes"]),
            "views": "" if source.get("views") is None else str(source["views"]),
            **record,
        })

    with ENGAGEMENT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ENGAGEMENT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(exported)


def load_and_validate() -> dict:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    cases = read_csv(CASES, CASE_FIELDS)
    classified = read_csv(CLASSIFIED, CLASSIFIED_FIELDS)
    engagement = read_csv(ENGAGEMENT, ENGAGEMENT_FIELDS)
    require(len(cases) == snapshot["curated_cases"] == 168, "Curated denominator changed")
    require(len(classified) == snapshot["domain_style_classified_files"] == 1401,
            "Classified-file denominator changed")
    require(len(engagement) == len(cases), "Engagement must cover all curated cases")
    require({row["domain"] for row in classified} == {key for key, _, _ in DOMAINS},
            "Domain vocabulary changed")
    require({row["style"] for row in classified} == {key for key, _, _ in STYLES},
            "Style vocabulary changed")
    require({row["opus_made"] for row in classified} == {"yes", "likely", "no"},
            "Classifier label vocabulary changed")

    class_by_key: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    counts: Counter[tuple[str, str]] = Counter()
    for row in classified:
        key = (row["post_url"], row["duration_s"])
        identifier(row["post_url"])
        class_by_key[key].append(row)
        if row["opus_made"] in {"yes", "likely"}:
            counts[row["domain"], row["style"]] += 1
    require(sum(counts.values()) == 1119, "yes+likely denominator changed")
    require(len(counts) == 92, "Nonempty matrix-cell count changed")

    case_by_id: dict[str, dict[str, str]] = {}
    vetted: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for case in cases:
        post_id = identifier(case["source_url"])
        require(post_id not in case_by_id, f"Repeated curated post ID: {post_id}")
        case_by_id[post_id] = case
        require(case["hypit_status"] == "tile_ok", f"Case lacks sampled preview: {post_id}")
        key = (case["source_url"], case["duration_s"])
        matches = class_by_key.get(key, [])
        require(len(matches) == 1, f"Case needs one exact URL+duration classifier match: {key}; found {len(matches)}")
        category = matches[0]
        if category["opus_made"] in {"yes", "likely"}:
            vetted[category["domain"], category["style"]].append({
                "post_id": post_id, "case": case, "category": category,
            })
    require(sum(len(items) for items in vetted.values()) == 157,
            "Curated yes+likely intersection changed")
    require(len(vetted) == 58, "Curated matrix-cell coverage changed")

    metrics: dict[str, dict[str, str]] = {}
    snapshot_time = parse_utc(snapshot["snapshot_utc"])
    for row in engagement:
        post_id = row["post_id"]
        require(post_id in case_by_id and post_id not in metrics,
                f"Engagement post ID missing or repeated: {post_id}")
        require(row["source_url"] == case_by_id[post_id]["source_url"],
                f"Engagement URL mismatch: {post_id}")
        posted = parse_utc(row["post_created_at_utc"])
        require(posted <= snapshot_time, f"Post created after snapshot: {post_id}")
        for field in ("likes", "views"):
            if row[field]:
                require(row[field].isdigit() and int(row[field]) >= 0,
                        f"Invalid {field} for {post_id}: {row[field]!r}")
        if row["source_quality"] == "saved_raw_search":
            require(bool(row["observed_at_utc"]) and not row["observed_before_utc"],
                    f"Raw query date malformed: {post_id}")
            require(parse_utc(row["observed_at_utc"]) <= snapshot_time,
                    f"Raw query appears after frozen snapshot: {post_id}")
            age = (parse_utc(row["observed_at_utc"]) - posted).total_seconds() / 3600
            require(age >= 0 and row["hours_after_post"] and
                    abs(float(row["hours_after_post"]) - age) <= 0.01,
                    f"Post age mismatch: {post_id}")
            require(bool(row["likes"]) and bool(row["views"]) and bool(row["source_ref"]),
                    f"Raw query lacks both metrics or source key: {post_id}")
        elif row["source_quality"] == "merged_cache_time_unknown":
            require(not row["observed_at_utc"] and bool(row["observed_before_utc"]),
                    f"Cache date malformed: {post_id}")
            require(not row["hours_after_post"], f"Cache age implies exact capture time: {post_id}")
            require(parse_utc(row["observed_before_utc"]) <= snapshot_time,
                    f"Cache date after frozen snapshot: {post_id}")
            require(row["source_ref"] == "x-posts.json", f"Unknown cache source: {post_id}")
        else:
            raise ValueError(f"Unknown source quality: {row['source_quality']}")
        metrics[post_id] = row
    require(set(metrics) == set(case_by_id), "Engagement IDs do not equal curated case IDs")

    for items in vetted.values():
        for item in items:
            item["engagement"] = metrics[item["post_id"]]
    selected: dict[tuple[str, str], list[dict]] = {}
    for cell, items in vetted.items():
        complete = [item for item in items
                    if item["engagement"]["likes"] and item["engagement"]["views"]]
        complete.sort(key=lambda item: (
            -int(item["engagement"]["likes"]),
            -int(item["engagement"]["views"]),
            item["post_id"],
        ))
        if complete:
            selected[cell] = complete[:2]
        else:
            # Keep a reviewed visual example without assigning it a popularity rank.
            selected[cell] = [sorted(items, key=lambda item: item["post_id"])[0]]
    require(len(selected) == 58, "Vetted cell selection changed")
    note_rows = read_csv(ENGLISH_NOTES, ENGLISH_NOTE_FIELDS)
    english_notes: dict[str, dict[str, str]] = {}
    for note in note_rows:
        post_id = note["post_id"]
        require(post_id.isdigit() and post_id not in english_notes,
                f"Invalid or repeated English atlas note ID: {post_id}")
        for field in ENGLISH_NOTE_FIELDS[1:]:
            require(bool(note[field].strip()) and not CJK.search(note[field]),
                    f"English atlas note has empty or CJK {field}: {post_id}")
        english_notes[post_id] = note
    selected_cjk_ids = {
        item["post_id"] for items in selected.values() for item in items
        if any(CJK.search(item["case"][field])
               for field in ("label", "creator_disclosure", "review_note"))
    }
    require(set(english_notes) == selected_cjk_ids,
            "English atlas notes must match selected cases with CJK fields exactly; "
            f"missing={sorted(selected_cjk_ids - set(english_notes))}, "
            f"stale={sorted(set(english_notes) - selected_cjk_ids)}")
    return {"snapshot": snapshot, "counts": counts, "vetted": vetted,
            "selected": selected, "engagement": metrics, "english_notes": english_notes}


def number(value: str) -> str:
    return f"{int(value):,}" if value else "N/A"


def safe_inline(value: str) -> str:
    return html.escape(re.sub(r"\s+", " ", value.strip()), quote=False)


def matrix(state: dict, chinese: bool) -> list[str]:
    lines = ["| " + ("主题 / 用途" if chinese else "Domain / use") + " | " +
             " | ".join(label_zh if chinese else label_en for _, label_en, label_zh in STYLES) + " |",
             "|---|" + "---:|" * len(STYLES)]
    for domain, label_en, label_zh in DOMAINS:
        cells = []
        for style, _, _ in STYLES:
            cell = (domain, style)
            count = state["counts"][cell]
            if count == 0:
                cells.append("—")
            elif cell in state["vetted"]:
                cells.append(f"[{count}](#cell-{domain}-{style})")
            else:
                cells.append(f"{count}†")
        lines.append("| " + (label_zh if chinese else label_en) + " | " + " | ".join(cells) + " |")
    return lines


def metric_line(row: dict[str, str], chinese: bool) -> str:
    likes, views = number(row["likes"]), number(row["views"])
    if row["source_quality"] == "saved_raw_search":
        timestamp = row["observed_at_utc"].replace("T", " ")
        age = row["hours_after_post"]
        if chinese:
            return (f"观察值：**{likes} 赞、{views} 浏览**；原始搜索文件写入于 "
                    f"{timestamp}（UTC，发帖后约 {age} 小时；查询 `{row['source_ref']}`）。"
                    "这是存档时间，不是精确的 X 读数时间。")
        return (f"Observed: **{likes} likes, {views} views**; saved search file written "
                f"{timestamp} (UTC, about {age} hours after posting; query `{row['source_ref']}`). "
                "File-write time is not the exact X read time.")
    deadline = row["observed_before_utc"].replace("T", " ")
    if chinese:
        return (f"缓存观察值：**{likes} 赞、{views} 浏览**；不晚于 {deadline}（UTC），"
                "具体采集时间不明；缺失值不参与排名。")
    return (f"Cached observation: **{likes} likes, {views} views**; no later than "
            f"{deadline} (UTC), exact capture time unknown. Missing values are not ranked.")


def render(state: dict, chinese: bool) -> str:
    snapshot = state["snapshot"]["snapshot_utc"]
    complete_cells = sum(any(item["engagement"]["likes"] and item["engagement"]["views"]
                             for item in items) for items in state["vetted"].values())
    complete_cases = sum(bool(row["likes"] and row["views"]) for row in state["engagement"].values())
    raw_cases = sum(row["source_quality"] == "saved_raw_search" for row in state["engagement"].values())
    raw_selected = sum(item["engagement"]["source_quality"] == "saved_raw_search"
                       for items in state["selected"].values() for item in items)
    post_ages = sorted(float(row["hours_after_post"]) for row in state["engagement"].values()
                       if row["hours_after_post"])
    age_summary = f"{post_ages[0]:.2f}–{post_ages[-1]:.2f}"
    age_median = f"{statistics.median(post_ages):.2f}"
    selected_count = sum(len(items) for items in state["selected"].values())
    if chinese:
        lines = [
            "# Opus 5.5 视频：主题 × 视觉风格图谱", "",
            "[English](domain-style-atlas.md) · 本页由 [`generate_domain_style_atlas.py`](../scripts/generate_domain_style_atlas.py) "
            "根据[分类 CSV](../data/domain-style.csv)、[案例 CSV](../data/cases.csv)和[互动量观察表](../data/case-engagement-observed.csv)生成。",
            "", f"**数据截点：** {snapshot}（UTC）。矩阵单元是**视频文件数**：存档快照报告 1,401 个 SHA-256 "
            "去重文件，公开分类 CSV 有对应的 1,401 行，但没有文件哈希，读者无法仅凭公开文件重做去重。"
            "图谱仅纳入分类器标为 `yes` 或 `likely` 的 1,119 个文件。每个文件只进一个主要主题和一种主要风格；"
            "`style2` 未计入。分类器判断不等于原作者身份或真实模型调用得到验证。", "",
            f"143 个组合里有 92 个非空格。168 个审读帖子中，157 个案例对应 `yes`／`likely` 的文件，"
            f"落在 58 格；其余 34 个非空格没有已审读案例。当前 168 个案例里 {complete_cases} 个有赞和浏览两项观察值，"
            f"其中 {raw_cases} 个来自保存的搜索原始结果；另外 7 个旧合并缓存案例缺浏览量，"
            f"无法进入互动量排序。{complete_cells} 个格子至少有一个双指标案例。"
            f"下方共展示 {selected_count} 个带截图案例，{raw_selected} 个选例的互动量均来自保存的原始搜索。", "",
            "**选例规则：** 先限定在 168 个已审读案例中，再按原帖 URL 和预览时长精确对应分类结果；"
            "每格从有赞和浏览两项观察值的案例里，按观察到的点赞降序、浏览降序、帖子 ID 升序选择最多两例。"
            "若全格都缺一项指标，只展示一例并明确不排名。赞和浏览属于 X 原帖，浏览数不是视频播放次数；"
            "多个视频附件可能共用同一帖指标；"
            "这不是质量、制作难度、Opus 贡献或效果的评分。", "",
            "**时间限制：** 这些不是“最终”或同一时点的数字。原始搜索文件跨 9 月 24–26 日保存；"
            f"少数合并缓存没有精确采集时间。161 个原始搜索观察值在发帖后约 {age_summary} 小时存档，"
            f"中位数 {age_median} 小时。较早发表、粉丝更多或转发更多的帖子获得互动的机会不同；"
            "不要把格子内名次当成公平的作品比较。截图仅用于辨认画面，取自可取得的 X 预览；"
            "权利仍归原作者。详情请看[统计说明](statistics.zh-CN.md)和[完整 168 案例目录](cases-index.zh-CN.md)。", "",
            "## 全部主题 × 风格矩阵", "",
            "表内数字为文件数。可点击的数字跳转到有截图的审读案例；`†` 代表有分类文件、但没有落在该格的已审读案例；"
            "`—` 表示该次检索样本中没有文件，不代表全网不存在。手机上可横向滚动。", "",
        ]
    else:
        lines = [
            "# Opus 5.5 videos: domain × visual style atlas", "",
            "[中文](domain-style-atlas.zh-CN.md) · Generated by [`generate_domain_style_atlas.py`](../scripts/generate_domain_style_atlas.py) "
            "from the [classifier CSV](../data/domain-style.csv), [case CSV](../data/cases.csv), "
            "[engagement observation table](../data/case-engagement-observed.csv), and "
            "[English case-note translations](../data/atlas-case-notes-en.csv).", "",
            f"**Frozen data:** {snapshot} (UTC). A matrix cell counts **video files**. The snapshot reports "
            "1,401 SHA-256-distinct files, and the public classifier CSV has 1,401 corresponding rows. "
            "It does not expose hashes, so public files alone cannot repeat the byte deduplication. "
            "This atlas includes the 1,119 labeled `yes` or `likely` by the classifier. Each file "
            "has one primary domain and one primary style; `style2` is excluded. Classifier labels do not "
            "verify original authorship or actual model calls.", "",
            f"Of 143 possible combinations, 92 contain files. Among 168 reviewed source-post cases, 157 "
            f"match `yes`/`likely` files in 58 cells; the other 34 populated cells have no reviewed case. "
            f"Both likes and views are available for {complete_cases} of 168 cases, all {raw_cases} from "
            f"saved raw search results. The other seven cases have older merged-cache values without views "
            f"and cannot enter the engagement ordering. All {complete_cells} cells with a reviewed case "
            f"have at least one case with both metrics. There are {selected_count} illustrated cases below; "
            f"all {raw_selected} selected examples use saved raw search observations.", "",
            "**Selection rule:** First restrict to the 168 reviewed cases, then match classifier rows by exact "
            "original-post URL and preview duration. Within each cell, select up to two cases with both "
            "metrics, ordering by observed likes descending, views descending, then post ID ascending. "
            "If every reviewed case in a cell lacks a metric, show one without a rank. Likes and views "
            "belong to the X post; views are not video plays. Several video attachments can share these "
            "metrics. Popularity does not score quality, "
            "production difficulty, Opus's contribution, or effectiveness.", "",
            "**Timing limit:** These are neither final nor simultaneous counts. The saved raw search files "
            f"span September 24–26, and some merged cache rows lack an exact capture time. The 161 raw "
            f"observations were saved about {age_summary} hours after posting (median {age_median} hours). "
            "Earlier posts, "
            "larger audiences, and reposting have different chances to accumulate engagement. Do not treat "
            "within-cell order as a fair performance comparison. Stills identify the look of an accessible "
            "X preview; image rights remain with the original creator. See the [statistical profile](statistics.md) "
            "and [full 168-case directory](cases-index.zh-CN.md).", "",
            "## Complete domain × style matrix", "",
            "Cells count files. Linked numbers jump to illustrated reviewed cases; `†` means classified "
            "files exist but no reviewed case maps to that cell. `—` means none in this retrieved sample, "
            "not none across X. Scroll horizontally on a phone.", "",
        ]
    lines += matrix(state, chinese)
    lines += ["", "## " + ("逐格案例" if chinese else "Illustrated cell examples"), ""]
    for domain, d_en, d_zh in DOMAINS:
        for style, s_en, s_zh in STYLES:
            cell = (domain, style)
            if cell not in state["vetted"]:
                continue
            lines += [f'<a id="cell-{domain}-{style}"></a>', "",
                      "### " + (f"{d_zh} × {s_zh}" if chinese else f"{d_en} × {s_en}"), ""]
            count = state["counts"][cell]
            vetted_count = len(state["vetted"][cell])
            lines += [(f"{count} 个分类文件；{vetted_count} 个对应已审读案例。"
                       if chinese else f"{count} classified {'file' if count == 1 else 'files'}; "
                       f"{vetted_count} matching reviewed {'case' if vetted_count == 1 else 'cases'}."), ""]
            for rank, item in enumerate(state["selected"][cell], 1):
                case = item["case"]
                category = item["category"]
                engagement = item["engagement"]
                post_id = item["post_id"]
                url = case["source_url"]
                english_note = state["english_notes"].get(post_id) if not chinese else None
                title = safe_inline(english_note["title_en"] if english_note else case["label"])
                topic = safe_inline(category["topic_en"])
                route = safe_inline(case["primary_path"])
                creator = safe_inline(english_note["creator_account_en"] if english_note else case["creator_disclosure"])
                review = safe_inline(english_note["review_limit_en"] if english_note else case["review_note"])
                complete = bool(engagement["likes"] and engagement["views"])
                heading = (f"{rank}. [{title}]({url})" if complete else
                           f"{rank}. [{title}]({url}) " + ("（未排名）" if chinese else "(unranked)"))
                lines += [f"#### {heading}", "",
                          f'<a href="{url}"><img src="../assets/case-thumbnails/{post_id}.webp" '
                          f'width="160" loading="lazy" alt="Still from {html.escape(title, quote=True)}"></a>', "",
                          (f"**画面主题：** {topic} · **案例制作路径：** `{route}` · "
                           f"[完整目录](cases-index.zh-CN.md)" if chinese else
                           f"**Subject:** {topic} · **Reviewed production path:** `{route}` · "
                           f"[Full case directory](cases-index.zh-CN.md)"), "",
                          (f"**作者披露：** {creator}" if chinese else f"**Creator account:** {creator}"), "",
                          (f"**审读边界：** {review}" if chinese else f"**Review limit:** {review}"), "",
                          metric_line(engagement, chinese), ""]
    lines += ["---", "", ("复核页面：`python3 scripts/generate_domain_style_atlas.py --check`。"
                           if chinese else "Check generated pages: `python3 scripts/generate_domain_style_atlas.py --check`."), ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate public data and generated pages")
    parser.add_argument("--export-engagement-from", type=Path, metavar="PRIVATE_ROOT",
                        help="reconstruct CSV from saved private X search results without a network call")
    args = parser.parse_args()
    require(not (args.check and args.export_engagement_from),
            "--check and --export-engagement-from cannot be combined")
    if args.export_engagement_from:
        snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        cases = read_csv(CASES, CASE_FIELDS)
        export_engagement(args.export_engagement_from, cases, snapshot)
    state = load_and_validate()
    expected = {OUTPUTS[0]: render(state, False), OUTPUTS[1]: render(state, True)}
    if args.check:
        missing_thumbnails = sorted({item["post_id"] for items in state["selected"].values()
                                     for item in items if not (THUMBNAILS / f'{item["post_id"]}.webp').is_file()})
        require(not missing_thumbnails, f"Missing selected thumbnails: {', '.join(missing_thumbnails)}")
        mismatches = []
        for path, content in expected.items():
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != content:
                mismatches.extend(difflib.unified_diff(current.splitlines(), content.splitlines(),
                                                       fromfile=str(path), tofile="generated", lineterm=""))
        if mismatches:
            print("\n".join(mismatches[:120]), file=sys.stderr)
            return 1
        print("Atlas and engagement joins OK; generated pages are current")
        return 0
    for path, content in expected.items():
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
