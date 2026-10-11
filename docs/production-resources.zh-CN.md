# 制作路径与开源工程

[首页](../README.zh-CN.md) · [English](production-resources.md)

## 七种制作路径，先看画面

![Opus 参与制作视频的四种总体角色：写绘图代码、编辑已有素材、调度外部模型和制作录屏应用](../assets/production-paths.svg)

每张小图都链接原作者帖子。这七例是有目的地选出的制作路径样本，不是质量排名或各路径的总体比例。[14 条成对证据案例](evidence-examples.zh-CN.md)比较外观相近却输入、工具不同的作品；[168 条案例目录](cases-index.zh-CN.md)则让每条深读案例都有一张可见截图。

| 路径 | 看一个案例 | 需要核对什么 |
|---|---|---|
| 程序二维逐帧绘图 | <a href="https://x.com/hanifproduktif/status/2102742924148830211"><img src="../assets/case-thumbnails/2102742924148830211.webp" width="180" alt="蚂蚁群落动画截图"></a><br>[蚂蚁群落与对应源码](https://x.com/hanifproduktif/status/2102742924148830211) | 公开工程的场景、时序、素材是否与成片对应？ |
| 知识讲解 | <a href="https://x.com/LinearUncle/status/2103128559174971663"><img src="../assets/case-thumbnails/2103128559174971663.webp" width="180" alt="Manim 导数课截图"></a><br>[Manim 导数课](https://x.com/LinearUncle/status/2103128559174971663) | 公式、事实、旁白与既有教材是否逐项核对？ |
| 三维与实时图形 | <a href="https://x.com/Aurelien_Gz/status/2102786378282987591"><img src="../assets/case-thumbnails/2102786378282987591.webp" width="180" alt="Clearwater 浅水场景截图"></a><br>[Clearwater 与 WebGL 工程](https://x.com/Aurelien_Gz/status/2102786378282987591) | 这是实时程序录屏、三维渲染还是外部视频模型？ |
| 现有素材改编 | <a href="https://x.com/AxtonLiu/status/2102827887732932956"><img src="../assets/case-thumbnails/2102827887732932956.webp" width="180" alt="真人口播线稿重制截图"></a><br>[真人口播线稿重制](https://x.com/AxtonLiu/status/2102827887732932956) | 原表演、音轨或产品文件提供了什么？ |
| 外部视频模型编排 | <a href="https://x.com/abxxai/status/2102775755646337530"><img src="../assets/case-thumbnails/2102775755646337530.webp" width="180" alt="Opus 与 Seedance 合作样片截图"></a><br>[Opus＋Seedance](https://x.com/abxxai/status/2102775755646337530) | Opus 负责分镜调度，还是输出运动画面像素？ |
| 应用与游戏录屏 | <a href="https://x.com/masaya_1980/status/2103115017755500561"><img src="../assets/case-thumbnails/2103115017755500561.webp" width="180" alt="捡罐模拟器截图"></a><br>[捡罐模拟器](https://x.com/masaya_1980/status/2103115017755500561) | 交付物是否为可玩的程序，视频只是录屏？ |
| 混合或路径未确定 | <a href="https://x.com/leogao25/status/2102544078927741369"><img src="../assets/case-thumbnails/2102544078927741369.webp" width="180" alt="双模型物理机关对比截图"></a><br>[双模型物理机关对比](https://x.com/leogao25/status/2102544078927741369) | 输入、预算与评价方法是否可比？ |

单看截图无法判断完整制作链。我们区分作者披露、匹配的公开工程或提示词，以及对 X 预览片的独立取样观察。[制作适配指南](visual-effects-fit.zh-CN.md)给出任务与验收建议，这些例子没有构成模型成功率实验。

## 可复用的开源制作工程

| 预览与工程 | 能复用什么，截图展示什么 |
|---|---|
| <a href="https://lemomo-ai.github.io/lemo-opuscar/"><img src="../assets/resource-thumbnails/lemo-opuscar.webp" width="210" alt="Lemo-Opuscar 官方封面的多种影片风格拼贴"></a><br>[Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) · [作者原帖](https://x.com/lemomo_ai/status/2103811634565415152) | 当前[图鉴收录 43 种风格](https://lemomo-ai.github.io/lemo-opuscar/)，每种附样片与 `STYLE.md`；旧封面仍作预览。另有 [OPUSCAR 98](https://lemomo-ai.github.io/lemo-opuscar/opuscar98/#styles)，这是一支致敬 98 部最佳影片的合辑，并按获奖片逐项公开风格、画面、可复用提示与镜头说明。两组条目不是同一种计数。[导演指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/DIRECTOR.md)、[技术指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/TECHNIQUE.md)和[样片代码](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/crayon-book/demo/film.js)公开需求确认、分镜、确定性逐帧渲染、共用时间线与音频检查。作者称用 Canvas／WebGL 绘帧，没有调用视频生成模型；仓库本身无法逐片审计模型调用和成片质量。本次核对的[根许可文件](https://github.com/lemomo-ai/lemo-opuscar/blob/e3cb16f63768c68693ff0e15171d6e755457cc32/LICENSE)为 MIT；第三方素材按各自条款使用。 |
| <a href="https://github.com/francozanardi/papermotion#first-snow-snow"><img src="../assets/resource-thumbnails/papermotion.webp" width="210" alt="Papermotion 标为 Opus 5.5 的 snow 短片雪景"></a><br>[Papermotion](https://github.com/francozanardi/papermotion) | 可复用的纸片风动画引擎，含确定性物理、角色 rig、离线渲染、帧抓取、contact sheet 和音频检查。截图取自 README 标为 Opus 5.5 的 *snow*；*demo*、*rooftops*、*sea* 也标为 Opus 5.5，*light*、*embers* 则标为 GPT 6 Astra。应按逐片标注理解来源。 |
| <a href="https://x.com/servasyy/status/2104039075175182487"><img src="../assets/new-case-thumbnails/2104039075175182487.webp" width="210" alt="作者使用 ClaudeAnimationBase 制作的角色动画截图"></a><br>[ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) · [作者示例](https://x.com/servasyy/status/2104039075175182487) | 公开的 p5.js／p5.brush 动画底座，提供角色表情、分镜、contact sheet 和渲染流程。截图是 @servasyy 利用该底座制作的个人故事；开源底座是可复用输入，不能代表成片每个镜头的精确源码。 |
| <a href="https://x.com/makevoid/status/2103869704955900023"><img src="../assets/new-case-thumbnails/2103869704955900023.webp" width="210" alt="makevoid 的动态图形音乐视频截图"></a><br>[Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill) · [作者示例](https://x.com/makevoid/status/2103869704955900023) | Claude Code 插件与 Ruby 工具包，根据提供的歌曲和创意要求规划、组装音乐视频动态图形。其 p5.js 流程可调用外部 Fal 图像、视频和音频模型；截图来自多工具制作示例，不代表全部运动画面像素都由 Opus 生成。 |

四个资源的 README、文件目录与根许可于 **2026-10-11** 重新核查，均列 MIT；[版本与核查记录](../data/resource-review-2026-10-11.csv)固定本次来源。未运行这些项目的渲染任务，示例截图沿用此前取样。后两个作者示例也收录在[新案例证据页](new-cases-2026-09-27.zh-CN.md)。它们都在 9 月 26 日冻结语料之外，**不计入**上面的 1,401 个文件或 168 条深读案例。预览图来源和权利说明见 [THIRD_PARTY.md](../THIRD_PARTY.md)。

## 从哪个文件开始

| 想完成的任务 | 可直接阅读的入口 | 本次核查补充 |
|---|---|---|
| 给自己的故事选画风 | [Lemo-Opuscar 风格目录](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/README.md)与[制作 skill](https://github.com/lemomo-ai/lemo-opuscar/tree/main/plugin/skills/lemo-opuscar) | 插件将共用指南与每部影片工程分开。先交代故事、声音素材和是否需要分镜确认。 |
| 制作有纸片物理的场景 | [Papermotion 使用说明](https://github.com/francozanardi/papermotion#how-it-works) | 作者建议以模板为起点扩充场景组件；固定步长和随机种子用于逐帧复现。 |
| 延续一个手绘角色 | [ClaudeAnimationBase 动画指南](https://github.com/JohnHeibel/ClaudeAnimationBase/blob/main/ANIMATION_GUIDE.md) | 角色、镜头时间线与渲染器分开。作者说明水彩填充在无独显机器上可能渲染较慢。 |
| 配合一首现成歌曲做 MV | [Motion Graphics Music Video 快速开始](https://github.com/makevoid/motion-graphics-music-video-skill#quick-start) | 插件组装歌曲、角色与多类外部生成结果。Fal 生成开销应与 Claude 用量分开记录。 |

[研究结论](research-guide.zh-CN.md) · [全部文档](README.zh-CN.md)

## 10 月 11 日新增的制作资源

| 工程 | 可以复用什么 | 先了解的制作条件 |
|---|---|---|
| [3d-product](https://github.com/nicceasy/3d-product) · [原作者样片](https://x.com/nicceasy/status/2108018789468250448) | 从专利图、照片或 CAD 进入产品建模、构图、镜头、渲染和后期。[固定版本制作说明](https://github.com/nicceasy/3d-product/blob/b7e2025cbcb33ffd9625cd21ad506343b8b6e83d/README.md)。 | 样片作者披露九天制作、四 GPU 的 Octane 渲染，并使用第三方布景、标签画面与音乐。流程由人决定意图、镜头、剪辑、音乐与渲染启动。适合需要精细控制的产品片。 |
| [SwiftUI Agent Thinking Text Animations](https://github.com/amosgyamfi/SwiftUI-Agent-Thinking-Text-Animations) | 184 个 SwiftUI 文字动效的源码，可单独复用或修改。[固定版本说明](https://github.com/amosgyamfi/SwiftUI-Agent-Thinking-Text-Animations/blob/03736d2461fb24a33dfb31d4322ed6888adefd90/README.md)。 | 作者先做两个，称其余交由 Opus 5.5 扩展。它是界面动画组件库；184 是组件条目数，不是 184 支视频或已核实模型运行。 |
| [Video Production Skills](https://github.com/Ucmp0001/video-production-skills) | 11 个按工序组合的技能，连接资料、稿件、分镜、配音字幕和交付。[固定版本目录](https://github.com/Ucmp0001/video-production-skills/blob/ea682de6edf7520a73bdd3c69c0f1651729b6ca5/README.md)。 | 通用工作流模板，适用于支持 SKILL.md 的助手。声音、渲染和生成工具需另行配置；不把工具包本身当作模型成片能力证明。 |

这三项的 README 与根许可于 2026-10-11 核查，均为 MIT；没有安装或运行它们。加上前四项，[资源版本账本](../data/resource-review-2026-10-11.csv)共有七项。外部服务、付费渲染器和素材各用自己的条款。
