# Awesome Claude 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](README.md) · [全部来源](docs/library.zh-CN.md) · [参与维护](CONTRIBUTING.md)

精选使用 **Claude 5.5** 参与制作的视频、动画与可复用工程。覆盖 Opus、Sonnet、Haiku，以及作者报告的 Fable 灰度作品。原帖、模型角色、制作输入与证据分别记录。

## 目录

- [按模型找作品](#按模型找作品)
- [四个作品入口](#四个作品入口)
- [自己动手](#自己动手)
- [我们看到了什么](#我们看到了什么)
- [研究与数据](#研究与数据)
- [更新记录](#更新记录)
- [参与维护与许可](#参与维护与许可)

## 按模型找作品

<!-- collection-summary:start -->

截至 2026-10-10：**394 条去重来源帖**，其中 **194 条有九帧预览取样**。

| 模型浏览入口 | 来源帖 |
|---|---:|
| [Opus](docs/library.zh-CN.md#opus) | 282 |
| [Sonnet](docs/library.zh-CN.md#sonnet) | 45 |
| [Haiku](docs/library.zh-CN.md#haiku) | 15 |
| [Fable](docs/library.zh-CN.md#fable) | 65 |

[完整目录](docs/library.zh-CN.md) · [证据与作者分布](docs/collection-analysis.zh-CN.md) · [批次汇总](data/collection-summary.json)

<!-- collection-summary:end -->

多模型对照会进入多个分组，表格行不能相加。Opus 旧快照按研究背景归组；Fable 保留疑似路由标记。来源帖含回复与版本变体，不是独立影片数量。

[按制作路径看图](docs/cases-index.zh-CN.md) · [按内容与画风找案例](docs/domain-style-atlas.zh-CN.md) · [制作证据对照](docs/evidence-examples.zh-CN.md)

## 四个作品入口

| Opus | Sonnet | Haiku | Fable（作者报告） |
|:---:|:---:|:---:|:---:|
| [<img src="assets/case-thumbnails/2102786378282987591.webp" width="180" alt="Clearwater 水面">](https://x.com/Aurelien_Gz/status/2102786378282987591) | [<img src="assets/claude55-2026-10-10-followup/2107548992640880755.jpg" width="180" alt="建楼示意">](https://x.com/Solvaix/status/2107548992640880755) | [<img src="assets/claude55-2026-10-10-followup/2108089492016103775.jpg" width="180" alt="动效自荐片">](https://x.com/badboyfoxy/status/2108089492016103775) | [<img src="assets/claude55-2026-10-10-followup/2107958931230241037.jpg" width="180" alt="涂鸦人类史">](https://x.com/oalanicolas/status/2107958931230241037) |
| [Clearwater 水面](https://x.com/Aurelien_Gz/status/2102786378282987591) | [建楼示意](https://x.com/Solvaix/status/2107548992640880755) | [动效自荐片](https://x.com/badboyfoxy/status/2108089492016103775) | [涂鸦人类史](https://x.com/oalanicolas/status/2107958931230241037) |
| 实时 WebGL 图形 | 逐步建造的交互场景 | 文字、缓动与轨道图形 | 年代变化与持续角色 |

这是四种任务的入口，不是同提示模型排名。预览已做九帧取样，不能验证完整动态或模型调用。[新取样与制作说明](docs/maintenance-2026-10-10-followup.zh-CN.md)。

## 自己动手

### 制作路径

- [程序二维绘图](https://x.com/hanifproduktif/status/2102742924148830211)：蚁群动画，附匹配源码。
- [知识讲解](https://x.com/LinearUncle/status/2103128559174971663)：Manim 微积分课。
- [三维与实时图形](https://x.com/Aurelien_Gz/status/2102786378282987591)：Clearwater 水面模拟，附 WebGL 工程。
- [已有素材改编](https://x.com/AxtonLiu/status/2102827887732932956)：把真人讲述改成线稿动画。
- [外部视频模型](https://x.com/abxxai/status/2102775755646337530)：Opus 调度 Seedance。
- [应用与游戏录屏](https://x.com/masaya_1980/status/2103115017755500561)：收集罐子的模拟程序。
- [混合流程与对照](https://x.com/leogao25/status/2102544078927741369)：分屏物理模拟比较。

[选制作方法](docs/visual-effects-fit.zh-CN.md) · [路径图文与来源核对](docs/production-resources.zh-CN.md) · [提示模板](docs/prompt-playbook.zh-CN.md) · [提示／工作流矩阵](docs/prompt-matrix.zh-CN.md)

### 开源工程

- [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar)：画风库、导演指南与确定性 Canvas／WebGL 场景代码。
- [Papermotion](https://github.com/francozanardi/papermotion)：纸片动画引擎、角色骨架、物理与离线渲染。示例逐片标注模型。
- [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)：p5.js／p5.brush 角色动画、分镜与渲染底座。
- [Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill)：根据歌曲制作动效视频的 Claude Code 插件与 Ruby 工具包，可调用外部图像、视频和音频模型。

[工程预览、可复用文件与来源说明](docs/production-resources.zh-CN.md)。工程说明核对于 9 月 27 日，外部项目可能继续变化。

## 我们看到了什么

- **输入决定任务。**参考视频、角色设定、歌曲和已有工程，都会改变“模型做了什么”。
- **一条提示不等于一轮制作。**F1 作者称 Opus 反复拒绝中间结果；Taxtello 记录了五个版本。
- **看整项任务费用。**金门桥对照中，作者报告 Haiku 的费用为 Opus 的 72.0%；F1 的执行端占团队费用的 64.2%。这不是模型通用排名。
- **动画可信感与事实正确分开。**Sonnet 建楼作者明确说明顺序是编排的，未做工程计算。

[制作方式与费用分析](docs/workflow-analysis.zh-CN.md) · [取样覆盖与作者分布](docs/collection-analysis.zh-CN.md)

## 研究与数据

- [统一来源 CSV](data/collection-index.csv)：所有批次、模型角色、原帖与证据入口。
- [收录与证据分析](docs/collection-analysis.zh-CN.md)：模型标签、取样覆盖、账号分布与批次统计。
- [冻结快照分析](docs/snapshot-analysis.zh-CN.md)、[完整统计](docs/statistics.zh-CN.md)与[配色研究](docs/color-modes.zh-CN.md)。
- [方法](docs/methodology.zh-CN.md)、[媒体属性](docs/media-profile.zh-CN.md)与[图表复现](docs/chart-generation.md)。

9 月 26 日文件快照仍为 1,401 个逐字节不同的文件，分类纳入 1,119 个。游戏、广告与 AI 自谈占 57.7%；动态图形／界面与三维渲染占 60.2%。后续来源不混入这套文件分母。

取样说明可见内容；作者披露说明制作主张。后台身份、完整动态、费用与音乐原创未逐条独立核实。仓库不分发原始 MP4。本项目独立维护。

## 更新记录

- [2026-10-10 补搜与分析](docs/maintenance-2026-10-10-followup.zh-CN.md)。
- [2026-10-10 首轮维护与 Haiku](docs/maintenance-2026-10-10.zh-CN.md)。
- [2026-10-03 分类作品目录](docs/claude55-update-2026-10-03.zh-CN.md)。
- [2026-10-02 Fable 报告与 Sonnet 对照](docs/claude55-update-2026-10-02.zh-CN.md)。
- [2026-09-27 新增工作流](docs/new-cases-2026-09-27.zh-CN.md)。

## 参与维护与许可

[提交原帖或可复用工程](CONTRIBUTING.md)。优先收录不同制作方式、清楚输入或可检查源码。欢迎纠错与补充原作者。

原创文字与图表使用 [CC BY 4.0](LICENSE)。链接作品与截图归原作者，按各自条款使用。[第三方素材](THIRD_PARTY.md)。
