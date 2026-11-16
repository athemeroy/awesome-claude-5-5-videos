# Claude Fable 5.2 Video Ecosystem Report (2026-11-16)

[Home](../README.md) · [Complete directory](library.md#fable-5-2) · [中文](fable-5-2.zh-CN.md) · [Source ledger CSV](../data/source-review-2026-11-16-fable52.csv)

## Context: From October Leaks to the November 9 Launch

In early October 2026, several creators shared videos attributed to a suspected "Fable 5.5" routing experiment (preserved under [Fable (pre-release)](library.md#fable-pre-release)). On **November 9, 2026**, Anthropic officially launched **[Claude Fable 5.2](https://www.anthropic.com/claude/fable)** alongside Mythos 5.2:

- **Positioning**: Anthropic's flagship model for complex technical work, 3D/hardware/motion design, and long-horizon agent orchestration—capable of building interactive 3D worlds, simulations, and educational videos with synthesized sound in code.
- **Pricing & Speed**: **$8 / M input tokens and $40 / M output tokens** (down 20% from Fable 5.1's $10 / $50), with $0.20 / M cache reads. Fast mode delivers up to 2.5x speed at $16 / $80.
- **Safeguards**: Cybersecurity and biology safeguards may route flagged queries to less capable fallback models; 30-day data retention applies by default unless Enterprise Frontier Safeguards (EFS) is configured.

This update adds **173 distinct Fable 5.2 source posts** published between November 9 and November 13, 2026, each with verified X source URLs, durations, and category labels.

## Breakdown of the 173 Fable 5.2 Works

| Category | Count | Share | Typical outputs |
|---|---:|---:|---|
| Motion graphics (`motion`) | 56 | 32.4% | Particle films, code-only shaders, lyric motion videos, showreels, LilyPond fugues |
| 3D scenes (`3d`) | 45 | 26.0% | Blender modeling/rigging, photo-to-3D/AR walkthroughs, Three.js physics sims |
| Interactive & games (`interactive`) | 30 | 17.3% | Open-world driving, 3rd-person exploration, 3D basketball, physics UI switches |
| Launch & promo films (`promo`) | 15 | 8.7% | Keynote-style product films, vertical app trailers, style-matched reels |
| Model comparisons (`comparison`) | 15 | 8.7% | Fable 5.2 vs Opus 5.5 / GPT-6 Astra side-by-side timing, cost and first-pass checks |
| Explainers (`explainer`) | 12 | 6.9% | Symmetry math visuals, watercolor science explainers, 10-minute narrated decks |

- **Duration**: Min 5s, **median 30s**, max **10m 15s (615s)**.
- **Tooling**: Notable mentions include **Blender** (18), **AR / spatial reconstruction** (16), **Motion** (14), **Three.js / WebGL** (14), **Pixel / Voxel** (16), plus code-synthesized audio (shaders, Web Audio, LilyPond).

## Key Takeaways: What Changed vs. Opus 5.5?

Across the 15 side-by-side comparisons and creator reports (un-audited creator disclosures):

1. **Higher First-Pass Reliability on Complex 3D & Code Scenes**
   - [@leohuanfang's sailing ship rerun](https://x.com/leohuanfang/status/2120024307573137874): Fable 5.2 finished in **27m 46s ($7.59)** with zero errors on first open, whereas Opus 5.5 took three tries and 50 minutes.
   - [@Trace_AR's AR reconstruction](https://x.com/Trace_AR/status/2121284000232714559): Rebuilt a lunch spot into a full 3D building and AR walkthrough from eight photos in a few hours.
2. **Deeper Self-Iteration Shifts Cost & Runtime**
   - [@motion_so's Motion comparison](https://x.com/motion_so/status/2120029008809361891): On the same prompt, Fable 5.2 ran 2h 35m and spent **$88.09**, compared to Opus 5.5 at 3h+ and $17.03. Fable 5.2's deeper verification loops produce higher output token volume on open-ended tasks.
3. **Cross-Modal Code Synthesis (Video + Audio)**
   - [@tankazunori0914](https://x.com/tankazunori0914/status/2120012834461646927) generated both shader visuals and synthesized music purely in code; [@aug5thmusic](https://x.com/aug5thmusic/status/2119907891419480107) wrote a 2m05s organ fugue in D minor using LilyPond.

## Index of 17 Creator-Published Prompts

| Creator | Category | Duration | Title | Source & Prompt |
|---|---|---:|---|---|
| @czzzzzzJ_ | promo | 298s | A keynote-style promo film for a Chinese AI knowledge site | [View post](https://x.com/czzzzzzJ_/status/2120023093464682817) |
| @himanshutwtxs | motion | 15s | A one-prompt motion designer showreel: timing, easing, shape and type | [View post](https://x.com/himanshutwtxs/status/2120017106804900304) |
| @wshuyi | 3d | 28s | A sabertooth cat hunts a bison on a golden steppe | [View post](https://x.com/wshuyi/status/2120014892040417720) |
| @takamasa045 | motion | 53s | Just your voice: a Japanese lyric motion video in black, cream and orange | [View post](https://x.com/takamasa045/status/2120014216753262816) |
| @tankazunori0914 | motion | 64s | From a point to a world: a code-only shader video with a synthesized song | [View post](https://x.com/tankazunori0914/status/2120012834461646927) |
| @ericmaskfr | interactive | 135s | An open-world Miami-style crime game with car paint shops and timed races | [View post](https://x.com/ericmaskfr/status/2119910195325481026) |
| @itssotsot | interactive | 95s | A toy-room third-person game with a small explorer collecting items | [View post](https://x.com/itssotsot/status/2119909017216491720) |
| @aug5thmusic | motion | 125s | An organ fugue in D minor, written in LilyPond | [View post](https://x.com/aug5thmusic/status/2119907891419480107) |
| @kaif9998 | motion | 15s | A terminal model picker that turns into a showreel of animated type | [View post](https://x.com/kaif9998/status/2119903824848761287) |
| @heypearlai | motion | 15s | A self-made motion design showreel of type, shapes and UI loops | [View post](https://x.com/heypearlai/status/2119903760529113116) |
| @kplikethebird | 3d | 30s | Jerusalem at Passover: a 3D fly-through from the Temple to the Stepped Street | [View post](https://x.com/kplikethebird/status/2119900775727902732) |
| @maxt3chno | comparison | 21s | GPT-6 Astra vs Fable 5.2 building a zombie eagle creature in Blender | [View post](https://x.com/maxt3chno/status/2119896698281467952) |
| @joshvlc | interactive | 19s | Harbor City Arena: a 3D basketball game between the Tides and the Embers | [View post](https://x.com/joshvlc/status/2119894656221958575) |
| @al_maxgo | promo | 28s | FBPlot: a vertical trailer for a football chart and stats app | [View post](https://x.com/al_maxgo/status/2119891197317591040) |
| @danteeonsol | 3d | 30s | A UFO lands at a night-time Area 51 base and an alien greets the crew | [View post](https://x.com/danteeonsol/status/2119887623070077213) |
| @N1njaCodex | interactive | 11s | Deep Dive Switch: a toggle that sinks from the sea surface to the abyss | [View post](https://x.com/N1njaCodex/status/2119883560937001387) |
| @hello_amani | motion | 36s | amani/studio: a chrome logo reveal drawn from blueprint grid lines | [View post](https://x.com/hello_amani/status/2119873980786237842) |

## Limitations

- All 173 entries in this batch are `source-only` (not yet locally nine-frame sampled).
- Runtime, cost, and one-shot claims are creator-reported and have not been independently audited.
