#!/usr/bin/env python3
"""Check the published, frozen color study without private preview videos.

This checks conservation across the classifier, per-file vectors, mode
assignments, mode summaries, swatches, and the full JSON. It cannot verify the
original frame extraction or refit clusters without the private contact sheets.
"""

from __future__ import annotations

import csv
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COLOR = DATA / "color-study"
POST_URL = re.compile(r"https://x\.com/([^/]+)/status/(\d+)")
SHA256 = re.compile(r"[0-9a-f]{64}")
HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}")
FAMILIES = ("style", "domain")
FRAMES_PER_FILE = 9
PIXELS_PER_FRAME = 32 * 32
PIXELS_PER_FILE = FRAMES_PER_FILE * PIXELS_PER_FRAME
# The September 26/27 study is frozen; these are its published claims in
# docs/color-modes.md and the two README files.
PUBLISHED_POSTS = 1099
PUBLISHED_MODES = 53
PUBLISHED_SPLIT_CATEGORIES = {"style": 11, "domain": 10}
PUBLISHED_MODES_WITH_FIVE_EXACT_LIKES = 20
HUES = (
    "neutral", "red_orange", "yellow_green", "green_cyan",
    "cyan_blue", "blue_purple", "purple_red",
)
BINS = tuple(f"{light}_{hue}" for light in ("dark", "middle", "light") for hue in HUES)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rows(path: Path, columns: set[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames is not None and columns <= set(reader.fieldnames),
                f"Missing columns in {path}")
        require(len(reader.fieldnames) == len(set(reader.fieldnames)),
                f"Repeated column in {path}")
        result = list(reader)
    require(bool(result), f"Empty CSV: {path}")
    require(all(None not in row and all(value is not None for value in row.values())
                for row in result), f"Malformed CSV row: {path}")
    return result


def number(value: str | int | float, context: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid number for {context}: {value!r}") from exc
    require(math.isfinite(result), f"Nonfinite number for {context}")
    return result


def count(value: str | int, context: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid count for {context}: {value!r}") from exc
    require(str(result) == str(value) and result >= 0, f"Invalid count for {context}: {value!r}")
    return result


def close(actual: float, expected: float, places: int, context: str) -> None:
    # Derived CSVs round each value; allow one unit in the last published place.
    require(abs(actual - expected) <= 10 ** -places + 1e-12,
            f"{context}: {actual} != {expected}")


def post_parts(url: str) -> tuple[str, str]:
    match = POST_URL.fullmatch(url)
    require(match is not None, f"Invalid X post URL: {url}")
    return match.group(1).lower(), match.group(2)


def check() -> dict[str, int]:
    snapshot = json.loads((DATA / "corpus-snapshot.json").read_text(encoding="utf-8"))
    classified = rows(DATA / "domain-style.csv", {"post_url", "opus_made", "style", "domain"})
    labels = Counter(row["opus_made"] for row in classified)
    require(len(classified) == snapshot["domain_style_classified_files"],
            "Classifier row count differs from frozen snapshot")
    require(dict(labels) == snapshot["classifier_opus_made_labels"],
            "Classifier labels differ from frozen snapshot")
    included = [row for row in classified if row["opus_made"] in {"yes", "likely"}]

    vectors = rows(COLOR / "per-video-color-vectors.csv",
                   {"sha256", "post_id", "source_url", "style", "domain",
                    "archive_likes", "exact_likes_20260927", "saturation_median",
                    "lightness_median", "colorful_pixel_share", "dark_pixel_share", *BINS})
    require(len(vectors) == len(included), "Color vectors do not cover the included classifier rows")
    expected_sources = Counter((row["post_url"], row["style"], row["domain"])
                               for row in included)
    actual_sources = Counter((row["source_url"], row["style"], row["domain"])
                             for row in vectors)
    require(actual_sources == expected_sources,
            "Color vector source/category multiset differs from classifier")
    by_sha = {}
    for row in vectors:
        sha = row["sha256"]
        require(SHA256.fullmatch(sha) is not None and sha not in by_sha,
                f"Invalid or repeated vector SHA: {sha}")
        require(post_parts(row["source_url"])[1] == row["post_id"],
                f"Vector post ID disagrees with URL: {sha}")
        values = [number(row[key], f"{sha}/{key}") for key in BINS]
        require(all(0 <= value <= 1 for value in values), f"Invalid color bin: {sha}")
        close(sum(values), 1, 5, f"Color vector sum for {sha}")
        for key in ("saturation_median", "colorful_pixel_share", "dark_pixel_share"):
            require(0 <= number(row[key], f"{sha}/{key}") <= 1,
                    f"Invalid {key}: {sha}")
        require(0 <= number(row["lightness_median"], f"{sha}/lightness") <= 100,
                f"Invalid lightness: {sha}")
        for key in ("archive_likes", "exact_likes_20260927"):
            if row[key]:
                count(row[key], f"{sha}/{key}")
        by_sha[sha] = row

    assignments = rows(COLOR / "per-video-color-modes.csv",
                       {"sha256", "post_id", "source_url", "group_type", "group_id",
                        "mode_id", "post_ambiguous_across_modes", "archive_likes",
                        "exact_likes_20260927"})
    require(len(assignments) == len(vectors) * len(FAMILIES),
            "Each vector needs one style and one domain assignment")
    by_file_family = {}
    by_mode = defaultdict(list)
    post_modes = defaultdict(set)
    for row in assignments:
        sha, family = row["sha256"], row["group_type"]
        require(sha in by_sha and family in FAMILIES, f"Unknown assignment: {sha}/{family}")
        key = (sha, family)
        require(key not in by_file_family, f"Repeated file/family assignment: {key}")
        source = by_sha[sha]
        require(row["group_id"] == source[family] and
                all(row[field] == source[field] for field in
                    ("post_id", "source_url", "archive_likes", "exact_likes_20260927")),
                f"Assignment/source mismatch: {key}")
        require(row["mode_id"].startswith(f"{family}/{row['group_id']}/"),
                f"Mode ID/category mismatch: {key}")
        require(row["post_ambiguous_across_modes"] in {"True", "False"},
                f"Invalid ambiguity flag: {key}")
        by_file_family[key] = row
        by_mode[row["mode_id"]].append(row)
        post_modes[(family, row["group_id"], row["post_id"])].add(row["mode_id"])
    require(len(by_file_family) == len(vectors) * len(FAMILIES),
            "Incomplete file/family assignments")
    for row in assignments:
        key = (row["group_type"], row["group_id"], row["post_id"])
        require((row["post_ambiguous_across_modes"] == "True") == (len(post_modes[key]) > 1),
                f"Incorrect cross-mode post flag: {key}")

    summary = rows(COLOR / "color-mode-summary.csv",
                   {"group_type", "group_id", "mode_id", "mode_rank", "n_group_files",
                    "n_files", "n_posts", "n_authors", "n_frames", "n_sampled_pixels",
                    "median_saturation", "median_lightness", "median_colorful_pixel_share",
                    "neutral_pixel_share", "archive_n", "archive_median_likes",
                    "exact_n", "exact_median_likes", "representative_url"})
    mode_summary = {}
    group_summary = defaultdict(list)
    for row in summary:
        mode = row["mode_id"]
        require(mode not in mode_summary and mode in by_mode, f"Unknown or repeated mode: {mode}")
        require(row["group_type"] in FAMILIES, f"Invalid mode family: {mode}")
        key = (row["group_type"], row["group_id"])
        members = by_mode[mode]
        require(all((item["group_type"], item["group_id"]) == key for item in members),
                f"Mode contains another category: {mode}")
        require(count(row["n_files"], f"{mode}/n_files") == len(members),
                f"Mode file count mismatch: {mode}")
        require(count(row["n_posts"], f"{mode}/n_posts") == len({item["post_id"] for item in members}),
                f"Mode post count mismatch: {mode}")
        authors = {post_parts(item["source_url"])[0] for item in members}
        require(count(row["n_authors"], f"{mode}/n_authors") == len(authors),
                f"Mode author count mismatch: {mode}")
        require(count(row["n_frames"], f"{mode}/n_frames") == len(members) * FRAMES_PER_FILE,
                f"Mode frame count mismatch: {mode}")
        require(count(row["n_sampled_pixels"], f"{mode}/pixels") == len(members) * PIXELS_PER_FILE,
                f"Mode pixel count mismatch: {mode}")
        for vector_field, summary_field, places in (
            ("saturation_median", "median_saturation", 4),
            ("lightness_median", "median_lightness", 2),
            ("colorful_pixel_share", "median_colorful_pixel_share", 4),
        ):
            median = statistics.median(number(by_sha[item["sha256"]][vector_field],
                                              vector_field)
                                       for item in members)
            close(number(row[summary_field], f"{mode}/{summary_field}"), median,
                  places, f"{mode}/{summary_field}")
        neutral = statistics.mean(sum(number(by_sha[item["sha256"]][f"{band}_neutral"],
                                             f"{mode}/{band}_neutral")
                                      for band in ("dark", "middle", "light"))
                                  for item in members)
        close(number(row["neutral_pixel_share"], f"{mode}/neutral share"), neutral, 4,
              f"{mode}/neutral share")
        for source_field, count_field, median_field in (
            ("archive_likes", "archive_n", "archive_median_likes"),
            ("exact_likes_20260927", "exact_n", "exact_median_likes"),
        ):
            likes = {item["post_id"]: count(item[source_field], f"{mode}/{source_field}")
                     for item in members if item["post_ambiguous_across_modes"] == "False"
                     and item[source_field]}
            require(count(row[count_field], f"{mode}/{count_field}") == len(likes),
                    f"Engagement denominator mismatch: {mode}/{source_field}")
            if likes:
                close(number(row[median_field], f"{mode}/{median_field}"),
                      statistics.median(likes.values()), 1, f"{mode}/{median_field}")
            else:
                require(not row[median_field], f"Unexpected empty engagement median: {mode}")
        require(row["representative_url"] in {item["source_url"] for item in members},
                f"Representative is outside mode: {mode}")
        mode_summary[mode] = row
        group_summary[key].append(row)
    require(set(by_mode) == set(mode_summary), "An assigned mode lacks a summary")
    require(len(summary) == PUBLISHED_MODES, "Mode count differs from published study")
    for family, expected in PUBLISHED_SPLIT_CATEGORIES.items():
        actual = sum(len(modes) > 1 for (kind, _), modes in group_summary.items()
                     if kind == family)
        require(actual == expected, f"{family} split count differs from published study")

    swatches = rows(COLOR / "color-mode-swatches.csv",
                    {"group_type", "group_id", "mode_id", "n_files", "rank",
                     "hex", "pixel_share", "sampled_pixels"})
    by_swatch_mode = defaultdict(list)
    for row in swatches:
        mode = row["mode_id"]
        require(mode in mode_summary, f"Swatch has unknown mode: {mode}")
        summary_row = mode_summary[mode]
        require((row["group_type"], row["group_id"], row["n_files"]) ==
                (summary_row["group_type"], summary_row["group_id"], summary_row["n_files"]),
                f"Swatch category/count mismatch: {mode}")
        require(HEX_COLOR.fullmatch(row["hex"]) is not None, f"Invalid swatch color: {mode}")
        by_swatch_mode[mode].append(row)
    require(set(by_swatch_mode) == set(mode_summary), "A mode lacks swatches")
    for mode, palette in by_swatch_mode.items():
        require(len(palette) == 6 and {count(item["rank"], f"{mode}/rank") for item in palette}
                == set(range(1, 7)), f"Expected six ranked swatches: {mode}")
        pixels = count(mode_summary[mode]["n_sampled_pixels"], f"{mode}/pixels")
        require(sum(count(item["sampled_pixels"], f"{mode}/swatch pixels") for item in palette)
                == pixels, f"Swatch pixels do not conserve mode pixels: {mode}")
        for item in palette:
            close(number(item["pixel_share"], f"{mode}/pixel share"),
                  count(item["sampled_pixels"], f"{mode}/swatch pixels") / pixels, 6,
                  f"{mode}/pixel share")

    full = json.loads((COLOR / "color-modes.json").read_text(encoding="utf-8"))
    require(full["n_files"] == len(vectors) and
            full["n_posts"] == len({row["post_id"] for row in vectors}) == PUBLISHED_POSTS and
            full["n_frames"] == len(vectors) * FRAMES_PER_FILE and
            full["n_sampled_pixels_per_family"] == len(vectors) * PIXELS_PER_FILE,
            "Full JSON totals differ from published file vectors")
    json_groups = {(group["group_type"], group["group_id"]): group
                   for group in full["groups"]}
    require(len(json_groups) == len(full["groups"]) == len(group_summary),
            "Repeated or missing JSON categories")
    require(set(json_groups) == set(group_summary), "JSON/CSV category sets differ")
    for key, group in json_groups.items():
        members = [item for item in assignments if (item["group_type"], item["group_id"]) == key]
        require(group["n_files"] == len(members) and
                group["n_posts"] == len({item["post_id"] for item in members}) and
                group["n_modes"] == len(group_summary[key]) and
                group["n_posts_ambiguous_across_modes"] ==
                sum(len(modes) > 1 for (family, group_id, _), modes in post_modes.items()
                    if (family, group_id) == key), f"JSON category totals differ: {key}")
        require(all(count(row["n_group_files"], f"{key}/n_group_files") == len(members)
                    for row in group_summary[key]), f"CSV category file count differs: {key}")
        json_modes = {mode["mode_id"]: mode for mode in group["modes"]}
        require(len(json_modes) == len(group["modes"]) == len(group_summary[key]) and
                set(json_modes) == {row["mode_id"] for row in group_summary[key]},
                f"JSON/CSV mode sets differ: {key}")
        for mode_id, mode in json_modes.items():
            published = mode_summary[mode_id]
            for field in ("mode_rank", "n_files", "n_posts", "n_authors", "n_frames",
                          "n_sampled_pixels", "color_signature_zh", "color_signature_en"):
                require(str(mode[field]) == published[field],
                        f"JSON/CSV {field} differs: {mode_id}")
            for field in ("median_saturation", "median_lightness",
                          "median_colorful_pixel_share", "neutral_pixel_share"):
                require(float(mode[field]) == number(published[field], f"{mode_id}/{field}"),
                        f"JSON/CSV {field} differs: {mode_id}")
            for field, prefix in (("archive_likes", "archive"),
                                  ("exact_likes_20260927", "exact")):
                require(mode[field]["n_posts_with_likes"] ==
                        count(published[f"{prefix}_n"], f"{mode_id}/{prefix}_n"),
                        f"JSON/CSV engagement count differs: {mode_id}")
                require(mode[field]["median"] ==
                        (number(published[f"{prefix}_median_likes"], mode_id)
                         if published[f"{prefix}_median_likes"] else None),
                        f"JSON/CSV engagement median differs: {mode_id}")
            require(mode["representatives"] and
                    mode["representatives"][0]["source_url"] == published["representative_url"],
                    f"JSON/CSV representative differs: {mode_id}")
            json_palette = {item["rank"]: item for item in mode["palette"]}
            require(len(json_palette) == len(mode["palette"]) == 6,
                    f"JSON palette is incomplete: {mode_id}")
            for item in by_swatch_mode[mode_id]:
                source = json_palette[count(item["rank"], f"{mode_id}/rank")]
                require(source["hex"].upper() == item["hex"].upper() and
                        source["sampled_pixels"] == count(item["sampled_pixels"], mode_id) and
                        source["pixel_share"] == number(item["pixel_share"], mode_id),
                        f"JSON/CSV swatch differs: {mode_id}")

    modes_with_five_exact_likes = sum(
        count(row["exact_n"], row["mode_id"]) >= 5 for row in summary
    )
    require(modes_with_five_exact_likes == PUBLISHED_MODES_WITH_FIVE_EXACT_LIKES,
            "Exact-like coverage differs from published study")
    return {"files": len(vectors), "posts": full["n_posts"],
            "categories": len(json_groups), "modes": len(summary),
            "assignments": len(assignments), "swatches": len(swatches),
            "modes_with_five_exact_like_posts": modes_with_five_exact_likes}


def main() -> int:
    try:
        print(json.dumps(check(), sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        print(f"Color-study check failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
