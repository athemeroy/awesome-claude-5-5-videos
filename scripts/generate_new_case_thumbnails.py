#!/usr/bin/env python3
"""Generate preview stills for seven separately dated September 27 cases.

The source MP4s were checked against the original posts during the September
27 review and are kept outside this public repository. Pass a local folder of
the nine named preview files to --source-dir; --check validates the committed
images and the explicit post/attachment mapping without any MP4s.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

from generate_case_thumbnails import check_webp, extract_still


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "new-case-thumbnails"
MANIFEST = OUTPUT / "frames.csv"
FIELDS = ["post_id", "source_url", "input_file", "media_index", "frame_ordinal", "at_seconds", "duration_s"]
# post_id, original handle, local MP4 filename, attachment number, duration in
# the public case notes, chosen ordinal among nine evenly spaced frame samples
CASES = (
    ("2104131805175844923", "JurgenPloeger", "opus55-jurgen-comparison.mp4", 1, 48.043, 3),
    ("2104009748874141941", "Gorden_Sun", "opus55-gorden-edit.mp4", 1, 15.104, 4),
    ("2103923067277733943", "Fr_Sorrentino", "opus55-sorrentino.mp4", 1, 40.192, 6),
    ("2104039075175182487", "servasyy", "opus55-servasyy.mp4", 1, 80.043, 2),
    ("2104021764863078697", "challenger_ND", "opus55-challenger-a.mp4", 1, 25.131, 1),
    ("2103869704955900023", "makevoid", "opus55-makevoid.mp4", 1, 85.547, 1),
    ("2104011150471917838", "arambarnett", "opus55-arambarnett.mp4", 1, 20.053, 6),
    # Two posts attach two different clips. Show both, preserving their roles.
    ("2104009748874141941", "Gorden_Sun", "opus55-gorden-original.mp4", 2, 15.104, 5),
    ("2104021764863078697", "challenger_ND", "opus55-challenger-b.mp4", 2, 21.000, 4),
)


def filename(post_id: str, media_index: int) -> str:
    return f"{post_id}{'-m2' if media_index == 2 else ''}.webp"


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def generate(source_dir: Path) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for post_id, handle, name, media_index, duration, ordinal in CASES:
        video = source_dir / name
        if abs(probe_duration(video) - duration) > 0.02:
            raise ValueError(f"Preview duration mismatch for {post_id}: {video}")
        at = duration * (ordinal - 0.5) / 9
        extract_still(video, at, OUTPUT / filename(post_id, media_index))
        rows.append(dict(post_id=post_id, source_url=f"https://x.com/{handle}/status/{post_id}",
                         input_file=name, media_index=str(media_index), frame_ordinal=str(ordinal),
                         at_seconds=f"{at:.3f}", duration_s=f"{duration:.3f}"))
    with MANIFEST.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} new-case stills")


def check() -> None:
    with MANIFEST.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("Unexpected new-case manifest columns")
        records = list(reader)
    if len(records) != len(CASES):
        raise ValueError(f"Expected {len(CASES)} new-case stills, found {len(records)}")
    if len({entry[0] for entry in CASES}) != 7:
        raise ValueError("Expected thumbnails for seven distinct new posts")
    for record, (post_id, handle, name, media_index, duration, ordinal) in zip(records, CASES, strict=True):
        if record != dict(post_id=post_id, source_url=f"https://x.com/{handle}/status/{post_id}",
                          input_file=name, media_index=str(media_index), frame_ordinal=str(ordinal),
                          at_seconds=f"{duration * (ordinal - 0.5) / 9:.3f}", duration_s=f"{duration:.3f}"):
            raise ValueError(f"Incorrect source/frame mapping for {post_id}")
        check_webp(OUTPUT / filename(post_id, media_index))
    if {p.name for p in OUTPUT.glob("*.webp")} != {filename(entry[0], entry[3]) for entry in CASES}:
        raise ValueError("New-case image set does not match the manifest")
    print(f"Verified {len(records)} new-case stills and source mappings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-dir", type=Path)
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(args.source_dir)
        check()


if __name__ == "__main__":
    main()
