# Awesome Claude 5.5 Videos [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

[English](README.md) · [完整作品目录](docs/library.zh-CN.md) · [全部文档](docs/README.zh-CN.md)

精选 Claude 5.5 参与制作的视频、动画和开源工程。覆盖 Opus、Sonnet、Haiku，以及作者报告的 Fable 作品。看案例、学制作，也用原帖与数据研究这些作品的共同特点。

**[找作品](#作品入口) · [看研究结论](#研究结论) · [自己制作](#自己制作) · [数据与维护](#数据与维护) · [最近更新](#最近更新)**

<a id="按模型找作品"></a>

## 作品入口

<!-- collection-summary:start -->

截至 2026-10-11：**424 条去重来源帖**，其中 **199 条有九帧预览取样**。

| 模型浏览入口 | 来源帖 |
|---|---:|
| [Opus](docs/library.zh-CN.md#opus) | 301 |
| [Sonnet](docs/library.zh-CN.md#sonnet) | 54 |
| [Haiku](docs/library.zh-CN.md#haiku) | 21 |
| [Fable](docs/library.zh-CN.md#fable) | 68 |

[完整目录](docs/library.zh-CN.md) · [证据与作者分布](docs/collection-analysis.zh-CN.md) · [批次汇总](data/collection-summary.json)

<!-- collection-summary:end -->

多模型对照会进入多个分组，表格行不能相加。来源帖含回复与版本变体；Opus 旧快照按研究背景归组，Fable 保留作者报告标记。

<a id="四个作品入口"></a>

| Opus | Sonnet | Haiku | Fable（作者报告） |
|:---:|:---:|:---:|:---:|
| [<img src="assets/claude55-2026-10-11/2108018789468250448.jpg" width="180" alt="Braun 唱盘产品片">](https://x.com/nicceasy/status/2108018789468250448) | [<img src="assets/claude55-2026-10-10-followup/2107548992640880755.jpg" width="180" alt="建楼示意">](https://x.com/Solvaix/status/2107548992640880755) | [<img src="assets/claude55-2026-10-11/2108934243636408790.jpg" width="180" alt="西湖素材宣传片">](https://x.com/shengtang135754/status/2108934243636408790) | [<img src="assets/claude55-2026-10-10-followup/2107958931230241037.jpg" width="180" alt="涂鸦人类史">](https://x.com/oalanicolas/status/2107958931230241037) |
| [Braun 唱盘产品片](https://x.com/nicceasy/status/2108018789468250448) | [建楼示意](https://x.com/Solvaix/status/2107548992640880755) | [西湖素材宣传片](https://x.com/shengtang135754/status/2108934243636408790) | [涂鸦人类史](https://x.com/oalanicolas/status/2107958931230241037) |
| 三维渲染与人的导演决策 | 逐步建造的交互场景 | 素材剪辑、章节与字幕 | 年代变化与持续角色 |

这是四种任务的入口，不是同提示模型排名。预览已做九帧取样，不能验证完整动态或模型调用。取样说明：[10 月 10 日](docs/maintenance-2026-10-10-followup.zh-CN.md) · [10 月 11 日](docs/maintenance-2026-10-11.zh-CN.md)。

[按内容与画风看截图](docs/domain-style-atlas.zh-CN.md) · [按制作路径看案例](docs/cases-index.zh-CN.md) · [最新补搜](docs/maintenance-2026-10-11.zh-CN.md)

<a id="我们看到了什么"></a>

## 研究结论

下面的内容与配色结果来自 **2026-09-26 的 1,119 个纳入文件**。制作条件分析另用原帖、作者回复和精选案例。完整计算与来源见[研究导读](docs/research-guide.zh-CN.md)。

### 内容与画风：游戏偏三维，广告偏动态图形

[![十一种内容与十三种画风的交叉计数；游戏与三维、广告与动态图形最集中](assets/domain-style-heatmap.svg)](docs/domain-style-atlas.zh-CN.md)

游戏／交互中 **70.0%** 归为三维渲染（161/230）；广告／发布片中 **71.6%** 归为动态图形／界面（154/215）。只计较明确的 `yes` 标签时，这两个搭配仍占各自领域的多数。

教育与故事的画风更分散。教育最大的动态图形组占 37.4%，故事最大的扁平卡通组占 33.0%。选制作方案时，可以参考相近内容的多种画风。[交叉图谱与案例](docs/domain-style-atlas.zh-CN.md) · [分母与阈值](docs/statistics.zh-CN.md)

### 配色：同一类别里，深浅两套方案都常见

[![四类作品的类内配色模式；色条宽度表示取样像素占比，点赞记录另有日期和帖子分母](assets/color-study/color-modes-highlight.svg)](docs/color-modes.zh-CN.md)

350 个动态图形／界面文件中，深色中性组有 **198 个**，浅色中性组有 **152 个**。只给整个类别一张平均色卡，会掩盖这两套设计选择。

音乐视频的彩色像素占比中位数为 45.5%，广告为 17.6%。这可以帮助选择视觉参考。图中的点赞来自 9 月 27 日另一组帖子观察，不能用来判断哪套配色更有效。[完整配色研究](docs/color-modes.zh-CN.md)

### 制作流程：输入、修改轮次和总费用一起看

本轮新增的[三种流程](docs/workflow-analysis.zh-CN.md#10-月-11-日补充把自动化放回完整制作过程)把分工说得更具体：Haiku 西湖片公开素材、配音和逐段计时要求；Opus＋9 个 Sonnet 的文章片经历时长与配音修正；三维唱盘片作者披露九天制作与多个由人决策的环节。

| 发现 | 来源实例 | 对自己制作的启发 |
|---|---|---|
| 简短请求也可能有丰富输入 | 混合媒体任务提供 skill、参考素材与逐帧安排；北京宣传片任务要求素材视频和外部旁白。 | 一并准备素材、声音和交付要求。[输入分析](docs/workflow-analysis.zh-CN.md#输入不同任务也不同) |
| 一条人类提示可以触发多轮修改 | F1 作者披露 Opus 多次驳回中间结果；五条公开委托长度从 172 到 17,664 字符。 | 记录人类提示与内部审查，保留可复用的制作条件。[提示与条件矩阵](docs/prompt-matrix.zh-CN.md) |
| 看整项任务的账，而非只看模型单价 | 金门桥作者报告 Haiku $2.19、Opus $3.04；F1 的 Haiku 执行端占团队报告费用的 64.2%。 | 将修改、工具和外部素材费用一起列出。任务不同，不能拼成模型排名。[费用分析](docs/workflow-analysis.zh-CN.md#每-token-便宜不等于整项任务同比例便宜) |

[五个研究方向与实用结论](docs/research-guide.zh-CN.md) · [模型标签与取样覆盖图](docs/collection-analysis.zh-CN.md) · [片长、提示长度与完整快照图表](docs/snapshot-analysis.zh-CN.md)

<a id="自己动手"></a>

## 自己制作

### 先选任务，再选制作路径

| 想做什么 | 从哪个案例开始 | 可复用说明 |
|---|---|---|
| 二维代码动画 | [蚁群动画与对应源码](https://x.com/hanifproduktif/status/2102742924148830211) | [零外部视觉素材模板](docs/prompt-playbook.zh-CN.md#1-零外部视觉素材的代码动画) |
| 知识讲解 | [Manim 微积分课](https://x.com/LinearUncle/status/2103128559174971663) | [内容与视觉验收](docs/visual-effects-fit.zh-CN.md) |
| 三维或实时场景 | [Clearwater 水面与 WebGL 工程](https://x.com/Aurelien_Gz/status/2102786378282987591) | [三维场景模板](docs/prompt-playbook.zh-CN.md#4-三维场景把建场景与拍电影分开) |
| 改编已有素材 | [真人口播变线稿](https://x.com/AxtonLiu/status/2102827887732932956) | [输入与制作证据对照](docs/evidence-examples.zh-CN.md) |
| 调用外部视频模型 | [Opus 调度 Seedance](https://x.com/abxxai/status/2102775755646337530) | [导演与生成工具的分工](docs/production-resources.zh-CN.md) |
| 做可交互作品 | [捡罐模拟程序](https://x.com/masaya_1980/status/2103115017755500561) | [交付物与检查条件](docs/production-brief.zh-CN.md) |

### 可复用的开源工程

- [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar)：43 种画风、导演与技术指南；另有 [OPUSCAR 98 风格与镜头资料](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#styles)。
- [Papermotion](https://github.com/francozanardi/papermotion)：纸片动画模板、角色、物理与离线渲染，示例逐片标注模型。
- [ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)：p5.js／p5.brush 角色、分镜时间线与渲染底座。
- [Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill)：围绕歌曲组装 MV 的插件，可调用外部图像、视频和音频服务。

- [3d-product](https://github.com/nicceasy/3d-product)：产品三维影片流程，包含构图预览、渲染与后期，并保留人的导演决策。
- [SwiftUI 文字动效集](https://github.com/amosgyamfi/SwiftUI-Agent-Thinking-Text-Animations)：184 个界面动效组件；作者先做两个，再让 Opus 扩展。
- [Video Production Skills](https://github.com/Ucmp0001/video-production-skills)：11 个资料、分镜、配音字幕和交付技能，可按工序选择。

七个工程的 README 与许可于 **2026-10-11** 复核。[预览、起步文件与版本记录](docs/production-resources.zh-CN.md) · [制作任务单](docs/production-brief.zh-CN.md) · [七类提示模板](docs/prompt-playbook.zh-CN.md)

<a id="研究与数据"></a>

## 数据与维护

当前收藏按**来源帖**更新；9 月 26 日内容与配色研究按**文件**统计。冻结研究共有 1,401 个逐字节不同的文件，其中 1,119 个纳入分类分析；168 条来源帖经过深读。预览取样说明可见内容，作者披露说明制作主张。

| 想核对什么 | 入口 |
|---|---|
| 当前所有来源、模型标签与取样状态 | [统一 CSV](data/collection-index.csv) · [收录分析](docs/collection-analysis.zh-CN.md) |
| 内容、画风、片长和颜色的计算 | [统计口径](docs/statistics.zh-CN.md) · [配色方法](docs/color-modes.zh-CN.md) |
| 如何复现或继续更新 | [维护指南](docs/maintenance.md) · [图表生成](docs/chart-generation.md) · [贡献说明](CONTRIBUTING.md) |

所有分析方向、日期更新和原始长文都能从[文档总入口](docs/README.zh-CN.md)找到。

<a id="更新记录"></a>

## 最近更新

- [2026-10-11：新来源与项目重构](docs/maintenance-2026-10-11.zh-CN.md)。
- [2026-10-10：补搜、Haiku 与制作方式分析](docs/maintenance-2026-10-10-followup.zh-CN.md)。
- [2026-10-10：首轮维护与 Haiku](docs/maintenance-2026-10-10.zh-CN.md)。
- [全部更新归档](docs/README.zh-CN.md#更新归档)。

## 参与维护与许可

[提交原帖、工程或纠错](CONTRIBUTING.md)。优先补充不同制作方式、明确输入与可检查源码。

原创文字与图表使用 [CC BY 4.0](LICENSE)。作品与截图归各自作者，权利和来源见 [THIRD_PARTY.md](THIRD_PARTY.md)。本项目独立维护，不分发原始 MP4。
