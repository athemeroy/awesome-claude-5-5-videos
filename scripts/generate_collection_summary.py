#!/usr/bin/env python3
"""Reconcile dated source-post sets and update the bilingual README totals."""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- collection-summary:start -->'
END = '<!-- collection-summary:end -->'


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    groups = []
    ids = set()
    sources = [('2026-09-26', 'data/cases.csv'),
               ('2026-09-27', 'assets/new-case-thumbnails/frames.csv')]
    sources += [(p.stem.removeprefix('claude55-source-review-'), str(p.relative_to(ROOT)))
                for p in sorted((ROOT / 'data').glob('claude55-source-review-*.csv'))]
    for date, file in sources:
        batch = set()
        for row in rows(ROOT / file):
            match = re.fullmatch(r'https://x\.com/[^/]+/status/(\d+)', row['source_url'])
            if not match:
                raise ValueError(f'Invalid source URL in {file}')
            if row.get('post_id', match[1]) != match[1]:
                raise ValueError(f'Post ID differs from source URL in {file}')
            if match[1] in batch and 'frames.csv' not in file:
                raise ValueError(f'Duplicate source in {file}: {match[1]}')
            batch.add(match[1])
        groups.append(dict(date=date, source=file, unique_source_posts=len(batch),
                           newly_listed_source_posts=len(batch - ids),
                           overlaps_earlier_batches=len(batch & ids)))
        ids.update(batch)
    summary = dict(as_of=groups[-1]['date'], unit='source post ID; includes replies, comparisons and variants',
                   unique_source_posts=len(ids), batches=groups,
                   frozen_media_snapshot='data/corpus-snapshot.json')
    outputs = {ROOT / 'data/collection-summary.json': json.dumps(summary, ensure_ascii=False, indent=2) + '\n'}
    for zh in (False, True):
        file = ROOT / ('README.zh-CN.md' if zh else 'README.md')
        text = file.read_text()
        table = ['| 批次 | 来源帖 | 比此前新增 |' if zh else '| Batch | Source posts | New to earlier batches |', '|---|---:|---:|']
        table += [f'| [{g["date"]}]({g["source"]}) | {g["unique_source_posts"]} | {g["newly_listed_source_posts"]} |' for g in groups]
        table += ['', f'截至 {summary["as_of"]}，合计 **{len(ids)} 条去重来源帖**。' if zh else f'As of {summary["as_of"]}: **{len(ids)} distinct source posts**.']
        if text.count(START) != 1 or text.count(END) != 1:
            raise ValueError(f'Expected one summary block in {file}')
        before, rest = text.split(START); _, after = rest.split(END)
        outputs[file] = before + START + '\n\n' + '\n'.join(table) + '\n\n' + END + after
    stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if args.check:
        if stale:
            raise SystemExit('Stale collection totals: ' + ', '.join(stale))
        print('Collection totals match all public source batches')
    else:
        for p, text in outputs.items():
            p.write_text(text)
        print(f'{len(ids)} unique source posts across {len(groups)} batches')


if __name__ == '__main__':
    main()
