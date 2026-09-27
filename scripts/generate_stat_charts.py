#!/usr/bin/env python3
"""Render reproducible SVG charts from the public, frozen CSV snapshot.

All marks are counts or quantiles of the published rows. Run with --check in CI;
the script then compares the rendered SVG bytes without changing any files.
"""

from __future__ import annotations

import argparse
import html
import math
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path

from generate_statistics import DOMAINS, PATHS, STYLES, duration, quartiles, summary


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    "style-labels.svg": ROOT / "assets" / "style-labels.svg",
    "preview-duration.svg": ROOT / "assets" / "preview-duration.svg",
    "domain-style-heatmap.svg": ROOT / "assets" / "domain-style-heatmap.svg",
}
INK = "#172742"
MUTED = "#50627e"
GRID = "#dce5f0"
YES = "#365d9d"
LIKELY = "#e6a34b"
BG = "#fbfcff"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, *, size: int = 17,
         weight: int = 400, fill: str = INK, anchor: str = "start",
         extra: str = "") -> str:
    return (f'<text x="{x:g}" y="{y:g}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'{extra}>{esc(value)}</text>')


def line(x1: float, y1: float, x2: float, y2: float,
         *, stroke: str = GRID, width: float = 1) -> str:
    return (f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
            f'stroke="{stroke}" stroke-width="{width:g}"/>')


def rect(x: float, y: float, width: float, height: float, fill: str,
         *, rx: int = 0, stroke: str = "none") -> str:
    return (f'<rect x="{x:g}" y="{y:g}" width="{width:g}" height="{height:g}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}"/>')


def svg(width: int, height: int, title: str, description: str,
        shapes: list[str]) -> str:
    return "\n".join([
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        'role="img" aria-labelledby="chart-title chart-description">',
        f'<title id="chart-title">{esc(title)}</title>',
        f'<desc id="chart-description">{esc(description)}</desc>',
        '<style>text{font-family:Inter,"DejaVu Sans",Arial,sans-serif}</style>',
        rect(0, 0, width, height, BG),
        *shapes,
        '</svg>',
        '',
    ])


def style_labels(data: dict) -> str:
    yes = Counter(row["style"] for row in data["strict"])
    likely = Counter(row["style"] for row in data["classified"] if row["opus_made"] == "likely")
    keys = sorted(STYLES, key=lambda key: (-(yes[key] + likely[key]), key))
    assert sum(yes.values()) == len(data["strict"])
    assert sum(likely.values()) == data["labels"]["likely"]
    max_tick = max(400, math.ceil(max(yes[key] + likely[key] for key in keys) / 100) * 100)
    x0, scale, y0, row = 365, 680 / max_tick, 186, 52
    bottom = y0 + len(keys) * row
    parts = [
        text(56, 64, "Primary visual styles in the retrieved corpus", size=34, weight=700),
        text(56, 96, f"{len(data['classified']):,} classified MP4 files · {len(data['strict']):,} yes + "
             f"{sum(likely.values()):,} likely shown · one primary style per file", size=17, fill=MUTED),
        rect(58, 121, 22, 16, YES, rx=3), text(88, 135, "yes", size=16),
        rect(162, 121, 22, 16, LIKELY, rx=3), text(192, 135, "likely (added)", size=16),
    ]
    for tick in range(0, max_tick + 1, 100):
        x = x0 + tick * scale
        parts.append(line(x, y0 - 23, x, bottom - 7))
        parts.append(text(x, bottom + 21, tick, size=15, fill=MUTED, anchor="middle"))
    for idx, key in enumerate(keys):
        cy = y0 + idx * row + 19
        strict, added = yes[key], likely[key]
        parts.append(text(x0 - 23, cy + 6, STYLES[key][0], size=18, anchor="end"))
        parts.append(rect(x0, cy - 13, strict * scale, 27, YES, rx=2))
        if added:
            parts.append(rect(x0 + strict * scale, cy - 13, added * scale, 27, LIKELY, rx=2))
        parts.append(text(x0 + (strict + added) * scale + 12, cy + 6,
                          strict + added, size=17, weight=700))
    parts.extend([
        text(x0, bottom + 58, "Number of distinct-file rows", size=16, fill=MUTED),
        text(56, 955, "Frozen " + datetime.fromisoformat(data["snapshot"]["snapshot_utc"]).strftime("%d %b %Y")
             + " · Search-retrieved files; classifier labels are not independently verified model use.", size=15, fill=MUTED),
        text(56, 978, "Counts describe this retrieval, not X-wide prevalence. See docs/statistics.md for denominators and limits.", size=15, fill=MUTED),
    ])
    return svg(1200, 1000, "Primary visual styles in the retrieved corpus",
               f"Horizontal stacked bars for {len(keys)} primary visual styles in "
               f"{len(data['strict'])} yes and {sum(likely.values())} likely classifier-labeled files.", parts)


def preview_duration(data: dict) -> str:
    rows = []
    for key, en, _ in PATHS:
        values = [duration(case, "cases.csv") for case in data["cases"] if case["primary_path"] == key]
        q1, median, q3 = quartiles(values)
        rows.append((en, len(values), q1, median, q3))
    rows.sort(key=lambda item: item[3])
    assert sum(row[1] for row in rows) == len(data["cases"])
    max_tick = max(300, math.ceil(max(row[4] for row in rows) / 60) * 60)
    x0, scale, y0, row_gap = 405, 630 / max_tick, 194, 66
    bottom = y0 + len(rows) * row_gap
    parts = [
        text(55, 64, "Preview length by reviewed production path", size=34, weight=700),
        text(55, 96, f"{len(data['cases'])} selected source posts · dot = median · thick line = 25th–75th percentile", size=17, fill=MUTED),
        text(55, 125, "Ordered by median; different path sample sizes are shown beside their labels.", size=16, fill=MUTED),
    ]
    for tick in range(0, max_tick + 1, 60):
        x = x0 + tick * scale
        parts.append(line(x, y0 - 25, x, bottom - 35))
        parts.append(text(x, bottom - 3, tick, size=15, fill=MUTED, anchor="middle"))
    for idx, (label, count, q1, median, q3) in enumerate(rows):
        cy = y0 + idx * row_gap + 17
        parts.append(text(55, cy + 5, label, size=17))
        parts.append(text(x0 - 23, cy + 5, f"n={count}", size=15, fill=MUTED, anchor="end"))
        parts.append(line(x0 + q1 * scale, cy, x0 + q3 * scale, cy,
                          stroke="#a7bedb", width=16))
        parts.append(line(x0 + q1 * scale, cy - 11, x0 + q1 * scale, cy + 11,
                          stroke=YES, width=2))
        parts.append(line(x0 + q3 * scale, cy - 11, x0 + q3 * scale, cy + 11,
                          stroke=YES, width=2))
        parts.append(f'<circle cx="{x0 + median * scale:g}" cy="{cy:g}" r="8" fill="{YES}"/>')
        parts.append(text(x0 + q3 * scale + 13, cy + 5, f"{median:.1f}s median",
                          size=15, weight=700, fill=YES))
    parts.extend([
        text(x0, bottom + 32, "X preview duration (seconds)", size=16, fill=MUTED),
        text(55, 714, "These are manually selected cases, not a random sample or a measure of path success.", size=15, fill=MUTED),
        text(55, 737, "Preview length may differ from the upload master. Quartiles use Python's inclusive method.", size=15, fill=MUTED),
    ])
    return svg(1200, 760, "Preview length by reviewed production path",
               f"{len(rows)} reviewed production paths ordered by median duration, with median dots, interquartile bars, "
               f"and {len(data['cases'])} total case counts.", parts)


DOMAIN_SHORT = {
    "ai_self_meta": ("AI about", "AI"),
    "art_abstract": ("Art /", "abstract"),
    "data_viz": ("Data", "viz"),
    "education_science": ("Education /", "science"),
    "game_interactive": ("Games /", "interactive"),
    "history_culture": ("History /", "culture"),
    "humor_meme": ("Humor /", "meme"),
    "music_video": ("Music", "video"),
    "other": ("Other", ""),
    "product_ad": ("Ads /", "launches"),
    "story_short": ("Short", "story"),
}
HEAT_BINS = (
    (0, "#edf2f7", "#7b8ca3"),
    (4, "#dcebf8", INK),
    (9, "#a9d0ed", INK),
    (24, "#70abda", INK),
    (49, "#347eba", "#ffffff"),
    (99, "#195c98", "#ffffff"),
    (float("inf"), "#103b70", "#ffffff"),
)


def heat_color(count: int) -> tuple[str, str]:
    for maximum, fill, label in HEAT_BINS:
        if count <= maximum:
            return fill, label
    raise AssertionError(count)


def domain_style_heatmap(data: dict) -> str:
    counts = Counter((row["domain"], row["style"]) for row in data["inclusive"])
    domains = sorted(DOMAINS, key=lambda key: (-sum(counts[key, style] for style in STYLES), key))
    styles = sorted(STYLES, key=lambda key: (-sum(counts[domain, key] for domain in DOMAINS), key))
    assert sum(counts.values()) == len(data["inclusive"]) and set(domains) == set(DOMAIN_SHORT)
    x0, y0, w, h = 290, 195, 82, 48
    parts = [
        text(54, 62, "Where domains and styles meet", size=35, weight=700),
        text(54, 96, f"{len(data['inclusive']):,} files labeled yes or likely · "
             "one classifier-assigned primary domain and style per file", size=17, fill=MUTED),
        text(54, 126, "Color and printed value both encode file count. Blank cells contain zero files in this retrieval.", size=16, fill=MUTED),
    ]
    legend_x = 400
    legend_labels = ("0", "1–4", "5–9", "10–24", "25–49", "50–99", "100+")
    for idx, (_, fill, _) in enumerate(HEAT_BINS):
        x = legend_x + idx * 114
        parts.append(rect(x, 150, 23, 18, fill, rx=2, stroke="#cad6e6"))
        parts.append(text(x + 30, 165, legend_labels[idx], size=14, fill=MUTED))
    for ridx, style in enumerate(styles):
        cy = y0 + ridx * h + h / 2
        parts.append(text(x0 - 14, cy + 6, STYLES[style][0], size=17, anchor="end"))
        for cidx, domain in enumerate(domains):
            count = counts[domain, style]
            x, y = x0 + cidx * w, y0 + ridx * h
            fill, label_fill = heat_color(count)
            parts.append(rect(x + 2, y + 2, w - 4, h - 4, fill, rx=4))
            if count:
                parts.append(text(x + w / 2, y + h / 2 + 6, count,
                                  size=17, weight=700, fill=label_fill, anchor="middle"))
    label_y = y0 + len(styles) * h + 30
    for idx, key in enumerate(domains):
        cx = x0 + idx * w + w / 2
        a, b = DOMAIN_SHORT[key]
        parts.append(text(cx, label_y, a, size=14, anchor="middle"))
        if b:
            parts.append(text(cx, label_y + 19, b, size=14, anchor="middle"))
    parts.extend([
        text(54, 908, "This heatmap describes the retrieved files only. A file is not an independent creator or a verified Opus run.", size=15, fill=MUTED),
        text(54, 932, "Open the case atlas for pictured examples and the statistics page for method and denominator details.", size=15, fill=MUTED),
    ])
    return svg(1240, 960, "Where domains and styles meet",
               f"{len(domains)} domains by {len(styles)} visual styles, colored by count among "
               f"{len(data['inclusive'])} classified yes or likely files.", parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check rendered SVGs for drift")
    args = parser.parse_args()
    try:
        data = summary()
        rendered = {
            "style-labels.svg": style_labels(data),
            "preview-duration.svg": preview_duration(data),
            "domain-style-heatmap.svg": domain_style_heatmap(data),
        }
        for filename, value in rendered.items():
            ET.fromstring(value)
            target = OUTPUTS[filename]
            if args.check:
                if not target.exists() or target.read_text(encoding="utf-8") != value:
                    print(f"Stale chart: {target.relative_to(ROOT)}", file=sys.stderr)
                    return 1
            else:
                target.write_text(value, encoding="utf-8")
                print(f"Updated {target.relative_to(ROOT)}")
        if args.check:
            print("All three public statistical charts match the frozen CSV snapshot")
        return 0
    except (OSError, ValueError, KeyError, AssertionError, ET.ParseError) as exc:
        print(f"Chart generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
