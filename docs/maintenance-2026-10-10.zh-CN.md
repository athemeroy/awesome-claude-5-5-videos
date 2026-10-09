# 10 月 10 日：维护与近期来源复核

[首页](../README.zh-CN.md) · [English](maintenance-2026-10-10.md)

本轮执行 6 组搜索，6 组成功，返回 300 行，6 组达到 50 条上限。去重并纳入引用帖后，共保留 344 个候选 ID。本次精选新增 18 条来源帖，其中两段 Haiku 预览各取九帧并人工查看，其余为来源复核。

检索窗口从 10 月 3 日开始。最新排序与结果上限不能覆盖整个窗口。候选含转帖、宣传与玩笑；未入选不代表虚假。模型身份、费用与一次生成主张沿用作者说明，未独立核实。讲解视频的科学主张也未因此得到验证。

[搜索记录](../data/claude55-search-coverage-2026-10-10.csv) · [候选处理](../data/claude55-candidate-audit-2026-10-10.csv) · [来源账本](../data/claude55-source-review-2026-10-10.csv)

## 新增来源

| 原帖 | 作者报告的模型 | 制作说明 |
|---|---|---|
| [水墨动画与合成声音](https://x.com/gkxspace/status/2108506384711213108) · @gkxspace | Opus 5.5 | 作者说明纸张纤维、笔毛、角色骨架，以及用 Python 合成的古琴和箫声。 |
| [零零年代 Flash 风格动画](https://x.com/YanqingCheng/status/2108296567166042404) · @YanqingCheng | Reported Fable 5.5 | 作者请求一段带有零零年代 Flash 风格的怀旧动画。 |
| [随风响应的 JavaScript 骨架动画](https://x.com/adam_fresko/status/2107637770873417894) · @adam_fresko | Reported Fable 5.5 | 作者称动画完全用 JavaScript 实现，逆运动学随风响应，并指出文字仍有错误。 |
| [使用购买素材的游戏演示](https://x.com/Rush3rx/status/2108607656776876368) · @Rush3rx | Opus 5.5 + Tripo P2 | 作者说明约二十条提示、两天制作，以及 Tripo P2 和先前购买的素材。 |
| [讲解视频制作工具对照](https://x.com/avthar/status/2108603075174797490) · @avthar | Opus 5.5 + ElevenLabs | 作者测试 HyperFrames、Remotion 与 Manim，配合 ElevenLabs 旁白，并称视频含提示与结果。 |
| [Taxtello 宣传片第五版](https://x.com/daniel_haida/status/2108595684236755242) · @daniel_haida | Opus 5.5 | 作者说明 Canvas 绘图、NumPy 合成声音、五个版本和单独的批评 agent。 |
| [浏览器卡丁车与剪辑录屏](https://x.com/cafunify/status/2108581004432830683) · @cafunify | Opus 5.5 + Sonnet 5.5 | 作者称主要用 Sonnet 制作 Three.js 卡丁车，另由 Sonnet 游玩、录制和剪辑宣传视频。 |
| [三条提示的动效对照](https://x.com/mmmarcus_ai/status/2108550192882503797) · @mmmarcus_ai | Opus 5.5 / Sonnet 5.5 | 作者展示黏土风短片、辣酱广告和应用发布片，先 A/B 播放，再公布模型。 |
| [用 Three.js 绘制天坛祈年殿](https://x.com/shunshu32385143/status/2108480534254944719) · @shunshu32385143 | Opus 5.5 | 作者说明用 Three.js 分阶段线描、上色，并用代码合成古筝配乐。 |
| [三维踏板应力讲解](https://x.com/chang_/status/2108458503367200908) · @chang_ | Opus 5.5 + ElevenLabs | 作者说明五分钟 Three.js 踏板总成、着色器应力图、断裂动画与双语字幕，旁白用 ElevenLabs。 |
| [产品工程与参考视频作为输入](https://x.com/zhongerxin/status/2108532720414699696) · @zhongerxin | Opus 5.5 | 作者提供项目文件夹和参考视频地址，称只修改一次，并指出细节与排版粗糙。 |

## 两段 Haiku 预览

| 五七五自我介绍 | 三维鹈鹕 |
|:---:|:---:|
| [<img src="../assets/haiku-2026-10-10/2107985954648867292.jpg" width="300" alt="取样可见 FAST、LIGHT、SHARP 段落、深浅配色变化与大号五七数字。">](https://x.com/lemomo_ai/status/2107985954648867292) | [<img src="../assets/haiku-2026-10-10/2108156768023118268.jpg" width="300" alt="取样可见鹈鹕在水边骑车，鸟、自行车持续出现，镜头位置发生变化。">](https://x.com/xueyu1125/status/2108156768023118268) |
| 40.054 秒；有音轨 | 12.000 秒；有音轨 |

取样显示不同的制作任务：前者用文字、图形和配色组织段落；后者保持鹈鹕和自行车，并改变镜头位置。九帧不能判断连续运动或卡点准确性。原帖中的生成时间是制作耗时，不是视频片长。

[截图来源](../assets/haiku-2026-10-10/frames.csv) · [素材权利](../THIRD_PARTY.md)

## Haiku 视频与对照

| 原帖 | 作者报告的模型 | 制作说明 |
|---|---|---|
| [围绕五七五节奏的自我介绍](https://x.com/lemomo_ai/status/2107985954648867292) · @lemomo_ai | Haiku 5.5 | 作者说明自我介绍按五七五的小节组织，画面指示灯与段落对应。 |
| [《道程》诗歌短动画](https://x.com/tatsuyer/status/2108033626017587627) · @tatsuyer | Haiku 5.5 | 作者称仅通过聊天，用 Haiku 制作受高村光太郎《道程》启发的六点五秒动画。 |
| [三维鹈鹕骑自行车](https://x.com/xueyu1125/status/2108156768023118268) · @xueyu1125 | Haiku 5.5 | 作者称 Haiku 下载 Blender，再用 FFmpeg 输出三维鹈鹕骑车 MP4。 |
| [Haiku 发布动画](https://x.com/leo114119/status/2108033133002227738) · @leo114119 | Haiku 5.5 | 作者称让 Haiku 制作自己的发布动画，并认为创意弱于自己的 Fable 结果。 |
| [作者的 Haiku 剪辑示例](https://x.com/pruthvithinks/status/2108594104133423276) · @pruthvithinks | Haiku 5.5 | 作者将剪辑归于 Haiku，并报告费用为八十八美分。 |
| [Three.js 雪景球对照](https://x.com/buildwithrajath/status/2108571974222197055) · @buildwithrajath | Haiku 5.5 / GPT-6 Luna | 作者用相同提示和高思考强度比较 Three.js 雪景球；耗时与费用为作者记录。 |
| [CSS 折纸动画对照](https://x.com/UgoBit_/status/2107953568993141074) · @UgoBit_ | Haiku 5.5 / Sonnet 5.5 / GPT models | 作者用相同三维 CSS 折纸提示和中等思考强度比较四个模型。 |

## 首页整理

中英文首页改为目录、精选作品、制作方法、收录统计和更新记录。原有统计图与分析保留在[快照分析](snapshot-analysis.zh-CN.md)，完整路径和工程说明保留在[制作资源页](production-resources.zh-CN.md)。9 月 26 日文件统计保持原日期与分母。

组织形式参考：

- [sindresorhus/awesome](https://github.com/sindresorhus/awesome) — category navigation.
- [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) — concise entries and separate discovery/archive pages.
- [enaqx/awesome-react](https://github.com/enaqx/awesome-react) — grouped reusable resources.
