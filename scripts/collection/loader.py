"""Source ledger loading, validation, normalization, and batch merging."""
from __future__ import annotations

import csv
from datetime import date as calendar_date
from pathlib import Path

from .config import (
    LEGACY_LEDGER_RE,
    MODEL_GROUPS,
    MODERN_LEDGER_RE,
    NEW_CASES_2026_09_27,
    POST_URL_RE,
    ROOT,
)


def read_rows(path: Path, required: tuple[str, ...] = ("source_url",)) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = set(required) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path.name}: missing columns: {', '.join(sorted(missing))}")
        result: list[dict[str, str]] = []
        for number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{path.name}:{number}: row width does not match its header")
            if any(not row[field].strip() for field in required):
                raise ValueError(f"{path.name}:{number}: blank required field")
            result.append(row)
        if not result:
            raise ValueError(f"{path.name}: no source rows")
        return result


def extract_model_tags(label: str) -> list[str]:
    tags: list[str] = []
    for group in MODEL_GROUPS:
        if group.pattern.search(label):
            tags.append(group.key)
    return tags


def source_batches() -> list[tuple[str, str]]:
    """Discover all dated source ledgers in chronological listing order."""
    sources: list[tuple[str, str]] = [
        ("2026-09-26", "data/cases.csv"),
        ("2026-09-27", "assets/new-case-thumbnails/frames.csv"),
    ]
    ledgers: list[tuple[str, str]] = []
    candidates = list((ROOT / "data").glob("claude55-source-review-*.csv")) + list(
        (ROOT / "data").glob("source-review-*.csv")
    )
    for path in candidates:
        match = MODERN_LEDGER_RE.fullmatch(path.name) or LEGACY_LEDGER_RE.fullmatch(path.name)
        if not match:
            raise ValueError(f"Expected a dated source ledger: {path.name}")
        date_str = calendar_date.fromisoformat(match[1]).isoformat()
        ledgers.append((date_str, str(path.relative_to(ROOT))))
    return sources + sorted(ledgers, key=lambda item: (item[0], "followup" in item[1], item[1]))


def resolve_detail_page(file: str, explicit: str = "") -> str:
    """Resolve a batch's detail page without redirecting future follow-ups to an old date."""
    if explicit:
        candidates = [explicit]
    else:
        stem = Path(file).stem
        batch = stem.removeprefix("claude55-source-review-").removeprefix("source-review-")
        candidates = [f"docs/maintenance-{batch}.md", f"docs/claude55-update-{batch}.md"]
    for candidate in candidates:
        path = ROOT / candidate.partition("#")[0]
        if path.is_file() and path.resolve().is_relative_to(ROOT):
            return candidate
    raise ValueError(f"{file}: missing detail page; expected {' or '.join(candidates)}")


def normalize_source(row: dict[str, str], date_str: str, file: str) -> dict[str, str]:
    """Adapt public ledger formats into one canonical source-post record."""
    match = POST_URL_RE.fullmatch(row["source_url"].strip())
    if not match or row.get("post_id", match[2]).strip() != match[2]:
        raise ValueError(f"Invalid post ID / source URL in {file}: {row.get('source_url')}")
    author, pid = match.groups()
    item: dict[str, str] = {
        "post_id": pid,
        "creator": author,
        "source_url": row["source_url"].strip(),
        "first_listed_date": date_str,
        "model_attribution": "",
        "model_tags": "",
        "entry_kind": "example_or_comparison",
        "media_evidence": "source_only",
        "duration_seconds": row.get("preview_duration_s", "").strip(),
        "has_prompt": row.get("has_prompt", "").strip(),
        "title_en": "",
        "title_zh": "",
        "category": "",
        "source_ledger": file,
        "detail_page": "",
        "thumbnail": "",
    }
    if file == "data/cases.csv":
        if row["hypit_status"] != "tile_ok":
            raise ValueError(f"Unsampled frozen case: {pid}")
        item.update(
            model_attribution="Opus 5.5 snapshot context; consult individual source notes",
            model_tags="Opus 5.5",
            media_evidence="sampled_preview",
            title_en=row["label"],
            title_zh=row["label"],
            category=row["primary_path"],
            detail_page=f"docs/cases-index.zh-CN.md#case-{pid}",
            thumbnail=f"assets/case-thumbnails/{pid}.webp",
        )
    elif file.endswith("frames.csv"):
        if pid not in NEW_CASES_2026_09_27:
            raise ValueError(f"{file}: missing September 27 source description for {pid}")
        en, zh, label = NEW_CASES_2026_09_27[pid]
        item.update(
            model_attribution=label,
            model_tags=";".join(extract_model_tags(label)),
            media_evidence="sampled_preview",
            title_en=en,
            title_zh=zh,
            category="later_workflow",
            detail_page="docs/new-cases-2026-09-27.md",
            thumbnail=f"assets/new-case-thumbnails/{pid}.webp",
        )
    else:
        label = row["model_attribution"]
        context = row.get("source_kind") == "routing discussion"
        sampled = row["media_review"].startswith("nine frames inspected")
        item.update(
            model_attribution=label,
            model_tags="" if context else ";".join(extract_model_tags(label)),
            entry_kind="routing_context" if context else "example_or_comparison",
            media_evidence="sampled_preview" if sampled else "source_only",
            title_en=row.get("title_en") or f"@{author} — {row.get('source_kind', 'source')}",
            title_zh=row.get("title_zh") or f"@{author} — {row.get('source_kind', '来源')}",
            category=row.get("category") or row.get("source_kind", ""),
            detail_page=resolve_detail_page(file, row.get("detail_page", "")),
            thumbnail=row.get("thumbnail", ""),
        )

    for field in ("detail_page", "thumbnail"):
        value = item[field].partition("#")[0]
        if value and not (ROOT / value).is_file():
            raise ValueError(f"{file}: missing {field} for {pid}: {value}")
    return item


def batch_label(date_str: str, file: str) -> str:
    if "followup" in file:
        return f"{date_str} follow-up"
    if "fable52" in file:
        return f"{date_str} (Fable 5.2)"
    return date_str


def collect() -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    index: dict[str, dict[str, str]] = {}
    groups: list[dict[str, object]] = []
    for date_str, file in source_batches():
        batch_ids: set[str] = set()
        prior_total = len(index)
        required: tuple[str, ...] = ("source_url",)
        if "source-review-" in file:
            required += ("post_id", "model_attribution", "media_review")
        elif file == "data/cases.csv":
            required += ("label", "primary_path", "hypit_status")
        for row in read_rows(ROOT / file, required):
            item = normalize_source(row, date_str, file)
            pid = item["post_id"]
            if pid in batch_ids:
                if file.endswith("frames.csv"):
                    continue  # Two attachments still represent one post.
                raise ValueError(f"Duplicate source in {file}: {pid}")
            batch_ids.add(pid)
            if pid in index:
                prev = index[pid]
                if item["media_evidence"] == "sampled_preview":
                    prev.update(
                        media_evidence="sampled_preview",
                        thumbnail=item["thumbnail"] or prev["thumbnail"],
                    )
                prev["source_ledger"] += ";" + file
            else:
                index[pid] = item
        added = len(index) - prior_total
        groups.append(
            {
                "date": date_str,
                "label": batch_label(date_str, file),
                "source": file,
                "unique_source_posts": len(batch_ids),
                "newly_listed_source_posts": added,
                "overlaps_earlier_batches": len(batch_ids) - added,
            }
        )
    entries = sorted(index.values(), key=lambda x: x["post_id"], reverse=True)
    return entries, groups
