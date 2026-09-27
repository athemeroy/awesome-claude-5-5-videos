# One video category can contain several color palettes

[中文](color-modes.zh-CN.md) · [Back to README](../README.md)

We measured color in the **1,119 byte-distinct X-preview MP4s** that the project's classifier labeled `yes` or `likely` for Opus 5.5 involvement in its September 26, 2026 snapshot. They came from 1,099 posts. Nine evenly spaced frames per file yield **10,071 frames**. These labels do not independently verify how every video was made, and this retrieved sample is not a census of X.

The [four-category highlight](../assets/color-study/color-modes-highlight.png) shows education, short stories, motion/UI and ads. Its labels are mainly Chinese; the [13-style atlas](../assets/color-study/color-modes-style-atlas.png) and [11-domain atlas](../assets/color-study/color-modes-domain-atlas.png) can be opened at full size. In each row, the file count and the count of posts with exact same-day likes have different denominators.

## Findings

- One average palette per category hides differences within that category. **11 of 13 styles** and **10 of 11 domains** split into two or three color modes; the other three categories have only 4–11 files and remain single-mode. **15 of the 21 split categories** contain both a dark and a light mode.
- Motion graphics/UI splits 350 files into a 198-file dark neutral mode and a 152-file light neutral mode. Ads/launches split 215 files into modes of 97, 82 and 36 files. Modes describe color composition, not quality.
- The median video-level share of visibly colorful pixels is **45.5%** for 77 music-video files and **17.6%** for 215 ad/launch files. Repeating the frame reduction at 16, 32 and 64 pixels preserves that ordering. These are descriptive values for this sample.
- Likes never enter the clustering. Within motion/UI, the September 27 exact-like medians are **50** for dark and **104** for light, from **22 posts per mode**. The ranges are wide; this does not show that light colors cause more likes. Only **20 of 53 modes** have at least five exact same-day like observations.

## Measurement

We crop the nine-frame contact sheet to each frame's picture area, removing sheet gutters and timestamps, then resize each frame to 32 × 32 pixels. Letterboxing already inside a video remains. Each file contributes 9,216 pixels and one equally weighted color vector. Identical MP4s are SHA-256 deduplicated.

The vector has 21 proportions: three CIELAB lightness bands crossed with either a neutral bin (`C* < 18`) or one of six HSV hue sectors. We fit K-means within each style and domain, using square-root proportions (Hellinger geometry) and choose one to three modes with sample-size and silhouette rules. Categories below 12 files remain one mode. Six CIELAB swatches are then fitted within each mode. **A swatch's width represents the actual share of sampled pixels assigned to it within that mode**, not the share of videos in the category.

The colorful-pixel measure is the fraction with HSV saturation ≥ 0.25 and value ≥ 0.15. Sampling, X compression, classifier labels and letterboxing can affect it. Clusters are a descriptive partition of a continuous color distribution, not a discovery of fixed artistic genres.

## Engagement and data

The figure uses only exact likes refreshed on **September 27, 2026**. The refresh covers 166 of 168 deliberately selected reviewed posts, then intersects with this video sample. We deduplicate likes by source post within each mode. Posts with files spanning multiple modes in one category are excluded from that category's mode-level like comparison. Medians appear in the figure only with at least three posts, and counts below five are marked sparse. Older archived likes have mixed, unknown observation times and remain separate in the data. Author reach, topic, post age and distribution confound any popularity comparison; no causal effect of color was tested.

| File | Contents |
| --- | --- |
| [Mode summary](../data/color-study/color-mode-summary.csv) | 53 rows: category, mode, file counts, color and engagement summaries. |
| [Swatches and shares](../data/color-study/color-mode-swatches.csv) | Six rows per mode: hex value, assigned pixel count and share. |
| [Per-video vectors](../data/color-study/per-video-color-vectors.csv) | 1,119 rows: SHA, source post, category, 21-bin color vector and separately dated likes. |
| [Per-video mode assignments](../data/color-study/per-video-color-modes.csv) | One style and one domain assignment per file. |
| [Full JSON](../data/color-study/color-modes.json) | Methods, diagnostics, mode palettes, like distributions and representative source posts. |

The published derived data supports recalculating these summaries and trying other clustering methods. Source MP4s, nine-frame sheets and the internal crawl archive are not redistributed, so these CSVs alone cannot reproduce frame extraction. Representative posts were selected for proximity to a color center, not for likes; the maintainer's own video remains in historical counts but is excluded from displayed representatives.

For production, specify background lightness, primary and accent colors, and a per-shot color-consistency check when color is important. That is a practical suggestion, not an experimentally proven best palette. A [later creator's prompt](https://x.com/brainextends/status/2104148921027346476) explicitly specified hex colors and per-shot color correction; it is outside this frozen sample.
