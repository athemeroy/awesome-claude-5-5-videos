#!/usr/bin/env python3
"""Draw the frozen classifier-domain chart from the public file-level CSV.

Requires matplotlib. Run from any directory; the input CSV is never modified.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "domain-style.csv"
SNAPSHOT = ROOT / "data" / "corpus-snapshot.json"
OUTPUT = ROOT / "assets" / "domain-labels.svg"

NAMES = {
    "game_interactive": "Games & interactive demos",
    "product_ad": "Ads & launches",
    "ai_self_meta": "AI about AI",
    "education_science": "Explainers",
    "story_short": "Short stories",
    "music_video": "Music videos",
    "history_culture": "History & culture",
    "art_abstract": "Art & abstract",
    "humor_meme": "Humor & memes",
    "data_viz": "Data visualization",
    "other": "Other",
}


def main() -> None:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    labels = Counter(row["opus_made"] for row in rows)
    assert len(rows) == snapshot["domain_style_classified_files"] == 1401
    assert dict(labels) == snapshot["classifier_opus_made_labels"]
    assert set(row["domain"] for row in rows) <= set(NAMES)

    yes = Counter(row["domain"] for row in rows if row["opus_made"] == "yes")
    likely = Counter(row["domain"] for row in rows if row["opus_made"] == "likely")
    domains = sorted(NAMES, key=lambda key: (-(yes[key] + likely[key]), key))
    y = range(len(domains))
    strict = [yes[key] for key in domains]
    added = [likely[key] for key in domains]
    total = [a + b for a, b in zip(strict, added)]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "svg.fonttype": "path",
            "svg.hashsalt": "opus55-domain-labels-20260926",
        }
    )
    fig, ax = plt.subplots(figsize=(10.6, 7.2), facecolor="#fbfcff")
    ax.set_facecolor("#fbfcff")
    ax.barh(y, strict, height=0.66, color="#4056a1", label="yes (strict label)")
    ax.barh(y, added, left=strict, height=0.66, color="#e6a84a", label="likely (added)")
    ax.set_yticks(list(y), [NAMES[key] for key in domains])
    ax.invert_yaxis()
    ax.set_xlim(0, max(total) * 1.17)
    ax.set_xlabel("Byte-distinct X MP4 files labeled yes or likely")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#dfe5ef", linewidth=0.8)
    ax.tick_params(axis="both", length=0, colors="#26324d")
    for spine in ax.spines.values():
        spine.set_visible(False)
    for index, count in enumerate(total):
        ax.text(count + 2, index, str(count), va="center", fontsize=10, color="#26324d")
    ax.legend(
        loc="lower right",
        frameon=False,
        ncol=2,
        fontsize=10,
        bbox_to_anchor=(1.0, -0.15),
    )
    fig.suptitle(
        "Classifier-assigned domain counts",
        x=0.11,
        y=0.98,
        ha="left",
        fontsize=20,
        weight="bold",
        color="#18233d",
    )
    fig.text(
        0.11,
        0.925,
        "Frozen Sep 26, 2026 snapshot · 1,401 classified files · 980 yes + 139 likely shown",
        ha="left",
        fontsize=10,
        color="#4d5c75",
    )
    fig.text(
        0.11,
        0.015,
        "Search-retrieved files; one model-assigned primary domain per file. Counts are not X-wide prevalence or verified authorship.",
        ha="left",
        fontsize=9,
        color="#4d5c75",
    )
    fig.subplots_adjust(left=0.30, right=0.96, top=0.88, bottom=0.17)
    fig.savefig(OUTPUT, format="svg", metadata={"Date": "2026-09-26"})
    svg = OUTPUT.read_text(encoding="utf-8")
    OUTPUT.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
