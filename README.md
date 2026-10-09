# Awesome Claude 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[中文](README.zh-CN.md) · [Visual directory](docs/cases-index.zh-CN.md) · [Contribute](CONTRIBUTING.md)

A curated collection of videos, animations and reusable production workflows made with **Claude 5.5**. Covers Opus, Sonnet, Haiku and creator-reported Fable testing. Each example links to its source and explains Claude's role: rendering code, supplied-media editing, external-model direction or a recorded app.

## Contents

- [Watch examples](#watch-examples)
- [Browse the collection](#browse-the-collection)
- [Make your own](#make-your-own)
- [Collection statistics](#collection-statistics)
- [Research and data](#research-and-data)
- [Updates](#updates)
- [Contributing and license](#contributing-and-license)

## Watch examples

| History | Art | Science |
|:---:|:---:|:---:|
| [<img src="assets/claude55-2026-10-03/2106081142143168580.jpg" width="240" alt="Human progress shown on a one-day clock">](https://x.com/imjustnewatai/status/2106081142143168580) | [<img src="assets/claude55-2026-10-03/2106095190285144331.jpg" width="240" alt="An artist and cat travel through art history">](https://x.com/cherry_mx_reds/status/2106095190285144331) | [<img src="assets/claude55-2026-10-03/2106190594775097663.jpg" width="240" alt="A continuous zoom from microscopic structures to galaxies">](https://x.com/imjustnewatai/status/2106190594775097663) |
| [Human progress in one day](https://x.com/imjustnewatai/status/2106081142143168580) · @imjustnewatai | [40,000 years of art, with a cat](https://x.com/cherry_mx_reds/status/2106095190285144331) · @cherry_mx_reds | [The Long Way Out](https://x.com/imjustnewatai/status/2106190594775097663) · @imjustnewatai |
| A clock carries the story into imagined futures. | Recurring characters connect changing art styles. | One zoom connects quarks, people and galaxies. |

All three are creator-reported Fable 5.5 examples with unverified backend identity. We inspected nine sampled frames per preview. [Production claims and review notes](docs/claude55-update-2026-10-03.md).

## Browse the collection

- [Haiku videos and comparisons](docs/maintenance-2026-10-10.md#haiku-videos-and-comparisons) — poetry, motion design, a 3D pelican, editing and graphics comparisons.
- [Visual case directory](docs/cases-index.zh-CN.md) — 168 reviewed source posts, each with a frame, original link and production notes.
- [Claude video directory](docs/claude55-update-2026-10-03.md#browse-all-added-sources-by-purpose) — history, science, stories, launches, music, games and visual experiments.
- [Domain × style atlas](docs/domain-style-atlas.md) — find pictured examples by subject and look.
- [Evidence comparisons](docs/evidence-examples.md) — similar looks, different inputs and tool roles.
- [Fable / Opus and Sonnet comparisons](docs/claude55-update-2026-10-02.md) — early creator reports with source notes.

## Make your own

### Production routes

- [Code-drawn 2D](https://x.com/hanifproduktif/status/2102742924148830211) — ant-colony animation with matching source.
- [Educational explainers](https://x.com/LinearUncle/status/2103128559174971663) — a Manim calculus lesson.
- [3D and real-time graphics](https://x.com/Aurelien_Gz/status/2102786378282987591) — Clearwater water simulation with WebGL source.
- [Existing-footage editing](https://x.com/AxtonLiu/status/2102827887732932956) — a talking-head performance remade as line art.
- [External video models](https://x.com/abxxai/status/2102775755646337530) — Opus directing Seedance.
- [App and game recordings](https://x.com/masaya_1980/status/2103115017755500561) — a can-collection simulation.
- [Mixed workflows and comparisons](https://x.com/leogao25/status/2102544078927741369) — a split-screen physics comparison.

[Choose a route](docs/visual-effects-fit.md) · [Pictured routes and source checks](docs/production-resources.md) · [Prompt templates](docs/prompt-playbook.zh-CN.md) · [Prompt / workflow matrix](docs/prompt-matrix.zh-CN.md)

### Open-source resources

- [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) — style library, director guide and deterministic Canvas/WebGL scene examples.
- [Papermotion](https://github.com/francozanardi/papermotion) — paper-cut animation engine, character rigs, physics and offline rendering. Samples have separate model labels.
- [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) — p5.js / p5.brush starter for character animation, storyboards and rendering.
- [Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill) — Claude Code plugin and Ruby toolkit for supplied-song videos; can call external image, video and audio models.

[Previews, reusable files and attribution notes](docs/production-resources.md#reusable-open-source-production-systems). Resource descriptions were checked September 27; external projects may change.

## Collection statistics

<!-- collection-summary:start -->

| Batch | Source posts | New to earlier batches |
|---|---:|---:|
| [2026-09-26](data/cases.csv) | 168 | 168 |
| [2026-09-27](assets/new-case-thumbnails/frames.csv) | 7 | 7 |
| [2026-10-02](data/claude55-source-review-2026-10-02.csv) | 22 | 22 |
| [2026-10-03](data/claude55-source-review-2026-10-03.csv) | 157 | 157 |
| [2026-10-10](data/claude55-source-review-2026-10-10.csv) | 18 | 18 |

As of 2026-10-10: **372 distinct source posts**.

<!-- collection-summary:end -->

These are source-post counts, including replies, comparisons and variants, rather than independent-film or verified-model-run counts. Totals are deduplicated across dated batches. [Reproducible totals](data/collection-summary.json).

The **September 26 Opus snapshot** contains 1,401 byte-distinct files, of which 1,119 were labeled `yes` / `likely`. Its main findings:

- Games, ads and AI-about-AI comprise **57.7%** of included files.
- Motion graphics / UI and 3D render comprise **60.2%**.
- Reviewed previews have a **52.37 s** median; all classified files have a **39.20 s** median. The samples use different units and selection rules.

[Charts and analysis](docs/snapshot-analysis.md) · [Full statistics](docs/statistics.md) · [Color study](docs/color-modes.md)

## Research and data

- [Methodology](docs/methodology.zh-CN.md), [search coverage](docs/search-coverage.zh-CN.md) and [media profile](docs/media-profile.zh-CN.md).
- [Reviewed cases](data/cases.csv), [file classifications](data/domain-style.csv) and [field guide](docs/case-index-guide.zh-CN.md).
- [Research report](docs/report.zh-CN.md) and [Article version](docs/x-article.zh-CN.md).
- [Chart reproduction](docs/chart-generation.md). Detailed charts stay on the research pages.

Model labels follow creator disclosures. Sampled frames establish visible content, not hidden tool calls, full-motion quality or music provenance. Original MP4s and private acquisition records are not distributed. This is an independent collection.

## Updates

- [October 10: maintenance and source review](docs/maintenance-2026-10-10.md).
- [October 3: grouped Claude video directory](docs/claude55-update-2026-10-03.md).
- [October 2: Fable reports and Sonnet comparisons](docs/claude55-update-2026-10-02.md).
- [September 27: seven additional workflows](docs/new-cases-2026-09-27.md).
- [September 26: frozen Opus research snapshot](docs/snapshot-analysis.md).

## Contributing and license

[Suggest an original video or reusable project](CONTRIBUTING.md). Prefer a distinct workflow, clear inputs or inspectable source. Corrections and missing creator links are welcome.

Original writing and diagrams: [CC BY 4.0](LICENSE). Linked works and preview frames belong to their creators and have separate terms. [Third-party material](THIRD_PARTY.md).
