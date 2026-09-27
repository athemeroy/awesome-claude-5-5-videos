#!/usr/bin/env python3
"""Generate nine small stills from our eight Thusfar ads and X video essay.

The eight ad stills use the verified local X previews. The video essay uses
the 47.062-second local upload master named in the project handoff. No video
files are copied into the public repository. ``--check`` needs public files
only; ``--source-root`` regenerates from the private local source project.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

from generate_case_thumbnails import check_webp, extract_still


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "our-videos"
MANIFEST = OUTPUT / "frames.csv"
FIELDS = ["file", "source_url", "theme", "language", "media_index", "at_seconds"]
# Both attachment languages were confirmed by inspecting all eight nine-frame
# samples: attachment 1 is Chinese and attachment 2 is English in each post.
ADS = (
    ("core-zh.webp", "2103108551799632050", "core idea", "Chinese", 1, 5),
    ("core-en.webp", "2103108551799632050", "core idea", "English", 2, 4),
    ("features-zh.webp", "2103109243377504468", "features", "Chinese", 1, 6),
    ("features-en.webp", "2103109243377504468", "features", "English", 2, 5),
    ("technology-zh.webp", "2103109979905675371", "technology", "Chinese", 1, 6),
    ("technology-en.webp", "2103109979905675371", "technology", "English", 2, 6),
    ("teaser-zh.webp", "2103110282444771733", "vertical teaser", "Chinese", 1, 5),
    ("teaser-en.webp", "2103110282444771733", "vertical teaser", "English", 2, 5),
)
ESSAY_FILE = "opus-world-en.webp"
ESSAY_POST = "https://x.com/WangYeruo/status/2103279925960876265"
ESSAY_DURATION = 47.062
ESSAY_FRAME_AT = 13.1  # colorful domain jars in the published video


def source_for(source_root: Path, post_id: str, media_index: int) -> tuple[dict, Path]:
    suffix = "" if media_index == 1 else "-m2"
    receipt_path = source_root / "data" / "media-receipts" / f"{post_id}{suffix}.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    video = source_root / "media" / f"{post_id}{suffix}.mp4"
    if receipt.get("source_post_id", receipt["id"]) != post_id:
        raise ValueError(f"Wrong source post for {post_id}{suffix}")
    if receipt.get("media_index", 1) != media_index or receipt["status"] != "tile_ok":
        raise ValueError(f"Wrong attachment or failed media check for {post_id}{suffix}")
    if hashlib.sha256(video.read_bytes()).hexdigest() != receipt["sha256"]:
        raise ValueError(f"MP4 hash mismatch for {post_id}{suffix}")
    return receipt, video


def generate(source_root: Path) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for filename, post_id, theme, language, media_index, frame_ordinal in ADS:
        receipt, video = source_for(source_root, post_id, media_index)
        at = receipt["tile"]["frames"][frame_ordinal - 1]["at"]
        extract_still(video, at, OUTPUT / filename)
        rows.append(
            dict(file=filename, source_url=f"https://x.com/WangYeruo/status/{post_id}",
                 theme=theme, language=language, media_index=str(media_index),
                 at_seconds=f"{at:.3f}")
        )
    essay_video = source_root / "reports" / "opus-world-en.mp4"
    if not essay_video.is_file():
        raise ValueError("Missing local master for the 47-second published essay")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(essay_video)],
        check=True, capture_output=True, text=True,
    )
    if abs(float(probe.stdout.strip()) - ESSAY_DURATION) > 0.02:
        raise ValueError("Local essay master does not match the published 47-second version")
    extract_still(essay_video, ESSAY_FRAME_AT, OUTPUT / ESSAY_FILE)
    rows.append(dict(file=ESSAY_FILE, source_url=ESSAY_POST, theme="video essay",
                     language="English", media_index="local upload master",
                     at_seconds=f"{ESSAY_FRAME_AT:.3f}"))
    with MANIFEST.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} first-party video stills")


def check() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("Unexpected first-party still manifest columns")
        rows = list(reader)
    expected = [entry[0] for entry in ADS] + [ESSAY_FILE]
    if [row["file"] for row in rows] != expected:
        raise ValueError("First-party still manifest order or coverage changed")
    if {p.name for p in OUTPUT.glob("*.webp")} != set(expected):
        raise ValueError("First-party still files do not match the manifest")
    for row in rows:
        if not row["source_url"].startswith("https://x.com/WangYeruo/status/"):
            raise ValueError(f"Wrong source URL for {row['file']}")
        check_webp(OUTPUT / row["file"])
    print(f"Verified {len(rows)} first-party stills and source mappings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-root", type=Path)
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(args.source_root)
        check()


if __name__ == "__main__":
    main()
