# October 10: maintenance and recent source review

[Home](../README.md) · [中文](maintenance-2026-10-10.zh-CN.md)

This run attempted 6 searches; 6 succeeded, returning 300 rows, with 6 hitting the 50-row cap. Deduplication including embedded quotes retains 344 candidate IDs. We selected 18 new source posts. Two Haiku previews were probed and reviewed through nine sampled frames each; the remaining entries are source-only.

Queries start October 3. Latest ordering and result caps do not cover the whole window. Candidates include reposts, marketing and jokes; exclusion does not mean a post is false. Model identity, costs and one-shot claims are creator reports. An explainer video does not validate its scientific claims.

[Search coverage](../data/claude55-search-coverage-2026-10-10.csv) · [Candidate audit](../data/claude55-candidate-audit-2026-10-10.csv) · [Source ledger](../data/claude55-source-review-2026-10-10.csv)

## Added sources

| Original post | Reported model | Production notes |
|---|---|---|
| [Ink animation with synthesized sound](https://x.com/gkxspace/status/2108506384711213108) · @gkxspace | Opus 5.5 | Creator describes paper fibers, brush bristles, character skeletons and Python-synthesized guqin/flute sounds. |
| [A 2000s Flash-style animation](https://x.com/YanqingCheng/status/2108296567166042404) · @YanqingCheng | Reported Fable 5.5 | Creator requested a nostalgic Flash-style animation. |
| [JavaScript animation with wind-responsive IK](https://x.com/adam_fresko/status/2107637770873417894) · @adam_fresko | Reported Fable 5.5 | Creator reports JavaScript-only animation with inverse kinematics reacting to wind, and notes remaining text errors. |
| [Game demo with purchased assets](https://x.com/Rush3rx/status/2108607656776876368) · @Rush3rx | Opus 5.5 + Tripo P2 | Creator reports about twenty prompts over two days, Tripo P2 and previously purchased assets. |
| [Comparing explainer production tools](https://x.com/avthar/status/2108603075174797490) · @avthar | Opus 5.5 + ElevenLabs | Creator tests HyperFrames, Remotion and Manim with ElevenLabs narration and says the video contains prompts and results. |
| [Taxtello launch film, fifth revision](https://x.com/daniel_haida/status/2108595684236755242) · @daniel_haida | Opus 5.5 | Creator reports Canvas frames, NumPy-synthesized sound, five versions and a separate critic agent. |
| [Browser kart racing and an edited recording](https://x.com/cafunify/status/2108581004432830683) · @cafunify | Opus 5.5 + Sonnet 5.5 | Creator reports a Three.js kart game made mainly with Sonnet, plus Sonnet playing, recording and editing its trailer. |
| [Three-prompt motion graphics comparison](https://x.com/mmmarcus_ai/status/2108550192882503797) · @mmmarcus_ai | Opus 5.5 / Sonnet 5.5 | Creator presents claymation, a hot-sauce ad and an app launch in A/B pairs followed by model reveals. |
| [Drawing the Temple of Heaven in Three.js](https://x.com/shunshu32385143/status/2108480534254944719) · @shunshu32385143 | Opus 5.5 | Creator describes staged line drawing and coloring in Three.js, with a code-synthesized guzheng score. |
| [A 3D pedal-stress explainer](https://x.com/chang_/status/2108458503367200908) · @chang_ | Opus 5.5 + ElevenLabs | Creator describes a five-minute Three.js pedal assembly, shader stress maps, fracture animation and bilingual captions with ElevenLabs narration. |
| [Product folder plus a reference video](https://x.com/zhongerxin/status/2108532720414699696) · @zhongerxin | Opus 5.5 | Creator supplied a project folder and a reference-video URL, reports one revision, and notes rough details and typography. |

## Two sampled Haiku previews

| 5–7–5 self-introduction | 3D cycling pelican |
|:---:|:---:|
| [<img src="../assets/haiku-2026-10-10/2107985954648867292.jpg" width="300" alt="Samples show FAST, LIGHT and SHARP chapters, changing dark/light palettes and large 5/7 numerals.">](https://x.com/lemomo_ai/status/2107985954648867292) | [<img src="../assets/haiku-2026-10-10/2108156768023118268.jpg" width="300" alt="Samples show a pelican cycling beside water, with recurring bicycle, bird and moving camera positions.">](https://x.com/xueyu1125/status/2108156768023118268) |
| 40.054 s; audio track present | 12.000 s; audio track present |

The samples show different tasks: the first organizes chapters through typography, graphics and palette changes; the second keeps a recurring bird and bicycle while changing camera position. Nine frames cannot assess continuous motion or beat accuracy. Reported generation time is production time, not preview length.

[Frame provenance](../assets/haiku-2026-10-10/frames.csv) · [Rights](../THIRD_PARTY.md)

## Haiku videos and comparisons

| Original post | Reported model | Production notes |
|---|---|---|
| [A self-introduction built around 5–7–5](https://x.com/lemomo_ai/status/2107985954648867292) · @lemomo_ai | Haiku 5.5 | Creator describes a self-introduction organized into 5–7–5 musical sections, with matching indicator lights. |
| [Dōtei: a short poetry animation](https://x.com/tatsuyer/status/2108033626017587627) · @tatsuyer | Haiku 5.5 | Creator attributes a 6.5-second animation inspired by Takamura Kōtarō’s Dōtei to Haiku, using chat only. |
| [A 3D pelican riding a bicycle](https://x.com/xueyu1125/status/2108156768023118268) · @xueyu1125 | Haiku 5.5 | Creator reports Haiku downloading Blender and using FFmpeg to produce a 3D cycling-pelican MP4. |
| [A Haiku launch animation](https://x.com/leo114119/status/2108033133002227738) · @leo114119 | Haiku 5.5 | Creator reports asking Haiku to make its own launch animation, and describes weaker creativity than their Fable result. |
| [A creator’s video edit](https://x.com/pruthvithinks/status/2108594104133423276) · @pruthvithinks | Haiku 5.5 | Creator attributes the edit to Haiku and reports a cost of 88 cents. |
| [Three.js snow-globe comparison](https://x.com/buildwithrajath/status/2108571974222197055) · @buildwithrajath | Haiku 5.5 / GPT-6 Luna | Creator compares a Three.js snow globe under the same prompt and high effort; times and costs are self-reported. |
| [CSS origami animation comparison](https://x.com/UgoBit_/status/2107953568993141074) · @UgoBit_ | Haiku 5.5 / Sonnet 5.5 / GPT models | Creator compares four models on the same 3D CSS origami prompt with Medium thinking. |

## README changes

Both home pages now organize navigation, selected works, production routes, collection totals and dated updates. Existing charts and analysis remain in [snapshot analysis](snapshot-analysis.md); full production and resource notes remain in [production resources](production-resources.md). September 26 file statistics retain their date and denominators.

Organization references:

- [sindresorhus/awesome](https://github.com/sindresorhus/awesome) — category navigation.
- [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) — concise entries and separate discovery/archive pages.
- [enaqx/awesome-react](https://github.com/enaqx/awesome-react) — grouped reusable resources.
