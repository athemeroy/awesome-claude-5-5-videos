# X 检索覆盖记录

数据快照：2026-09-26T13:53:20.929497+00:00（UTC）。本表记录每条预设检索是否成功及返回条数；搜索排序、权限、限流与结果窗口都会造成漏检。

每次调用设置的返回上限是 50 条；这不是 X 全站该查询的实际结果总数。`候选帖`还包括引用原帖、作者回复、转载、对照和检索噪音。

| 序号 | 查询 | 模式 | 已返回 | 状态 |
|---:|---|---|---:|---|
| 1 | `"Opus 5.5" filter:videos` | top | 50 | ok |
| 2 | `"Opus 5.5" filter:videos since:2026-09-21` | live | 50 | ok |
| 3 | `"Claude Opus 5.5" filter:videos` | top | 50 | ok |
| 4 | `"Claude Opus 5.5" filter:videos since:2026-09-21` | live | 50 | ok |
| 5 | `"Opus5.5" filter:videos` | top | 50 | ok |
| 6 | `opus55 filter:videos` | top | 34 | ok |
| 7 | `#Opus55 filter:videos` | top | 21 | ok |
| 8 | `"Opus 5.5" "one shot"` | top | 50 | cached |
| 9 | `"Opus 5.5" "made a video"` | top | 6 | cached |
| 10 | `"Opus 5.5" "video generation"` | top | 26 | ok |
| 11 | `"Opus 5.5" animation filter:videos` | top | 50 | ok |
| 12 | `"Opus 5.5" "motion graphics"` | top | 22 | ok |
| 13 | `"Opus 5.5" "music video"` | top | 37 | ok |
| 14 | `"Opus 5.5" Remotion` | top | 34 | ok |
| 15 | `"Opus 5.5" p5.js` | top | 25 | ok |
| 16 | `"Opus 5.5" Manim` | top | 3 | ok |
| 17 | `"Opus 5.5" Blender filter:videos` | top | 50 | ok |
| 18 | `"Opus 5.5" Three.js filter:videos` | top | 50 | ok |
| 19 | `"Opus 5.5" SVG filter:videos` | top | 20 | ok |
| 20 | `"Opus 5.5" prompt filter:videos` | top | 50 | ok |
| 21 | `"plan a video" "Opus 5.5"` | top | 1 | ok |
| 22 | `"Opus 5.5" 视频 filter:videos` | top | 50 | ok |
| 23 | `"Opus 5.5" 动画 filter:videos` | top | 34 | ok |
| 24 | `"Opus 5.5" 動画 filter:videos` | top | 1 | ok |
| 25 | `"Opus 5.5" アニメ filter:videos` | top | 20 | ok |
| 26 | `"Opus 5.5" "code" video` | top | 50 | ok |
| 27 | `"claude" "5.5" video filter:videos` | top | 50 | ok |
| 28 | `"Opus 5_5" filter:videos` | top | 0 | ok |
| 29 | `"opus-5-5" video` | top | 20 | ok |
| 30 | `"Opus 5.5" since:2026-09-24 filter:videos` | live | 50 | ok |
| 31 | `"Opus 5.5" filter:videos since:2026-09-22 until:2026-09-23` | top | 50 | ok |
| 32 | `"Opus 5.5" filter:videos since:2026-09-23 until:2026-09-24` | top | 50 | ok |
| 33 | `"Opus 5.5" filter:videos since:2026-09-24 until:2026-09-25` | top | 50 | ok |
| 34 | `"Opus 5.5" filter:videos since:2026-09-24 until:2026-09-25` | live | 50 | ok |
| 35 | `Opus5.5 動画 filter:videos since:2026-09-24` | live | 1 | ok |
| 36 | `Opus5.5 视频 filter:videos since:2026-09-24` | live | 9 | ok |
| 37 | `"Opus 5.5" 영상 filter:videos` | top | 2 | ok |
| 38 | `"Opus 5.5" animación filter:videos` | top | 11 | ok |
| 39 | `"Opus 5.5" vidéo filter:videos` | top | 50 | ok |
| 40 | `"Opus 5.5" Seedance filter:videos` | top | 36 | ok |
| 41 | `"Opus 5.5" filter:videos since:2026-09-22 until:2026-09-23` | live | 50 | ok |
| 42 | `"Opus 5.5" filter:videos since:2026-09-23 until:2026-09-24` | live | 50 | ok |
| 43 | `"Opus 5.5" filter:videos since:2026-09-24` | live | 50 | ok |

## 2026-09-25 增量刷新

这些是新增的 X Top / Latest 查询回执，每次最多返回 50 条。`since` 是 X 的日期筛选词；回执保留实际帖文 UTC 时间，不能把筛选词直接解释成精确 UTC 起点。

| 查询 | 模式 | 返回 | 状态 |
|---|---|---:|---|
| `"Opus 5.5" animation filter:videos since:2026-09-25` | top | 38 | ok |
| `"Opus 5.5" 视频 filter:videos since:2026-09-25` | live | 0 | rate_limited |
| `"Opus 5.5" filter:videos since:2026-09-25` | live | 50 | ok |
| `"Opus 5.5" filter:videos since:2026-09-25` | top | 50 | ok |
| `Opus5.5 動画 filter:videos since:2026-09-25` | live | 1 | ok |
| `"Opus 5.5" video since:2026-09-25` | live | 50 | ok |

## 2026-09-26 增量刷新

这些是新增的 X Top / Latest 查询回执，每次最多返回 50 条。`since` 是 X 的日期筛选词；回执保留实际帖文 UTC 时间，不能把筛选词直接解释成精确 UTC 起点。

| 查询 | 模式 | 返回 | 状态 |
|---|---|---:|---|
| `"Opus 5.5" animation filter:videos since:2026-09-25` | top | 60 | ok |
| `"Opus 5.5" 视频 filter:videos since:2026-09-25` | live | 60 | ok |
| `"Opus 5.5" filter:videos since:2026-09-26` | live | 60 | cached |
| `"Opus 5.5" filter:videos since:2026-09-25` | top | 60 | cached |
| `Opus5.5 動画 filter:videos since:2026-09-26` | live | 1 | ok |
| `"Opus 5.5" motion filter:videos since:2026-09-25` | top | 60 | ok |
| `"Opus 5.5" video since:2026-09-26` | live | 60 | ok |

成功保存的查询：55 / 56；各查询累计返回 2013 条（含重复），去重、引用来源回溯和作者回复补充后的候选帖为 1511 条。

HTTP 429 原始响应保留在内部 `data/x-search-raw/`；失败调用的返回数为零，不把它算作成功覆盖。
