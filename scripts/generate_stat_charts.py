#!/usr/bin/env python3
"""Render four reproducible statistical SVGs from the frozen public CSVs.

Install requirements-charts.txt first. All marks and conclusions derive from
published rows; --check compares SVG bytes without changing the assets.
"""

from __future__ import annotations

import argparse
import io
import math
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch, Rectangle

from generate_statistics import DOMAINS, PATHS, STYLES, duration, quartiles, summary


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    name: ROOT / "assets" / name
    for name in (
        "domain-labels.svg", "style-labels.svg", "domain-style-heatmap.svg",
        "preview-duration.svg",
    )
}
BG = "#f8f6f1"
INK = "#172b32"
MUTED = "#536368"
GRID = "#dedfd6"
YES = "#287e81"
LIKELY = "#dfaa56"
SVG_NS = "http://www.w3.org/2000/svg"
HEAT_COLORS = ("#eeeae1", "#e0eeea", "#b8d6cf", "#85bdb6", "#5b9e9c", YES, "#174d51")
HEAT_LABELS = ("0", "1–4", "5–9", "10–24", "25–49", "50–99", "100+")
DOMAIN_SHORT = {
    "ai_self_meta": "AI about\nAI",
    "art_abstract": "Art /\nabstract",
    "data_viz": "Data\nvisualization",
    "education_science": "Education /\nscience",
    "game_interactive": "Games /\ninteractive",
    "history_culture": "History /\nculture",
    "humor_meme": "Humor /\nmeme",
    "music_video": "Music\nvideo",
    "other": "Other",
    "product_ad": "Ads /\nlaunches",
    "story_short": "Short\nstory",
}
PATH_SHORT = {
    "procedural_2d": "Code-drawn 2D",
    "educational_explainer": "Educational explainer",
    "3d_or_realtime_graphics": "3D / real-time graphics",
    "existing_source_transformation": "Existing-source edit",
    "external_video_model": "External video model",
    "app_or_game_capture": "App / game capture",
    "mixed_or_not_established": "Mixed / unestablished",
}


def configure() -> None:
    """Pin font metrics, generated IDs and SVG metadata for byte comparisons."""
    matplotlib.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "svg.fonttype": "path",
        "svg.hashsalt": "hypit-frozen-statistics-v2",
        "axes.unicode_minus": False,
    })


def figure(size: tuple[float, float], category: str, title: str,
           subtitle: str, data: dict) -> plt.Figure:
    fig = plt.figure(figsize=size)
    fig.text(.055, .956, category.upper(), color=YES, fontsize=10, weight="bold", va="top")
    fig.text(.055, .91, title, fontsize=23, weight="bold", va="top")
    fig.text(.055, .853, subtitle, color=MUTED, fontsize=10.7, va="top")
    frozen = datetime.fromisoformat(data["snapshot"]["snapshot_utc"]).strftime("%d %b %Y")
    fig.text(.055, .035, f"Frozen {frozen} UTC · Public CSV snapshot", color=MUTED, fontsize=9.5)
    return fig


def finish(fig: plt.Figure, title: str, description: str,
           preview_dir: Path | None, filename: str) -> str:
    """Use stable SVG bytes while adding an accessible chart description."""
    if preview_dir is not None:
        preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_dir / filename.replace(".svg", ".png"), dpi=140)
    stream = io.StringIO()
    fig.savefig(stream, format="svg", metadata={"Date": None, "Creator": "hypit statistical charts"})
    plt.close(fig)
    value = stream.getvalue()
    # Preserve Matplotlib's serialization, which includes stable font paths and
    # IDs, rather than reserializing the entire XML with platform-dependent prefixes.
    root = ET.fromstring(value)
    root_start = value.index("<svg ")
    root_end = value.index(">", root_start)
    accessible = ' role="img" aria-labelledby="chart-title chart-description"'
    title_node = ET.Element("title", {"id": "chart-title"})
    title_node.text = title
    desc_node = ET.Element("desc", {"id": "chart-description"})
    desc_node.text = description
    extra = ET.tostring(title_node, encoding="unicode") + "\n " + ET.tostring(desc_node, encoding="unicode")
    value = value[:root_end] + accessible + value[root_end:root_end + 1] + "\n " + extra + value[root_end + 1:]
    assert root.tag == f"{{{SVG_NS}}}svg"
    value = "\n".join(line.rstrip() for line in value.splitlines()) + "\n"
    ET.fromstring(value)
    return value


def clean_axes(ax: plt.Axes, *, grid_axis: str = "x") -> None:
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color=GRID, linewidth=.8)
    ax.tick_params(axis="both", length=0)


def label_counts(data: dict, key: str) -> tuple[Counter, Counter]:
    yes = Counter(row[key] for row in data["strict"])
    likely = Counter(row[key] for row in data["classified"] if row["opus_made"] == "likely")
    assert sum(yes.values()) == len(data["strict"])
    assert sum(likely.values()) == data["labels"]["likely"]
    assert sum(yes.values()) + sum(likely.values()) == len(data["inclusive"])
    return yes, likely


def label_bars(data: dict, key: str, labels: dict, preview_dir: Path | None) -> str:
    yes, likely = label_counts(data, key)
    keys = sorted(labels, key=lambda item: (-(yes[item] + likely[item]), item))
    total = len(data["inclusive"])
    totals = [yes[item] + likely[item] for item in keys]
    if key == "domain":
        share = sum(yes[item] + likely[item] for item in
                    ("game_interactive", "product_ad", "ai_self_meta")) / total * 100
        title = f"Games, ads and AI account for {share:.0f}% of files"
        category = "Primary domains"
        height = 8.2
    else:
        share = sum(yes[item] + likely[item] for item in
                    ("motion_graphics_ui", "3d_render")) / total * 100
        title = f"Motion graphics and 3D account for {share:.0f}%"
        category = "Primary visual styles"
        height = 9.0
    subtitle = f"{total:,} yes / likely files of {len(data['classified']):,} byte-distinct MP4s · one primary {key} per file"
    fig = figure((12, height), category, title, subtitle, data)
    fig.legend(
        handles=[Patch(facecolor=YES, label=f"yes · {sum(yes.values()):,}"),
                 Patch(facecolor=LIKELY, label=f"likely · {sum(likely.values()):,}")],
        loc="upper left", bbox_to_anchor=(.045, .81), ncols=2,
        frameon=False, fontsize=10.5, handlelength=1.5, columnspacing=2,
    )
    ax = fig.add_axes((.265, .18, .67, .57))
    positions = np.arange(len(keys))
    ax.barh(positions, [yes[item] for item in keys], color=YES, height=.62)
    ax.barh(positions, [likely[item] for item in keys],
            left=[yes[item] for item in keys], color=LIKELY, height=.62)
    ax.set_yticks(positions, [labels[item][0] for item in keys], fontsize=11.5)
    ax.tick_params(axis="y", pad=13)
    ax.invert_yaxis()
    ax.set_ylim(len(keys) - .35, -.65)
    largest = max(totals)
    upper = math.ceil(largest / 50) * 50
    ax.set_xlim(0, upper * 1.27)
    ticks = np.arange(0, upper + 1, 50 if upper <= 300 else 100)
    ax.set_xticks(ticks)
    ax.set_xlabel("File count", fontsize=10.5, labelpad=13)
    clean_axes(ax)
    for index, count in enumerate(totals):
        ax.text(count + largest * .025, index,
                f"{count:,}  ·  {count / total * 100:.1f}%", fontsize=10.8,
                va="center", weight="bold")
    fig.text(.055, .091, "Bars show classifier labels; percentages use the 1,119 yes / likely files.".replace("1,119", f"{total:,}"),
             fontsize=9.8, color=MUTED)
    fig.text(.055, .064, "Retrieved files describe this sample; they do not measure X-wide prevalence or verified model use.",
             fontsize=9.8, color=MUTED)
    description = f"{total} yes or likely files. " + "; ".join(
        f"{labels[item][0]}: {yes[item]} yes, {likely[item]} likely, {totals[index] / total * 100:.1f}% of included files"
        for index, item in enumerate(keys)
    ) + ". Classifier labels are not independently verified model use."
    return finish(fig, title, description, preview_dir, f"{key}-labels.svg")


def domain_labels(data: dict, preview_dir: Path | None = None) -> str:
    return label_bars(data, "domain", DOMAINS, preview_dir)


def style_labels(data: dict, preview_dir: Path | None = None) -> str:
    return label_bars(data, "style", STYLES, preview_dir)


def domain_style_heatmap(data: dict, preview_dir: Path | None = None) -> str:
    counts = Counter((row["domain"], row["style"]) for row in data["inclusive"])
    domains = sorted(DOMAINS, key=lambda item: (-sum(counts[item, style] for style in STYLES), item))
    styles = sorted(STYLES, key=lambda item: (-sum(counts[domain, item] for domain in DOMAINS), item))
    matrix = np.array([[counts[domain, style] for domain in domains] for style in styles])
    assert int(matrix.sum()) == len(data["inclusive"]) and set(domains) == set(DOMAIN_SHORT)
    strongest = counts.most_common(2)
    leading = sum(value for _, value in strongest)
    total = len(data["inclusive"])
    leading_pairs = {("game_interactive", "3d_render"), ("product_ad", "motion_graphics_ui")}
    title = ("Games × 3D and ads × motion graphics lead"
             if {pair for pair, _ in strongest} == leading_pairs
             else "Two domain / style pairs lead the sample")
    subtitle = f"{total:,} yes / likely files · the two largest pairs contain {leading:,} files ({leading / total * 100:.1f}%)"
    fig = figure((12.8, 9.8), "Domain × visual style", title, subtitle, data)
    ax = fig.add_axes((.245, .255, .705, .495))
    boundaries = [-.5, .5, 4.5, 9.5, 24.5, 49.5, 99.5, max(100, int(matrix.max())) + .5]
    colors = ListedColormap(HEAT_COLORS)
    norm = BoundaryNorm(boundaries, colors.N)
    ax.imshow(matrix, cmap=colors, norm=norm, aspect="auto", interpolation="none")
    ax.set_xticks(np.arange(len(domains)), [DOMAIN_SHORT[item] for item in domains], fontsize=9.5)
    ax.set_yticks(np.arange(len(styles)), [STYLES[item][0] for item in styles], fontsize=11)
    ax.tick_params(axis="x", length=0, pad=12)
    ax.tick_params(axis="y", length=0, pad=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(domains), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(styles), 1), minor=True)
    ax.grid(which="minor", color=BG, linewidth=3)
    ax.tick_params(which="minor", length=0)
    for row_index, style in enumerate(styles):
        for col_index, domain in enumerate(domains):
            count = counts[domain, style]
            ax.text(col_index, row_index, str(count) if count else "–",
                    ha="center", va="center", fontsize=10.7,
                    weight="bold" if count else "normal",
                    color="#ffffff" if count >= 50 else (INK if count else "#9b9f96"))
    for (domain, style), _ in strongest:
        ax.add_patch(Rectangle((domains.index(domain) - .47, styles.index(style) - .47), .94, .94,
                               fill=False, edgecolor=LIKELY, linewidth=2.5, zorder=4))
    fig.text(.055, .16, "Files per cell", fontsize=10, color=MUTED, va="center")
    for index, (color, label) in enumerate(zip(HEAT_COLORS, HEAT_LABELS)):
        x = .245 + index * .095
        fig.add_artist(Rectangle((x, .15), .022, .019, transform=fig.transFigure,
                                  facecolor=color, edgecolor=GRID, linewidth=.6))
        fig.text(x + .029, .1595, label, fontsize=9.5, va="center", color=MUTED)
    fig.text(.245, .122, "Amber outlines mark the two largest pairs; dashes indicate zero files.", fontsize=9.6, color=MUTED)
    fig.text(.055, .078, "One primary domain and style per file. Classifier labels describe retrieved files, not independent creators.",
             fontsize=9.7, color=MUTED)
    description = f"Heatmap of {total} yes or likely files, {len(domains)} domains and {len(styles)} styles. " + "; ".join(
        f"{DOMAINS[domain][0]} / {STYLES[style][0]}: {count}"
        for (domain, style), count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ) + ". Missing pairs have zero files."
    return finish(fig, title, description, preview_dir, "domain-style-heatmap.svg")


def preview_duration(data: dict, preview_dir: Path | None = None) -> str:
    rows = []
    for key, _, _ in PATHS:
        values = [duration(case, "cases.csv") for case in data["cases"] if case["primary_path"] == key]
        q1, median, q3 = quartiles(values)
        rows.append((key, len(values), q1, median, q3))
    rows.sort(key=lambda item: (item[3], item[0]))
    assert sum(row[1] for row in rows) == len(data["cases"])
    title = f"Path medians range from {rows[0][3]:.0f} to {rows[-1][3]:.0f} seconds"
    fig = figure((12, 7.6), "Reviewed preview duration", title,
                 f"{len(data['cases'])} selected source posts · dots show medians; bars show the middle 50% of previews", data)
    fig.text(.055, .79, "Sorted by median · n is the number of selected cases in each path", fontsize=10.5, color=MUTED)
    ax = fig.add_axes((.31, .22, .62, .51))
    upper = max(300, math.ceil(max(row[4] for row in rows) / 60) * 60)
    ax.set_xlim(0, upper)
    positions = np.arange(len(rows))
    ax.set_yticks(positions, [f"{PATH_SHORT[key]}  (n={count})" for key, count, *_ in rows], fontsize=11)
    ax.tick_params(axis="y", pad=12)
    ax.set_ylim(len(rows) - .3, -.7)
    ax.set_xticks(np.arange(0, upper + 1, 60))
    ax.set_xlabel("X preview duration (seconds)", fontsize=10.5, labelpad=14)
    clean_axes(ax)
    for index, (_, _, q1, median, q3) in enumerate(rows):
        ax.plot([q1, q3], [index, index], linewidth=12, color="#a8cec4", solid_capstyle="round")
        ax.plot([q1, q3], [index, index], linestyle="none", marker="|", markersize=18,
                markeredgewidth=1.7, color=YES)
        ax.scatter([median], [index], s=110, color=YES, edgecolor=BG, linewidth=1.6, zorder=3)
        ax.text(q3 + upper * .035, index, f"{median:.1f}s", fontsize=11,
                color=YES, weight="bold", va="center")
    fig.text(.055, .12, "Selected examples are not a random sample; preview length does not measure production time or success.",
             fontsize=9.7, color=MUTED)
    fig.text(.055, .088, "The upload master may be longer. Quartiles use the inclusive method.", fontsize=9.7, color=MUTED)
    description = f"{len(data['cases'])} selected source posts, ordered by path median preview duration. " + "; ".join(
        f"{PATH_SHORT[key]}, n={count}: median {median:.3f} seconds, middle 50% {q1:.3f} to {q3:.3f} seconds"
        for key, count, q1, median, q3 in rows
    ) + ". These manually selected cases are not a random sample."
    return finish(fig, title, description, preview_dir, "preview-duration.svg")


def render(data: dict, preview_dir: Path | None = None) -> dict[str, str]:
    configure()
    return {
        "domain-labels.svg": domain_labels(data, preview_dir),
        "style-labels.svg": style_labels(data, preview_dir),
        "domain-style-heatmap.svg": domain_style_heatmap(data, preview_dir),
        "preview-duration.svg": preview_duration(data, preview_dir),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check all four rendered SVGs for drift")
    parser.add_argument("--preview-dir", type=Path, help="Also export PNGs to this directory for visual review")
    args = parser.parse_args()
    if args.check and args.preview_dir:
        parser.error("--preview-dir writes PNG files; use it without --check")
    try:
        rendered = render(summary(), args.preview_dir)
        stale = []
        for filename, value in rendered.items():
            target = OUTPUTS[filename]
            if args.check:
                if not target.exists() or target.read_text(encoding="utf-8") != value:
                    stale.append(target.relative_to(ROOT))
            else:
                target.write_text(value, encoding="utf-8")
                print(f"Updated {target.relative_to(ROOT)}")
        if stale:
            for target in stale:
                print(f"Stale chart: {target}", file=sys.stderr)
            return 1
        if args.check:
            print("All four public statistical charts match the frozen CSV snapshot")
        return 0
    except (OSError, ValueError, KeyError, AssertionError, ET.ParseError) as exc:
        print(f"Chart generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
