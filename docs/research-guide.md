# From examples to production choices: five findings

[Home](../README.md) · [All documentation](README.md) · [Browse the collection](library.md) · [简体中文](research-guide.zh-CN.md)

The collection answers “what examples exist?” This guide asks what content tends to look like, how inputs change the production task, how much work sits behind a prompt, and how to read reported costs.

Content and color figures use the **frozen 26 September 2026 sample**: 1,119 files labeled `yes` or `likely` by the classifier. Production routes use a separate set of 168 selected source posts. Later posts add qualitative examples without entering either denominator. [Current collection analysis](collection-analysis.md) tracks ongoing source-post additions.

## 1. Content–style pairings are more useful than a domain ranking

![File counts across eleven content domains and thirteen primary visual styles](../assets/domain-style-heatmap.svg)

Games often use 3D; ads often use motion graphics. Those two cells contain 315 files, or **28.2%** of the included sample. Education and stories have less concentrated leading styles.

| Content and its most common primary style | `yes` + `likely`: share within the domain | `yes` only: share within the domain |
|---|---:|---:|
| Games / interactive → 3D render | 161 / 230 = 70.0% | 129 / 187 = 69.0% |
| Ads / launches → motion graphics / UI | 154 / 215 = 71.6% | 140 / 191 = 73.3% |
| Education / science → motion graphics / UI | 55 / 147 = 37.4% | 52 / 139 = 37.4% |
| Short stories → flat cartoon | 37 / 112 = 33.0% | 36 / 105 = 34.3% |

Each denominator is the file count for that content domain. The first two pairings stay near 70% under both inclusion rules; education and stories have leading styles around one third. Games and ads exchange places in the overall domain ranking when `likely` files are included, but these pairings are more stable.

**Production implication:** the dense UI-motion and interactive-3D cells are useful places to find references. For education and stories, start with the explanation or narrative and choose its visual treatment. This is a working suggestion from the sample, not a route success rate. [Clickable atlas](domain-style-atlas.md) · [Classification CSV](../data/domain-style.csv) · [Threshold analysis](statistics.md).

## 2. List the inputs before choosing the model's job

The 168 selected cases have seven primary routes: code-drawn 2D, 52; existing-source transformations, 32; educational explainers, 27; 3D / real-time graphics, 19; app / game captures, 14; mixed or unestablished, 14; and external video-model orchestration, 10. These cases were selected to examine production conditions, not to estimate market shares. [Case data](../data/cases.csv).

| Available input | Work described in a reviewed example | What to settle before production |
|---|---|---|
| Product repository, UI and branding | [Social SDK](https://x.com/leodev/status/2102897952587133299) describes existing animation components, scene direction and tool changes. | Which states need actual product captures, and which graphics need to be made. |
| Footage, voice and captions | The [talking-head transformation](https://x.com/AxtonLiu/status/2102827887732932956) asks to preserve the performance, sound and duration. | What stays, what gets redrawn, and how the timelines align. |
| Character and shot references | The [Blender-to-Seedance example](https://x.com/OriSilver/status/2102817977812824335) separates camera blocking from final image production. | Who designs the shot, supplies the character and renders the final footage. |
| Reference video | The Clearwater creator reports supplying a [reference video](https://x.com/Aurelien_Gz/status/2102479887495758076); the [published output project](https://github.com/Aureliengmz/clearwater) is a WebGL water scene with an embedded texture. | Whether the deliverable is an interactive scene, editable code or an offline video. |

**Production implication:** writing animation code, editing footage, orchestrating a video model and building an application to record require different inputs and deliverables. Choose that route before copying a prompt. [Illustrated production routes](production-resources.md) · [14 paired examples](evidence-examples.md) · [Reusable production brief](production-brief.md).

## 3. One visual style needs more than one palette reference

![Color modes within education, stories, motion graphics and ads; swatch widths represent pixel shares](../assets/color-study/color-modes-highlight.svg)

The 350 motion-graphics / UI files divide into **198 dark-neutral** and **152 light-neutral** files: 56.6% and 43.4% of that style. The 215 ad files divide into three color modes of 97, 82 and 36 files. A single average palette would hide these choices.

The per-video median share of colorful pixels is **45.5%** for music videos (77 files), compared with **17.6%** for ads (215 files). “Colorful” means HSV saturation ≥ 0.25 and value ≥ 0.15. This measures a difference in sampled appearance, not a design score.

**Production implication:** specify background brightness, main colors, accents and consistency between shots instead of asking only for “motion graphics.” Swatch widths are pixel shares; likes use a separate post denominator. Dark and light motion groups have same-day median likes of 50 and 104, but only 22 posts each. This does not establish a palette that causes more engagement. [Color methods and full atlases](color-modes.md) · [Color vectors](../data/color-study/per-video-color-vectors.csv) · [Mode summary](../data/color-study/color-mode-summary.csv).

## 4. One human prompt can contain substantial design and revision work

Five public briefs contain **172 to 17,664 visible characters**. A short request can call an existing skill, product project or song; a long brief can specify every scene, color and technical constraint. “One prompt” therefore does not describe the full input size.

The later [F1 team example](https://x.com/rubenssoto_ai/status/2108289170871582851) adds another variable. The creator reports one human prompt but explains in a [reply](https://x.com/rubenssoto_ai/status/2108608936295408050) that Opus rejected intermediate results repeatedly. Human prompt count and internal revision count are separate records.

**Production implication:** keep four things together: the human brief, existing assets and systems, internal revisions, and the final acceptance criteria. That makes reuse easier to assess. [Prompt-length chart](../assets/prompt-lengths.svg) · [Five source-linked counts](../data/visible-prompt-lengths.json) · [88-case conditions matrix, Chinese](prompt-matrix.zh-CN.md) · [Seven experimental templates, Chinese](prompt-playbook.zh-CN.md).

## 5. Read task costs together with roles and rework

Two creator comparisons give concrete task-level observations. The Golden Gate example reports $2.19 / $3.04 for Haiku / Opus, **28.0% less** for the former. The fluffy-crab example reports $11.25 / $13.30 for Sonnet / Opus, **15.4% less** for the former. These do not share a common acceptance score and cannot be pooled into a model ranking.

The F1 team reports that the Haiku executor accounted for **89.6% of tokens** and **64.2% of team cost**, with Opus planning and reviewing. Usage share and cost share differ, and repeated review adds work. These are creator-reported figures, without independent billing verification.

**Production implication:** compare the final total cost, time to acceptance and revision count for similar tasks. Record the roles of planning, execution, external services and human work. [Reported costs, calculations and counterexamples](workflow-analysis.md) gives the source posts and context.

The October 11 review adds footage editing, multi-agent assembly and a human-directed 3D workflow. The West Lake promo, Opus-plus-nine-Sonnets article video and nine-day turntable project expose inputs, automated fixes and human decisions within the same production chain. [New analysis and sources](workflow-analysis.md#october-11-automation-within-the-full-production-process).

## Choose the next question

| Question | Read next |
|---|---|
| Find examples for a model or type of work | [Complete source directory](library.md), [content–style atlas](domain-style-atlas.md) |
| Choose tools or a reusable project | [Production resources](production-resources.md), [task-to-route guide](visual-effects-fit.md) |
| Turn an example into a brief | [Prompt matrix, Chinese](prompt-matrix.zh-CN.md), [templates, Chinese](prompt-playbook.zh-CN.md), [production brief](production-brief.md) |
| Recheck a number or its scope | [Frozen statistics](statistics.md), [current collection analysis](collection-analysis.md), [methodology, Chinese](methodology.zh-CN.md) |
| Update sources, statistics and pages | [Maintenance](maintenance.md), [documentation index](README.md) |

This page synthesizes saved data and public disclosures without treating creator claims as independent verification. Nine sampled frames support observations about appearance; continuous motion, sound and factual accuracy require their own complete checks.
