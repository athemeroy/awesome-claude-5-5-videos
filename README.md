# Awesome Claude Opus 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[中文说明](README.zh-CN.md)

A curated, source-linked guide to videos people made **with** Claude Opus 5.5. It focuses on what the model actually did: writing rendering code, directing external models, editing supplied footage, or building an app that someone recorded. This is an independent project, not affiliated with Anthropic or X. We use Hypit to inspect accessible video previews.

## Start here

- **Watch first:** see [our own nine published videos](#videos-we-made) and how we made them.
- **Browse by picture:** open the [168-case visual directory](docs/cases-index.zh-CN.md); every reviewed case has a small frame from its sampled X preview.
- **Explore the grid:** use the [domain × visual-style atlas](docs/domain-style-atlas.md) to compare cell counts and open pictured cases, with dated engagement observations.
- **Compare evidence:** read [14 paired cases](docs/evidence-examples.md) across seven production paths and the [reproducible statistical profile](docs/statistics.md).
- **Find the latest additions:** read [seven cases published after the frozen search cutoff](docs/new-cases-2026-09-27.md).
- **Choose a production route:** use the [visual-effects production guide](docs/visual-effects-fit.md) to match a task with tools, inputs, checks, and likely limits.

## Videos we made

The maintainer [@WangYeruo](https://x.com/WangYeruo) made **eight Thusfar / 页读 product films** in four Chinese–English pairs, plus a [47-second research-summary animation](https://x.com/WangYeruo/status/2103279925960876265). These are first-party examples of the workflows discussed here. The summary video depicts the **September 25 morning** research snapshot; the current counts are below.

<a href="https://x.com/WangYeruo/status/2103279925960876265"><img src="assets/our-videos/opus-world-en.webp" width="440" alt="Frame from our 47-second visual research summary"></a>

*Our 47-second summary animation depicts the September 25 morning snapshot; click for the published X video.*

| Theme | Chinese film | English film | Input and role |
|---|---|---|---|
| Core idea | <a href="https://x.com/WangYeruo/status/2103108551799632050"><img src="assets/our-videos/core-zh.webp" width="170" alt="Chinese Thusfar core-idea film frame"></a> | <a href="https://x.com/WangYeruo/status/2103108551799632050"><img src="assets/our-videos/core-en.webp" width="170" alt="English Thusfar core-idea film frame"></a> | Existing reading-app code and copy → Opus-authored Remotion visuals |
| Features | <a href="https://x.com/WangYeruo/status/2103109243377504468"><img src="assets/our-videos/features-zh.webp" width="170" alt="Chinese Thusfar features film frame"></a> | <a href="https://x.com/WangYeruo/status/2103109243377504468"><img src="assets/our-videos/features-en.webp" width="170" alt="English Thusfar features film frame"></a> | Product features and interface → motion graphics |
| How it works | <a href="https://x.com/WangYeruo/status/2103109979905675371"><img src="assets/our-videos/technology-zh.webp" width="170" alt="Chinese Thusfar technical-explainer film frame"></a> | <a href="https://x.com/WangYeruo/status/2103109979905675371"><img src="assets/our-videos/technology-en.webp" width="170" alt="English Thusfar technical-explainer film frame"></a> | Spoiler-control architecture → explainer graphics |
| Vertical trailer | <a href="https://x.com/WangYeruo/status/2103110282444771733"><img src="assets/our-videos/teaser-zh.webp" width="112" alt="Chinese Thusfar vertical-trailer frame"></a> | <a href="https://x.com/WangYeruo/status/2103110282444771733"><img src="assets/our-videos/teaser-en.webp" width="112" alt="English Thusfar vertical-trailer frame"></a> | Product message → vertical short |

The [production note](https://x.com/WangYeruo/status/2103110282444771733) says Opus 5.5 in Claude Code used the existing app codebase and Remotion for visuals, transitions, music, and effects; Gemini 3.8 Flash TTS supplied narration. The group took three or four rounds of human revisions according to that note. We measured and sampled all eight accessible X preview MP4s, but did not independently audit the original model sessions, project files, or subscription dashboard. The four posts form **one reviewed source case** in the 168-case directory, not eight separate case rows. In the frozen visual classification, four of these known first-party files were labeled `yes` and four `no`—a useful reminder that a classifier label alone cannot settle model involvement.

> **Refresh:** X searches ran through September 26, 2026, 21:05 China Standard Time; this snapshot was reconciled at 21:53. Across 56 recorded queries, 55 succeeded and one query had been rate-limited in an earlier batch. The corpus has 1,511 unique candidate posts, 1,419 with MP4, and 1,449 attachments. Hypit 0.2.3 probed and sampled nine frames from all 1,449; SHA-256 found 1,401 distinct files. We reviewed 168 source-linked cases. Search limits, reposts, and unrelated results mean these numbers are **not** a count of original Opus videos or all of X. See the [search receipts summary](docs/search-coverage.zh-CN.md) and [frozen snapshot](data/corpus-snapshot.json).

![Four common production routes from an Opus request to video pixels](assets/opus55-video-paths.png)

## What people made, and how it looks

> Refresh, Sep 26 2026: a vision model (Gemini 3.8 Flash) classified the nine-frame samples and post text for all 1,401 byte-distinct MP4s. It labeled 980 “yes” and 139 “likely” for Opus involvement. Those 1,119 labels are classifier judgments, not verified authorship; one label per video can also miss mixed domains or styles. The classifier sorts by topic and look. It does **not** predict virality. Data: [`data/domain-style.csv`](data/domain-style.csv). The [published X Article](https://x.com/WangYeruo/article/2103278277536485482) and [47-second video summary](https://x.com/WangYeruo/status/2103279925960876265) preserve their original September 25 morning snapshot.

![Classifier-assigned domain counts for the frozen September 26 file sample, with yes and likely labels shown separately](assets/domain-labels.svg)

The chart counts only the 1,119 files tagged `yes` or `likely`, with one primary domain per file. The largest two main styles are motion graphics / UI (350) and 3D render (324). Explore the full **domain × visual-style matrix** in the [visual atlas](docs/domain-style-atlas.md): every nonempty cell reports its file count, and cells with reviewed examples lead to stills and original posts. Its popularity figures are dated observations, not final engagement or a measure of production quality.

**Classifier-threshold check:** among `yes` files only, ads and launches (191) narrowly exceed games and interactive demos (187). Adding `likely` reverses that order to games (230) and ads (215). The lead depends on the classifier threshold, not a measured change in what people made. The [reproducible statistical profile](docs/statistics.md) shows denominators, durations, and cross-tabs.

One Top result on Western civilization had 42,836 likes when collected. Its 136.5-second MP4 was byte-identical to a later repost captioned as an Opus 5.5 video, while the earlier [post](https://x.com/IterIntellectus/status/2103212539895017864) only says “Claude.” We kept both posts in the candidate corpus but left the video out of the reviewed Opus case index because the original model version is unclear. Engagement is not evidence of authorship.

## Seven production paths, with frames

Each picture links to the creator's original post. These are deliberately chosen examples, not the most common or highest-quality outcomes. The [14 paired evidence cases](docs/evidence-examples.md) show why a similar look can come from different inputs and tools; the [168-case visual directory](docs/cases-index.zh-CN.md) shows one sampled frame for every reviewed case.

| Production path | Watch an example | What to check |
|---|---|---|
| Code-drawn 2D | <a href="https://x.com/hanifproduktif/status/2102742924148830211"><img src="assets/case-thumbnails/2102742924148830211.webp" width="180" alt="Ant colony animation preview"></a><br>[Ant colony and matching source](https://x.com/hanifproduktif/status/2102742924148830211) | Does the public code match the scenes, timing, and assets? |
| Educational explainer | <a href="https://x.com/LinearUncle/status/2103128559174971663"><img src="assets/case-thumbnails/2103128559174971663.webp" width="180" alt="Calculus lesson preview"></a><br>[Manim calculus lesson](https://x.com/LinearUncle/status/2103128559174971663) | Were the facts, formulas, narration, and supplied material checked? |
| 3D or real-time graphics | <a href="https://x.com/Aurelien_Gz/status/2102786378282987591"><img src="assets/case-thumbnails/2102786378282987591.webp" width="180" alt="Clearwater shallow-water preview"></a><br>[Clearwater and WebGL source](https://x.com/Aurelien_Gz/status/2102786378282987591) | Is this a program capture, a rendered scene, or video-model output? |
| Existing-source transformation | <a href="https://x.com/AxtonLiu/status/2102827887732932956"><img src="assets/case-thumbnails/2102827887732932956.webp" width="180" alt="Talking-head line-art remake preview"></a><br>[Talking-head line-art remake](https://x.com/AxtonLiu/status/2102827887732932956) | What did the supplied performance, audio, or product files contribute? |
| External video-model pipeline | <a href="https://x.com/abxxai/status/2102775755646337530"><img src="assets/case-thumbnails/2102775755646337530.webp" width="180" alt="Opus and Seedance video preview"></a><br>[Opus plus Seedance](https://x.com/abxxai/status/2102775755646337530) | Which tool supplied the moving pixels, and what did Opus direct? |
| App or game capture | <a href="https://x.com/masaya_1980/status/2103115017755500561"><img src="assets/case-thumbnails/2103115017755500561.webp" width="180" alt="Can-collection simulation preview"></a><br>[Can-collection simulation](https://x.com/masaya_1980/status/2103115017755500561) | Is the deliverable a playable program, with video as its recording? |
| Mixed or not established | <a href="https://x.com/leogao25/status/2102544078927741369"><img src="assets/case-thumbnails/2102544078927741369.webp" width="180" alt="Split-screen physics comparison preview"></a><br>[Two-model physics comparison](https://x.com/leogao25/status/2102544078927741369) | Are the inputs, budgets, and scoring procedure comparable? |

Anthropic's [Opus 5.5 model description](https://platform.claude.com/docs/en/models/opus-5-5/overview) specifies text and image input with text output. A video can instead come from code it wrote, a program it controlled, existing footage it edited, or another model it directed. A frame alone cannot prove the production path. We distinguish creator disclosures, publicly matching projects or prompts, and direct observations of sampled X previews. The [production guide](docs/visual-effects-fit.md) explains suitable tasks and checks as engineering advice, not measured model success rates.

## Reusable open-source production systems

| Preview and project | What can be reused and what the preview shows |
|---|---|
| <a href="https://lemomo-ai.github.io/lemo-opuscar/"><img src="assets/resource-thumbnails/lemo-opuscar.webp" width="210" alt="Lemo-Opuscar official cover showing a collage of film styles"></a><br>[Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) · [original post](https://x.com/lemomo_ai/status/2103811634565415152) | The official cover previews a [gallery of 39 styles](https://lemomo-ai.github.io/lemo-opuscar/), each with sample films and `STYLE.md` links. The [director guide](https://github.com/lemomo-ai/lemo-opuscar/blob/main/DIRECTOR.md), [technique guide](https://github.com/lemomo-ai/lemo-opuscar/blob/main/TECHNIQUE.md), and [sample scene code](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/crayon-book/demo/film.js) make the brief, storyboard, deterministic frame rendering, shared timing, and sound checks inspectable. The creator says Canvas/WebGL code draws the films without a video-generation model; the repository alone cannot audit every model call or finished film. Its [license](https://github.com/lemomo-ai/lemo-opuscar/blob/main/LICENSE) assigns MIT to code and CC BY 4.0 to guides, style files, and films, subject to third-party asset terms. |
| <a href="https://github.com/francozanardi/papermotion#first-snow-snow"><img src="assets/resource-thumbnails/papermotion.webp" width="210" alt="Snowy paper-cut scene from Papermotion's Opus 5.5 snow film"></a><br>[Papermotion](https://github.com/francozanardi/papermotion) | A reusable paper-cut animation engine with deterministic physics, character rigs, offline rendering, frame grabs, contact sheets, and sound checks. The still comes from its *snow* film, which the README labels Opus 5.5. The README also labels *demo*, *rooftops*, and *sea* Opus 5.5; *light* and *embers* are labeled GPT 6 Astra. Read each sample's model label separately. |
| <a href="https://x.com/servasyy/status/2104039075175182487"><img src="assets/new-case-thumbnails/2104039075175182487.webp" width="210" alt="Character animation by a creator using ClaudeAnimationBase"></a><br>[ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) · [creator example](https://x.com/servasyy/status/2104039075175182487) | A public p5.js and p5.brush animation starter with character expressions, storyboard and contact-sheet steps, and a render workflow. The preview shows @servasyy's personal-story film made with this base; the public starter is reusable input, not the exact source for every shot in the finished film. |
| <a href="https://x.com/makevoid/status/2103869704955900023"><img src="assets/new-case-thumbnails/2103869704955900023.webp" width="210" alt="Motion-graphics music-video preview by makevoid"></a><br>[Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill) · [creator example](https://x.com/makevoid/status/2103869704955900023) | A Claude Code plugin and Ruby toolkit for planning and assembling music-video motion graphics from a supplied song and brief. Its p5.js workflow can call external Fal image, video, and audio models; the preview is a multi-tool creator example, not evidence that Opus supplied all moving pixels. |

These resources were checked on September 27, 2026. The two creator examples above are also described on the [new-case evidence page](docs/new-cases-2026-09-27.md). All four resources sit outside the September 26 frozen corpus and do **not** increase the 1,401-file or 168-case counts. Preview-image provenance and rights are recorded in [THIRD_PARTY.md](THIRD_PARTY.md).

## New since the frozen search cutoff

Seven creator posts published after **September 26, 21:05 China Standard Time** have a separate [dated evidence page](docs/new-cases-2026-09-27.md), each with a sampled-frame preview and a note on what remains unverified. They are **outside** the 1,401-file / 168-case snapshot. Three useful starting points:

| Frame and original post | Why this case matters |
|---|---|
| <a href="https://x.com/JurgenPloeger/status/2104131805175844923"><img src="assets/new-case-thumbnails/2104131805175844923.webp" width="210" alt="Handmade original and Opus remake shown together"></a><br>[Handmade launch film versus code remake](https://x.com/JurgenPloeger/status/2104131805175844923) | The creator supplied the original film and Figma files, then revised the remake's pacing. The comparison makes those inputs visible. |
| <a href="https://x.com/servasyy/status/2104039075175182487"><img src="assets/new-case-thumbnails/2104039075175182487.webp" width="210" alt="Square character in a personal-story animation"></a><br>[Personal story using ClaudeAnimationBase](https://x.com/servasyy/status/2104039075175182487) | A reusable open-source animation base and autobiographical material are part of the production path. |
| <a href="https://x.com/arambarnett/status/2104011150471917838"><img src="assets/new-case-thumbnails/2104011150471917838.webp" width="210" alt="Data-driven motion video with figures and charts"></a><br>[Video with checked data slots](https://x.com/arambarnett/status/2104011150471917838) | The creator describes a guard that prevents the model from inventing on-screen figures; the guard's code is not public. |

The September 25–26 additions remain in the [visual case directory](docs/cases-index.zh-CN.md), with all 168 reviewed original posts and one frame each.

## Dataset and method

The [case index](data/cases.csv) and [field definitions](docs/case-index-guide.zh-CN.md) cover all 168 reviewed examples.

Read the [full Chinese research report](docs/report.zh-CN.md), [Article version](docs/x-article.zh-CN.md), [prompt/workflow matrix](docs/prompt-matrix.zh-CN.md), and [reusable prompt templates](docs/prompt-playbook.zh-CN.md).

The [search coverage](docs/search-coverage.zh-CN.md), [media profile](docs/media-profile.zh-CN.md), [methodology](docs/methodology.zh-CN.md), and [frozen counts](data/corpus-snapshot.json) explain the collection boundaries.

The original X MP4s, raw search results, private paths, and nine-frame contact sheets are **not** distributed here. Small single-frame previews link to the creators' posts and remain the creators' material; they are outside this repository's CC BY license. Case notes distinguish creator disclosures from what Hypit independently observed. Nine sampled frames cannot establish full-motion quality, audio quality, knowledge accuracy, hidden model calls, or the highest-resolution master.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a new original post or reusable production project, improve a source link, or correct a workflow classification. The original annotations, writing, and diagrams in this repository are offered under [CC BY 4.0](LICENSE); the linked X posts, videos, music, creator prompts, and external projects remain with their respective rightsholders. See [THIRD_PARTY.md](THIRD_PARTY.md).
