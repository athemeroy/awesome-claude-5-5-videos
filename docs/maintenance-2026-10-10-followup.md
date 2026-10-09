# October 10 follow-up: workflows, Haiku and more sources

[Home](../README.md) · [Complete directory](library.md) · [中文](maintenance-2026-10-10-followup.zh-CN.md)

Adds **22 source posts**, eight involving Haiku. Eight searches returned 400 rows, all reaching the fifty-row cap; 3 creator threads were also read. Including embedded quotes, this run retains 486 deduplicated candidate IDs.

Queries requested partitioned date windows, but returned timestamp fields place **233 rows** outside those windows. Actual results are retained, without claiming coverage of the requested windows. They remain discovery leads; selected sources were checked against their original post and author disclosures.

[Search / timestamp coverage](../data/claude55-search-coverage-2026-10-10-followup.csv) · [Candidate audit](../data/claude55-candidate-audit-2026-10-10-followup.csv) · [Source ledger](../data/claude55-source-review-2026-10-10-followup.csv)

## Three sampled previews

| Haiku motion design | Sonnet construction visualization | Fable human history |
|:---:|:---:|:---:|
| [<img src="../assets/claude55-2026-10-10-followup/2108089492016103775.jpg" width="240" alt="Motion design with code and Blender">](https://x.com/badboyfoxy/status/2108089492016103775) | [<img src="../assets/claude55-2026-10-10-followup/2107548992640880755.jpg" width="240" alt="Illustrative tower construction">](https://x.com/Solvaix/status/2107548992640880755) | [<img src="../assets/claude55-2026-10-10-followup/2107958931230241037.jpg" width="240" alt="Human history in doodles">](https://x.com/oalanicolas/status/2107958931230241037) |
| 30.059 s | 29.118 s | 88.853 s |

Each preview was probed with ffprobe and inspected through nine sampled frames; all three have audio tracks. The Sonnet post describes a 68-second timeline, while the available recording is about 29 seconds. Other entries are source-only reviews. Full motion, beat accuracy, model calls and original music are not independently verified.

## Added sources

| Original post | Model / production role | Production notes |
|---|---|---|
| [CoLateral promo](https://x.com/nvandewetering/status/2107989438227779883) · @nvandewetering | Haiku 5.5 | Creator reports a promo made with Haiku, with an eight-minute run and 38-cent cost; explicitly says it is not fantastic. |
| [Beijing promo with supplied production constraints](https://x.com/shengtang135754/status/2108549555528872041) · @shengtang135754 | Haiku 5.5 + MiniMax narration + sourced footage | Creator’s brief asks the model to find footage, use MiniMax narration, vary camera angles and synchronize narration with text. |
| [Electric-motor explainer comparison](https://x.com/rubenssoto_ai/status/2107919226728050775) · @rubenssoto_ai | Haiku 5.5 / Sonnet 5.5 | Creator compares two models on the same cinematic 3D electric-motor animation brief; reports 11m13s and 33m03s. |
| [Golden Gate Bridge task-cost comparison](https://x.com/Solomonrojie/status/2108322280094728219) · @Solomonrojie | Haiku 5.5 / Opus 5.5 | Creator compares the same Three.js bridge brief from an empty folder, reporting $2.19 for Haiku and $3.04 for Opus. |
| [Motion design with code and Blender](https://x.com/badboyfoxy/status/2108089492016103775) · @badboyfoxy | Haiku 5.5 | Creator reports asking Haiku to demonstrate motion design, with code and Blender and a 24-minute production run. Samples show title cards, easing curves, orbital forms and vertical light bars. |
| [SVG cycling-pelican comparison](https://x.com/xueyu1125/status/2108082476975554587) · @xueyu1125 | Haiku 5.5 / GPT-6 Luna | Creator compares a cycling-pelican SVG/H5 animation using Haiku in OpenCode and Luna in Codex; the harnesses differ. |
| [Night-train counterexample](https://x.com/EnvolDev/status/2107973447230091623) · @EnvolDev | Haiku 5.5 / GPT-6 Luna | Creator prefers Luna on their night-train test and reports lower time and expense than Haiku; included alongside favorable Haiku examples. |
| [F1 pit-stop orchestrator and executor comparison](https://x.com/rubenssoto_ai/status/2108289170871582851) · @rubenssoto_ai | Opus 5.5 + Haiku 5.5 / GPT models | Creator assigns Opus to orchestration and Haiku to execution for a procedural Three.js pit stop, and compares a Sol/Luna team. |
| [Understory: procedural-art action RPG](https://x.com/DannyLimanseta/status/2107505970809336071) · @DannyLimanseta | Sonnet 5.5 | Creator reports a Three.js action/puzzle RPG across five biomes, with procedural 2D art, several days of work and human handholding. |
| [Slow Me Down](https://x.com/kevin_t_ngo/status/2106864721525915941) · @kevin_t_ngo | Sonnet 5.5 | Creator attributes a short film about a father deliberately losing a game to his daughter to Sonnet, using real Claude Code sessions. |
| [Illustrative tower construction](https://x.com/Solvaix/status/2107548992640880755) · @Solvaix | Sonnet 5.5 | Creator describes a single-HTML 40-floor construction sequence and explicitly says the sequence is invented and geometry simplified, without engineering calculations. Samples show successive tower stages and changing crane positions. The accessible recording is 29.118s, whereas the post describes a 68s timeline. |
| [Fluffy-crab same-prompt comparison](https://x.com/vib3coded/status/2108190478889824662) · @vib3coded | Opus 5.5 / Sonnet 5.5 | Creator compares two crab scenes under one prompt and reports costs of $13.30 and $11.25. |
| [Classic stick fight](https://x.com/AndrewOnXYZ/status/2107262468502544435) · @AndrewOnXYZ | Reported Fable 5.5 | Creator reports asking Fable for a classic stick-fight animation. |
| [Balatro × League of Legends](https://x.com/Vince__Russell/status/2107315127292952696) · @Vince__Russell | Reported Fable 5.5 | Creator describes a Three.js game on Tesana with poker hands mapped to champion kills and multipliers. |
| [Human history in doodles](https://x.com/oalanicolas/status/2107958931230241037) · @oalanicolas | Reported Fable 5.5 | Creator describes sixteen eras in an 88-second film, with art techniques and music changing by era. Samples show a recurring drawn character across framed era panels, changing from paper/ink to pixel-game treatments. |
| [Reference-led recreation with a skill](https://x.com/notdwd/status/2107816799840690589) · @notdwd | Reported Fable 5.5 | Creator supplied a skill and brief. Their public reply specifies portrait/hand footage, Pexels defaults, a music track, paper texture and frame-level timing for a mixed-media film. |
| [Half a blanket across the miles](https://x.com/Vallabh469/status/2108494077389926611) · @Vallabh469 | Opus 5.5 | Creator supplied the concept, narrative and character sheets; attributes split-screen composition, character animation and sound design to Opus. |
| [Audio- and motion-reactive compositing](https://x.com/aicreataro/status/2108091976574988390) · @aicreataro | Opus 5.5 + Blender + MiniMax + Midjourney | Creator specifies MiniMax H3 people, Midjourney key art and MiniMax music, with Blender/Python depth, particles and camera moves responding to sound and motion. |
| [Reference-character scene with Higgsfield](https://x.com/luqmanedits/status/2108476552057172312) · @luqmanedits | Opus 5.5 + Higgsfield | Creator attributes a scene to Opus plus Higgsfield and explicitly names character sheets, location and final animation as Higgsfield inputs/outputs. |
| [Model-themed video with human narration](https://x.com/dorszafranski/status/2108493804068118778) · @dorszafranski | Opus 5.5 + creator voice | Creator attributes a Mistral-themed video to Opus and explicitly says the voice is their own. |
| [Launch film after several iterations](https://x.com/_MasterMal/status/2108471807372325100) · @_MasterMal | Opus 5.5 | Creator reports making a launch film for usevano with Opus after several iterations. |
| [Data-led football-goal reconstruction](https://x.com/lv_feng47448/status/2108397996740432136) · @lv_feng47448 | Opus 5.5 + Blender + data + mocap | Creator reports StatsBomb 360 positions, simulated ball physics and motion capture, with Blender rendering; notes rough-looking players. |

## Read next

[Workflow analysis](workflow-analysis.md) examines inputs, code rendering versus media editing, model roles, revision rounds and cost units. [Collection analysis](collection-analysis.md) computes model-label coverage, sampling and account concentration. [The unified directory](library.md) merges every dated batch.
