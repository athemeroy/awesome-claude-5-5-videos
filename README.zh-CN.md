# Awesome Claude 5.5 Videos

[English](README.md) · 独立维护的、带原帖来源的精选列表与研究档案。

这份仓库收录**使用 Claude 5.5 参与制作**的视频与动画，覆盖 Opus 5.5、Sonnet 5.5，并单独标记社区报告的下一代 Fable 灰度作品。我们追问模型负责的是编写绘图代码、调度外部模型、改编已有素材，还是制作被录屏的应用。已有深读语料通过 Hypit 检查可取得的 X 预览片；新增仅来源条目则明确区分作者披露与独立媒体检查。

## 10 月 2 日更新：Fable 灰度作品

X 上已有作者持续发布自己称为 **Fable 5.5、疑似由 Fable 5.1 自动路由**的动画。这里记录的是试用与路由主张，尚未核实公开发布或后台模型身份。[新增作品与比较页](docs/claude55-update-2026-10-02.zh-CN.md)链接同提示 Opus 对照、作者回复、Sonnet 作品，以及获取资格的不确定性。

目前最具体的优势反馈是**主体更集中、节奏更从容、音画同步更好、场景细节更丰富**。最直接的动态图形对照来自同一位作者；其他作品的工具与输入不同，暂不能推出 Fable 5.5 在质量、速度或成本上全面领先。新增条目仅核对来源，不计入下方冻结的 Opus 统计。

## 从这里开始

- **看最新模型作品：**[10 月 2 日 Claude 5.5 更新](docs/claude55-update-2026-10-02.zh-CN.md)，含暂定 Fable 灰度作品与 Sonnet 来源。
- **看图找原帖：**[168 条双语案例目录](docs/cases-index.zh-CN.md)给每条深读案例附一张取样截图、原帖与来源语言的说明。
- **选方法、复用工程：**看[制作适配指南](docs/visual-effects-fit.zh-CN.md)、[七种路径的图文案例](#七种制作路径先看画面)与[开源制作工程](#可复用的开源制作工程)。
- **对照制作证据：**[14 条成对案例](docs/evidence-examples.zh-CN.md)比较外观相近却输入、工具不同的作品。
- **看数据与分析：**本页先给关键结论，[领域 × 画风图谱](docs/domain-style-atlas.zh-CN.md)、[配色研究](docs/color-modes.zh-CN.md)与[可复算统计页](docs/statistics.zh-CN.md)保留完整表格与方法。
- **看截点后的作品：**[七条新增案例](docs/new-cases-2026-09-27.zh-CN.md)单独标明日期与证据。

## 冻结快照：每个数字数的是什么

最后一次成功的 X 检索是 **2026 年 9 月 26 日 21:05（北京时间）**，文件快照整理于 21:53。56 组保存的查询中，55 组成功或使用缓存，较早另有一组遇到限流；[检索覆盖记录](docs/search-coverage.zh-CN.md)说明查询边界。截点之后的新增案例单独列出，不改写这些冻结计数。

![冻结语料分层计数，区分帖子、附件、不同文件、分类标签和有目的挑选的深读案例](assets/corpus-overview.svg)

| 数量 | 计数单位 | 公开来源与边界 |
|---|---|---|
| 1,511 | 去重候选帖 | [冻结快照](data/corpus-snapshot.json)；包含转帖、比较与检索噪音。 |
| 1,419 | 带 MP4 的候选帖 | [冻结快照](data/corpus-snapshot.json)；一条帖子可能附多个文件。 |
| 1,449 | 取得的 MP4 附件 | [冻结快照](data/corpus-snapshot.json)；Hypit 0.2.3 已全部探测并各取九帧。 |
| 1,401 | 报告为 SHA-256 不同的文件 | [分类 CSV](data/domain-style.csv)逐文件一行；源文件与哈希未公开。 |
| 1,119 | 分类器标为 `yes` 或 `likely` 的文件 | [分类 CSV](data/domain-style.csv)；下文领域、画风和配色分析的分母。 |
| 168 | 有目的挑选的来源帖深读案例 | [案例 CSV](data/cases.csv)；为检查制作路径与证据而选择，并非随机抽样。 |

**1,449 − 1,401 = 48** 个附件是逐字节相同的额外副本。同一作品的不同编码仍可能计为不同文件。这些计数不能当作独立创作者、已核实的 Opus 运行次数或 X 全站原创作品数。[统计口径与可复算范围](docs/statistics.zh-CN.md#先分清统计单位)说明哪些数字能由公开数据独立复核。

## 检索样本中的内容与画风

Gemini 3.8 Flash 根据 1,401 个文件的帖文与九帧取样分类：与 Opus 相关的判断为 **980 个 `yes`、139 个 `likely`、282 个 `no`**，每文件另取一个主领域与主画风。标签用于整理样本，不能证明模型调用与作者身份。本节领域、画风与配色图使用 **1,119 个 `yes`／`likely` 文件**。[分类数据](data/domain-style.csv) · [分类边界](docs/statistics.zh-CN.md)。

### 主要领域，以及随阈值变化的头名

![十一种主领域的不同文件计数，区分 yes 与额外纳入的 likely](assets/domain-labels.svg)

游戏／交互 230 个、广告／发布片 215 个、AI 自谈 201 个，前三类合计 **646 个，占纳入文件的 57.7%**。前两类的次序随标签纳入规则改变：

| 纳入标签 | 文件分母 | 游戏／交互 | 广告／发布片 | 第一名 |
|---|---:|---:|---:|---|
| `yes` | 980 | 187（19.1%） | 191（19.5%） | 广告／发布片 |
| `yes` + `likely` | 1,119 | 230（20.6%） | 215（19.2%） | 游戏／交互 |

翻转来自分类阈值，不能解释为时间趋势；两种阈值也不是实际 Opus 使用量的上下界。

![十三种主画风的不同文件计数，区分 yes 与 likely](assets/style-labels.svg)

动态图形／界面 350 个、三维渲染 324 个，合计 **674 个，占 60.2%**。只计 `yes` 时，两者仍居前二，分别为 308 和 265 个。一支视频可能混合多种外观，这里只数分类器指定的主画风。

### 内容与画风最集中的交叉格

![一千一百一十九个文件在十一种主领域与十三种主画风上的交叉计数](assets/domain-style-heatmap.svg)

最大的两格是**游戏／交互 × 三维渲染：161 个（14.4%）**，以及**广告／发布片 × 动态图形／界面：154 个（13.8%）**，合计 315 个、占 **28.2%**。每个纳入文件只进入一格，零表示纳入的 `yes`／`likely` 文件中该格为空。[可点击的二维图谱](docs/domain-style-atlas.zh-CN.md)连接格子、截图案例与原帖；[统计页](docs/statistics.zh-CN.md)保留更多交叉格。

图谱选例使用[另行刷新的 9 月 27 日互动量](data/case-engagement-refresh-2026-09-27.csv)：168 条深读帖中取得 **166 条的精确赞数与精确帖子浏览数**。采集时段为 11:50–12:32（UTC），并非同一瞬间。互动量只描述这组精选帖的可见传播，不能证明作者身份或成片质量。

### 同一类别，存在多套配色

![十一种内容领域的彩色像素占比中位数与四分位区间](assets/color-study/color-modes-overview.svg)

逐视频的**彩色像素占比中位数**，音乐视频为 **45.5%（77 个文件）**，广告／发布片为 **17.6%（215 个文件）**。指标统计 HSV 饱和度至少 0.25、明度至少 0.15 的取样像素，描述彩色面积，不是审美评分。[逐视频测量值](data/color-study/per-video-color-vectors.csv)可用于重算。

[![四类视频的类内配色模式，色条按像素占比绘制，同日点赞另计帖子样本量](assets/color-study/color-modes-highlight.svg)](docs/color-modes.zh-CN.md)

按颜色在类别内分组，**13 种画风中有 11 种**、**11 个领域中有 10 个**分出 2–3 种模式。动态图形／界面就分为**深色中性 198 个**和**浅色中性 152 个**文件。色卡段宽是该模式的取样像素占比，而不是视频数量占比。[配色研究](docs/color-modes.zh-CN.md)提供 53 组模式、完整图谱与测量规则。

点赞没有参与分组。动态图形深／浅两组的同日点赞中位数分别为 **50 与 104**，每组仅 **22 条帖子**；53 个模式中只有 **20 个**有至少五条 9 月 27 日精确点赞记录。作者受众、主题、帖龄与平台分发都会影响互动，这组观察无法检验配色对点赞的因果效果。[模式总表](data/color-study/color-mode-summary.csv) · [点赞口径](docs/color-modes.zh-CN.md#点赞口径与数据)。

### 预览片长也受选例方式影响

| 样本与单位 | n | 预览中位数（秒） | 第 25–75 百分位（秒） |
|---|---:|---:|---:|
| 全部分类文件 | 1,401 | 39.20 | 21.91–77.07 |
| 深读案例主帖 MP4 | 168 | 52.37 | 29.76–117.04 |

深读集合的预览较长，但两行的计数单位和选择规则不同，差异不能归因于制作路径。这里测量的是可取得的 X 预览片，可能与上传母版不同。[可复算片长统计](docs/statistics.zh-CN.md)列明计算规则。

![一百六十八条深读案例按七种制作路径统计的 X 预览片长中位数与四分位区间](assets/preview-duration.svg)

深读案例中，知识讲解片的预览中位数最长，为 **102.28 秒**；另六条路径的中位数为 **24.76–51.79 秒**。圆点为中位数，粗线为第 25–75 百分位区间。片长不能证明制作耗时、模型速度、成本或路径成功率。

## 七种制作路径，先看画面

![Opus 参与制作视频的四种总体角色：写绘图代码、编辑已有素材、调度外部模型和制作录屏应用](assets/production-paths.svg)

每张小图都链接原作者帖子。这七例是有目的地选出的制作路径样本，不是质量排名或各路径的总体比例。[14 条成对证据案例](docs/evidence-examples.zh-CN.md)比较外观相近却输入、工具不同的作品；[168 条案例目录](docs/cases-index.zh-CN.md)则让每条深读案例都有一张可见截图。

| 路径 | 看一个案例 | 需要核对什么 |
|---|---|---|
| 程序二维逐帧绘图 | <a href="https://x.com/hanifproduktif/status/2102742924148830211"><img src="assets/case-thumbnails/2102742924148830211.webp" width="180" alt="蚂蚁群落动画截图"></a><br>[蚂蚁群落与对应源码](https://x.com/hanifproduktif/status/2102742924148830211) | 公开工程的场景、时序、素材是否与成片对应？ |
| 知识讲解 | <a href="https://x.com/LinearUncle/status/2103128559174971663"><img src="assets/case-thumbnails/2103128559174971663.webp" width="180" alt="Manim 导数课截图"></a><br>[Manim 导数课](https://x.com/LinearUncle/status/2103128559174971663) | 公式、事实、旁白与既有教材是否逐项核对？ |
| 三维与实时图形 | <a href="https://x.com/Aurelien_Gz/status/2102786378282987591"><img src="assets/case-thumbnails/2102786378282987591.webp" width="180" alt="Clearwater 浅水场景截图"></a><br>[Clearwater 与 WebGL 工程](https://x.com/Aurelien_Gz/status/2102786378282987591) | 这是实时程序录屏、三维渲染还是外部视频模型？ |
| 现有素材改编 | <a href="https://x.com/AxtonLiu/status/2102827887732932956"><img src="assets/case-thumbnails/2102827887732932956.webp" width="180" alt="真人口播线稿重制截图"></a><br>[真人口播线稿重制](https://x.com/AxtonLiu/status/2102827887732932956) | 原表演、音轨或产品文件提供了什么？ |
| 外部视频模型编排 | <a href="https://x.com/abxxai/status/2102775755646337530"><img src="assets/case-thumbnails/2102775755646337530.webp" width="180" alt="Opus 与 Seedance 合作样片截图"></a><br>[Opus＋Seedance](https://x.com/abxxai/status/2102775755646337530) | Opus 负责分镜调度，还是输出运动画面像素？ |
| 应用与游戏录屏 | <a href="https://x.com/masaya_1980/status/2103115017755500561"><img src="assets/case-thumbnails/2103115017755500561.webp" width="180" alt="捡罐模拟器截图"></a><br>[捡罐模拟器](https://x.com/masaya_1980/status/2103115017755500561) | 交付物是否为可玩的程序，视频只是录屏？ |
| 混合或路径未确定 | <a href="https://x.com/leogao25/status/2102544078927741369"><img src="assets/case-thumbnails/2102544078927741369.webp" width="180" alt="双模型物理机关对比截图"></a><br>[双模型物理机关对比](https://x.com/leogao25/status/2102544078927741369) | 输入、预算与评价方法是否可比？ |

单看截图无法判断完整制作链。我们区分作者披露、匹配的公开工程或提示词，以及对 X 预览片的独立取样观察。[制作适配指南](docs/visual-effects-fit.zh-CN.md)给出任务与验收建议，这些例子没有构成模型成功率实验。

## 公开提示词能说明什么

![五条公开制作委托的可见字符数，从一百七十二到一万七千六百六十四字符](assets/prompt-lengths.svg)

五条有来源的公开委托从 **172 到 17,664 个可见字符**，涵盖开放式要求、技术规格以及参考视频加逐秒分镜。字符数只量帖子中可见的文本，不记录全部素材、前文、迭代或模型成本；五个选例也不构成提示词长度的总体分布。[逐条计数与原帖](data/visible-prompt-lengths.json) · [88 例提示词／制作条件矩阵](docs/prompt-matrix.zh-CN.md) · [可复用模板](docs/prompt-playbook.zh-CN.md)。

复用一份要求时，应一并核对它需要的输入、渲染路径与验收项。相似的公开措辞也不能证明独立执行：一条后发 MV 委托的独特连续五词序列中，**87.0%** 与较早委托重合。[词序列对照记录](data/prompt-overlap.json)保留了算法与两条原帖，无法仅由重合判断谁读过或复制过什么。

## 可复用的开源制作工程

| 预览与工程 | 能复用什么，截图展示什么 |
|---|---|
| <a href="https://lemomo-ai.github.io/lemo-opuscar/"><img src="assets/resource-thumbnails/lemo-opuscar.webp" width="210" alt="Lemo-Opuscar 官方封面的多种影片风格拼贴"></a><br>[Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) · [作者原帖](https://x.com/lemomo_ai/status/2103811634565415152) | 官方封面预览[39 种风格图鉴](https://lemomo-ai.github.io/lemo-opuscar/)；每种风格附样片与 `STYLE.md`。[导演指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/DIRECTOR.md)、[技术指南](https://github.com/lemomo-ai/lemo-opuscar/blob/main/TECHNIQUE.md)和[样片代码](https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/crayon-book/demo/film.js)公开需求确认、分镜、确定性逐帧渲染、共用时间线与音频检查。作者称用 Canvas／WebGL 绘帧，没有调用视频生成模型；仓库本身无法逐片审计模型调用和成片质量。[许可文件](https://github.com/lemomo-ai/lemo-opuscar/blob/main/LICENSE)将代码列为 MIT，指南、风格说明和影片列为 CC BY 4.0，第三方素材另按各自许可。 |
| <a href="https://github.com/francozanardi/papermotion#first-snow-snow"><img src="assets/resource-thumbnails/papermotion.webp" width="210" alt="Papermotion 标为 Opus 5.5 的 snow 短片雪景"></a><br>[Papermotion](https://github.com/francozanardi/papermotion) | 可复用的纸片风动画引擎，含确定性物理、角色 rig、离线渲染、帧抓取、contact sheet 和音频检查。截图取自 README 标为 Opus 5.5 的 *snow*；*demo*、*rooftops*、*sea* 也标为 Opus 5.5，*light*、*embers* 则标为 GPT 6 Astra。应按逐片标注理解来源。 |
| <a href="https://x.com/servasyy/status/2104039075175182487"><img src="assets/new-case-thumbnails/2104039075175182487.webp" width="210" alt="作者使用 ClaudeAnimationBase 制作的角色动画截图"></a><br>[ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) · [作者示例](https://x.com/servasyy/status/2104039075175182487) | 公开的 p5.js／p5.brush 动画底座，提供角色表情、分镜、contact sheet 和渲染流程。截图是 @servasyy 利用该底座制作的个人故事；开源底座是可复用输入，不能代表成片每个镜头的精确源码。 |
| <a href="https://x.com/makevoid/status/2103869704955900023"><img src="assets/new-case-thumbnails/2103869704955900023.webp" width="210" alt="makevoid 的动态图形音乐视频截图"></a><br>[Motion Graphics Music Video skill](https://github.com/makevoid/motion-graphics-music-video-skill) · [作者示例](https://x.com/makevoid/status/2103869704955900023) | Claude Code 插件与 Ruby 工具包，根据提供的歌曲和创意要求规划、组装音乐视频动态图形。其 p5.js 流程可调用外部 Fal 图像、视频和音频模型；截图来自多工具制作示例，不代表全部运动画面像素都由 Opus 生成。 |

四个资源于 2026-09-27 核查；后两个作者示例也收录在[新案例证据页](docs/new-cases-2026-09-27.zh-CN.md)。它们都在 9 月 26 日冻结语料之外，**不计入**上面的 1,401 个文件或 168 条深读案例。预览图来源和权利说明见 [THIRD_PARTY.md](THIRD_PARTY.md)。

## 冻结截点之后的新案例

9 月 26 日 21:05（北京时间）检索截止后，又出现七条有视频的原作者帖子；[单独的增量案例页](docs/new-cases-2026-09-27.zh-CN.md)给每条附一张取样截图和证据边界。它们**没有计入**上面的 1,401 个文件或 168 条案例。建议先看这三条：

| 截图与原帖 | 为什么值得看 |
|---|---|
| <a href="https://x.com/JurgenPloeger/status/2104131805175844923"><img src="assets/new-case-thumbnails/2104131805175844923.webp" width="210" alt="手工原片与 Opus 代码重建片的画面对照"></a><br>[手工发布片与代码重建片](https://x.com/JurgenPloeger/status/2104131805175844923) | 作者提供旧片和 Figma 文件，再逐轮调整重建片节奏；对照让现有输入可见。 |
| <a href="https://x.com/servasyy/status/2104039075175182487"><img src="assets/new-case-thumbnails/2104039075175182487.webp" width="210" alt="方块角色演绎个人故事的动画截图"></a><br>[复用 ClaudeAnimationBase 的个人故事](https://x.com/servasyy/status/2104039075175182487) | 已有开源动画底座和作者的人生素材，都是制作路径的重要输入。 |
| <a href="https://x.com/arambarnett/status/2104011150471917838"><img src="assets/new-case-thumbnails/2104011150471917838.webp" width="210" alt="数字与图表组成的动态图解截图"></a><br>[带数据槽校验的数字短片](https://x.com/arambarnett/status/2104011150471917838) | 作者描述禁止模型随意填写屏幕数字的约束；约束代码尚未公开。 |

9 月 25–26 日补入的旧案例都在[带图案例目录](docs/cases-index.zh-CN.md)，可按制作路径查看 168 条人工深读原帖。

## 研究材料

- [完整中文报告](docs/report.zh-CN.md)与[适合 X Article 的版本](docs/x-article.zh-CN.md)。
- [88 例提示词与制作条件矩阵](docs/prompt-matrix.zh-CN.md)、[七类可复用提示词模板](docs/prompt-playbook.zh-CN.md)。
- [方法和证据等级](docs/methodology.zh-CN.md)、[56 组查询回执](docs/search-coverage.zh-CN.md)、[MP4 文件属性](docs/media-profile.zh-CN.md)、[冻结计数](data/corpus-snapshot.json)。

图表从公开数据重绘。先运行 `python3 -m pip install -r requirements-charts.txt`，再用 Python 运行 `scripts/generate_intro_charts.py`、`scripts/generate_stat_charts.py` 和 `scripts/generate_color_charts.py`；三个脚本的 `--check` 均纳入 CI。详见[图表生成与复核步骤](docs/chart-generation.md)。

本仓库不转载创作者的 MP4、音乐或完整第三方提示词，也不分发原始抓取记录与九帧总览图。页面只用单张低分辨率取样截图帮助辨认画风，每张都回链创作者原帖；截图仍属原权利人，不受本仓库 CC BY 许可覆盖。案例说明区分**创作者披露**、**公开工程佐证**和**Hypit 对预览 MP4 的独立观察**。九帧无法验收全片运动、音质、知识正确性或隐藏调用。

欢迎按 [CONTRIBUTING.md](CONTRIBUTING.md) 提交原作者帖子、可复用开源工程、提示词来源或更正。原创文字、标注和图示按 [CC BY 4.0](LICENSE) 开放；第三方内容权利仍归原权利人，详见 [THIRD_PARTY.md](THIRD_PARTY.md)。
