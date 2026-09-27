# Contributing

Thank you for helping make this list more accurate. Contributions can add a creator's original post, supply a missing prompt or project link, correct a production path, or flag a deleted source.

## Propose a case

Open an issue using the **New video case** template or a pull request. Please include:

1. The original X post URL and creator handle. If you found a repost or quote, include the earlier original separately.
2. A short description of the video and why it adds a distinct technique, workflow, or well-documented example.
3. Links to the creator's own prompt, replies, source repository, or making-of account, if public.
4. The supplied assets: earlier footage, photographs, music, documents, product code, character files, or prepared skills.
5. The role of Opus, the renderer or external model that produced the pixels, and any named audio tools. Use “creator says” when no source or execution log confirms a step.
6. Human revision rounds, cost, and elapsed time only when sourced; distinguish subscription allowance, API-equivalent estimates, and actual bills.

Please do **not** upload third-party MP4s, music, screenshots of private conversations, credentials, or complete third-party prompt text. Link to the creator's original publication and paraphrase what is relevant. If you are the creator and wish to share your own assets or full prompt, link to a repository you control.

## Propose a reusable resource

Use the **Reusable project or resource** issue template or a pull request for an open-source engine, skill, style library, or production guide. Link the maintainer's original project, a representative demo or announcement, and the exact files or commands readers can reuse. State which examples the maintainer attributes to Opus 5.5; a multi-model project's other examples should keep their own labels. Include the project's license, any separate asset terms, the date you checked it, and claims that remain unverified.

A source-only resource can be useful without an original X MP4. List it in the open-source production systems section when it teaches a distinct, inspectable workflow. Do not add it to the frozen September 26 video-case or media counts unless it independently qualifies as a new case in a later, separately dated snapshot.

## Review standard

The home-page list is a **curated selection**, not an exhaustive search result. A proposed entry should teach a distinct production pattern or provide unusually strong evidence. The larger [case index](data/cases.csv) can include useful comparisons and uncertainty when they are labeled clearly. We do not infer the rendering pipeline from aesthetics alone or count a quote/repost as another original work.

Use one primary path from the [field guide](docs/case-index-guide.zh-CN.md), then describe any mixed roles in prose. Keep creator reports, public-project evidence, and direct file observations separate. For corrections, cite the exact original post, author reply, project file, or measured result that changes the record.

## Updating the dataset

Each CSV row represents one original X post ID. Keep the existing columns and UTF-8 encoding. Do not add NAS paths, raw media URLs, access tokens, user cookies, or individual downloaded MP4 metadata that could become a redistribution channel. Include a brief review note describing what the sources do **not** establish.

If you edit `data/cases.csv`, regenerate the [browsable directory](docs/cases-index.zh-CN.md) with `python3 scripts/generate_cases.py`, then run `python3 scripts/generate_cases.py --check`. The generator rejects duplicate post IDs, unknown production paths, and cases without a nine-frame sampling record.

The [statistical profile](docs/statistics.md) is generated from the public case and classification CSV files plus the frozen snapshot. If either CSV changes in a separately dated release, run `python3 scripts/generate_statistics.py` and `python3 scripts/generate_stat_charts.py`, then rerun both with `--check`. The profile treats classifier labels as judgments and the case index as a purposive selection; do not report population confidence intervals, p-values, or quality rankings from these data. The new style, duration, and domain × style SVG charts use only the Python standard library. The separate domain chart is rebuilt with `python3 scripts/plot_domain_labels.py` (Matplotlib required for this chart only).

The [domain × style atlas](docs/domain-style-atlas.md) reads the frozen classifier/case CSVs, the [September 24–26 engagement archive](data/case-engagement-observed.csv), and a separate [September 27 public X-page refresh](data/case-engagement-refresh-2026-09-27.csv). Do not overwrite an older observation table with later counters. To make a new dated snapshot, use `python3 scripts/refresh_case_engagement.py --date YYYY-MM-DD` against an existing Chrome CDP session with Playwright available; use `--resume` after interruption and `--resume --fill-from-html` for bounded, source-checked missing-field recovery. `--check --require-complete` validates a finished CSV without Playwright or browser access. The collector associates a rendered counter with the target post ID before reading its article: an X reply page may show a parent post first. Its HTML fallback checks the target ID and creation time. Then regenerate the atlas and run `python3 scripts/generate_domain_style_atlas.py --check`. Large likes may appear only as rounded text in X's UI; retain the display and conservative interval unless an exact count can be verified from the same official post page. Counts were observed at different times, are not final totals, and do not measure video quality.

The visual directory's 168 small stills are indexed in [`assets/case-thumbnails/frames.csv`](assets/case-thumbnails/frames.csv). Maintainers regenerate them from locally verified X previews with `scripts/generate_case_thumbnails.py`; its public `--check` mode checks file coverage and mapping without the MP4s or third-party Python packages. Later-case stills have a separate manifest and check mode in `scripts/generate_new_case_thumbnails.py`. The two external-project previews have a source and rights manifest in [`assets/resource-thumbnails/frames.csv`](assets/resource-thumbnails/frames.csv). Link a new original post rather than uploading a third-party MP4, contact sheet, or arbitrary screenshot in a pull request. The stills remain the original creators' material; see [THIRD_PARTY.md](THIRD_PARTY.md).

The current corpus snapshot is frozen at September 26, 2026, 21:53 China Standard Time; its counts are recorded in [`data/corpus-snapshot.json`](data/corpus-snapshot.json). New cases and source-only resources should carry their own verification date in the issue or pull request. Do not silently revise the frozen counts or present an unprobed X post as a `tile_ok` video case.
