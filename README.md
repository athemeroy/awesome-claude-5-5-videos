# Awesome Claude Opus 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[中文说明](README.zh-CN.md)

A curated, source-linked guide to videos people made **with** Claude Opus 5.5. It focuses on what the model actually did: writing rendering code, directing external models, editing supplied footage, or building an app that someone recorded. This is an independent project, not affiliated with Anthropic, X, Hypit, or the Awesome directory.

> **Snapshot:** September 25, 2026, 06:22 China Standard Time. We searched 43 X query windows, saved 1,104 unique candidate posts, and used Hypit 0.2.3 to probe and sample nine frames from each of 1,044 accessible MP4 attachments. We reviewed 152 cases against creator posts, replies, prompts, or source code. Search limits, reposts, and unrelated results mean these numbers are **not** a count of original Opus videos or all of X.

![Four common production routes from an Opus request to video pixels](assets/opus55-video-paths.png)

## What people made, and how it looks

> Update, Sep 25 2026: we labeled every distinct accessible video (1,008 after removing duplicates) by domain and visual style. A vision model (Gemini 3.8 Flash) read each video's nine sampled frames plus the post text; we spot-checked a random sample. 786 were judged to be made by the poster with Opus 5.5. Single labels can be wrong (we already know of one missed case). Data: [`data/domain-style.csv`](data/domain-style.csv). Write-up: [X Article (Chinese)](https://x.com/WangYeruo/article/2103278277536485482) · [47-second video summary](https://x.com/WangYeruo/status/2103279925960876265).

![Jars of videos by domain](assets/domains-jars.png)

| Domain | Videos | Example |
|---|---:|---|
| Games & interactive demos | 184 | [@MengTo, Japanese canal boat ride](https://x.com/MengTo/status/2102760783344189761) |
| AI about AI | 153 | [@kevin_t_ngo, a girl asks Claude what it loves](https://x.com/kevin_t_ngo/status/2102437977435893771) |
| Ads & launches | 119 | [@deedydas, startup launch video](https://x.com/deedydas/status/2102787937482252537) |
| Explainers | 99 | [@RyanSael, camera focus lab](https://x.com/RyanSael/status/2102591147927654847) |
| Short stories | 85 | [@AndrewOnXYZ, Mars rover short](https://x.com/AndrewOnXYZ/status/2102512879258009818) |
| Music videos | 59 | [@other__reality](https://x.com/other__reality/status/2102514581684052169) |
| Art | 33 | [@majidmanzarpour, pixel wizard](https://x.com/majidmanzarpour/status/2102476258948927543) |
| History & culture | 28 | [@paji_a, Sekigahara 3D map](https://x.com/paji_a/status/2102581158487945540) |
| Other (memes, data viz, misc.) | 26 | |

Styles: 3D 270 · motion graphics / UI 178 · flat cartoon 131 · pixel art 50 · hand-drawn 34 · ink, sand & paint 29 · paper cut-out 29 · generative 17 · math diagrams 14 · photoreal 14 · anime 12. Games are mostly 3D; ads and explainers lean on motion graphics; stories and music videos favor flat cartoons.

## Contents

- [What people made, and how it looks](#what-people-made-and-how-it-looks)
- [How to read the list](#how-to-read-the-list)
- [Code-drawn 2D and motion graphics](#code-drawn-2d-and-motion-graphics)
- [Educational explainers](#educational-explainers)
- [3D and real-time graphics](#3d-and-real-time-graphics)
- [Existing footage, audio, or project transformation](#existing-footage-audio-or-project-transformation)
- [External video-model pipelines](#external-video-model-pipelines)
- [Apps and games shown through capture](#apps-and-games-shown-through-capture)
- [Dataset and method](#dataset-and-method)
- [Contributing and license](#contributing-and-license)

## How to read the list

Anthropic's [Opus 5.5 model description](https://platform.claude.com/docs/en/models/opus-5-5/overview) specifies text and image input with text output. An MP4 can come from code the model wrote, a program it controlled, source material it edited, or another video model it called. Each entry links to the original X post. The evidence labels below describe what is public, **not** a rating of artistic quality:

**Code matched:** A creator-linked public project has scenes, text, timing, or output corresponding to the sampled X video. This still does not reveal the full Claude conversation.
**Prompt shown:** A creator published a prompt or a detailed workflow. A request to call a service does not prove that it was called.
**Creator account:** The workflow comes from the creator's post or reply; our independent observation is limited to the accessible MP4 and nine sampled frames.

This home page deliberately selects examples with distinct production paths. The 152-case audit table includes comparisons and less certain cases and should not be interpreted as a prevalence survey.

## Code-drawn 2D and motion graphics

- [Ant colony - @hanifproduktif](https://x.com/hanifproduktif/status/2102742924148830211) - A 32-second animation with a [matching Node Canvas source project](https://github.com/buildwithhanif/claude-animation-skill), character rig, frame checks, and FFmpeg workflow. **Code matched.**
- [Shaml paper-lightbox scene - @makwired](https://x.com/makwired/status/2103008945220567166) - The [matching project](https://github.com/klsoen/opus-js-animations) documents code-drawn frames, a pre-existing spoken-word recording, and several human revisions. **Code matched.**
- [Pixel platformer - @riku720720](https://x.com/riku720720/status/2102515055116063144) - A single-HTML Canvas animation guided by a [detailed 160×90 pixel, palette, and timing specification](https://x.com/riku720720/status/2102515058010132554). **Prompt shown.**
- [39-scene Clawd music video - @Aadidev0](https://x.com/Aadidev0/status/2102692569792835994) - The [creator's production account](https://x.com/Aadidev0/status/2102693243662024855) describes a reference repository, Canvas scenes, browser frame rendering, Node audio, and FFmpeg; the measured 164-second MP4 fits the stated 3,936 frames at 24 fps. **Creator account.**
- [Anime battle trailer - @ishuagra02](https://x.com/ishuagra02/status/2103247844542922825) - A [short public creative brief](https://x.com/ishuagra02/status/2103247960272433307) led to a 100.8-second accessible MP4. JavaScript frame generation, cost, and run time remain creator claims without published source or billing logs. **Prompt shown.**

## Educational explainers

- [Calculus lesson - @LinearUncle](https://x.com/LinearUncle/status/2103128559174971663) - The creator names Manim for visuals and edge-tts for narration. Subject accuracy and pronunciation require separate review. **Creator account.**
- [Six-minute English lesson - @0x0funky](https://x.com/0x0funky/status/2102736587708854585) - A lesson built from prepared course content with Remotion, React/SVG, and local CosyVoice according to the creator's reply. **Creator account.**
- [VAE explainer - @ng169onX](https://x.com/ng169onX/status/2103183904563998809) - A 334.5-second sampled MP4 with formulas and diagrams; the claimed MNIST training and Qwen3-TTS voice work need separate verification. **Creator account.**

## 3D and real-time graphics

- [Clearwater - @Aurelien_Gz](https://x.com/Aurelien_Gz/status/2102786378282987591) - Photographic-looking shallow water whose [public WebGL2 project](https://github.com/Aureliengmz/clearwater) documents waves, refraction, and caustics. The X video is a real-time graphics capture. **Code matched.**
- [Pelican bicycle scene - @AxtonLiu](https://x.com/AxtonLiu/status/2103119648271290566) - A 38.059-second file consistent with the creator's 1,140-frame/30-fps account; the ray-marching and zero-external-asset claims have no public source attached. **Creator account.**
- [Architectural exploded view - @zdkiel_labs](https://x.com/zdkiel_labs/status/2102722754172850310) - Started from one supplied image, then involved [six human answers and a Blender bridge](https://x.com/zdkiel_labs/status/2102724195549659613) according to the creator. **Creator account.**

## Existing footage, audio, or project transformation

- [Talking-head line-art remake - @AxtonLiu](https://x.com/AxtonLiu/status/2102827887732932956) - The request supplied an 83-second human performance and kept its audio, captions, and duration while redrawing the main image. **Prompt shown.**
- [Thirteen-take talking-head edit - @gregpr07](https://x.com/gregpr07/status/2102984873351037161) - The creator says Opus and video-use selected and edited supplied takes; the 18-second result visibly includes the speaker and a candidate-take grid. **Creator account.**
- [Twelve-hour music-video commission - @donaldjewkes](https://x.com/donaldjewkes/status/2102801274173587569) - The [roughly 9,500-character public prompt](https://x.com/donaldjewkes/status/2102801469976248500) supplied a video, song, code, and project files and requested several possible services. It proves the brief's inputs, not every hidden tool call. **Prompt shown.**
- [Session-story skill - @jake11moran](https://x.com/jake11moran/status/2103247490237825416) - A short trigger reportedly uses a prepared HyperFrames skill and local Claude Code history as story material; the sampled X MP4 runs 52.7 seconds. **Creator account.**

## External video-model pipelines

- [Opus plus Seedance - @abxxai](https://x.com/abxxai/status/2102775755646337530) - The creator explicitly assigns Opus and Seedance 2.5 separate roles. **Creator account.**
- [Infinite-zoom collage - @koldo2k](https://x.com/koldo2k/status/2103129343253778767) - The [full public brief](https://x.com/koldo2k/status/2103129347791986942) assigns scenery, cutouts, animated figures, and music to several external models while Opus coordinates shots and transitions. **Prompt shown.**
- [Blender blocking into Seedance - @OriSilver](https://x.com/OriSilver/status/2102817977812824335) - The split-screen post pairs low-poly camera blocking with final-looking shots; the creator describes Blender as a control draft for Seedance. **Creator account.**

## Apps and games shown through capture

- [Can-collection simulation - @masaya_1980](https://x.com/masaya_1980/status/2103115017755500561) - A [live browser demo](https://www.kakeru-d.jp/lab/akikan/) and [making-of post](https://www.kakeru-d.jp/blog/claude-animation-akikan/) show a program, human design approval, revisions, and frame export. **Public project and creator account.**
- [Interactive island - @Acemation_](https://x.com/Acemation_/status/2103150350211354966) - A captured navigable environment rather than a finished linear film; costs and development time are creator reports. **Creator account.**
- [Game demonstration - @NiloTechInc](https://x.com/NiloTechInc/status/2102741813719138661) - The creator credits human-made character, animation, and clothing assets alongside Opus-assisted game development. **Creator account.**

## Dataset and method

The [case index](data/cases.csv) and [field definitions](docs/case-index-guide.zh-CN.md) cover all 152 reviewed examples.

Read the [full Chinese research report](docs/report.zh-CN.md), [Article version](docs/x-article.zh-CN.md), [prompt/workflow matrix](docs/prompt-matrix.zh-CN.md), and [reusable prompt templates](docs/prompt-playbook.zh-CN.md).

The [search coverage](docs/search-coverage.zh-CN.md), [media profile](docs/media-profile.zh-CN.md), [methodology](docs/methodology.zh-CN.md), and [frozen counts](data/corpus-snapshot.json) explain the collection boundaries.

The original X MP4s, raw search results, private paths, and individual contact sheets are **not** distributed here. The public table links to creators and distinguishes their disclosures from what Hypit independently observed. Nine sampled frames cannot establish full-motion quality, audio quality, knowledge accuracy, hidden model calls, or the highest-resolution master.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a new original post, improve a source link, or correct a workflow classification. The original annotations, writing, and diagrams in this repository are offered under [CC BY 4.0](LICENSE); the linked X posts, videos, music, creator prompts, and external projects remain with their respective rightsholders. See [THIRD_PARTY.md](THIRD_PARTY.md).
