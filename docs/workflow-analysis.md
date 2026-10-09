# What the newer video examples actually tell us

[Home](../README.md) · [Full directory](library.md) · [中文](workflow-analysis.zh-CN.md)

The newer posts reveal several production patterns. They do not establish a general winner among Opus, Sonnet, Haiku and reported Fable. This analysis uses creator disclosures, three follow-up threads and sampled previews. [Source ledger](../data/claude55-source-review-2026-10-10-followup.csv) · [Sampling and account coverage](collection-analysis.md).

## The input changes the task

| Example | Disclosed input | Claude's reported role | What readers can learn |
|---|---|---|---|
| [Reference-led mixed-media film](https://x.com/notdwd/status/2107816799840690589) | A skill and [detailed public brief](https://x.com/notdwd/status/2107817421981843679): portrait and hand clips, Pexels defaults, music, paper texture and frame timing. | Reported Fable turns a specified design into a mixed-media film. | A small triggering request can sit on top of prepared assets and a precise production system. |
| [Half a blanket](https://x.com/Vallabh469/status/2108494077389926611) | Human-designed concept, narrative and character sheets. | Opus handles composition, animation and sound according to the creator. | Attribute the story and character design to the person who supplied them. |
| [Beijing promo](https://x.com/shengtang135754/status/2108549555528872041) | A brief requiring sourced footage and MiniMax narration. | Haiku selects/assembles footage, text and narration. | A video made with Haiku can be an editing workflow rather than code drawing every pixel. |
| [Sound/motion visualization](https://x.com/aicreataro/status/2108091976574988390) | MiniMax H3 people, Midjourney key art, MiniMax music. | Opus plus Blender/Python applies depth, particles and camera movement. | Model-generated assets and code-driven effects are distinct stages. |

These are deliberately selected examples, not a measured distribution of inputs. Aesthetic similarity does not show that the same tools were used. Preserve the inputs when adapting a public prompt.

## One prompt can still contain many revisions

The [F1 pit-stop post](https://x.com/rubenssoto_ai/status/2108289170871582851) describes one human prompt. In a [reply](https://x.com/rubenssoto_ai/status/2108608936295408050), the creator says Opus repeatedly rejected results, which they believe increased usage and elapsed time. The creator also [expresses uncertainty about procedural audio](https://x.com/rubenssoto_ai/status/2108608684876071241).

Other sources make the human work explicit: [Taxtello is version five, with a critic agent](https://x.com/daniel_haida/status/2108595684236755242); [the game developer supplied purchased assets and used roughly twenty prompts over two days](https://x.com/Rush3rx/status/2108607656776876368); [Understory needed several days and human guidance](https://x.com/DannyLimanseta/status/2107505970809336071).

Record three separate quantities: human prompts, internal tool/review passes, and time to the accepted result. The posts do not disclose all three consistently, so “one-shot” is not a common production-effort unit.

## Lower token prices do not fix total task cost

These are selected creator-reported task costs, not verified bills or a controlled benchmark. No API price claims are needed to compare the reported totals.

| Creator's comparison | Reported costs | Ratio calculated from those costs | Boundary |
|---|---:|---:|---|
| [Golden Gate Bridge](https://x.com/Solomonrojie/status/2108322280094728219): Haiku / Opus | $2.19 / $3.04 | Haiku = 72.0% of Opus, or 28.0% less. | Same scene brief; creator describes different details in the results. |
| [Fluffy crab](https://x.com/vib3coded/status/2108190478889824662): Sonnet / Opus | $11.25 / $13.30 | Sonnet = 84.6% of Opus, or 15.4% less. | Same prompt; no common acceptance score or independent billing record. |
| [F1 pit-stop team](https://x.com/rubenssoto_ai/status/2108289170871582851): Haiku executor / whole Claude team | $61.77 / $96.27 | Executor = 64.2% of the reported team cost. | Opus is the planner/reviewer; this is a team, not a standalone Haiku film. |

The F1 creator reports 819.9M of 914.7M tokens in the executor, or 89.6%. They also describe repeated review. This shows why token volume and revision loops belong beside unit prices when assessing a pipeline. It does not explain every charge in the bill.

Do not average these dollar amounts into a model ranking. The deliverables, asset inputs, effort settings, tools and acceptance criteria differ. See the [cost recording guide](visual-effects-fit.md#compare-costs-against-the-same-deliverable).

## Haiku has several roles, with mixed outcomes

The collection now contains creator-reported Haiku motion graphics, poetry, SVG animation, scene comparisons, footage editing and executor roles. In the sampled [30.059-second motion reel](https://x.com/badboyfoxy/status/2108089492016103775), we see typography, easing diagrams, orbital forms and light bars. In the [Beijing example](https://x.com/shengtang135754/status/2108549555528872041), the brief requests footage and external narration. These are different tasks.

Keep counterexamples: [EnvolDev prefers Luna in a night-train test](https://x.com/EnvolDev/status/2107973447230091623), while [the SVG-pelican creator favors Haiku](https://x.com/xueyu1125/status/2108082476975554587). The latter uses OpenCode for Haiku and Codex for Luna, so the harness is another difference. These reports support trying Haiku on specific tasks; they do not support “Haiku always wins” or a general quality score.

## A plausible animation is not a validated explanation

The [Sonnet tower creator](https://x.com/Solvaix/status/2107548992640880755) explicitly says the construction sequence is invented, geometry simplified and engineering calculations absent. Our samples show a rising tower and changing crane positions. The available recording is 29.118 seconds, while the post describes a 68-second timeline. Keep recording duration separate from timeline duration.

The [football reconstruction](https://x.com/lv_feng47448/status/2108397996740432136) reports position data, ball simulation and motion capture. Naming those inputs is useful, but it does not independently validate the physical reconstruction. Similarly, a rendered mathematical or scientific explanation does not prove its underlying claim.

For reuse, choose the intended deliverable first: an illustration, a recorded interactive scene, a footage edit, or a validated explanation. Then carry over the source material, renderer and observable checks. The [production guide](visual-effects-fit.md) gives task-specific checks; [pictured routes](production-resources.md) link working examples.
