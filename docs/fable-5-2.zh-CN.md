# Claude Fable 5.2 视频生态专题报告（2026-11-16）

[首页](../README.zh-CN.md) · [完整目录](library.zh-CN.md#fable-5-2) · [English](fable-5-2.md) · [来源账本 CSV](../data/source-review-2026-11-16-fable52.csv)

## 背景：从 10 月灰度传闻到 11 月 9 日正式发布

2026 年 10 月初，社区曾出现多起疑似“Fable 5.5”灰度路由的视频案例（已保留在 [Fable 早期灰度分组](library.zh-CN.md#fable-pre-release) 中）。**2026 年 11 月 9 日**，Anthropic 正式发布 **[Claude Fable 5.2](https://www.anthropic.com/claude/fable)**（与 Mythos 5.2 同日发布）：

- **官方定位**：面向复杂工程、3D/硬件/动态设计（Design for 3D, hardware, and motion）与长周期 Agent 编排的旗舰模型，支持构建交互式 3D 世界、物理仿真、带音频的代码动画及教学视频。
- **定价与速度**：API 价格为 **$8 / 百万输入 tokens、$40 / 百万输出 tokens**（较 Fable 5.1 的 $10 / $50 下降 20%），缓存读取 $0.20 / 百万 tokens；Fast mode 提速最高 2.5 倍（$16 / $80）。
- **核心边界**：包含网络安全与生物安全防护（Safeguards），触发时可能回退至较弱模型；默认需 30 天安全留存（支持 EFS 的企业客户除外）。

本轮更新共收录 **173 条 Fable 5.2 来源帖**（发布于 2026-11-09 至 2026-11-13，来源于公开社区账本交叉核验），全部附带可核验的 X 原帖链接、视频时长与作者分类。

## 173 条 Fable 5.2 案例分布

| 类别 | 数量 | 占比 | 典型表现 |
|---|---:|---:|---|
| 动态图形（motion） | 56 | 32.4% | 粒子片、纯着色器视频、日文歌词动效、品牌秀场、LilyPond 管风琴赋格 |
| 三维场景（3d） | 45 | 26.0% | Blender 建模与渲染、照片重建 3D/AR 建筑漫游、Three.js 物理仿真 |
| 交互与游戏（interactive） | 30 | 17.3% | 开放世界驾驶、第三人称探索、3D 篮球赛、创意 UI 物理开关 |
| 宣传与发布片（promo） | 15 | 8.7% | 发布会风格产品片、竖版 App 预告、自定义风格迁移 Reel |
| 模型同题对比（comparison） | 15 | 8.7% | Fable 5.2 vs Opus 5.5 / GPT-6 Astra 的耗时、费用与一次通过率对照 |
| 科普讲解（explainer） | 12 | 6.9% | 对称性数学讲解、水彩科普、长达 10 分钟的日文发布解析片 |

- **时长分布**：最短 5 秒，**中位数 30 秒**，最长 **10 分 15 秒（615 秒）**。
- **工具栈趋势**：明确提及 **Blender**（18 条）、**AR / 空间重建**（16 条）、**Motion**（14 条）、**Three.js / WebGL**（14 条）、**像素 / 体素风**（16 条），以及 **Shader / LilyPond / 语音合成** 等纯代码音频技术。

## 关键发现：Fable 5.2 相比 Opus 5.5 强在哪里？

从 15 条同题对比（`comparison`）和社区实测披露中，可以看到三个较一致的工程信号（均为作者披露，未做独立审计）：

1. **一次成片率与复杂度上限显著提高**
   - [@leohuanfang 的三连复现对比](https://x.com/leohuanfang/status/2120024307573137874)：帆船场景任务中，Fable 5.2 耗时 **27 分 46 秒、花费 $7.59**，首次打开即零报错通过；Opus 5.5 则需要 3 次尝试和 50 分钟。
   - [@Trace_AR 的照片重建 AR 漫游](https://x.com/Trace_AR/status/2121284000232714559)：仅用 8 张午餐店照片，数小时内构建出完整 3D 建筑模型与 AR 漫游体验。
2. **自主迭代与耗时/费用结构变化**
   - [@motion_so 的 Motion 同题对比](https://x.com/motion_so/status/2120029008809361891)：Fable 5.2 会进行更深度的多轮自检，耗时 2 小时 35 分、花费 **$88.09**；Opus 5.5 耗时更久（3 小时+）但花费 $17.03。可见 Fable 5.2 在复杂编排下输出 token 密度更高，需要结合任务预算控制 Effort。
3. **跨模态协调（音频 + 着色器 + 镜头）**
   - [@tankazunori0914](https://x.com/tankazunori0914/status/2120012834461646927) 用纯代码同时生成着色器画面与合成音乐；[@aug5thmusic](https://x.com/aug5thmusic/status/2119907891419480107) 用 LilyPond 编写出 2 分 05 秒的 D 小调管风琴赋格。

## 17 个作者公开的 Prompt 索引

以下 17 条案例附带了作者公开的原始提示词链接，适合直接作为制作模板参考：

| 作者 | 类别 | 时长 | 作品标题 | 原帖与 Prompt 来源 |
|---|---|---:|---|---|
| @czzzzzzJ_ | promo | 298s | 发布会风格的中文 AI 知识站宣传片 | [查看原帖](https://x.com/czzzzzzJ_/status/2120023093464682817) |
| @himanshutwtxs | motion | 15s | 一条提示词的动效设计师作品集：节奏、缓动、形状与字体 | [查看原帖](https://x.com/himanshutwtxs/status/2120017106804900304) |
| @wshuyi | 3d | 28s | 剑齿虎在金色草原上捕猎野牛 | [查看原帖](https://x.com/wshuyi/status/2120014892040417720) |
| @takamasa045 | motion | 53s | 只要声音就够了：黑、米白、橙配色的日文歌词动态视频 | [查看原帖](https://x.com/takamasa045/status/2120014216753262816) |
| @tankazunori0914 | motion | 64s | 从一个点到一个世界：只用代码的着色器视频与合成音乐 | [查看原帖](https://x.com/tankazunori0914/status/2120012834461646927) |
| @ericmaskfr | interactive | 135s | 迈阿密风格开放世界犯罪游戏，含改装店和计时赛 | [查看原帖](https://x.com/ericmaskfr/status/2119910195325481026) |
| @itssotsot | interactive | 95s | 玩具房第三人称探索小游戏 | [查看原帖](https://x.com/itssotsot/status/2119909017216491720) |
| @aug5thmusic | motion | 125s | 用 LilyPond 写成的 D 小调管风琴赋格 | [查看原帖](https://x.com/aug5thmusic/status/2119907891419480107) |
| @kaif9998 | motion | 15s | 终端里的模型选择菜单变成一段动态文字作品集 | [查看原帖](https://x.com/kaif9998/status/2119903824848761287) |
| @heypearlai | motion | 15s | 自我展示的动效设计作品集：文字、形状与界面循环 | [查看原帖](https://x.com/heypearlai/status/2119903760529113116) |
| @kplikethebird | 3d | 30s | 逾越节的耶路撒冷：从圣殿到阶梯街的 3D 漫游 | [查看原帖](https://x.com/kplikethebird/status/2119900775727902732) |
| @maxt3chno | comparison | 21s | GPT-6 Astra 对比 Fable 5.2 在 Blender 里制作僵尸鹰怪物 | [查看原帖](https://x.com/maxt3chno/status/2119896698281467952) |
| @joshvlc | interactive | 19s | Harbor City Arena：潮汐队对阵余烬队的 3D 篮球游戏 | [查看原帖](https://x.com/joshvlc/status/2119894656221958575) |
| @al_maxgo | promo | 28s | FBPlot：足球数据图表应用的竖版预告片 | [查看原帖](https://x.com/al_maxgo/status/2119891197317591040) |
| @danteeonsol | 3d | 30s | 夜色中的 51 区：飞碟降落，外星人向人群打招呼 | [查看原帖](https://x.com/danteeonsol/status/2119887623070077213) |
| @N1njaCodex | interactive | 11s | Deep Dive Switch：从海面一路沉到深渊的拨动开关 | [查看原帖](https://x.com/N1njaCodex/status/2119883560937001387) |
| @hello_amani | motion | 36s | amani/studio：从蓝图网格线生成的镀铬 Logo 揭幕动画 | [查看原帖](https://x.com/hello_amani/status/2119873980786237842) |

## 说明与限制

- 本批次 173 条来源于公开社群整理与交叉核验，标记为 `source-only`（尚未对视频帧进行本地九帧抽样检查）。
- 所有耗时、费用与一次成片声明均为原作者发布内容，未做独立审计。
