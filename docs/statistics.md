# Statistical snapshot: units, denominators, and sensitivity

[中文](statistics.zh-CN.md) · Generated from the public CSVs and [frozen snapshot](../data/corpus-snapshot.json) by [`scripts/generate_statistics.py`](../scripts/generate_statistics.py). Run `python3 scripts/generate_statistics.py --check` to detect drift.

Snapshot: 2026-09-26T13:53:20.929497+00:00. These are **descriptive statistics for the retrieved corpus**, not a census of X, a quality score, or a model success rate.

## Count the right unit

| Count | Unit | Reproducible from public files? |
|---|---|---|
| 56; 55 succeeded or used cache | Saved search queries | Only the summary and [coverage notes](search-coverage.zh-CN.md) are public; raw receipts are not. A successful query does not imply full coverage. |
| 1,511 | Deduplicated candidate posts | Recorded only in the snapshot; raw candidate rows are private. |
| 1,419 | Candidate posts with MP4 | Recorded only in the snapshot. |
| 1,449 | Retrieved MP4 attachments with nine-frame samples | Recorded only in the snapshot; a post can have several attachments. |
| 1,401 | MP4 files reported as SHA-256 distinct | The [classifier CSV](../data/domain-style.csv) has 1,401 rows, but no public file hashes or per-attachment IDs to independently repeat deduplication. |
| 168 | Manually reviewed source-post cases | The [case CSV](../data/cases.csv) has 168 unique post IDs, each marked as sampled. |

The snapshot also reports 39 byte-identical groups and 48 extra attachments in those groups; 1,401 + 48 = 1,449. That arithmetic is checkable; the underlying hashes are not public.

## The classifier threshold changes first place

A vision classifier assigned one `opus_made` label, one primary domain, and one primary style per file from the post text and nine sampled frames. Its labels do not independently establish authorship, model calls, or finished-video quality.

| Included labels | File denominator | Games / interactive | Ads / launches | First place |
|---|---:|---:|---:|---|
| `yes` only | 980 | 187 (19.1%) | 191 (19.5%) | Ads / launches |
| `yes` + `likely` | 1,119 | 230 (20.6%) | 215 (19.2%) | Games / interactive |

Across all 1,401 classified files, there are 980 `yes`, 139 `likely`, and 282 `no` labels. The two thresholds include 70.0% and 79.9% of these files; **these are not lower and upper bounds on actual Opus use**. The leading domain flips from ads to games, so that ranking depends on how `likely` is handled. The two leading primary styles remain motion graphics / UI (308 → 350) and 3D render (265 → 324).

## Domain × primary style: ten largest cells

This table uses only the 1,119 **files** labeled `yes` or `likely`. Each file contributes to one cell; percentages use that file denominator. Only ten cells are shown, so their counts do not sum to the denominator.

| Domain | Primary style | Files | Share of included files |
|---|---|---:|---:|
| Games / interactive | 3D render | 161 | 14.4% |
| Ads / launches | Motion graphics / UI | 154 | 13.8% |
| AI about AI | Motion graphics / UI | 62 | 5.5% |
| AI about AI | 3D render | 60 | 5.4% |
| Education / science | Motion graphics / UI | 55 | 4.9% |
| Short story | Flat cartoon | 37 | 3.3% |
| AI about AI | Flat cartoon | 34 | 3.0% |
| Games / interactive | Motion graphics / UI | 34 | 3.0% |
| Education / science | Flat cartoon | 25 | 2.2% |
| Ads / launches | 3D render | 25 | 2.2% |

The classifier CSV has 1,371 distinct post IDs, not 1,401 distinct posts. 23 posts have multiple classified files (53 rows), and 7 have differing `opus_made` labels across attachments. The optional secondary style `style2` is blank on 442 rows and is excluded here. Re-encoded copies of one work can also remain distinct files; these rows are not independent creators.

## Preview-duration distribution

Durations describe accessible X preview MP4s, not necessarily the uploaded masters. Some older prose notes differ from the numeric duration and remain unreconciled. The median and 25th–75th percentiles describe skewed distributions. Quartiles use Python `statistics.quantiles(n=4, method='inclusive')`. These selected cases cannot rank production-path success.

| Unit | n | Median (s) | 25th–75th percentile (s) |
|---|---:|---:|---:|
| Classified file | 1,401 | 39.20 | 21.91–77.07 |
| Curated case's main-post MP4 | 168 | 52.37 | 29.76–117.04 |

These rows have different units and selection rules; their difference cannot be attributed to a production route or model performance.

| Curated case's primary path | Cases | Median (s) | 25th–75th percentile (s) |
|---|---:|---:|---:|
| Code-drawn 2D | 52 | 46.38 | 30.00–105.64 |
| Educational explainer | 27 | 102.28 | 60.05–256.54 |
| 3D or real-time graphics | 19 | 34.18 | 23.02–64.17 |
| Existing-source transformation | 32 | 40.54 | 26.81–56.85 |
| External video-model pipeline | 10 | 24.76 | 19.33–52.82 |
| App or game capture | 14 | 50.30 | 32.65–116.13 |
| Mixed or unestablished pipeline | 14 | 51.79 | 27.53–152.91 |

## Curated cases are not classifier ground truth

Matching original post ID and preview duration (tolerance ≤0.05 s) gives 152 `yes`, 5 `likely`, and 11 `no` labels among the 168 curated cases. A `no` label is not automatically a classifier error, and inclusion in the case index does not prove an Opus call. For example, [one MP4 compares two models](https://x.com/leogao25/status/2102544078927741369), [one records a game](https://x.com/The_Alex/status/2102440678282412195), and [one creator describes the workflow later](https://x.com/leodev/status/2102781872107659270). These require case-level reading of the original and follow-up disclosures.

## Examples that test what the counts mean

These are deliberately chosen evidence contrasts, **not** randomly sampled representatives of statistical cells.

| Original post | Evidence boundary |
|---|---|
| <a href="https://x.com/Aurelien_Gz/status/2102786378282987591"><img src="../assets/case-thumbnails/2102786378282987591.webp" width="160" alt="Sampled X preview frame"></a><br>@Aurelien_Gz · Clearwater | A matching public WebGL source project supports the rendering route; the X preview does not reveal the full model conversation. |
| <a href="https://x.com/WangYeruo/status/2103108551799632050"><img src="../assets/case-thumbnails/2103108551799632050.webp" width="160" alt="Sampled X preview frame"></a><br>@WangYeruo · Thusfar product films | The creator discloses an existing codebase, external TTS, and revisions; a visible ad is not evidence of a blank-input one-shot. |
| <a href="https://x.com/ng169onX/status/2103183904563998809"><img src="../assets/case-thumbnails/2103183904563998809.webp" width="160" alt="Sampled X preview frame"></a><br>@ng169onX · VAE explainer | The sampled frames show diagrams, while the training run, mathematical accuracy, and audio still require separate checks. |
| <a href="https://x.com/jantijssen/status/2102861462461124755"><img src="../assets/case-thumbnails/2102861462461124755.webp" width="160" alt="Sampled X preview frame"></a><br>@jantijssen · Externally rendered music video | The creator assigns song, video clips, and editing to different tools; the classifier says `no`, so role and label must be read separately. |
| <a href="https://x.com/leogao25/status/2102544078927741369"><img src="../assets/case-thumbnails/2102544078927741369.webp" width="160" alt="Sampled X preview frame"></a><br>@leogao25 · Two-model comparison | The posted MP4 compares two outputs; it is not a full inspection of either underlying production run. |
| <a href="https://x.com/pradeepXkapoor/status/2102782449478668290"><img src="../assets/case-thumbnails/2102782449478668290.webp" width="160" alt="Sampled X preview frame"></a><br>@pradeepXkapoor · Unfinished ink-film attempt | The creator calls the work unfinished despite a visible MP4; attachment presence is not a success measure. |

## Limits on inference

X search depends on terms, languages, ranking, per-query limits, account visibility, and rate limits. The case index was then chosen deliberately for production routes and evidence conditions. We therefore report no X-wide technique shares, time trends, population confidence intervals, or p-values. Preview length cannot establish cost, quality, creative independence, or model superiority. Nine frames cannot verify continuous motion, audio, factual accuracy, or hidden tool calls. See the [methodology](methodology.zh-CN.md) and [case-field guide](case-index-guide.zh-CN.md).

[AAPOR's Transparency Initiative](https://aapor.org/standards-and-ethics/transparency-initiative/) distinguishes disclosure of methods from certification of their quality; this page likewise states the limits of its statistics.
