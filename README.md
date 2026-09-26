# Awesome Claude Opus 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[中文说明](README.zh-CN.md)

A curated, source-linked guide to videos people made **with** Claude Opus 5.5. It focuses on what the model actually did: writing rendering code, directing external models, editing supplied footage, or building an app that someone recorded. This is an independent project, not affiliated with Anthropic, X, Hypit, or the Awesome directory.

> **Refresh:** X searches ran through September 26, 2026, 21:05 China Standard Time; this snapshot was reconciled at 21:53. Across 56 recorded queries, 55 succeeded and one query had been rate-limited in an earlier batch. The corpus has 1,511 unique candidate posts, 1,419 with MP4, and 1,449 attachments. Hypit 0.2.3 probed and sampled nine frames from all 1,449; SHA-256 found 1,401 distinct files. We reviewed 168 source-linked cases. Search limits, reposts, and unrelated results mean these numbers are **not** a count of original Opus videos or all of X. See the [search receipts summary](docs/search-coverage.zh-CN.md) and [frozen snapshot](data/corpus-snapshot.json).

![Four common production routes from an Opus request to video pixels](assets/opus55-video-paths.png)

## What people made, and how it looks

> Refresh, Sep 26 2026: a vision model (Gemini 3.8 Flash) classified the nine-frame samples and post text for all 1,401 byte-distinct MP4s. It labeled 980 “yes” and 139 “likely” for Opus involvement. Those 1,119 labels are classifier judgments, not verified authorship; one label per video can also miss mixed domains or styles. The classifier sorts by topic and look. It does **not** predict virality. Data: [`data/domain-style.csv`](data/domain-style.csv). The [published X Article](https://x.com/WangYeruo/article/2103278277536485482) and [47-second video summary](https://x.com/WangYeruo/status/2103279925960876265) preserve their original September 25 morning snapshot.

![Jars of videos by domain](assets/domains-jars.png)

The counts below cover only the 1,119 files labeled “yes” or “likely” for Opus involvement; each file contributes one primary domain and style.

| Domain | Videos | Example |
|---|---:|---|
| Games & interactive demos | 230 | [@MengTo, Japanese canal boat ride](https://x.com/MengTo/status/2102760783344189761) · [@JaydenDavisNC, Splatoon gameplay](https://x.com/JaydenDavisNC/status/2103357848961036304) |
| Ads & launches | 215 | [@deedydas, startup launch video](https://x.com/deedydas/status/2102787937482252537) · [@shushant_l, motion-ad skill video](https://x.com/shushant_l/status/2103829449359966629) |
| AI about AI | 201 | [@kevin_t_ngo, a girl asks Claude what it loves](https://x.com/kevin_t_ngo/status/2102437977435893771) |
| Explainers | 147 | [@RyanSael, camera focus lab](https://x.com/RyanSael/status/2102591147927654847) · [@dotey, Transformer explainer](https://x.com/dotey/status/2103683057689522564) |
| Short stories | 112 | [@AndrewOnXYZ, Mars rover short](https://x.com/AndrewOnXYZ/status/2102512879258009818) |
| Music videos | 77 | [@other__reality](https://x.com/other__reality/status/2102514581684052169) |
| History & culture | 49 | [@paji_a, Sekigahara 3D map](https://x.com/paji_a/status/2102581158487945540) |
| Art | 42 | [@majidmanzarpour, pixel wizard](https://x.com/majidmanzarpour/status/2102476258948927543) · [@AxtonLiu, living rice paper](https://x.com/AxtonLiu/status/2103288413969621231) |
| Humor, data viz & other | 46 | |

Styles: motion graphics / UI 350 · 3D 324 · flat cartoon 162 · pixel art 58 · hand-drawn 52 · paper cut-out 39 · ink, sand & paint 37 · generative 23 · anime 21 · math diagrams 21 · photoreal 17 · live action 11 · retro terminal / ASCII 4. Motion graphics surged past 3D rendering to become the #1 most prevalent visual style, driven by the explosion of SaaS product ads, skill-generated showreels, and UI animations.

One Top result on Western civilization had 42,836 likes when collected. Its 136.5-second MP4 was byte-identical to a later repost captioned as an Opus 5.5 video, while the earlier [post](https://x.com/IterIntellectus/status/2103212539895017864) only says “Claude.” We kept both posts in the candidate corpus but left the video out of the reviewed Opus case index because the original model version is unclear. Engagement is not evidence of authorship.

## Contents

- [What people made, and how it looks](#what-people-made-and-how-it-looks)
- [How to read the list](#how-to-read-the-list)
- [Code-drawn 2D and motion graphics](#code-drawn-2d-and-motion-graphics)
- [Educational explainers](#educational-explainers)
- [3D and real-time graphics](#3d-and-real-time-graphics)
- [Existing footage, audio, or project transformation](#existing-footage-audio-or-project-transformation)
- [External video-model pipelines](#external-video-model-pipelines)
- [Apps and games shown through capture](#apps-and-games-shown-through-capture)
- [New cases from the September 26 refresh](#new-cases-from-the-september-26-refresh)
- [New cases from the September 25 refresh](#new-cases-from-the-september-25-refresh)
- [Dataset and method](#dataset-and-method)
- [Contributing and license](#contributing-and-license)

## How to read the list

Anthropic's [Opus 5.5 model description](https://platform.claude.com/docs/en/models/opus-5-5/overview) specifies text and image input with text output. An MP4 can come from code the model wrote, a program it controlled, source material it edited, or another video model it called. Each entry links to the original X post. The evidence labels below describe what is public, **not** a rating of artistic quality:

**Code matched:** A creator-linked public project has scenes, text, timing, or output corresponding to the sampled X video. This still does not reveal the full Claude conversation.
**Prompt shown:** A creator published a prompt or a detailed workflow. A request to call a service does not prove that it was called.
**Creator account:** The workflow comes from the creator's post or reply; our independent observation is limited to the accessible MP4 and nine sampled frames.

This home page deliberately selects examples with distinct production paths. The 168-case audit table includes comparisons and less certain cases and should not be interpreted as a prevalence survey.

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

## New cases from the September 26 refresh

| Case | What the creator reports and what the X preview shows |
|---|---|
| [15-second résumé reel - @stephanlivera](https://x.com/stephanlivera/status/2103315922098470926) | Viral resume-style motion design reel (14k+ likes) demonstrating the brief contagion behind identical 15-second showreels. |
| [Deconstructed motion workflow - @rexan_wong](https://x.com/rexan_wong/status/2103707054108299437) | Detailed 6-stage engineering and directorial pipeline (reference video, HyperFrames/Remotion, 21st.dev UI components, storyboard approvals, director notes) deconstructing the "one-prompt" myth. |
| [Four-tool multimodal animation - @sankakuten91256](https://x.com/sankakuten91256/status/2103483923783373039) | Multimodal pipeline orchestrating GPT Images (frames), Grok (green screen dance video), Opus 5.5 (motion graphics background/code), and Astra (audio replacement). |
| [Runway MCP documentary - @gavinpurcell](https://x.com/gavinpurcell/status/2103304514329854102) | Claude Agent (Fig) hooked to Runway MCP to script, prompt, and direct a 5-minute Netflix-style documentary, using Opus as an agentic coordinator for external diffusion models. |
| [Splatoon gameplay capture - @JaydenDavisNC](https://x.com/JaydenDavisNC/status/2103357848961036304) | A playable browser game written from scratch by Opus 5.5, captured during live gameplay; illustrates the app/game capture production route. |
| [Living rice paper ink wash - @AxtonLiu](https://x.com/AxtonLiu/status/2103288413969621231) | Open-ended creative brief rendered as progressive procedural stroke-by-stroke Canvas Chinese painting; highlights the aesthetic ceiling of 2D code art. |
| [motion-ad skill product spot - @shushant_l](https://x.com/shushant_l/status/2103829449359966629) | 15-second commercial motion ad produced via Danny Postma's portable Claude Code `motion-ad` skill, demonstrating the shift from ad-hoc prompts to packaged tools. |
| [Transformer explainer - @dotey](https://x.com/dotey/status/2103683057689522564) | 12-minute technical deep-dive into Transformer attention mechanisms produced with Claude Code and web toolchain capabilities. |

## New cases from the September 25 refresh

| Case | What the creator reports and what the X preview shows |
|---|---|
| [15-second résumé reel - @ajith_io](https://x.com/ajith_io/status/2103449416325890146) | The post includes the short “show me your motion design” prompt. Hypit sampled a 15.1-second graphic reel; no source project was published. Similar prompt variants appeared in the same search window. |
| [Mid-Autumn cutout collage - @NFT_Chen](https://x.com/NFT_Chen/status/2103380404791333144) | The creator says they supplied a script and song, generated background and paper textures with Nano Banana Pro, animated them using JavaScript / p5.js / p5.brush, and synthesized effects in Node. The 39.3-second preview shows a cat trying to fill a gap in the moon. |
| [Post-human robot story - @Hesamation](https://x.com/Hesamation/status/2103457566978162901) | The creator attributes the story, animation, sound effects, and music to Opus 5.5 and says the video was coded in JavaScript. The 87.6-second X preview shows a robot moving through an empty city. Audio and source code were not independently checked. |
| [Watercolor-style short - @mablesjoseph](https://x.com/mablesjoseph/status/2103465246014746943) | The creator says the 45-second animation uses code-drawn brushstrokes and sound, but explicitly says it was not a one-shot: 163 model calls and about 6¾ hours elapsed. The usage and cost figures are self-reported. |
| [White Russian recipe animation - @Sarut0biSasuke](https://x.com/Sarut0biSasuke/status/2103418429248069973) | A published prompt and hand-drawn reference led, according to the creator, to a single HTML / SVG / JavaScript animation in about 25 minutes. Hypit measured a 30-second X preview; the claimed 1080p master was not available for inspection. |
| [Arabic-dubbed anime pilot - @sbalhatlani](https://x.com/sbalhatlani/status/2103475507471806929) | The creator reports an 8:33 episode built with Claude Code, 211 planned shots, more than 300 generated images, 11 characters, 70 Arabic voice lines, and 16 music cues. Hypit measured 513.3 seconds; production counts and audio quality remain creator claims. |
| [Claude Code session recap - @shneural](https://x.com/shneural/status/2103472385563459833) | The creator says Opus turned its coding session into a 56.3-second video, using a Python engine, Blender, music, and 900 rendered frames. The post reports 92 minutes and $81 at API list prices; the logs and bill were not published. |
| [Jev + Opus live visualizer - @TheViableEdge](https://x.com/TheViableEdge/status/2103494684374900862) | The creator says Opus 5.5 and Jev built a live visualizer for charts, effects, and themes, with possible use as a social-video overlay. The 56.5-second clip is a tool demo; the post does not show a finished short or explain Jev's exact role. |

## Dataset and method

The [case index](data/cases.csv) and [field definitions](docs/case-index-guide.zh-CN.md) cover all 168 reviewed examples.

Read the [full Chinese research report](docs/report.zh-CN.md), [Article version](docs/x-article.zh-CN.md), [prompt/workflow matrix](docs/prompt-matrix.zh-CN.md), and [reusable prompt templates](docs/prompt-playbook.zh-CN.md).

The [search coverage](docs/search-coverage.zh-CN.md), [media profile](docs/media-profile.zh-CN.md), [methodology](docs/methodology.zh-CN.md), and [frozen counts](data/corpus-snapshot.json) explain the collection boundaries.

The original X MP4s, raw search results, private paths, and individual contact sheets are **not** distributed here. The public table links to creators and distinguishes their disclosures from what Hypit independently observed. Nine sampled frames cannot establish full-motion quality, audio quality, knowledge accuracy, hidden model calls, or the highest-resolution master.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) to propose a new original post, improve a source link, or correct a workflow classification. The original annotations, writing, and diagrams in this repository are offered under [CC BY 4.0](LICENSE); the linked X posts, videos, music, creator prompts, and external projects remain with their respective rightsholders. See [THIRD_PARTY.md](THIRD_PARTY.md).
