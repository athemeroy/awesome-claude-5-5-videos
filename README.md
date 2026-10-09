# Awesome Claude 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[中文](README.zh-CN.md) · [All sources](docs/library.md) · [Contribute](CONTRIBUTING.md)

Curated videos, animations and reusable workflows made with **Claude 5.5**: Opus, Sonnet, Haiku and creator-reported Fable testing. Original posts, model roles, inputs and evidence are recorded separately.

## Contents

- [Browse by model](#browse-by-model)
- [Four starting points](#four-starting-points)
- [Make your own](#make-your-own)
- [What we learned](#what-we-learned)
- [Research and data](#research-and-data)
- [Updates](#updates)
- [Contributing and license](#contributing-and-license)

## Browse by model

<!-- collection-summary:start -->

As of 2026-10-10: **394 distinct source posts**, with **194 receiving nine-frame preview sampling**.

| Browse by model | Source posts |
|---|---:|
| [Opus](docs/library.md#opus) | 282 |
| [Sonnet](docs/library.md#sonnet) | 45 |
| [Haiku](docs/library.md#haiku) | 15 |
| [Fable](docs/library.md#fable) | 65 |

[Complete directory](docs/library.md) · [Evidence and account coverage](docs/collection-analysis.md) · [Batch totals](data/collection-summary.json)

<!-- collection-summary:end -->

Multi-model comparisons appear in several groups, so rows cannot be summed. Older Opus cases use snapshot context; Fable includes suspected routing. Source posts include replies and variants, not independent-film counts.

[Pictured production paths](docs/cases-index.zh-CN.md) · [Subject × style atlas](docs/domain-style-atlas.md) · [Evidence comparisons](docs/evidence-examples.md)

## Four starting points

| Opus | Sonnet | Haiku | Fable (creator report) |
|:---:|:---:|:---:|:---:|
| [<img src="assets/case-thumbnails/2102786378282987591.webp" width="180" alt="Clearwater water">](https://x.com/Aurelien_Gz/status/2102786378282987591) | [<img src="assets/claude55-2026-10-10-followup/2107548992640880755.jpg" width="180" alt="Tower construction">](https://x.com/Solvaix/status/2107548992640880755) | [<img src="assets/claude55-2026-10-10-followup/2108089492016103775.jpg" width="180" alt="Motion showreel">](https://x.com/badboyfoxy/status/2108089492016103775) | [<img src="assets/claude55-2026-10-10-followup/2107958931230241037.jpg" width="180" alt="Doodle history">](https://x.com/oalanicolas/status/2107958931230241037) |
| [Clearwater water](https://x.com/Aurelien_Gz/status/2102786378282987591) | [Tower construction](https://x.com/Solvaix/status/2107548992640880755) | [Motion showreel](https://x.com/badboyfoxy/status/2108089492016103775) | [Doodle history](https://x.com/oalanicolas/status/2107958931230241037) |
| Real-time WebGL graphics | A staged interactive scene | Type, easing and orbital forms | Changing eras and a recurring character |

These illustrate four different tasks, not a same-prompt model ranking. Previews received nine-frame sampling, which cannot verify full motion or model calls. [New preview and workflow notes](docs/maintenance-2026-10-10-followup.md).

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

## What we learned

- **Inputs define the task.** References, character sheets, songs and existing projects change what the model actually contributes.
- **One prompt can trigger many passes.** The F1 creator reports repeated rejection of intermediate results; Taxtello records five versions.
- **Compare task cost.** In reported costs, Haiku uses 72.0% of Opus’s bridge budget; the F1 executor accounts for 64.2% of its team total. These are not general model rankings.
- **Appearance and correctness need separate evidence.** The Sonnet tower creator says the sequence is invented and not engineering-calculated.

[Workflow and cost analysis](docs/workflow-analysis.md) · [Sampling and account coverage](docs/collection-analysis.md)

## Research and data

- [Unified source CSV](data/collection-index.csv): every batch, model/role label, original post and evidence link.
- [Collection and evidence analysis](docs/collection-analysis.md): model labels, sampling, publishing accounts and batches.
- [Frozen snapshot analysis](docs/snapshot-analysis.md), [full statistics](docs/statistics.md) and [color study](docs/color-modes.md).
- [Methodology](docs/methodology.zh-CN.md), [media profile](docs/media-profile.zh-CN.md) and [chart reproduction](docs/chart-generation.md).

The September 26 file snapshot remains 1,401 byte-distinct files, with 1,119 included by classification. Games, ads and AI-about-AI comprise 57.7%; motion/UI and 3D render comprise 60.2%. Later sources do not enter these file denominators.

Samples document visible content; disclosures document production claims. Backend identity, full motion, costs and original music are not independently verified for every entry. Original MP4s are not distributed. This collection is independent.

## Updates

- [2026-10-10 follow-up and analysis](docs/maintenance-2026-10-10-followup.md).
- [2026-10-10 first maintenance and Haiku](docs/maintenance-2026-10-10.md).
- [2026-10-03 grouped video directory](docs/claude55-update-2026-10-03.md).
- [2026-10-02 Fable reports and Sonnet comparisons](docs/claude55-update-2026-10-02.md).
- [2026-09-27 additional workflows](docs/new-cases-2026-09-27.md).

## Contributing and license

[Suggest an original post or reusable project](CONTRIBUTING.md). Prefer distinct workflows, clear inputs or inspectable source. Corrections and missing creator links are welcome.

Original writing and diagrams: [CC BY 4.0](LICENSE). Linked works and preview frames belong to their creators and have separate terms. [Third-party material](THIRD_PARTY.md).
