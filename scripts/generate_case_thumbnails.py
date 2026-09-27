#!/usr/bin/env python3
"""Make one small, attributed preview still per curated video case.

Generation needs the private, locally downloaded X previews and Hypit media
receipts. The public repository distributes only the resulting stills and a
frame manifest, never the MP4s or nine-frame audit sheets. ``--check`` needs
only public files and verifies coverage, dimensions, and the manifest join.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_CSV = ROOT / "data" / "cases.csv"
THUMB_DIR = ROOT / "assets" / "case-thumbnails"
MANIFEST = THUMB_DIR / "frames.csv"
FIELDNAMES = ["post_id", "source_url", "media_index", "frame_ordinal", "at_seconds"]
MAX_DIMENSION = 480
# Selected after reviewing every thumbnail in a four-page montage. These six
# heuristic picks were blank transitions or obscured subjects in their clips.
MANUAL_FRAMES = {
    "2103108551799632050": 5,  # visible first-party product interface
    "2102436464323661880": 6,  # black-hole scene, not empty transition sky
    "2103449416325890146": 4,  # generative graphic, not blue transition
    "2103024907965612250": 5,  # Dictus product phone, not transition sky
    "2103171975220781332": 8,  # visible character face
    "2102463796149440888": 7,  # colorful sunflower scene
}


def cases() -> list[dict[str, str]]:
    with CASE_CSV.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 168:
        raise ValueError(f"Expected frozen 168 curated cases; found {len(rows)}")
    ids = [row["source_url"].rsplit("/", 1)[-1] for row in rows]
    if len(set(ids)) != len(ids) or not all(i.isdecimal() for i in ids):
        raise ValueError("Case post IDs are missing or repeated")
    return rows


def still_score(cell: Image.Image, ordinal: int) -> float:
    """Favor a legible interior frame over a blank/title/end frame.

    This is only a visual triage heuristic. The complete 168-image montage is
    inspected after generation; a still is not a quality score for a video.
    """
    from PIL import ImageStat

    rgb = cell.convert("RGB")
    gray = rgb.convert("L")
    stats = ImageStat.Stat(gray)
    mean = stats.mean[0]
    dark = sum(gray.histogram()[:18]) / (gray.width * gray.height)
    bright = sum(gray.histogram()[240:]) / (gray.width * gray.height)
    saturation = ImageStat.Stat(rgb.convert("HSV")).mean[1] / 255
    return (
        gray.entropy()
        + stats.stddev[0] / 70
        + min(saturation, 0.6)
        - 3 * max(0, dark - 0.65)
        - 2 * max(0, bright - 0.78)
        + 0.25 * (1 - abs(ordinal - 4) / 4)
    )


def choose_frame(receipt: dict, tile_path: Path, post_id: str) -> tuple[int, float]:
    from PIL import Image

    tile = receipt["tile"]
    frames = tile["frames"]
    if len(frames) != 9 or tile["columns"] != 3 or tile["rows"] != 3:
        raise ValueError("Unexpected nine-frame sampling layout")
    with Image.open(tile_path) as source:
        width, height = source.size
        cell_width = tile["cellWidth"]
        if width != 3 * (cell_width + 8) + 8 or (height - 8) % 3:
            raise ValueError(f"Unexpected contact-sheet dimensions: {tile_path}")
        stride = (height - 8) // 3
        cell_height = stride - 33  # eight-pixel gutter and timestamp strip
        if cell_height < 40:
            raise ValueError(f"Invalid contact-sheet cell height: {tile_path}")
        scores = []
        for ordinal, frame in enumerate(frames):
            col, row = ordinal % 3, ordinal // 3
            left = 8 + col * (cell_width + 8)
            top = 8 + row * stride
            cell = source.crop((left, top, left + cell_width, top + cell_height))
            scores.append(still_score(cell, ordinal))
    ordinal = MANUAL_FRAMES.get(post_id, max(range(9), key=lambda i: scores[i]) + 1) - 1
    return ordinal + 1, float(frames[ordinal]["at"])


def expected_image(post_id: str) -> Path:
    return THUMB_DIR / f"{post_id}.webp"


def verify_media(row: dict[str, str], receipt: dict, video_path: Path) -> None:
    post_id = row["source_url"].rsplit("/", 1)[-1]
    if receipt.get("source_post_id", receipt["id"]) != post_id or receipt.get("media_index", 1) != 1:
        raise ValueError(f"Receipt is not first attachment for {post_id}")
    if receipt["status"] != "tile_ok" or not video_path.is_file():
        raise ValueError(f"Missing verified MP4 for {post_id}")
    if abs(float(row["duration_s"]) - float(receipt["probe"]["duration"])) > 0.011:
        raise ValueError(f"CSV/receipt duration mismatch for {post_id}")
    digest = hashlib.sha256(video_path.read_bytes()).hexdigest()
    if digest != receipt["sha256"]:
        raise ValueError(f"Video hash mismatch for {post_id}")


def extract_still(video_path: Path, at_seconds: float, output: Path) -> None:
    from PIL import Image

    with tempfile.TemporaryDirectory(prefix="hypit-still-") as work:
        png = Path(work) / "frame.png"
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-ss",
                f"{at_seconds:.6f}", "-i", str(video_path), "-frames:v", "1",
                "-y", str(png),
            ],
            check=True,
        )
        with Image.open(png) as source:
            image = source.convert("RGB")
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
            image.save(output, format="WEBP", quality=72, method=6)


def check_webp(path: Path) -> None:
    """Validate basic WebP structure and size without image dependencies."""
    data = path.read_bytes()
    if len(data) < 30 or len(data) > 200_000 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError(f"Invalid or oversized WebP thumbnail: {path}")
    if int.from_bytes(data[4:8], "little") + 8 != len(data):
        raise ValueError(f"Truncated WebP thumbnail: {path}")
    kind = data[12:16]
    if kind == b"VP8 ":
        if data[23:26] != b"\x9d\x01\x2a":
            raise ValueError(f"Invalid VP8 frame header: {path}")
        width = int.from_bytes(data[26:28], "little") & 0x3FFF
        height = int.from_bytes(data[28:30], "little") & 0x3FFF
    elif kind == b"VP8L":
        if data[20] != 0x2F:
            raise ValueError(f"Invalid VP8L frame header: {path}")
        b1, b2, b3, b4 = data[21:25]
        width = 1 + b1 + ((b2 & 0x3F) << 8)
        height = 1 + (b2 >> 6) + (b3 << 2) + ((b4 & 0x0F) << 10)
    elif kind == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
    else:
        raise ValueError(f"Unsupported WebP thumbnail format: {path}")
    if not 40 <= min(width, height) <= max(width, height) <= MAX_DIMENSION:
        raise ValueError(f"Unexpected thumbnail dimensions {width}x{height}: {path}")


def generate(source_root: Path) -> None:
    rows = cases()
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    for number, row in enumerate(rows, 1):
        post_id = row["source_url"].rsplit("/", 1)[-1]
        receipt_path = source_root / "data" / "media-receipts" / f"{post_id}.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        video = source_root / "media" / f"{post_id}.mp4"
        tile = source_root / "evidence" / f"{post_id}.jpg"
        verify_media(row, receipt, video)
        ordinal, at_seconds = choose_frame(receipt, tile, post_id)
        extract_still(video, at_seconds, expected_image(post_id))
        manifest.append(
            {
                "post_id": post_id,
                "source_url": row["source_url"],
                "media_index": "1",
                "frame_ordinal": str(ordinal),
                "at_seconds": f"{at_seconds:.3f}",
            }
        )
        if number % 25 == 0 or number == len(rows):
            print(f"Generated {number}/{len(rows)} curated stills", flush=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest)


def check() -> None:
    rows = cases()
    with MANIFEST.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError("Unexpected thumbnail manifest columns")
        records = list(reader)
    if len(records) != len(rows):
        raise ValueError(f"Thumbnail manifest has {len(records)} rows for {len(rows)} cases")
    for row, record in zip(rows, records, strict=True):
        post_id = row["source_url"].rsplit("/", 1)[-1]
        if record["post_id"] != post_id or record["source_url"] != row["source_url"]:
            raise ValueError(f"Thumbnail/source mismatch for {post_id}")
        if record["media_index"] != "1" or int(record["frame_ordinal"]) not in range(1, 10):
            raise ValueError(f"Invalid selected frame for {post_id}")
        at = float(record["at_seconds"])
        if not math.isfinite(at) or not 0 < at < float(row["duration_s"]):
            raise ValueError(f"Thumbnail time is outside preview for {post_id}")
        check_webp(expected_image(post_id))
    actual = {p.name for p in THUMB_DIR.glob("*.webp")}
    expected = {f"{record['post_id']}.webp" for record in records}
    if actual != expected:
        raise ValueError(f"Thumbnail file count/mapping mismatch: {len(actual)} vs {len(expected)}")
    print(f"Verified {len(records)} one-frame thumbnails and source mappings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-root", type=Path, help="local Hypit source root with media and receipts")
    group.add_argument("--check", action="store_true", help="check public coverage without MP4s")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        generate(args.source_root)
        check()


if __name__ == "__main__":
    main()
