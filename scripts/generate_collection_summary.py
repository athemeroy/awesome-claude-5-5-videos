#!/usr/bin/env python3
"""Reconcile public source ledgers; generate totals, model directory, charts, and coverage analysis."""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path

from collection.config import ROOT
from collection.loader import collect
from collection.render_charts import render_coverage_chart
from collection.render_docs import inject_readme_block, render_analysis, render_library, render_readme_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify outputs are up to date without writing")
    args = parser.parse_args()

    entries, groups = collect()
    total = len(entries)
    summary: dict[str, object] = {
        "as_of": max(str(g["date"]) for g in groups),
        "unit": "source post ID; includes replies, comparisons and variants",
        "unique_source_posts": total,
        "sampled_source_posts": sum(e["media_evidence"] == "sampled_preview" for e in entries),
        "routing_context_posts": sum(e["entry_kind"] == "routing_context" for e in entries),
        "batches": groups,
        "frozen_media_snapshot": "data/corpus-snapshot.json",
    }

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(entries[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(entries)

    outputs: dict[Path, str] = {
        ROOT / "assets/collection-coverage.svg": render_coverage_chart(entries, groups),
        ROOT / "data/collection-summary.json": json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        ROOT / "data/collection-index.csv": buffer.getvalue(),
    }

    for zh in (False, True):
        suffix = ".zh-CN" if zh else ""
        outputs[ROOT / f"docs/library{suffix}.md"] = render_library(entries, zh)
        outputs[ROOT / f"docs/collection-analysis{suffix}.md"] = render_analysis(entries, groups, zh)
        readme_path = ROOT / ("README.zh-CN.md" if zh else "README.md")
        outputs[readme_path] = inject_readme_block(readme_path, render_readme_summary(entries, summary, zh))

    stale = [
        str(path.relative_to(ROOT))
        for path, content in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != content
    ]
    if args.check:
        if stale:
            raise SystemExit("Stale collection outputs: " + ", ".join(stale))
        print(f"Collection index, directory, analysis and README totals match {total} public source posts")
        return 0

    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"{total} source posts; {summary['sampled_source_posts']} with sampled previews")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
