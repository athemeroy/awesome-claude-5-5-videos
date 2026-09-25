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

## Review standard

The home-page list is a **curated selection**, not an exhaustive search result. A proposed entry should teach a distinct production pattern or provide unusually strong evidence. The larger [case index](data/cases.csv) can include useful comparisons and uncertainty when they are labeled clearly. We do not infer the rendering pipeline from aesthetics alone or count a quote/repost as another original work.

Use one primary path from the [field guide](docs/case-index-guide.zh-CN.md), then describe any mixed roles in prose. Keep creator reports, public-project evidence, and direct file observations separate. For corrections, cite the exact original post, author reply, project file, or measured result that changes the record.

## Updating the dataset

Each CSV row represents one original X post ID. Keep the existing columns and UTF-8 encoding. Do not add NAS paths, raw media URLs, access tokens, user cookies, or individual downloaded MP4 metadata that could become a redistribution channel. Include a brief review note describing what the sources do **not** establish.

The current snapshot is frozen at September 25, 2026, 06:22 China Standard Time. New cases should carry their own verification date in the pull request; do not silently revise the historical counts in the 2026-09-25 report.
