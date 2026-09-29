#!/usr/bin/env python3
"""Generate the bilingual domain/style atlas from frozen and dated public data.

The optional --export-engagement-from argument reconstructs a dated engagement
archive from the maintainers' saved X search results. It never contacts X. The
separate 2026-09-27 refresh is a dated official-page observation, not a change
to the frozen corpus. Public readers can run --check using repository files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import html
import json
import re
import sys
from collections import Counter, defaultdict
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CASES = DATA / "cases.csv"
CLASSIFIED = DATA / "domain-style.csv"
SNAPSHOT = DATA / "corpus-snapshot.json"
ENGAGEMENT = DATA / "case-engagement-observed.csv"
REFRESH = DATA / "case-engagement-refresh-2026-09-27.csv"
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
REFRESH_FIELDS = (
    "post_id", "source_url", "post_created_at_utc", "likes", "views",
    "likes_display", "views_display", "likes_lower_bound", "likes_upper_bound",
    "observed_at_utc", "source_method", "page_http_status", "page_url",
    "status", "error",
)
REFRESH_STATUSES = {"ok", "partial", "failed", "not_attempted"}
OFFICIAL_REFRESH_METHODS = {"x_public_post_ui_hover", "x_public_post_html"}
# Retained in the historical 168-case data, but omitted from featured examples.
SHOWCASE_EXCLUDED_POST_IDS = {"2103108551799632050"}
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


def like_bounds(row: dict[str, str]) -> tuple[int, int] | None:
    """Return exact likes or the collector's conservative display interval."""
    if row["likes"]:
        count = int(row["likes"])
        return count, count
    if row["likes_lower_bound"]:
        return int(row["likes_lower_bound"]), int(row["likes_upper_bound"])
    return None


def exact_views(row: dict[str, str]) -> int | None:
    return int(row["views"]) if row["views"] else None


def unabridged_display(value: str) -> int | None:
    """A bare UI integer can cross-check HTML data; abbreviations cannot."""
    normalized = re.sub(r"[,\u00a0\u202f\s]", "", value.strip())
    return int(normalized) if re.fullmatch(r"[0-9]+", normalized) else None


def validate_refresh(rows: list[dict[str, str]], cases: dict[str, dict[str, str]],
                     archive: dict[str, dict[str, str]], snapshot_time: dt.datetime) -> dict[str, dict[str, str]]:
    """Check that the dated public refresh is complete and never implies false precision."""
    require(len(rows) == len(cases), "Dated refresh must have one row for every curated case")
    refreshed: dict[str, dict[str, str]] = {}
    for row in rows:
        post_id = row["post_id"]
        require(post_id in cases and post_id not in refreshed,
                f"Dated refresh has an unknown or repeated ID: {post_id}")
        require(row["source_url"] == cases[post_id]["source_url"],
                f"Dated refresh URL mismatch: {post_id}")
        require(parse_utc(row["post_created_at_utc"]) == parse_utc(archive[post_id]["post_created_at_utc"]),
                f"Dated refresh post-time mismatch: {post_id}")
        require(row["status"] in REFRESH_STATUSES, f"Unknown dated refresh status: {post_id}")
        require(row["status"] != "not_attempted", f"Dated refresh is still in progress: {post_id}")
        require(row["source_method"] in OFFICIAL_REFRESH_METHODS,
                f"Dated refresh lacks official-page provenance: {post_id}")
        require(bool(row["observed_at_utc"]), f"Dated refresh lacks capture time: {post_id}")
        observed = parse_utc(row["observed_at_utc"])
        require(observed >= snapshot_time and observed >= parse_utc(row["post_created_at_utc"]),
                f"Dated refresh time predates the corpus or post: {post_id}")
        if row["page_http_status"]:
            require(row["page_http_status"].isdigit(), f"Non-numeric page status: {post_id}")
        for field in ("likes", "views", "likes_lower_bound", "likes_upper_bound"):
            if row[field]:
                require(row[field].isdigit(), f"Invalid exact or interval metric {field}: {post_id}")
        require(bool(row["likes_lower_bound"]) == bool(row["likes_upper_bound"]),
                f"Only one like-interval endpoint: {post_id}")
        bounds = like_bounds(row)
        if row["source_method"] == "x_public_post_ui_hover" and not row["views_display"].strip():
            require(bounds is None,
                    f"UI likes lack a target-post views-link display: {post_id}")
        if row["likes"]:
            require(bounds == (int(row["likes"]), int(row["likes"])) and
                    row["likes_lower_bound"] == row["likes_upper_bound"] == row["likes"],
                    f"Exact likes and interval disagree: {post_id}")
        elif bounds is not None:
            require(bounds[0] <= bounds[1] and bool(row["likes_display"]),
                    f"Rounded like interval lacks a display or is inverted: {post_id}")
        views = exact_views(row)
        displayed_likes = unabridged_display(row["likes_display"])
        displayed_views = unabridged_display(row["views_display"])
        if row["likes"] and displayed_likes is not None:
            require(int(row["likes"]) == displayed_likes,
                    f"Exact likes disagree with unabridged X-page display: {post_id}")
        if views is not None and displayed_views is not None:
            require(views == displayed_views,
                    f"Exact post views disagree with unabridged X-page display: {post_id}")
        if bounds is not None or views is not None:
            page = urlsplit(row["page_url"])
            match = re.fullmatch(r"/[^/]+/status/(\d+)/?", page.path)
            require(page.scheme == "https" and page.hostname in
                    {"x.com", "www.x.com", "twitter.com", "www.twitter.com"} and
                    match is not None and match.group(1) == post_id,
                    f"A dated metric is not attached to its target post page: {post_id}")
        if row["status"] == "ok":
            require(bool(row["likes"]) and views is not None,
                    f"Successful refresh lacks both exact metrics: {post_id}")
        elif row["status"] == "partial":
            require(bounds is not None or views is not None,
                    f"Partial refresh has no usable metric: {post_id}")
            require(not (row["likes"] and views is not None),
                    f"Partial refresh has both exact metrics: {post_id}")
        else:
            require(not row["likes"] and views is None,
                    f"Failed refresh unexpectedly contains an exact metric: {post_id}")
        refreshed[post_id] = row
    require(set(refreshed) == set(cases), "Dated refresh IDs do not match reviewed cases")
    return refreshed


def select_examples(items: list[dict]) -> list[dict]:
    """Pick one like-led and one view-led example without treating ranges as exact."""
    measured = [item for item in items
                if like_bounds(item["refresh"]) is not None or exact_views(item["refresh"]) is not None]
    if not measured:
        fallback = min(items, key=lambda item: item["post_id"]).copy()
        fallback["selection_reason"] = "unranked"
        return [fallback]

    with_likes = [item for item in measured if like_bounds(item["refresh"]) is not None]
    if with_likes:
        highest_lower = max(like_bounds(item["refresh"])[0] for item in with_likes)
        plausible_leaders = [item for item in with_likes
                             if like_bounds(item["refresh"])[1] >= highest_lower]
        first = sorted(plausible_leaders, key=lambda item: (
            -(exact_views(item["refresh"]) if exact_views(item["refresh"]) is not None else -1),
            -like_bounds(item["refresh"])[0], item["post_id"],
        ))[0]
        first_reason = ("likes" if len(plausible_leaders) == 1 else
                        "overlap_views" if any(exact_views(item["refresh"]) is not None
                                               for item in plausible_leaders) else
                        "overlap_lower_bound")
    else:
        first = sorted(measured, key=lambda item: (-exact_views(item["refresh"]), item["post_id"]))[0]
        first_reason = "views"

    chosen = first.copy()
    chosen["selection_reason"] = first_reason
    result = [chosen]
    remaining = [item for item in measured if item["post_id"] != first["post_id"]]
    with_views = [item for item in remaining if exact_views(item["refresh"]) is not None]
    if with_views:
        second = sorted(with_views, key=lambda item: (-exact_views(item["refresh"]), item["post_id"]))[0]
        second_reason = "views"
    elif remaining:
        second = sorted(remaining, key=lambda item: (-like_bounds(item["refresh"])[0], item["post_id"]))[0]
        second_reason = "likes_remainder"
    else:
        second = None
    if second is not None:
        chosen = second.copy()
        chosen["selection_reason"] = second_reason
        result.append(chosen)
    return result


def load_and_validate() -> dict:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    cases = read_csv(CASES, CASE_FIELDS)
    classified = read_csv(CLASSIFIED, CLASSIFIED_FIELDS)
    engagement = read_csv(ENGAGEMENT, ENGAGEMENT_FIELDS)
    refresh_rows = read_csv(REFRESH, REFRESH_FIELDS)
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
    refreshed = validate_refresh(refresh_rows, case_by_id, metrics, snapshot_time)

    for items in vetted.values():
        for item in items:
            item["engagement"] = metrics[item["post_id"]]
            item["refresh"] = refreshed[item["post_id"]]
    require(SHOWCASE_EXCLUDED_POST_IDS <= set(case_by_id),
            "A maintainer showcase exclusion is absent from the retained case data")
    selectable = {cell: [item for item in items
                         if item["post_id"] not in SHOWCASE_EXCLUDED_POST_IDS]
                  for cell, items in vetted.items()}
    require(all(selectable.values()), "A cell would have only an excluded maintainer example")
    selected = {cell: select_examples(items) for cell, items in selectable.items()}
    require(len(selected) == 58, "Vetted cell selection changed")
    require(all(1 <= len(items) <= 2 for items in selected.values()),
            "Every reviewed atlas cell should show one or two cases")
    require(not any(item["post_id"] in SHOWCASE_EXCLUDED_POST_IDS
                    for items in selected.values() for item in items),
            "Maintainer case entered featured atlas examples")
    note_rows = read_csv(ENGLISH_NOTES, ENGLISH_NOTE_FIELDS)
    english_notes: dict[str, dict[str, str]] = {}
    for note in note_rows:
        post_id = note["post_id"]
        require(post_id.isdigit() and post_id not in english_notes,
                f"Invalid or repeated English atlas note ID: {post_id}")
        require(post_id in case_by_id and any(CJK.search(case_by_id[post_id][field])
                                               for field in ("label", "creator_disclosure", "review_note")),
                f"English atlas note does not match a CJK reviewed case: {post_id}")
        for field in ENGLISH_NOTE_FIELDS[1:]:
            require(bool(note[field].strip()) and not CJK.search(note[field]),
                    f"English atlas note has empty or CJK {field}: {post_id}")
        english_notes[post_id] = note
    selected_cjk_ids = {
        item["post_id"] for items in selected.values() for item in items
        if any(CJK.search(item["case"][field])
               for field in ("label", "creator_disclosure", "review_note"))
    }
    require(selected_cjk_ids <= set(english_notes),
            "English atlas notes must cover selected cases with CJK fields; "
            f"missing={sorted(selected_cjk_ids - set(english_notes))}")
    return {"snapshot": snapshot, "counts": counts, "vetted": vetted,
            "selected": selected, "engagement": metrics, "refresh": refreshed,
            "english_notes": english_notes}


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


def archived_metric_line(row: dict[str, str], chinese: bool) -> str:
    likes, views = number(row["likes"]), number(row["views"])
    if row["source_quality"] == "saved_raw_search":
        timestamp = row["observed_at_utc"].replace("T", " ")
        age = row["hours_after_post"]
        if chinese:
            return (f"历史存档观察值：**{likes} 赞、{views} 浏览**；原始搜索文件写入于 "
                    f"{timestamp}（UTC，发帖后约 {age} 小时；查询 `{row['source_ref']}`）。"
                    "这是存档时间，不是精确的 X 读数时间。")
        return (f"Archived observation: **{likes} likes, {views} views**; saved search file written "
                f"{timestamp} (UTC, about {age} hours after posting; query `{row['source_ref']}`). "
                "File-write time is not the exact X read time.")
    deadline = row["observed_before_utc"].replace("T", " ")
    if chinese:
        return (f"历史缓存观察值：**{likes} 赞、{views} 浏览**；不晚于 {deadline}（UTC），"
                "具体采集时间不明；缺失值不参与排名。")
    return (f"Archived cached observation: **{likes} likes, {views} views**; no later than "
            f"{deadline} (UTC), exact capture time unknown. Missing values are not ranked.")


def metric_line(row: dict[str, str], chinese: bool) -> str:
    """Show exact current values or the literal rounded display and its interval."""
    observed = row["observed_at_utc"].replace("T", " ")
    bounds = like_bounds(row)
    if row["likes"]:
        source = ("公开帖子 HTML" if row["source_method"] == "x_public_post_html" else "页面按钮")
        source_en = ("public post HTML" if row["source_method"] == "x_public_post_html" else "page button")
        likes = (f"{number(row['likes'])} 赞（{source} 精确值）" if chinese else
                 f"{number(row['likes'])} likes (exact {source_en} value)")
    elif bounds is not None:
        display = safe_inline(row["likes_display"])
        likes = (f"页面赞数显示「{display}」，保守区间 {bounds[0]:,}–{bounds[1]:,}（精确值未知）" if chinese else
                 f"X displays {display} for likes; conservative interval {bounds[0]:,}–{bounds[1]:,} "
                 "(exact count unknown)")
    else:
        display = safe_inline(row["likes_display"])
        likes = ((f"未取得精确赞数（页面显示 {display}）" if display else "本轮未取得赞数") if chinese else
                 (f"no exact likes captured (page shows {display})" if display else "likes unavailable in this refresh"))
    if row["views"]:
        source = ("公开帖子 HTML" if row["source_method"] == "x_public_post_html" else "页面 tooltip")
        source_en = ("public post HTML" if row["source_method"] == "x_public_post_html" else "page tooltip")
        views = (f"{number(row['views'])} 次帖子浏览（{source} 精确值）" if chinese else
                 f"{number(row['views'])} post views (exact {source_en} value)")
    else:
        display = safe_inline(row["views_display"])
        views = ((f"未取得精确帖子浏览量（页面显示 {display}）" if display else "本轮未取得帖子浏览量")
                 if chinese else
                 (f"no exact post views captured (page shows {display})" if display else
                  "post views unavailable in this refresh"))
    if chinese:
        return f"**本轮 X 页面观察：** {likes}；{views}。记录于 {observed}（UTC）。"
    return f"**Current X-page observation:** {likes}; {views}. Captured {observed} (UTC)."


def selection_line(reason: str, chinese: bool) -> str:
    translations = {
        "likes": (
            "按本轮点赞选出；在有赞数的案例中，下界高于其余案例的上界。",
            "Like-led among cases with current like counts; its lower bound exceeds the other upper bounds.",
        ),
        "overlap_views": (
            "可能领先的点赞区间重叠；按精确帖子浏览量选出，不能判定点赞严格名次。",
            "Plausible like leaders' intervals overlap; chosen by exact post views, without a strict like rank.",
        ),
        "overlap_lower_bound": (
            "点赞区间重叠且缺精确浏览量；按保守下界选出，不能断言严格名次。",
            "Like intervals overlap and exact views are missing; chosen by conservative lower bound, not strict rank.",
        ),
        "views": (
            "按本轮精确帖子浏览量选出。",
            "Chosen by current exact post views.",
        ),
        "likes_remainder": (
            "其余案例缺精确浏览量；按本轮点赞保守下界选出，不代表严格名次。",
            "Remaining cases lack exact views; chosen by current like lower bound, without a strict rank.",
        ),
        "unranked": (
            "本格缺本轮可用互动量；仅展示一条画面案例，不按旧值排名。",
            "No usable current counts in this cell; one visual example, not ranked by archived values.",
        ),
    }
    return ("**选例依据：** " if chinese else "**Selection basis:** ") + translations[reason][0 if chinese else 1]


def render(state: dict, chinese: bool) -> str:
    snapshot = state["snapshot"]["snapshot_utc"]
    refresh = state["refresh"]
    complete_cases = sum(bool(row["likes"] and row["views"]) for row in refresh.values())
    exact_likes = sum(bool(row["likes"]) for row in refresh.values())
    rounded_likes = sum(bool(not row["likes"] and row["likes_lower_bound"]) for row in refresh.values())
    rounded_zh = f"{rounded_likes} 帖仅有点赞缩写的保守区间，" if rounded_likes else ""
    rounded_en = (f"{rounded_likes} only a conservative interval for abbreviated likes, "
                  if rounded_likes else "")
    exact_view_cases = sum(bool(row["views"]) for row in refresh.values())
    failed_cases = sum(row["status"] == "failed" for row in refresh.values())
    measured_cells = sum(any(like_bounds(item["refresh"]) is not None or
                             exact_views(item["refresh"]) is not None
                             for item in items if item["post_id"] not in SHOWCASE_EXCLUDED_POST_IDS)
                         for items in state["vetted"].values())
    observed_times = sorted(parse_utc(row["observed_at_utc"]) for row in refresh.values())
    first_observed = observed_times[0].isoformat(timespec="seconds")
    last_observed = observed_times[-1].isoformat(timespec="seconds")
    selected_count = sum(len(items) for items in state["selected"].values())
    if chinese:
        lines = [
            "# Opus 5.5 视频：主题 × 视觉风格图谱", "",
            "[English](domain-style-atlas.md) · 本页由 [`generate_domain_style_atlas.py`](../scripts/generate_domain_style_atlas.py) "
            "根据[分类 CSV](../data/domain-style.csv)、[案例 CSV](../data/cases.csv)、"
            "[9 月 27 日 X 页面互动量观察](../data/case-engagement-refresh-2026-09-27.csv)生成；"
            "[9 月 24–26 日旧观察表](../data/case-engagement-observed.csv)保留供追溯。",
            "", f"**分类数据截点：** {snapshot}（UTC）。矩阵单元是**视频文件数**：存档快照报告 1,401 个 SHA-256 "
            "去重文件，公开分类 CSV 有对应的 1,401 行，但没有文件哈希，读者无法仅凭公开文件重做去重。"
            "图谱仅纳入分类器标为 `yes` 或 `likely` 的 1,119 个文件。每个文件只进一个主要主题和一种主要风格；"
            "`style2` 未计入。分类器判断不等于原作者身份或真实模型调用得到验证。", "",
            f"143 个组合里有 92 个非空格。168 个审读帖子中，157 个案例对应 `yes`／`likely` 的文件，"
            f"落在 58 格；其余 34 个非空格没有已审读案例。在本轮官方 X 帖子页面观察里，{complete_cases}/168 帖有"
            f"**精确赞数与精确浏览数**，{exact_likes} 帖有精确赞数，{rounded_zh}"
            f"{exact_view_cases} 帖有精确浏览数，{failed_cases} 帖两项精确值均未取得。"
            f"{measured_cells}/58 个有审读案例的格子至少有一条本轮可用互动量；"
            f"下方展示 {selected_count} 个带截图案例。", "",
            "**选例规则：** 先限定在 168 个已审读案例中，再按原帖 URL 和预览时长精确对应分类结果；"
            "每格先从有本轮精确点赞或点赞缩写保守区间的案例找一例。若可能领先的点赞区间互相重叠，"
            "用精确帖子浏览量在这些候选里选择，不声称严格点赞名次；若全格缺点赞，则首例按精确浏览量。"
            "随后从剩余案例中按精确浏览数选第二例；"
            "若没有精确浏览数，才用点赞保守下界。完全没有本轮可用指标的格子只展示一例且不排名。"
            "维护者自己的帖子留在历史案例数据里，但不作为本页的展示选例。"
            "页面缩写不被伪装成精确数；赞和浏览属于 X 原帖，浏览数不是视频播放次数，"
            "多个视频附件可能共用同一帖指标。这不是质量、制作难度、Opus 贡献或效果评分。", "",
            f"**时间限制：** 本轮记录逐帖发生在 {first_observed} 至 {last_observed}（UTC），不是同一瞬间，"
            "也不是“最终”互动量。各帖发表时间、粉丝和转发条件不同；格子内展示顺序不能当成公平的作品比较。"
            "旧观察表保存 9 月 24–26 日的原始检索记录，不与本轮数字混作一次观测。"
            "截图仅用于辨认可取得的 X 预览画面，"
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
            "[27 September X-page engagement refresh](../data/case-engagement-refresh-2026-09-27.csv), "
            "[archived September 24–26 observations](../data/case-engagement-observed.csv), and "
            "[English case-note translations](../data/atlas-case-notes-en.csv).", "",
            f"**Frozen classifier data:** {snapshot} (UTC). A matrix cell counts **video files**. The snapshot reports "
            "1,401 SHA-256-distinct files, and the public classifier CSV has 1,401 corresponding rows. "
            "It does not expose hashes, so public files alone cannot repeat the byte deduplication. "
            "This atlas includes the 1,119 labeled `yes` or `likely` by the classifier. Each file "
            "has one primary domain and one primary style; `style2` is excluded. Classifier labels do not "
            "verify original authorship or actual model calls.", "",
            f"Of 143 possible combinations, 92 contain files. Among 168 reviewed source-post cases, 157 "
            f"match `yes`/`likely` files in 58 cells; the other 34 populated cells have no reviewed case. "
            f"In the dated refresh, {complete_cases}/168 posts have **both exact likes and exact views**; "
            f"{exact_likes} have exact likes, {rounded_en}{exact_view_cases} exact post views, "
            f"and {failed_cases} neither exact metric. "
            f"At least one current metric is available in {measured_cells}/58 reviewed cells. "
            f"There are {selected_count} illustrated examples below.", "",
            "**Selection rule:** First restrict to the 168 reviewed cases, then match classifier rows by exact "
            "original-post URL and preview duration. In each cell, the first example is led by current exact "
            "likes or a conservative interval from an abbreviated display. When plausible like leaders' "
            "intervals overlap, use exact post views to choose among them without claiming a strict like "
            "rank; if no likes are available, use exact views for the first example. "
            "The second example, if available, has the highest exact post views among the remaining "
            "cases; absent those, use the conservative like lower bound. A cell with no usable current "
            "measure gets one unranked visual example. The maintainer's own post remains in the historical "
            "case data but is excluded from featured examples. Likes and views belong to the X post; views "
            "are not video plays. Several attachments may share post metrics. Engagement does not score "
            "quality, effort, Opus's contribution, or effectiveness.", "",
            f"**Timing limit:** The official X-page observations span {first_observed} to {last_observed} "
            "(UTC), neither a single instant nor final counts. Posts were published at different times and "
            "have different audiences and reposting conditions. Display order is not a fair comparison of "
            "works. The separate archive preserves older September 24–26 search observations and is not "
            "mixed into this refresh. Stills identify the look of an accessible "
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
            for index, item in enumerate(state["selected"][cell]):
                case = item["case"]
                category = item["category"]
                refresh_row = item["refresh"]
                post_id = item["post_id"]
                url = case["source_url"]
                directory_url = f"cases-index.zh-CN.md#case-{post_id}"
                english_note = state["english_notes"].get(post_id) if not chinese else None
                title = safe_inline(english_note["title_en"] if english_note else case["label"])
                topic = safe_inline(category["topic_en"])
                route = safe_inline(case["primary_path"])
                creator = safe_inline(english_note["creator_account_en"] if english_note else case["creator_disclosure"])
                review = safe_inline(english_note["review_limit_en"] if english_note else case["review_note"])
                letter = "AB"[index]
                heading = (f"示例 {letter}：[{title}]({url})" if chinese else
                           f"Example {letter}: [{title}]({url})")
                if item["selection_reason"] == "unranked":
                    heading += "（未排名）" if chinese else " (unranked)"
                lines += [f"#### {heading}", "",
                          f'<a href="{url}"><img src="../assets/case-thumbnails/{post_id}.webp" '
                          f'width="160" loading="lazy" alt="Still from {html.escape(title, quote=True)}"></a>', "",
                          (f"**画面主题：** {topic} · **案例制作路径：** `{route}` · "
                           f"[完整目录]({directory_url})" if chinese else
                           f"**Subject:** {topic} · **Reviewed production path:** `{route}` · "
                           f"[Full case directory]({directory_url})"), "",
                          (f"**作者披露：** {creator}" if chinese else f"**Creator account:** {creator}"), "",
                          (f"**审读边界：** {review}" if chinese else f"**Review limit:** {review}"), "",
                          metric_line(refresh_row, chinese), "",
                          selection_line(item["selection_reason"], chinese), ""]
                if item["selection_reason"] == "unranked":
                    lines += [archived_metric_line(item["engagement"], chinese), ""]
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
