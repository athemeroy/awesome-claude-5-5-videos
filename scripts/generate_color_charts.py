#!/usr/bin/env python3
"""Redraw the frozen color study using only its published derived data.

Install requirements-charts.txt before rendering. --check validates the
study and compares deterministic SVG bytes without writing files. PNG exports
preserve the original image links; their bytes are not a cross-platform gate.
Neither clustering nor private frame extraction is repeated by this renderer.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import FancyBboxPatch, Rectangle

from check_color_modes import check as check_data


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "color-study"
OUTPUT = ROOT / "assets" / "color-study"
BG = "#f8f6f1"
INK = "#172b32"
MUTED = "#58696d"
TEAL = "#287e81"
AMBER = "#dfaa56"
GRID = "#deded4"
LIGHT_TEAL = "#bcd9d4"
CARD = "#fffdf9"
HIGHLIGHTS = (
    ("domain", "education_science"),
    ("domain", "story_short"),
    ("style", "motion_graphics_ui"),
    ("domain", "product_ad"),
)
CHARTS = (
    "color-modes-highlight",
    "color-modes-style-atlas",
    "color-modes-domain-atlas",
    "color-modes-overview",
)
RENDER_SETTINGS = {
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "text.color": INK,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "svg.fonttype": "path",
    "svg.hashsalt": "opus55-public-color-study-v1",
    "path.simplify": False,
}


def label(ax, x, y, value, *, size=11, color=INK, weight="normal", **kwargs):
    return ax.text(x, y, str(value), fontsize=size, color=color,
                   fontweight=weight, va="center", **kwargs)


def canvas(width: float, height: float):
    fig = plt.figure(figsize=(width, height), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.set_axis_off()
    return fig, ax


def contrast_color(hex_color: str) -> str:
    rgb = to_rgb(hex_color)
    linear = [value / 12.92 if value <= 0.04045 else
              ((value + 0.055) / 1.055) ** 2.4 for value in rgb]
    luminance = sum(a * b for a, b in zip(linear, (0.2126, 0.7152, 0.0722)))
    return "#ffffff" if luminance < 0.18 else INK


def safe_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "-", value)


def load_data():
    # This checks the public classifier, vectors, assignments, summaries,
    # swatches, JSON, and post-level engagement denominators before rendering.
    validated = check_data()
    full = json.loads((DATA / "color-modes.json").read_text(encoding="utf-8"))
    with (DATA / "per-video-color-vectors.csv").open(encoding="utf-8", newline="") as stream:
        vectors = list(csv.DictReader(stream))
    if len(vectors) != validated["files"] or full["n_files"] != validated["files"]:
        raise ValueError("Color chart denominator differs from the checked study")
    return full, vectors


def signature(mode: dict) -> str:
    return mode["color_signature_en"].replace(" · ", " / ").replace(
        "neutral-dominant", "neutral")


def likes_label(mode: dict) -> str:
    stats = mode["exact_likes_20260927"]
    n = stats["n_posts_with_likes"]
    median = stats["median"]
    value = f"{median:,.0f}" if n >= 3 else "—"
    if n >= 3 and median != int(median):
        value = f"{median:,.1f}"
    return f"{value} · n={n}" + (" †" if n < 5 else "")


def palette_atlas(full: dict, groups: list[dict], title: str):
    width = 14.4
    row_height = 0.52
    card_gap = 0.18
    card_sizes = [0.61 + row_height * len(group["modes"]) for group in groups]
    header_height = 1.53
    body_end = header_height + sum(card_sizes) + card_gap * (len(groups) - 1)
    height = body_end + 1.20
    fig, ax = canvas(width, height)
    label(ax, 0.4, 0.48, title, size=24, weight="bold")
    label(ax, 0.4, 0.92,
          f"Frozen {full['sample_snapshot_date']} · {full['n_files']:,} distinct preview files · "
          f"{full['n_posts']:,} source posts · {full['n_frames']:,} frames",
          size=11, color=MUTED)
    label(ax, 0.63, 1.31, "MODE / COLOR COMPOSITION", size=10, weight="bold", color=MUTED)
    label(ax, 4.0, 1.31, "PALETTE · WIDTH = PIXEL SHARE", size=10, weight="bold", color=MUTED)
    label(ax, 10.35, 1.31, "FILES / CATEGORY", size=10, weight="bold", color=MUTED)
    label(ax, 12.23, 1.31, "LIKES · POST n", size=10, weight="bold", color=MUTED)
    palette_x, palette_width = 4.0, 5.95
    swatch_titles = {}
    top = header_height
    for group, card_height in zip(groups, card_sizes):
        ax.add_patch(FancyBboxPatch(
            (0.4, top), width - 0.8, card_height,
            boxstyle="round,pad=0,rounding_size=0.07", linewidth=0.7,
            edgecolor=GRID, facecolor=CARD))
        label(ax, 0.63, top + 0.28, group["name_en"], size=13, weight="bold")
        label(ax, 13.75, top + 0.28,
              f"{group['n_files']:,} files · {group['n_modes']} color "
              + ("mode" if group["n_modes"] == 1 else "modes"),
              size=10, color=MUTED, ha="right")
        ax.plot((0.63, 13.75), (top + 0.50, top + 0.50), color=GRID, lw=0.65)
        for idx, mode in enumerate(group["modes"]):
            y = top + 0.75 + idx * row_height
            label(ax, 0.63, y, f"{mode['mode_rank']:02d}", size=11, color=TEAL, weight="bold")
            label(ax, 1.06, y, signature(mode), size=11)
            pixel_total = mode["n_sampled_pixels"]
            x = palette_x
            for swatch in mode["palette"]:
                # Counts, rather than rounded proportions, conserve the full
                # bar length while encoding the actual assigned pixel shares.
                share = swatch["sampled_pixels"] / pixel_total
                swatch_width = palette_width * share
                patch = Rectangle((x, y - 0.15), swatch_width, 0.30,
                                  linewidth=0, facecolor=swatch["hex"])
                gid = f"swatch-{safe_id(mode['mode_id'])}-{swatch['rank']}"
                patch.set_gid(gid)
                swatch_titles[gid] = (f"{group['name_en']}, mode {mode['mode_rank']}: "
                                       f"{swatch['hex']}, {share * 100:.2f}% of sampled pixels")
                ax.add_patch(patch)
                if share >= 0.085:
                    label(ax, x + swatch_width / 2, y, f"{share * 100:.0f}%",
                          size=9, color=contrast_color(swatch["hex"]), ha="center")
                x += swatch_width
            ax.add_patch(Rectangle((palette_x, y - 0.15), palette_width, 0.30,
                                   fill=False, linewidth=0.65, edgecolor=GRID))
            file_share = mode["n_files"] / group["n_files"] * 100
            label(ax, 10.35, y, f"{mode['n_files']:,} / {group['n_files']:,}", size=11, weight="bold")
            label(ax, 11.98, y, f"{file_share:.1f}%", size=9, color=MUTED, ha="right")
            label(ax, 12.23, y, likes_label(mode), size=11)
        top += card_height + card_gap
    label(ax, 0.4, body_end + 0.31,
          "Six measured swatches per mode; each bar sums to 100% of that mode's pixels. "
          "File share and pixel share use different denominators.", size=10, color=MUTED)
    label(ax, 0.4, body_end + 0.60,
          "Likes = post-level median observed on 2026-09-27; n = posts with exact likes. "
          "† Fewer than 5 posts; medians hidden below 3.", size=10, color=MUTED)
    label(ax, 0.4, body_end + 0.89,
          "Likes do not enter color clustering. Ambiguous multi-mode posts are excluded from "
          "mode likes; these comparisons do not establish causation.", size=10, color=MUTED)
    description = (f"{title}. The study includes {full['n_files']} distinct files from "
                   f"{full['n_posts']} source posts. Each mode shows six swatches with widths "
                   "proportional to measured pixel assignments, its file count within the category, "
                   "and exact September 27 median likes with a separate post count. "
                   "Sparse like observations do not support causal comparisons.")
    return fig, title, description, swatch_titles


def colorful_overview(full: dict, vectors: list[dict]):
    names = {group["group_id"]: group["name_en"] for group in full["groups"]
             if group["group_type"] == "domain"}
    values = defaultdict(list)
    for vector in vectors:
        values[vector["domain"]].append(float(vector["colorful_pixel_share"]) * 100)
    if set(values) != set(names):
        raise ValueError("Overview domain set differs from the published modes")
    summaries = []
    for key, sample in values.items():
        q1, _, q3 = statistics.quantiles(sample, n=4, method="inclusive")
        summaries.append((key, len(sample), q1, statistics.median(sample), q3))
    summaries.sort(key=lambda row: (-row[3], row[0]))
    width, height = 13.4, 8.5
    fig, ax = canvas(width, height)
    title = "How much of each preview is visibly colorful?"
    label(ax, 0.45, 0.48, title, size=23, weight="bold")
    label(ax, 0.45, 0.95,
          f"{full['n_files']:,} distinct files · {len(summaries)} content domains · "
          "each file contributes equal weight", size=12, color=MUTED)
    label(ax, 0.45, 1.49, "CONTENT DOMAIN", size=10, color=MUTED, weight="bold")
    label(ax, 3.7, 1.49, "FILES", size=10, color=MUTED, weight="bold", ha="right")
    label(ax, 12.87, 1.49, "MEDIAN", size=10, color=MUTED, weight="bold", ha="right")
    x0, scale, y0, row_gap = 4.15, 0.069, 2.11, 0.435
    chart_bottom = y0 + (len(summaries) - 1) * row_gap
    for tick in (0, 25, 50, 75, 100):
        x = x0 + tick * scale
        ax.plot((x, x), (y0 - 0.28, chart_bottom + 0.25), color=GRID, lw=0.75, zorder=0)
        label(ax, x, 1.73, f"{tick}%", size=10, color=MUTED, ha="center")
    for index, (key, n_files, q1, median, q3) in enumerate(summaries):
        y = y0 + index * row_gap
        label(ax, 0.45, y, names[key], size=12)
        label(ax, 3.7, y, f"{n_files:,}", size=11, color=MUTED, ha="right")
        ax.plot((x0 + q1 * scale, x0 + q3 * scale), (y, y),
                color=LIGHT_TEAL, lw=10, solid_capstyle="butt")
        ax.plot((x0 + q1 * scale, x0 + q1 * scale), (y - 0.10, y + 0.10), color=TEAL, lw=1.2)
        ax.plot((x0 + q3 * scale, x0 + q3 * scale), (y - 0.10, y + 0.10), color=TEAL, lw=1.2)
        ax.scatter((x0 + median * scale,), (y,), s=55, c=TEAL, edgecolor=BG, linewidth=1.0, zorder=3)
        label(ax, 12.87, y, f"{median:.1f}%", size=12, weight="bold", ha="right")
    label(ax, x0, chart_bottom + 0.65, "Share of sampled pixels in each file", size=11, color=MUTED)
    label(ax, 0.45, 7.49,
          "Dot = median per-file share; line = middle 50% of files. "
          "Broad overlap describes variation within each domain.", size=11, color=MUTED)
    label(ax, 0.45, 7.83,
          "Colorful = HSV saturation ≥ 0.25 and value ≥ 0.15; "
          "9 frames × 32 × 32 pixels per file. Letterboxing remains.", size=10, color=MUTED)
    label(ax, 0.45, 8.15,
          f"Frozen {full['sample_snapshot_date']} · Retrieved, classifier-labeled yes/likely sample; "
          "this chart does not estimate X-wide prevalence.", size=10, color=MUTED)
    description = (f"Colorful pixel share by content domain in {full['n_files']} distinct files. "
                   "Domains are ordered by the median share. Points mark per-file medians, "
                   "bands show the 25th to 75th percentiles, and file counts appear separately. "
                   + "; ".join(f"{names[key]}: {median:.1f}% median, {n_files} files"
                               for key, n_files, _, median, _ in summaries) + ".")
    return fig, title, description, {}


def render_svg(fig, title: str, description: str, swatch_titles: dict) -> bytes:
    output = io.BytesIO()
    fig.savefig(output, format="svg", metadata={
        "Date": None,
        "Creator": "awesome-opus-5-5-videos public color study renderer",
        "Title": title,
        "Description": description,
    })
    svg = output.getvalue().decode("utf-8")
    # Font outlines preserve column alignment across reader platforms. Keep
    # chart-level accessibility and per-swatch tooltips alongside the paths.
    # Generated IDs are fixed by svg.hashsalt and explicit swatch IDs.
    svg = re.sub(r"<svg\b[^>]*>", lambda match:
                 match.group(0).replace("<svg ", '<svg role="img" aria-labelledby="chart-title chart-description" ', 1)
                 + f'\n <title id="chart-title">{html.escape(title)}</title>'
                 + f'\n <desc id="chart-description">{html.escape(description)}</desc>', svg, count=1)
    for gid, tooltip in swatch_titles.items():
        svg = svg.replace(f'<g id="{gid}">',
                          f'<g id="{gid}"><title>{html.escape(tooltip)}</title>', 1)
    return ("\n".join(line.rstrip() for line in svg.splitlines()) + "\n").encode("utf-8")


def build(full: dict, vectors: list[dict]):
    grouped = {(group["group_type"], group["group_id"]): group for group in full["groups"]}
    yield CHARTS[0], palette_atlas(full, [grouped[key] for key in HIGHLIGHTS],
                                  "Several color modes can coexist in one category")
    for name, family, title in (
        (CHARTS[1], "style", "Color palettes across all 13 visual styles"),
        (CHARTS[2], "domain", "Color palettes across all 11 content domains"),
    ):
        groups = [group for group in full["groups"] if group["group_type"] == family]
        groups.sort(key=lambda group: (-group["n_files"], group["group_id"]))
        yield name, palette_atlas(full, groups, title)
    yield CHARTS[3], colorful_overview(full, vectors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check SVG outputs without writing files")
    args = parser.parse_args()
    try:
        full, vectors = load_data()
        mismatches = []
        with plt.rc_context(RENDER_SETTINGS):
            for name, (fig, title, description, swatch_titles) in build(full, vectors):
                try:
                    rendered = render_svg(fig, title, description, swatch_titles)
                    path = OUTPUT / f"{name}.svg"
                    if args.check:
                        if not path.exists() or path.read_bytes() != rendered:
                            mismatches.append(str(path.relative_to(ROOT)))
                    else:
                        OUTPUT.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(rendered)
                        # Existing PNG links continue to show the redesigned
                        # charts. SVG is the reproducible, scalable source.
                        if name != CHARTS[3]:
                            fig.savefig(OUTPUT / f"{name}.png", dpi=140,
                                        metadata={"Software": "opus55 public color study renderer"})
                finally:
                    plt.close(fig)
        if mismatches:
            print("Color charts differ; rerun scripts/generate_color_charts.py:\n"
                  + "\n".join(mismatches), file=sys.stderr)
            return 1
        action = "Checked" if args.check else "Rendered"
        print(f"{action} {len(CHARTS)} color SVG charts from {full['n_files']:,} frozen files")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Color chart generation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
