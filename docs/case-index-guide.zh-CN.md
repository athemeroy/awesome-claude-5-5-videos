# 公开案例表说明

[`data/cases.csv`](../data/cases.csv) 是人工深读的 Opus 5.5 视频相关帖子索引，供读者按来源回看。它不是 X 上所有作品的名录，也不是随机样本；分类数量不能当作各工艺的市场占比。每行对应一个原帖 ID，`source_url` 链接原帖。数据截点与样本量以同时发布的[冻结快照](../data/corpus-snapshot.json)为准。

| 字段 | 含义 |
|---|---|
| `source_url` | 作者原帖或明确的案例主帖。 |
| `primary_path` | 为便于筛选而指定的一条主制作路径；实际个案可能兼用多条路径。 |
| `label` | 作者与案例简称。 |
| `creator_disclosure` | 作者原帖、回复、公开提示词或与帖子直接关联的工程材料所说的流程；自述没有自动变成独立验真的执行日志。 |
| `hypit_observation` | 对可取得 X MP4 使用 Hypit 媒体探测和九帧取样后可见的内容与边界。 |
| `review_note` | 人工判断、分类理由及不能推出的结论。 |
| `duration_s` | 下载到的 X MP4 预览文件时长（秒），并非一定是最高画质母版。目录以此列显示片长；少数旧版观察文字另有不同片长，尚未逐项复核原因。 |
| `hypit_status` | `tile_ok` 表示该主帖的首个 MP4 有媒体探测和九帧样张；同帖其他附件在内部媒体表另列。 |

| `primary_path` 值 | 中文解释 |
|---|---|
| `procedural_2d` | 代码绘制的二维／像素／排版／音画动画。 |
| `educational_explainer` | 教学图解与解说；可能同时使用 Canvas、Manim、Remotion 或 TTS。 |
| `3d_or_realtime_graphics` | Blender、Three.js、WebGL、程序三维等场景。 |
| `existing_source_transformation` | 真人原片、照片、歌曲、产品代码库或既有素材的改编与营销合成。 |
| `external_video_model` | Opus 策划／控制，外部视频模型生成主要运动画面；具体服务以逐案来源为准。 |
| `app_or_game_capture` | Opus 建网页、游戏或模拟器，X 视频主要是交互程序的演示。 |
| `mixed_or_not_established` | 多模型分工未讲清、主要渲染器证据不足，或比较／混合案例。 |

表中不含第三方 MP4、本机路径、账号凭据或未公开工程文件。原帖可能被作者删除或修改；本调查保存的媒体和检索收据只作本地审计，不随公开包分发。
