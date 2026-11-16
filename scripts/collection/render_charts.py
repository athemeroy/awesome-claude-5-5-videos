"""SVG chart rendering for collection coverage."""
from __future__ import annotations

import html


def render_coverage_chart(entries: list[dict[str, str]], groups: list[dict[str, object]]) -> str:
    width = 940
    height = 130 + len(groups) * 42
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Preview sampling coverage by collection batch</title>',
        '<desc id="desc">Source-post counts. Navy shows posts with nine-frame preview sampling; grey shows source-only posts. Batches use listing dates, not release dates.</desc>',
        f'<rect width="{width}" height="{height}" fill="#fafbfc"/>',
        '<g font-family="system-ui,sans-serif" fill="#1f2937">',
        '<text x="24" y="32" font-size="22" font-weight="600">How much of the collection has preview evidence?</text>',
        '<text x="24" y="55" font-size="13">Source posts by listing batch · nine-frame sampling does not verify full motion or model calls</text>',
        '<rect x="24" y="70" width="12" height="12" fill="#244b67"/><text x="42" y="81" font-size="12">Sampled preview</text>',
        '<rect x="195" y="70" width="12" height="12" fill="#d7dfe5"/><text x="213" y="81" font-size="12">Source only</text>',
    ]
    for i, group in enumerate(groups):
        source_file = str(group["source"])
        subset = [e for e in entries if source_file in e["source_ledger"].split(";")]
        sampled = sum(e["media_evidence"] == "sampled_preview" for e in subset)
        total = len(subset)
        y = 110 + i * 42
        bar = 470
        bar_x = 240
        parts += [
            f'<text x="24" y="{y + 17}" font-size="13">{html.escape(str(group["label"]))}</text>',
            f'<rect x="{bar_x}" y="{y}" width="{bar}" height="24" rx="3" fill="#d7dfe5"/>',
            f'<rect x="{bar_x}" y="{y}" width="{bar * sampled / total:.2f}" height="24" rx="3" fill="#244b67"/>',
            f'<text x="{bar_x + bar + 18}" y="{y + 17}" font-size="13">{sampled} / {total} sampled ({sampled / total:.1%})</text>',
        ]
    parts += ["</g></svg>"]
    return "\n".join(parts) + "\n"
