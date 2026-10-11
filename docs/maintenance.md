# Maintain the collection

[Home](../README.md) · [Contribution criteria](../CONTRIBUTING.md) · [Figure reproduction](chart-generation.md)

The project has two data layers. The **current collection** grows through dated source ledgers. The **September 26 research snapshot** keeps its original file-level denominators. One source post can contain several attachments, quote another work, or compare models; it is not a count of distinct films.

## One entry point

Use Python 3.12 or newer. The collection commands use only the standard library:

```sh
python3 scripts/maintain.py generate
python3 scripts/maintain.py check
```

Both commands default to `--scope collection`. Generation reads the public source records and updates the index, summaries and README statistics. Checking validates those records and compares every generated output without writing files.

| Scope | Included work | Dependencies |
|---|---|---|
| `collection` | Current source index, bilingual directory and coverage analysis, coverage SVG and README summary blocks | Python standard library |
| `snapshot` | Frozen case directory, statistics, domain/style atlas and figures; dated engagement, thumbnail and color-data checks | [Pinned chart packages](../requirements-charts.txt) |
| `all` | Snapshot first, then current collection | Same as `snapshot` |

For a complete check after changing shared scripts or snapshot research:

```sh
python3 -m venv .venv-charts
.venv-charts/bin/python -m pip install -r requirements-charts.txt
.venv-charts/bin/python scripts/maintain.py check --scope all
```

Reuse an existing environment with those pinned packages when available. To regenerate public research outputs, use `generate --scope snapshot` or `generate --scope all`. The entry point uses the same Python interpreter for its child scripts and works from any working directory when given its absolute path. It stops on the first failed command and returns a nonzero exit status.

`python3 scripts/maintain.py check --scope all --list` prints the exact commands without running them. The original script entry points remain supported. The existing GitHub workflow runs the ten snapshot checks; the current collection check is included in this maintenance entry point.

Generation never collects live counters or extracts new media. Checks that depend on private source files stay read-only even when the action is `generate`.

## Files and ownership

| Area | Edit these inputs | Generated outputs |
|---|---|---|
| Current collection | `data/claude55-source-review-YYYY-MM-DD[-followup].csv`; dated update pages | `data/collection-index.csv`, `data/collection-summary.json`, `docs/library*.md`, `docs/collection-analysis*.md`, `assets/collection-coverage.svg`, README collection blocks |
| Reviewed case snapshot | `data/cases.csv` with its existing schema | `docs/cases-index.zh-CN.md` |
| Snapshot statistics | `data/corpus-snapshot.json`, `data/cases.csv`, `data/domain-style.csv` | `docs/statistics*.md`; domain, style, duration and cross-tab SVGs |
| Domain/style atlas | Snapshot inputs, `data/case-engagement-observed.csv`, `data/case-engagement-refresh-2026-09-27.csv` | `docs/domain-style-atlas*.md` |
| Introductory figures | Frozen snapshot and `data/visible-prompt-lengths.json` | Corpus overview, production-role diagram and visible-prompt chart |
| Color study | `data/color-study/` summaries, vectors, assignments and palettes | `assets/color-study/` SVGs |
| Editorial analysis | `docs/workflow-analysis*.md`, `docs/snapshot-analysis*.md`, `docs/production-resources*.md`, other source-linked research pages | Edited by hand; headline findings can be summarized in both READMEs |
| Source stills | Small image files plus each directory's `frames.csv` source/rights manifest | Frozen and September 27 stills have dedicated check scripts |

Do not hand-edit generated pages or data exports. Edit the source ledger, input dataset or responsible generator. Keep hand-written README findings outside `<!-- collection-summary:start -->` and `<!-- collection-summary:end -->`; generation replaces only that block.

Existing paths remain stable. The seven September 27 source descriptions are a small compatibility table in `generate_collection_summary.py`; new batches belong in dated ledgers.

## Add a current source batch

1. Create `data/claude55-source-review-YYYY-MM-DD.csv`. For another batch on the same day, use a `-followup` suffix. These dates identify listing batches; preserve each post's actual publication time separately.
2. Add the bilingual dated update pages and their source links. Set each ledger row's `detail_page` to the English repository-relative page, such as `docs/maintenance-2026-10-11.md`. The Chinese directory uses the corresponding `.zh-CN.md` page when available.
3. Record search coverage and candidate decisions in separate dated CSVs. Keep returned timestamps, caps and failed queries visible so the update does not imply exhaustive coverage.
4. Add any permitted small stills with their source/rights manifest and update [THIRD_PARTY.md](../THIRD_PARTY.md). Keep downloaded MP4s and nine-frame sheets out of the repository.
5. Run `python3 scripts/maintain.py generate`, review the changed totals and pages, then run `python3 scripts/maintain.py check`.

The source ledger's required nonblank columns are `post_id`, `source_url`, `model_attribution` and `media_review`. Preserve the other provenance fields from the most recent ledger: source/checked dates, author, backend identity, claims, limitations and receipt keys. Use `title_en`, `title_zh`, `category`, `preview_duration_s`, `related_sources`, `thumbnail` and `detail_page` when applicable.

The generator validates required fields, CSV row widths, dates, post IDs, within-batch duplicates, detail pages and thumbnail paths. Without `detail_page`, it looks for `docs/maintenance-<batch>.md`, then `docs/claude55-update-<batch>.md`. Follow-up suffixes are part of the page name. A missing page is an error, rather than a link to an unrelated older update.

One original post ID is counted once across the collection. Re-listing it in a later batch adds provenance and can strengthen its sampling record; its earliest listing date, title and model attribution stay in the index. If the original attribution was wrong, correct the first source record with a dated explanation. Multiple attachments in the September 27 stills manifest also remain one post.

`media_review` beginning with `nine frames inspected` marks at least one sampled preview. Otherwise the source remains `source_only`. A still by itself does not establish sampling. The generator checks declared records and public file paths; it does not watch media or verify model calls.

Model groups follow explicit `Opus 5.5`, `Sonnet 5.5`, `Haiku 5.5` and `Fable 5.5` attribution text, plus the documented suspected Fable routing reports. Multi-model sources appear in every applicable group. Set `source_kind` to `routing discussion` for context-only reports. The older Opus-focused case collection retains its snapshot-context label.

## Preserve dated research

Keep the September 26 snapshot fixed. Corrections must explain the affected record and denominator; later observations use a new dated dataset. Adding a source-only post does not expand the frozen media or reviewed-case totals.

The [chart guide](chart-generation.md) maps each figure to its published inputs and pinned rendering dependencies. The [methodology](methodology.zh-CN.md) explains the sampling limits. The unified snapshot check also validates the September 27 engagement archive, both existing still manifests and color-study consistency.

Live engagement collection remains an explicit operation. With an existing Chrome CDP session and Playwright installed:

```sh
python3 scripts/refresh_case_engagement.py --date YYYY-MM-DD
```

Use `--resume` after interruption. Use `--resume --fill-from-html` for bounded, source-checked recovery of missing fields. Validate the finished file with `--date YYYY-MM-DD --check --require-complete`. Do not replace an older observation table with later counters. A new dated refresh needs an explicit analysis change before it is used by the atlas or maintenance checks.

Thumbnail extraction also remains explicit: `generate_case_thumbnails.py --source-root LOCAL_ROOT` and `generate_new_case_thumbnails.py --source-dir LOCAL_DIR` require locally verified media. Their `--check` modes only need public files. Author claims, preview observations and measured file properties must remain distinguishable in published analysis.
