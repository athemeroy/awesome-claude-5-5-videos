# Claude 5.5 demos and reported next-Fable testing

[中文](claude55-update-2026-10-02.zh-CN.md) · [Home](../README.md) · Checked October 2, 2026, China Standard Time

**Decision: expand the collection to Awesome Claude 5.5 Videos.** Sonnet 5.5 has distinct creator examples, and October 1–2 X posts include demos and comparisons that several creators attribute to Fable 5.5. Those sources are useful with explicit model uncertainty.

Here, Fable 5.5 means **a creator-reported version, often inferred from suspected routing behind Fable 5.1**. The official release pages we checked do not confirm that version; this does not rule out private testing. We have not verified the backend model ID. A real source post, an accessible demo, and confirmed model identity are separate findings.

## What do creators think improves over Opus 5.5?

| Dimension | Most direct source | Supported reading and limitation |
|---|---|---|
| Visual hierarchy and focus | [@mesmerlord's same-prompt motion comparison](https://x.com/mesmerlord/status/2105758042830549235) | The author sees stronger focus on a single subject in both reported Fable outputs. This is one creator's subjective assessment, with an explicit disclaimer about motion-design expertise. |
| Pacing, beat synchronization and sound | [Same post](https://x.com/mesmerlord/status/2105758042830549235) and [separate Opus baseline](https://x.com/mesmerlord/status/2105766824558174486) | The author finds Opus more hurried despite the same 15-second duration and considers its sound weaker. The beat-sync observation is tentative. No frame-level or listening blind test was performed. |
| Overall release-video composition | [@mesmerlord's paired release films](https://x.com/mesmerlord/status/2105771088374288692) | Both use Anthropic videos as references; the creator prefers Fable's first pass. Complete clip-to-model mapping is not explicit in the inspected text, and replies include disagreement. We do not certify commenters' guesses about the second clip. |
| Scene detail and personal style | [@TOPSTR1X's Minecraft model](https://x.com/TOPSTR1X/status/2105839618872738138), [@blueemi99's voxel world](https://x.com/blueemi99/status/2105804692811137242) | Both creators favor these results over their Opus experience. The former supplied BlockBench MCP and a custom skill encoding coloring/modeling preferences; the latter explicitly labels the version as uncertain. These are not isolated model effects. |
| Continuous motion across styles | [@chetaslua's Superman art-style journey](https://x.com/chetaslua/status/2105757136219504862) | The source and linked Artifact illustrate a useful production pattern. A creator reply attributes it to code without MCP, skills or plugins. There is no paired Opus baseline, so it shows capability rather than the size of an advantage. |
| Creative expansion from a short request | [@cherry_mx_reds's dot story](https://x.com/cherry_mx_reds/status/2105825930799432073), [another animation](https://x.com/cherry_mx_reds/status/2105816670896009224) | The creator attributes rich outputs to brief requests and reports about 15 minutes for the latter. Full context, revisions and rendering projects are not disclosed, so these are not reproducible one-prompt workflows yet. |

**Our interpretation of the reports: composition and timing are the clearest leads—focus, pacing and audiovisual relationships—followed by detail and style consistency.** This is a synthesis of attributed reports, not a model ranking. The strongest motion and release-film comparisons both come from @mesmerlord, not two independent testers.

Speed and cost have weaker support. In a [reply](https://x.com/mesmerlord/status/2105771524825522190), the release-film creator says Fable was slow and the displayed first pass preceded full completion. [@SPAC89](https://x.com/SPAC89/status/2105783511433318451) compares reported Fable 5.5 XHigh with GPT-6.1 Sol Ultra, each around 30 minutes. The reported 7% versus 1% weekly allowance comes from different subscription tiers; it is neither a token-price ratio nor an Opus comparison.

## Open these reported Fable demos

These are **source-only additions**, not new Hypit-reviewed cases. All Fable 5.5 identities remain creator-attributed and backend-unverified.

| Original creator post | Production role / reason to watch | Missing evidence |
|---|---|---|
| [@mesmerlord: 15-second motion reel](https://x.com/mesmerlord/status/2105758042830549235) | Two Fable candidates and a separately posted Opus baseline; focus and beat timing. | Full execution records, matched effort, all iterations and bills. |
| [@mesmerlord: mock release films](https://x.com/mesmerlord/status/2105771088374288692) | Paired films referencing Anthropic. The author says numerical claims are invented; do not cite their metrics. | Backend identity and complete clip labels. Codex image creation was allowed; a later reply says it appears unused. |
| [@chetaslua: Superman across art styles](https://x.com/chetaslua/status/2105757136219504862) · [public Artifact](https://claude.ai/artifact/7F2XhpmgiuyxHKgQ9Vgr9Q) | Creator reports pure code; continuing character movement through changing art treatments. | Full prompt and model-call records; Artifact source was not audited in this review. |
| [@cherry_mx_reds: a dot's story](https://x.com/cherry_mx_reds/status/2105825930799432073) | A brief request expands into character animation and scenery. Browser review confirmed the post and one video frame. | Full context, asset/tool sources and revision count. |
| [@cherry_mx_reds: another animation](https://x.com/cherry_mx_reds/status/2105816670896009224) | Creator reports roughly 15 minutes; another example of creative expansion. | Full context, production process and backend identity. |
| [@TOPSTR1X: Minecraft modeling](https://x.com/TOPSTR1X/status/2105839618872738138) | BlockBench MCP plus a custom Minecraft skill; personalized colors and detail. | Matched Opus output and call logs; treat as modeling/program demonstration. |
| [@blueemi99: voxel world](https://x.com/blueemi99/status/2105804692811137242) | Creator favors the detail over Opus and labels the version as uncertain. | Controlled comparison and exact model identity. |
| [@Chengzilhy: action-film prompting](https://x.com/Chengzilhy/status/2105850801663234374) | Creator attributes prompts to Fable and pixels to a workflow involving Seedance 2.5. | Full prompt, generation and editing records; not a Fable-only pixel-generation example. |

## Sonnet 5.5 belongs in the collection too

The [official release](https://www.anthropic.com/claude-sonnet-5-5) confirms Sonnet 5.5 launched September 28. These disclosures remain separate from the old corpus:

| Original post | Use and creator-disclosed production evidence | Boundary |
|---|---|---|
| [@kevin_t_ngo: rainbow colors](https://x.com/kevin_t_ngo/status/2105652774780420607) | Creator attributes every animation frame to Sonnet-written code. | Full code, audio and execution records unverified. |
| [@measure_plan: JavaScript forest](https://x.com/measure_plan/status/2104634071628337167) | Creator reports about 3,000 lines of JS / WebGL shaders, procedural realtime graphics and sound, without external assets or 3D models. | A realtime scene preview, not automatically a completed edited film. |
| [@petergyang: StarCraft level and sizzle reel](https://x.com/petergyang/status/2104736498151256303) | Explicitly uses Sketchfab SC2 models and Suno music; Sonnet makes the level and reel. | External assets and music are not Claude-drawn frames or Claude-composed music. |
| [@Tim_LB: TinyWorld comparison](https://x.com/Tim_LB/status/2104663105837932884) | Creator reports Sonnet $0.96 / 10.8 minutes versus Opus $4.79 / 22.7 minutes, with near-Opus quality. | One creator experiment, not a fixed 80% saving or universal speed ratio. |
| [@AxtonLiu: five-shot B-roll comparison](https://x.com/AxtonLiu/status/2105471099891068929) | Creator finds cards, charts and 3D close at about 54% cost, with weaker ink drawing; Opus took 38 rounds, Sonnet 24. | Explicitly a single trial. Fewer rounds can also omit causal and visual details, rather than establish greater efficiency. |

These examples give the wider Claude 5.5 scope substantive coverage and show why comparisons should be specific to a production task and style.

## How to read rollout claims

- [@chetaslua's routing report](https://x.com/chetaslua/status/2105733677003292983), [@Mr_Salio's claimed test](https://x.com/Mr_Salio/status/2105774088492916757), and [@kimmonismus's roundup](https://x.com/kimmonismus/status/2105740195832488447) establish that people are reporting access and routing.
- Asking about Tibo without web search is a community heuristic, **not backend identification**. [@EuanSpencer00](https://x.com/EuanSpencer00/status/2105855237018009840) reports passing it on Fable 5.1, while [@kumouX](https://x.com/kumouX/status/2105849312693588326) questions the inference. Output quality and model self-identification cannot independently establish a backend change either.
- [@rileybrown](https://x.com/rileybrown/status/2105853523862647081) also asks whether routing is speculation or real. We can document promising demos before an announcement while keeping identity claims provisional.

## Coverage and dataset boundaries

This run directly searched X through the existing Mini OpenCLI session and retained local raw query/thread receipts. Four Fable queries returned exact-phrase live (30), broad Fable + since:2026-09-28 live (50), exact-phrase top (50), and exact-phrase + Opus top (50). Sonnet video top returned 30. All five reached their caps, overlap, and must not be added into an original-work total. Broad Fable includes gaming noise; top queries have no date restriction.

Five additional threads cover motion, mock release, Minecraft, Superman and B-roll; replies can be truncated too. Browser checks covered the dot, motion, mock release, Superman and Minecraft source pages. A playback screenshot helps confirm visible content but is not a full-film technical audit or an audio rating. Original IDs distinguish creator posts from reposts; repost volume does not measure original-work count.

The [source ledger](../data/claude55-source-review-2026-10-02.csv) records model attribution, source kind and limits. No new `tile_ok`, original-authorship verification, or model-execution verification is claimed. **The September 26 Opus corpus, 168 reviewed cases and chart denominators remain unchanged.**
