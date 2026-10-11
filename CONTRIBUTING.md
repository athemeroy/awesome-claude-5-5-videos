# Contributing

Thank you for helping make this list more accurate. Contributions can add a creator's original post, supply a missing prompt or project link, correct a production path, or flag a deleted source.

## Model labels and early-access reports

The list covers Opus, Sonnet, Haiku and creator-reported Fable 5.5 video workflows. Record the exact model/version named by the creator, the model label shown in the interface if available, and whether backend identity is independently verified. For suspected next-Fable routing, use “creator reports Fable 5.5; backend unverified.” Keep those sources in a dated update and its separate source ledger until media review qualifies them for a later case collection. A knowledge question, model self-identification, or stronger-looking output does not verify a backend change.

The September 26 datasets remain an Opus 5.5 snapshot. Adding another model does not relabel those rows or expand their denominators. See the [October 2 update](docs/claude55-update-2026-10-02.md).

## Propose a case

Open an issue using the **New video case** template or a pull request. Please include:

1. The original X post URL and creator handle. If you found a repost or quote, include the earlier original separately.
2. A short description of the video and why it adds a distinct technique, workflow, or well-documented example.
3. Links to the creator's own prompt, replies, source repository, or making-of account, if public.
4. The supplied assets: earlier footage, photographs, music, documents, product code, character files, or prepared skills.
5. The role of Claude, the renderer or external model that produced the pixels, and any named audio tools. Use “creator says” when no source or execution log confirms a step.
6. Human revision rounds, cost, and elapsed time only when sourced; distinguish subscription allowance, API-equivalent estimates, and actual bills.

Please do **not** upload third-party MP4s, music, screenshots of private conversations, credentials, or complete third-party prompt text. Link to the creator's original publication and paraphrase what is relevant. If you are the creator and wish to share your own assets or full prompt, link to a repository you control.

## Propose a reusable resource

Use the **Reusable project or resource** issue template or a pull request for an open-source engine, skill, style library, or production guide. Link the maintainer's original project, a representative demo or announcement, and the exact files or commands readers can reuse. State which examples the maintainer attributes to each model; a multi-model project's other examples should keep their own labels. Include the project's license, any separate asset terms, the date you checked it, and claims that remain unverified.

A source-only resource can be useful without an original X MP4. List it in the open-source production systems section when it teaches a distinct, inspectable workflow. Do not add it to the frozen September 26 video-case or media counts unless it independently qualifies as a new case in a later, separately dated snapshot.

## Review standard

The home-page list is a **curated selection**, not an exhaustive search result. A proposed entry should teach a distinct production pattern or provide unusually strong evidence. The larger [case index](data/cases.csv) can include useful comparisons and uncertainty when they are labeled clearly. We do not infer the rendering pipeline from aesthetics alone or count a quote/repost as another original work.

Use one primary path from the [field guide](docs/case-index-guide.zh-CN.md), then describe any mixed roles in prose. Keep creator reports, public-project evidence, and direct file observations separate. For corrections, cite the exact original post, author reply, project file, or measured result that changes the record.

## Updating the collection

The [maintenance guide](docs/maintenance.md) explains the project structure, input/output ownership, ledger fields and complete checks. For a normal dated source update, use one entry point:

```sh
python3 scripts/maintain.py generate
python3 scripts/maintain.py check
```

These commands update the current collection and its README totals. Use `--scope snapshot` for the frozen research outputs or `--scope all` for both. Snapshot chart checks need the pinned packages in `requirements-charts.txt`; setup and exact commands are in the guide. Existing script entry points still work.

Each CSV row represents one original X post ID. Keep UTF-8 encoding and the existing provenance columns. Add the original URL, exact creator-reported model attribution, media-review status, claims, limitations and the dated detail-page path. Record search coverage separately. Do not add NAS paths, raw media URLs, credentials, cookies or downloaded MP4 metadata that could become a redistribution channel.

New batches go in `data/claude55-source-review-YYYY-MM-DD.csv`; same-day additions may use `-followup`. The generator combines those ledgers with the older reviewed cases, preserves the earliest listing, and counts a multi-model comparison in each applicable model group. Routing discussion stays separate from examples. Edit generated outputs through their inputs or generator, and keep editorial README summaries outside the generated collection markers.

The September 26, 2026, 21:53 China Standard Time snapshot remains frozen in [`data/corpus-snapshot.json`](data/corpus-snapshot.json). New source posts do not expand its media or case denominators. Do not present an unprobed post as a `tile_ok` case. Classifier labels are judgments and the case index is a purposive selection; these data do not support population confidence intervals, p-values or model-quality rankings.

Keep later engagement counts in a separate dated table. Retain rounded display values and conservative intervals unless an exact count is verified from the same official post. Counts observed at different times are not final totals or measures of video quality. The maintenance guide describes collection and validation separately.

Small source stills require a source/rights manifest and an entry in [THIRD_PARTY.md](THIRD_PARTY.md). Link original posts; do not upload third-party MP4s, contact sheets or arbitrary screenshots. The [chart guide](docs/chart-generation.md) covers figures reproduced from public research data.
