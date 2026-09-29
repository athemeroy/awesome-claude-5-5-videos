#!/usr/bin/env python3
"""Render the README evidence overview, workflow diagram and prompt counts.

The overview uses the frozen public snapshot; prompt bars use the published
source-linked count receipt. The workflow diagram summarizes reviewed roles.
Run --check to detect drift, or --preview-dir DIR for local PNG previews.
"""

from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import StrMethodFormatter

ROOT = Path(__file__).resolve().parents[1]
BG, INK, MUTED = "#f8f6f1", "#172b32", "#5c6d70"
TEAL, AMBER, GRID = "#287e81", "#dfaa56", "#deded5"
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "svg.hashsalt": "hypit-intro-20260926",
        "svg.fonttype": "path",
    }
)


def heading(fig, title, subtitle):
    fig.text(0.055, 0.925, title, fontsize=23, weight="bold", va="top")
    fig.text(0.055, 0.86, subtitle, fontsize=11, color=MUTED, va="top")


def overview(snapshot):
    fig = plt.figure(figsize=(12.8, 6.5))
    heading(
        fig,
        "From search hits to inspectable evidence",
        "Frozen 26 Sep 2026 corpus · counts use different units",
    )
    cards = [
        (
            snapshot["candidate_posts"],
            "Candidate posts",
            "Deduplicated source-post IDs",
            TEAL,
        ),
        (
            snapshot["candidate_posts_with_mp4"],
            "Posts with MP4",
            "A post can carry several files",
            TEAL,
        ),
        (
            snapshot["mp4_attachments"],
            "MP4 attachments",
            "Every attachment sampled in nine frames",
            TEAL,
        ),
        (
            snapshot["sha256_distinct"],
            "Byte-distinct files",
            "SHA-256 removes exact file copies",
            TEAL,
        ),
        (
            sum(snapshot["classifier_opus_made_labels"][k] for k in ("yes", "likely")),
            "Files labeled yes / likely",
            "Classifier judgments of Opus involvement",
            TEAL,
        ),
        (
            snapshot["curated_cases"],
            "Reviewed case posts",
            "Deliberately selected for evidence review",
            AMBER,
        ),
    ]
    for i, (n, label, note, accent) in enumerate(cards):
        x, y = 0.055 + (i % 3) * 0.305, 0.50 - (i // 3) * 0.30
        card = FancyBboxPatch(
            (x, y),
            0.28,
            0.255,
            transform=fig.transFigure,
            boxstyle="round,pad=0.012,rounding_size=0.016",
            facecolor="#ffffff",
            edgecolor=GRID,
            linewidth=0.8,
        )
        fig.add_artist(card)
        fig.text(
            x + 0.018, y + 0.172, f"{n:,}", fontsize=31, weight="bold", color=accent
        )
        fig.text(x + 0.018, y + 0.112, label, fontsize=13, weight="bold")
        fig.text(x + 0.018, y + 0.058, note, fontsize=8.8, color=MUTED)
    fig.text(
        0.055,
        0.085,
        "The 168 cases are a curated sample; these cards are not a statistical sampling funnel.",
        fontsize=10,
        color=MUTED,
    )
    fig.text(
        0.055,
        0.045,
        "Source: data/corpus-snapshot.json · search terms, caps and reposts limit coverage.",
        fontsize=9,
        color=MUTED,
    )
    return (
        fig,
        "From search hits to inspectable evidence",
        "Six different evidence counts from the frozen September 26 snapshot.",
    )


def production_paths():
    fig = plt.figure(figsize=(12.8, 7.4))
    heading(
        fig,
        "What made the pixels?",
        "Four broad roles in the reviewed workflows · a similar frame can come from different tools",
    )
    roles = [
        (
            "01",
            "Write rendering code",
            "Brief + assets",
            "Canvas / WebGL / Manim",
            "Code renders the frames",
        ),
        (
            "02",
            "Transform supplied media",
            "Footage, audio or images",
            "Redraw / edit / composite",
            "Existing inputs shape the result",
        ),
        (
            "03",
            "Direct external models",
            "Storyboard + prompts",
            "Image / video / audio tools",
            "Models supply media; tools assemble it",
        ),
        (
            "04",
            "Build an app or game",
            "Requirements + code",
            "Runnable interaction",
            "The video records the program",
        ),
    ]
    for i, (number, title, inputs, tools, result) in enumerate(roles):
        x, y = 0.055 + (i % 2) * 0.475, 0.485 - (i // 2) * 0.31
        card = FancyBboxPatch(
            (x, y),
            0.445,
            0.265,
            transform=fig.transFigure,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor="#ffffff",
            edgecolor=GRID,
            linewidth=0.9,
        )
        fig.add_artist(card)
        fig.text(x + 0.02, y + 0.205, number, fontsize=14, weight="bold", color=TEAL)
        fig.text(x + 0.065, y + 0.205, title, fontsize=16, weight="bold")
        fig.text(x + 0.02, y + 0.148, inputs, fontsize=11, color=MUTED)
        fig.text(x + 0.02, y + 0.099, "→  " + tools, fontsize=12, color=TEAL)
        fig.text(x + 0.02, y + 0.045, result, fontsize=10.5, color=MUTED)
    fig.text(
        0.055,
        0.088,
        "Read creator disclosures, matching public projects and sampled previews together.",
        fontsize=11,
        color=MUTED,
    )
    fig.text(
        0.055,
        0.047,
        "Seven detailed review paths and source examples are listed in data/cases.csv and the README.",
        fontsize=9,
        color=MUTED,
    )
    return (
        fig,
        "What made the pixels?",
        "Four broad workflow roles: code rendering, supplied-media transformation, external-model direction, and program capture.",
    )


def prompt_lengths(rows):
    required = {"author", "post_id", "source_url", "visible_characters"}
    if len(rows) != 5 or any(not required <= row.keys() for row in rows):
        raise ValueError("Expected the five published prompt-count receipts")
    seen = set()
    for row in rows:
        if (
            row["post_id"] in seen
            or not isinstance(row["visible_characters"], int)
            or row["visible_characters"] <= 0
            or row["source_url"]
            != f"https://x.com/{row['author'].removeprefix('@')}/status/{row['post_id']}"
        ):
            raise ValueError("Invalid prompt count or source URL")
        seen.add(row["post_id"])
    rows = sorted(rows, key=lambda row: row["visible_characters"])
    fig, ax = plt.subplots(figsize=(12.8, 6.5))
    low, high = rows[0]["visible_characters"], rows[-1]["visible_characters"]
    heading(
        fig,
        f"A ‘prompt’ can mean {low:,} or {high:,} visible characters",
        "Five selected public posts · reported character counts include visible technical instructions",
    )
    fig.subplots_adjust(left=0.24, right=0.92, bottom=0.23, top=0.73)
    ax.barh(
        range(len(rows)),
        [r["visible_characters"] for r in rows],
        color=TEAL,
        height=0.52,
    )
    ax.set_yticks(range(len(rows)), [r["author"] for r in rows], fontsize=12)
    ax.invert_yaxis()
    ax.set_xlim(0, 20500)
    ax.set_xticks([0, 5000, 10000, 15000, 20000])
    ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.tick_params(length=0, pad=10)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i, row in enumerate(rows):
        ax.text(
            row["visible_characters"] + 250,
            i,
            f"{row['visible_characters']:,}",
            va="center",
            fontsize=13,
            weight="bold",
        )
    ax.set_xlabel("Visible characters in the published post", fontsize=10, labelpad=13)
    fig.text(
        0.055,
        0.105,
        "Character count does not include supplied files, prior project work or hidden revisions.",
        fontsize=10,
        color=MUTED,
    )
    fig.text(
        0.055,
        0.061,
        "Selected examples do not measure typical prompt size, token cost or video quality.",
        fontsize=9,
        color=MUTED,
    )
    return (
        fig,
        "Visible prompt lengths in five selected posts",
        "Reported visible-character counts for five public prompts, from 172 to 17,664 characters.",
    )


def render(fig, title, description):
    buffer = io.StringIO()
    fig.savefig(
        buffer,
        format="svg",
        facecolor=BG,
        metadata={
            "Date": None,
            "Creator": "Hypit public chart generator",
            "Title": title,
            "Description": description,
        },
    )
    value = buffer.getvalue()
    value = re.sub(
        r"(<svg\b[^>]*)(>)",
        r'\1 role="img" aria-label="' + html.escape(title, quote=True) + r'"\2',
        value,
        count=1,
        flags=re.S,
    )
    ET.fromstring(value)
    return "\n".join(line.rstrip() for line in value.splitlines()) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    if args.check and args.preview_dir:
        parser.error("--check must not write previews")
    snapshot = json.loads((ROOT / "data/corpus-snapshot.json").read_text())
    prompts = json.loads((ROOT / "data/visible-prompt-lengths.json").read_text())
    figures = {
        "corpus-overview.svg": overview(snapshot),
        "production-paths.svg": production_paths(),
        "prompt-lengths.svg": prompt_lengths(prompts),
    }
    for name, (fig, title, description) in figures.items():
        target = ROOT / "assets" / name
        expected = render(fig, title, description)
        if args.check:
            if not target.exists() or target.read_text() != expected:
                print(f"Intro figure is stale: {name}", file=sys.stderr)
                return 1
        else:
            target.write_text(expected, encoding="utf-8")
            if args.preview_dir:
                args.preview_dir.mkdir(parents=True, exist_ok=True)
                fig.savefig(
                    args.preview_dir / Path(name).with_suffix(".png"),
                    dpi=140,
                    facecolor=BG,
                )
        plt.close(fig)
    print(
        "Three README introductory figures match the published source data"
        if args.check
        else "Wrote three README introductory figures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
