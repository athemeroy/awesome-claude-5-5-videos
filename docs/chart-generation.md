# Reproduce the public figures

The September 30 redraw uses the existing **September 26 frozen corpus** and separately dated September 27 color and engagement records. It adds no new X observations. All plotting runs locally from public CSV/JSON files; no X requests or private media are needed.

Use Python 3.12 or newer and the pinned rendering packages:

```sh
python3 -m venv .venv-charts
.venv-charts/bin/python -m pip install -r requirements-charts.txt
.venv-charts/bin/python scripts/generate_intro_charts.py
.venv-charts/bin/python scripts/generate_stat_charts.py
.venv-charts/bin/python scripts/generate_color_charts.py
```

| Figures | Generator | Published inputs and units |
|---|---|---|
| Corpus overview | `generate_intro_charts.py` | `data/corpus-snapshot.json`; posts, attachments, distinct files, classifier labels and curated case posts remain different units. |
| Four broad production roles | `generate_intro_charts.py` | Editorial diagram of the reviewed workflow distinctions; it is not a path-frequency chart. The seven detailed paths and source cases are in `data/cases.csv`. |
| Five visible prompt lengths | `generate_intro_charts.py` | `data/visible-prompt-lengths.json`; source-linked reported character counts, not total inputs or token cost. |
| Domain and style counts, domain/style cross-tab | `generate_stat_charts.py` | `data/domain-style.csv`, checked against the frozen snapshot; one primary category per file. |
| Preview duration by reviewed path | `generate_stat_charts.py` | `data/cases.csv`; medians and inclusive quartiles for deliberately selected case previews. |
| Color-mode highlight and both full atlases | `generate_color_charts.py` | `data/color-study/color-modes.json` and the published mode summaries; palette widths represent sampled-pixel shares. Files and dated-like posts have separate denominators. |
| Colorful-pixel share by domain | `generate_color_charts.py` | `data/color-study/per-video-color-vectors.csv`; each file has equal weight. This describes sampled frames, not color's effect on engagement. |

For a read-only comparison with the checked-in SVGs, pass `--check` to each generator. GitHub Actions runs those checks plus `scripts/check_color_modes.py`, which reconciles vectors, mode assignments, palettes, totals and engagement denominators. Matplotlib versions, fonts, SVG identifiers and metadata are fixed for stable output. SVGs include figure descriptions for assistive tools.

The published color vectors support redrawing summaries. They do not contain the original source MP4s or nine-frame sheets, so this process does not repeat the original frame extraction or clustering. See [color measurement](color-modes.md), [statistical definitions](statistics.md) and the [methodology](methodology.zh-CN.md) for those limits.
