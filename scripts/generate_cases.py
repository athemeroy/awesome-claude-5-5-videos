#!/usr/bin/env python3
"""Render the browsable case directory from the public CSV.

The CSV is the only source for cases, group counts, URLs, durations and
observations. Run with --check to detect a stale generated page.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import html
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "cases.csv"
OUTPUT = ROOT / "docs" / "cases-index.zh-CN.md"
THUMBNAIL_DIR = ROOT / "assets" / "case-thumbnails"

# Presentation order and display names; case data and counts come from SOURCE.
PATHS = (
    ("procedural_2d", "Code-drawn 2D and motion graphics", "程序逐帧绘图"),
    ("educational_explainer", "Educational explainers", "知识讲解"),
    ("3d_or_realtime_graphics", "3D and real-time graphics", "三维与实时图形"),
    ("existing_source_transformation", "Existing-source transformation", "现有素材改编"),
    ("external_video_model", "External video-model pipelines", "外部视频模型编排"),
    ("app_or_game_capture", "App and game capture", "应用与游戏录屏"),
    ("mixed_or_not_established", "Mixed or unestablished pipeline", "混合或流程未确定"),
)
REQUIRED_COLUMNS = (
    "source_url",
    "primary_path",
    "label",
    "creator_disclosure",
    "hypit_observation",
    "review_note",
    "duration_s",
    "hypit_status",
)
POST_URL = re.compile(r"^https://x\.com/[^/]+/status/(\d+)$")
LEADING_DURATION = re.compile(
    r"(?<!\d)(?:\d+m)?\d+(?:\.\d+)?\s*(?:s|秒)(?![A-Za-z])",
    re.IGNORECASE,
)
UNSAFE_START = re.compile(
    r"^(?:[／/、,，;；:：]|(?:with|and|or|of|for|to|in|on|at|by|from|as)\b)",
    re.IGNORECASE,
)


def read_cases() -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen_ids: set[str] = set()
    valid_paths = {key for key, _, _ in PATHS}
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != list(REQUIRED_COLUMNS):
            raise ValueError(f"Unexpected CSV columns: {reader.fieldnames!r}")
        for line_number, row in enumerate(reader, start=2):
            if not all(row.get(column, "").strip() for column in REQUIRED_COLUMNS):
                raise ValueError(f"Blank required field on CSV line {line_number}")
            match = POST_URL.fullmatch(row["source_url"])
            if not match:
                raise ValueError(f"Invalid original post URL on CSV line {line_number}")
            post_id = match.group(1)
            if post_id in seen_ids:
                raise ValueError(f"Duplicate post ID {post_id} on CSV line {line_number}")
            seen_ids.add(post_id)
            if row["primary_path"] not in valid_paths:
                raise ValueError(f"Unknown primary_path on CSV line {line_number}")
            if row["hypit_status"] != "tile_ok":
                raise ValueError(f"Case lacks nine-frame sampling on CSV line {line_number}")
            if not (THUMBNAIL_DIR / f"{post_id}.webp").is_file():
                raise ValueError(f"Case lacks a representative still on CSV line {line_number}")
            try:
                duration = float(row["duration_s"])
            except ValueError as exc:
                raise ValueError(f"Invalid duration on CSV line {line_number}") from exc
            if not (0 < duration < float("inf")):
                raise ValueError(f"Invalid duration on CSV line {line_number}")
            groups[row["primary_path"]].append(row)
    if not seen_ids:
        raise ValueError("Case CSV is empty")
    return groups


def table_text(value: str) -> str:
    """Preserve source wording while keeping each entry in one Markdown cell."""
    return " ".join(value.split()).replace("|", r"\|")


def observation_without_duplicate_duration(value: str) -> str:
    """Drop a standalone opening duration clause, preserving attached prose.

    The duration_s column is authoritative for this page. Some older prose in
    hypit_observation repeats a different length. An opening like "32 s with"
    or "32 秒／24fps" is not an independent clause; removing it would leave a
    dangling preposition or separator. Multi-cut observations stay intact.
    """
    observation = " ".join(value.split())
    match = LEADING_DURATION.search(observation)
    if match is None or match.start() > 45:
        return observation
    following = observation[match.end() :].lstrip()
    if not following or following[0] not in ",，.。;；:：":
        return observation
    without_prefix = following.lstrip(",，.。;；:： ")
    if not without_prefix or UNSAFE_START.match(without_prefix):
        return observation
    return without_prefix


def anchor(title: str, count: int) -> str:
    return "#" + re.sub(r"[^a-z0-9-]", "", title.lower().replace(" ", "-")) + f"-{count}"


def render(groups: dict[str, list[dict[str, str]]]) -> str:
    total = sum(len(rows) for rows in groups.values())
    lines = [
        "# Case directory / 案例目录",
        "",
        "<!-- Generated by scripts/generate_cases.py from data/cases.csv. Do not edit by hand. -->",
        "",
        f"This directory links to the original X posts for **{total} reviewed cases**. "
        "It is a curated index, not a census or quality ranking. Durations are from "
        "accessible X preview MP4s, not necessarily the creators' masters. A few older "
        "observation notes give different durations; their cause has not been reconciled. The final "
        "column draws from the CSV's `hypit_observation` field, omitting a "
        "standalone opening duration clause when possible. It describes the sampled X preview; any production "
        "attribution in that field remains a creator report. Nine frames cannot "
        "verify full-motion or audio quality or hidden model calls. Read the "
        "[CSV](../data/cases.csv) for creator disclosures and detailed review limits.",
        "",
        "Each small still is a single frame from the accessible X preview, "
        "selected to help identify the visible style. Click the adjacent case "
        "name or still to open the creator's original post. The frame is a "
        "commentary excerpt, not a licensed video, master-quality sample, or "
        "measure of animation quality; rights remain with its source creator.",
        "",
        f"本目录收录 **{total} 条人工深读案例**，标题直达 X 原帖。它不是全站作品数量或质量排名；"
        "时长来自可取得的 X 预览 MP4，不一定是作者母版；少数旧观察文字的片长另有差异，原因尚未逐项复核。"
        "末列取自 CSV 的 `hypit_observation`，"
        "只在开头片长构成独立短语时省去。它描述取样预览；其中的制作归因仍须按作者披露理解。"
        "九帧不能验收全片运动、声音或隐藏模型调用。"
        "作者披露及逐案审读边界见[原始 CSV](../data/cases.csv)。",
        "",
        "每张小图仅截取可取得的 X 预览视频一帧，用来辨认画面风格；点击图片或案例标题可看作者原帖。"
        "它并非获授权的完整视频、母版画质样本或动画质量评分；原画面权利仍属于创作者。",
        "",
        "## Browse by production path / 按制作路径浏览",
        "",
    ]
    for key, title, chinese in PATHS:
        count = len(groups.get(key, []))
        lines.append(f"- [{chinese} · {title} ({count})]({anchor(title, count)})")
    lines.append("")
    for key, title, chinese in PATHS:
        rows = groups.get(key, [])
        lines.extend(
            [
                f"## {title} ({len(rows)})",
                "",
                f"{chinese} · `primary_path={key}`",
                "",
                "| Still / 截图 | Case / 原帖 | Preview (s) / 秒 | Nine-frame note / 九帧记录 |",
                "|---|---|---:|---|",
            ]
        )
        for row in rows:
            label = table_text(row["label"]).replace("[", r"\[").replace("]", r"\]")
            observation = table_text(
                observation_without_duplicate_duration(row["hypit_observation"])
            )
            post_id = row["source_url"].rsplit("/", 1)[-1]
            still = (
                f'<a href="{html.escape(row["source_url"], quote=True)}">'
                f'<img src="../assets/case-thumbnails/{post_id}.webp" width="160" '
                f'loading="lazy" alt="X preview still for {html.escape(row["label"], quote=True)}"></a>'
            )
            lines.append(
                f'| {still} | [{label}]({row["source_url"]}) | {row["duration_s"]} | {observation} |'
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="fail if docs/cases-index.zh-CN.md is stale"
    )
    args = parser.parse_args()
    try:
        expected = render(read_cases())
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Case directory generation failed: {exc}\n")
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != expected:
            diff = difflib.unified_diff(
                current.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(OUTPUT),
                tofile="generated from data/cases.csv",
            )
            sys.stderr.writelines(diff)
            print("Case directory is out of date; run scripts/generate_cases.py", file=sys.stderr)
            return 1
        print(f"Case directory is current: {OUTPUT.relative_to(ROOT)}")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
