#!/usr/bin/env python3
"""Reconcile public source ledgers; generate totals, model directory and coverage analysis."""
import argparse
import csv
import io
import html
import json
import re
from collections import Counter
from datetime import date as calendar_date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- collection-summary:start -->'
END = '<!-- collection-summary:end -->'
MODELS = ('Opus', 'Sonnet', 'Haiku', 'Fable')
POST = re.compile(r'https://x\.com/([^/]+)/status/(\d+)')
LEDGER = re.compile(r'claude55-source-review-(\d{4}-\d{2}-\d{2})(-[a-z0-9-]+)?\.csv')
NEW_CASES = {
    '2104131805175844923': ('Handmade launch film versus code remake', '手工发布片与代码改编', 'Opus 5.5'),
    '2104009748874141941': ('Green-screen clip and edited version', '绿幕原片与编辑版本', 'Opus 5.5 + Grok footage'),
    '2103923067277733943': ('Wear OS product film with real assets', '使用真实素材的 Wear OS 产品片', 'Opus 5.5 + Fable 5.1'),
    '2104039075175182487': ('Personal story with ClaudeAnimationBase', '复用 ClaudeAnimationBase 的个人故事', 'Opus 5.5'),
    '2104021764863078697': ('Supplied draft, images and external audio', '提供草稿、图像与外部音频', 'Opus 5.5 + GPT-6 Astra + ElevenLabs'),
    '2103869704955900023': ('Multi-tool anime music video', '多工具动漫音乐视频', 'Opus 5.5 + external media models'),
    '2104011150471917838': ('Video with checked data slots', '带数据槽校验的视频', 'Opus 5.5'),
}


def rows(path, required=('source_url',)):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        missing = set(required) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f'{path.name}: missing columns: {", ".join(sorted(missing))}')
        result = []
        for number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path.name}:{number}: row width does not match its header')
            if any(not row[field].strip() for field in required):
                raise ValueError(f'{path.name}:{number}: blank required field')
            result.append(row)
        if not result:
            raise ValueError(f'{path.name}: no source rows')
        return result


def clean(value):
    return value.replace('|', '\\|').replace('\n', ' ')


def model_tags(label):
    tags = [m for m in MODELS if re.search(rf'\b{m}\s+5\.5\b', label, re.I)]
    if 'Fable' not in tags and 'Fable' in label and re.search(r'suspect[^;]*5\.5', label, re.I):
        tags.append('Fable')
    return tags


def source_batches():
    """Keep listing dates distinct from the original posts' publication dates."""
    sources = [('2026-09-26', 'data/cases.csv'), ('2026-09-27', 'assets/new-case-thumbnails/frames.csv')]
    ledgers = []
    for path in (ROOT / 'data').glob('claude55-source-review-*.csv'):
        match = LEDGER.fullmatch(path.name)
        if not match:
            raise ValueError(f'Expected a dated source ledger: {path.name}')
        date = calendar_date.fromisoformat(match[1]).isoformat()
        ledgers.append((date, str(path.relative_to(ROOT))))
    return sources + sorted(ledgers, key=lambda item: (item[0], 'followup' in item[1], item[1]))


def detail_page(file, explicit=''):
    """Resolve a batch's page without redirecting future follow-ups to an old date."""
    if explicit:
        candidates = [explicit]
    else:
        batch = Path(file).stem.removeprefix('claude55-source-review-')
        candidates = [f'docs/maintenance-{batch}.md', f'docs/claude55-update-{batch}.md']
    for candidate in candidates:
        path = ROOT / candidate.partition('#')[0]
        if path.is_file() and path.resolve().is_relative_to(ROOT):
            return candidate
    raise ValueError(f'{file}: missing detail page; expected {" or ".join(candidates)}')


def normalize_source(row, date, file):
    """Adapt the three public input formats to one source-post record."""
    match = POST.fullmatch(row['source_url'])
    if not match or row.get('post_id', match[2]) != match[2]:
        raise ValueError(f'Invalid post ID / source URL in {file}')
    author, pid = match.groups()
    item = dict(post_id=pid, creator=author, source_url=row['source_url'], first_listed_date=date,
                model_attribution='', model_tags='', entry_kind='example_or_comparison',
                media_evidence='source_only', title_en='', title_zh='', category='',
                source_ledger=file, detail_page='', thumbnail='')
    if file == 'data/cases.csv':
        item.update(model_attribution='Opus 5.5 snapshot context; consult individual source notes', model_tags='Opus',
                    media_evidence='sampled_preview', title_en=row['label'], title_zh=row['label'],
                    category=row['primary_path'], detail_page=f'docs/cases-index.zh-CN.md#case-{pid}',
                    thumbnail=f'assets/case-thumbnails/{pid}.webp')
        if row['hypit_status'] != 'tile_ok':
            raise ValueError(f'Unsampled frozen case: {pid}')
    elif file.endswith('frames.csv'):
        if pid not in NEW_CASES:
            raise ValueError(f'{file}: missing September 27 source description for {pid}')
        en, zh, label = NEW_CASES[pid]
        item.update(model_attribution=label, model_tags=';'.join(model_tags(label)),
                    media_evidence='sampled_preview', title_en=en, title_zh=zh,
                    category='later_workflow', detail_page='docs/new-cases-2026-09-27.md',
                    thumbnail=f'assets/new-case-thumbnails/{pid}.webp')
    else:
        label = row['model_attribution']
        context = row.get('source_kind') == 'routing discussion'
        item.update(model_attribution=label, model_tags='' if context else ';'.join(model_tags(label)),
                    entry_kind='routing_context' if context else 'example_or_comparison',
                    media_evidence='sampled_preview' if row['media_review'].startswith('nine frames inspected') else 'source_only',
                    title_en=row.get('title_en') or f'@{author} — {row.get("source_kind", "source")}',
                    title_zh=row.get('title_zh') or f'@{author} — {row.get("source_kind", "来源")}',
                    category=row.get('category', row.get('source_kind', '')),
                    detail_page=detail_page(file, row.get('detail_page', '')),
                    thumbnail=row.get('thumbnail', ''))
    for field in ('detail_page', 'thumbnail'):
        value = item[field].partition('#')[0]
        if value and not (ROOT / value).is_file():
            raise ValueError(f'{file}: missing {field} for {pid}: {value}')
    return item


def collect():
    index = {}
    groups = []
    for date, file in source_batches():
        batch = set()
        prior_total = len(index)
        required = ('source_url',)
        if file.startswith('data/claude55-source-review-'):
            required += ('post_id', 'model_attribution', 'media_review')
        elif file == 'data/cases.csv':
            required += ('label', 'primary_path', 'hypit_status')
        for row in rows(ROOT / file, required):
            item = normalize_source(row, date, file)
            pid = item['post_id']
            if pid in batch:
                if file.endswith('frames.csv'):
                    continue  # Two attachments still represent one post.
                raise ValueError(f'Duplicate source in {file}: {pid}')
            batch.add(pid)
            if pid in index:
                # Preserve the earliest listing and keep the strongest public media record.
                prev = index[pid]
                if item['media_evidence'] == 'sampled_preview':
                    prev.update(media_evidence='sampled_preview', thumbnail=item['thumbnail'] or prev['thumbnail'])
                prev['source_ledger'] += ';' + file
            else:
                index[pid] = item
        # Count additions from the union size before and after this batch.
        groups.append(dict(date=date, label=date + (' follow-up' if 'followup' in file else ''), source=file,
                           unique_source_posts=len(batch), newly_listed_source_posts=len(index) - prior_total,
                           overlaps_earlier_batches=len(batch) - (len(index) - prior_total)))
    return sorted(index.values(), key=lambda x: x['post_id'], reverse=True), groups


def render_library(entries, zh):
    suffix = '.zh-CN' if zh else ''
    title = '按模型浏览全部来源' if zh else 'Browse all sources by model'
    lines = [f'# {title}', '', '[首页](../README.zh-CN.md) · [English](library.md)' if zh else '[Home](../README.md) · [中文](library.zh-CN.md)', '',
             f'合并全部日期批次，共 **{len(entries)} 条去重来源帖**。案例说明沿用来源语言。' if zh else f'All dated batches in one directory: **{len(entries)} distinct source posts**. Older case titles retain their source language.', '',
             '模型分组按来源标签整理，多模型对照会出现在多个分组。Opus 旧快照条目按研究背景归组，并不核实逐条模型调用。Fable 包括作者怀疑的路由。路由讨论另列。' if zh else 'Groups follow source labels; multi-model comparisons appear in several groups. Older Opus entries are grouped by snapshot context, not verified calls. Fable includes suspected routing. Routing discussions are listed separately.', '',
             '[收录与证据分析](collection-analysis.zh-CN.md) · [制作方式分析](workflow-analysis.zh-CN.md) · [完整 CSV](../data/collection-index.csv)' if zh else '[Collection / evidence analysis](collection-analysis.md) · [Workflow analysis](workflow-analysis.md) · [Complete CSV](../data/collection-index.csv)', '']
    for model in MODELS:
        subset = [e for e in entries if model in e['model_tags'].split(';')]
        lines += [f'- [{model} ({len(subset)})](#{model.lower()})']
    lines += ['- [背景与其他对照](#context)' if zh else '- [Context and other comparisons](#context)', '']
    for model in (*MODELS, 'Context'):
        subset = [e for e in entries if model in e['model_tags'].split(';')] if model != 'Context' else [e for e in entries if not e['model_tags']]
        lines += [f'<a id="{model.lower()}"></a>', '', f'## {model} ({len(subset)})', '',
                  '| 原帖 | 模型／角色标签 | 证据 | 收录日期 |' if zh else '| Original post | Model / role label | Evidence | First listed |', '|---|---|---|---|']
        for e in subset:
            sampled = e['media_evidence'] == 'sampled_preview'
            evidence = ('九帧取样' if sampled else '仅来源') if zh else ('9-frame sample' if sampled else 'Source only')
            page, _, anchor = e['detail_page'].partition('#')
            if zh and page.endswith('.md') and (ROOT / (page[:-3] + '.zh-CN.md')).exists():
                page = page[:-3] + '.zh-CN.md'
            lines.append(f'| [{clean(e["title_zh" if zh else "title_en"])}]({e["source_url"]}) | {clean(e["model_attribution"])} | [{evidence}]({Path(page).name + ('#' + anchor if anchor else '')}) | {e["first_listed_date"]} |')
        lines += ['']
    return '\n'.join(lines).rstrip() + '\n'


def render_analysis(entries, groups, zh):
    latest_file = groups[-1]['source']
    latest_row = rows(ROOT / latest_file)[0]
    latest_page = detail_page(latest_file, latest_row.get('detail_page', ''))
    if zh and (ROOT / (latest_page[:-3] + '.zh-CN.md')).is_file():
        latest_page = latest_page[:-3] + '.zh-CN.md'
    latest_link = Path(latest_page).name
    total = len(entries); sampled = sum(e['media_evidence'] == 'sampled_preview' for e in entries)
    context = sum(e['entry_kind'] == 'routing_context' for e in entries)
    later = [e for e in entries if e['first_listed_date'] >= '2026-10-02' and e['entry_kind'] != 'routing_context']
    creators = Counter(e['creator'].lower() for e in entries)
    top = creators.most_common(5); top_count = sum(n for _, n in top)
    lines = ['# 收录与证据分析' if zh else '# Collection and evidence analysis', '',
             '[首页](../README.zh-CN.md) · [目录](library.zh-CN.md) · [English](collection-analysis.md)' if zh else '[Home](../README.md) · [Directory](library.md) · [中文](collection-analysis.zh-CN.md)', '',
             '这些统计描述本仓库选中的来源帖，不估计 X 全站比例，也不评价模型优劣。全部数字来自[统一来源索引](../data/collection-index.csv)，由 `scripts/generate_collection_summary.py` 生成。' if zh else 'These statistics describe selected source posts in this repository. They do not estimate X-wide prevalence or rank models. All figures derive from [the unified source index](../data/collection-index.csv), generated by `scripts/generate_collection_summary.py`.', '',
             '## 证据覆盖' if zh else '## Evidence coverage', '', '![按收录批次统计有九帧取样的来源帖比例](../assets/collection-coverage.svg)' if zh else '![Nine-frame preview sampling coverage by listing batch](../assets/collection-coverage.svg)', '',
             '| 单位 | 数量 | 解释 |' if zh else '| Unit | Count | Meaning |', '|---|---:|---|',
             f'| {"去重来源帖" if zh else "Distinct source posts"} | {total} | {"含回复、对照与版本变体" if zh else "Includes replies, comparisons and variants"} |',
             f'| {"有九帧预览取样" if zh else "Posts with nine-frame preview sampling"} | {sampled} ({sampled/total:.1%}) | {"按帖子计数，不是附件数或完整播放验收" if zh else "Posts, not attachments or full-playback acceptance"} |',
             f'| {"尚无媒体取样" if zh else "Posts without preview sampling"} | {total-sampled} | {"来源披露，含背景讨论" if zh else "Source disclosures, including context discussion"} |',
             f'| {"路由背景讨论" if zh else "Routing-context posts"} | {context} | {"属于总来源数；单列，不当作作品" if zh else "Included in total sources; kept separate from examples"} |', '',
             '取样数只表示至少一段预览接受了九帧检查。它不能验证完整动态、音画同步、配乐原创或后台模型。后续来源增加速度超过媒体检查速度，不能把新增帖数写成新增已验证影片数。' if zh else 'Sampling coverage means at least one preview received nine-frame inspection. It does not verify full motion, synchronization, original music or backend identity. Source additions outpace media review, so new-post totals must not be reported as new verified films.', '',
             '## 后续批次的模型标签' if zh else '## Model labels in later batches', '',
             f'只看 10 月 2 日起的 **{len(later)} 条非路由讨论来源**，避免把早期专搜 Opus 的 168 条深读样本当成跨模型分布。' if zh else f'Use the **{len(later)} non-routing-context sources listed since October 2**, avoiding the 168 older Opus-focused cases as a cross-model denominator.', '',
             '| 模型标签 | 来源帖 | 有取样 |' if zh else '| Model label | Source posts | With sampling |', '|---|---:|---:|']
    for model in MODELS:
        subset = [e for e in later if model in e['model_tags'].split(';')]
        lines.append(f'| {model} 5.5 | {len(subset)} | {sum(e["media_evidence"] == "sampled_preview" for e in subset)} |')
    multi = sum(len(e['model_tags'].split(';')) > 1 for e in later)
    unlabeled = sum(not e['model_tags'] for e in later)
    lines += ['', f'其中 {multi} 条同时提到多个 Claude 5.5 标签，{unlabeled} 条未匹配明确的 Claude 5.5 标签。因此表格行不能相加。Fable 标签含未核实路由，后台身份未确认。' if zh else f'{multi} sources mention multiple Claude 5.5 labels; {unlabeled} match no explicit Claude 5.5 label. Rows therefore cannot be summed. Fable includes unverified routing reports.', '',
              '## 来源作者分布' if zh else '## Source-account concentration', '',
              f'总来源涉及 **{len(creators)} 个不区分大小写的发布账号**。帖数最多的五个账号占 {top_count}/{total}（{top_count/total:.1%}）。发布账号不一定是原创作者。' if zh else f'The collection contains **{len(creators)} case-insensitive publishing handles**. The five most represented accounts contribute {top_count}/{total} ({top_count/total:.1%}). A publishing handle is not necessarily an original creator.', '',
              '| 发布账号 | 来源帖 |' if zh else '| Publishing handle | Source posts |', '|---|---:|']
    lines += [f'| @{name} | {count} |' for name, count in top]
    lines += ['', '这是选例与搜索造成的集中度，不是市场份额。同一作者的系列作品也不是多位创作者的独立复现。' if zh else 'This concentration reflects search and curation, not market share. A series by one author is not independent replication by many creators.', '',
              '## 各批次与搜索缺口' if zh else '## Batches and search gaps', '',
              '| 批次 | 来源帖 | 比此前新增 |' if zh else '| Batch | Source posts | New to earlier batches |', '|---|---:|---:|']
    lines += [f'| [{g["label"]}](../{g["source"]}) | {g["unique_source_posts"]} | {g["newly_listed_source_posts"]} |' for g in groups]
    lines += ['', f'批次按首次收录日期组织，不是作品发布趋势。搜索结果有数量上限，日期条件还需核对帖子的实际时间。补搜与复核记录见[本轮更新]({latest_link})。9 月 26 日逐文件领域、画风、片长和配色分析保留在[冻结快照分析](snapshot-analysis.zh-CN.md)。两套单位不混算。' if zh else f'Batches use first-listing dates, not a publication trend. Search results are capped, and requested dates need checking against actual post timestamps. See [this follow-up]({latest_link}) for coverage. September 26 file-level domain, style, duration and color results remain in [frozen snapshot analysis](snapshot-analysis.md); the units are not merged.', '']
    return '\n'.join(lines)


def render_coverage_chart(entries, groups):
    width = 920; height = 130 + len(groups) * 42
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Preview sampling coverage by collection batch</title>',
             '<desc id="desc">Source-post counts. Navy shows posts with nine-frame preview sampling; grey shows posts without sampling. Batches use listing dates, not release dates.</desc>',
             f'<rect width="{width}" height="{height}" fill="#fafbfc"/>',
             '<g font-family="system-ui,sans-serif" fill="#1f2937">',
             '<text x="24" y="32" font-size="22" font-weight="600">How much of the collection has preview evidence?</text>',
             '<text x="24" y="55" font-size="13">Source posts by listing batch · nine-frame sampling does not verify full motion or model calls</text>',
             '<rect x="24" y="70" width="12" height="12" fill="#244b67"/><text x="42" y="81" font-size="12">Sampled preview</text>',
             '<rect x="195" y="70" width="12" height="12" fill="#d7dfe5"/><text x="213" y="81" font-size="12">Source only</text>']
    for i, group in enumerate(groups):
        subset = [e for e in entries if group['source'] in e['source_ledger'].split(';')]
        sampled = sum(e['media_evidence'] == 'sampled_preview' for e in subset)
        total = len(subset); y = 110 + i * 42; bar = 480
        parts += [f'<text x="24" y="{y+17}" font-size="13">{html.escape(group["label"])}</text>',
                  f'<rect x="215" y="{y}" width="{bar}" height="24" rx="3" fill="#d7dfe5"/>',
                  f'<rect x="215" y="{y}" width="{bar*sampled/total:.2f}" height="24" fill="#244b67"/>',
                  f'<text x="715" y="{y+17}" font-size="13">{sampled} / {total} sampled ({sampled/total:.1%})</text>']
    parts += ['</g></svg>']
    return '\n'.join(parts) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    entries, groups = collect(); total = len(entries)
    summary = dict(as_of=max(g['date'] for g in groups), unit='source post ID; includes replies, comparisons and variants',
                   unique_source_posts=total, sampled_source_posts=sum(e['media_evidence'] == 'sampled_preview' for e in entries),
                   routing_context_posts=sum(e['entry_kind'] == 'routing_context' for e in entries), batches=groups,
                   frozen_media_snapshot='data/corpus-snapshot.json')
    buffer = io.StringIO(); w = csv.DictWriter(buffer, fieldnames=list(entries[0]), lineterminator='\n'); w.writeheader(); w.writerows(entries)
    outputs = {ROOT/'assets/collection-coverage.svg': render_coverage_chart(entries, groups), ROOT/'data/collection-summary.json': json.dumps(summary, ensure_ascii=False, indent=2)+'\n', ROOT/'data/collection-index.csv': buffer.getvalue()}
    for zh in (False, True):
        suffix = '.zh-CN' if zh else ''
        outputs[ROOT/f'docs/library{suffix}.md'] = render_library(entries, zh)
        outputs[ROOT/f'docs/collection-analysis{suffix}.md'] = render_analysis(entries, groups, zh)
        path = ROOT/('README.zh-CN.md' if zh else 'README.md'); text = path.read_text()
        if text.count(START) != 1 or text.count(END) != 1:raise ValueError(f'Expected one summary block: {path}')
        models = [f'| [{m}](docs/library{suffix}.md#{m.lower()}) | {sum(m in e["model_tags"].split(";") for e in entries)} |' for m in MODELS]
        block = [f'截至 {summary["as_of"]}：**{total} 条去重来源帖**，其中 **{summary["sampled_source_posts"]} 条有九帧预览取样**。' if zh else f'As of {summary["as_of"]}: **{total} distinct source posts**, with **{summary["sampled_source_posts"]} receiving nine-frame preview sampling**.', '',
                 '| 模型浏览入口 | 来源帖 |' if zh else '| Browse by model | Source posts |', '|---|---:|', *models, '',
                 '[完整目录](docs/library.zh-CN.md) · [证据与作者分布](docs/collection-analysis.zh-CN.md) · [批次汇总](data/collection-summary.json)' if zh else '[Complete directory](docs/library.md) · [Evidence and account coverage](docs/collection-analysis.md) · [Batch totals](data/collection-summary.json)']
        before, rest = text.split(START); _, after = rest.split(END)
        outputs[path] = before+START+'\n\n'+'\n'.join(block)+'\n\n'+END+after
    stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if args.check:
        if stale:raise SystemExit('Stale collection outputs: '+', '.join(stale))
        print(f'Collection index, directory, analysis and README totals match {total} public source posts')
    else:
        for p, text in outputs.items():p.write_text(text)
        print(f'{total} source posts; {summary["sampled_source_posts"]} with sampled previews')

if __name__ == '__main__':main()
