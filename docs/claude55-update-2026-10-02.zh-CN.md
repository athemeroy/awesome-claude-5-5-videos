# Claude 5.5 新作品与 Fable 灰度观察

后续：[10 月 3 日新增作品与取样目录](claude55-update-2026-10-03.zh-CN.md)。本页保留 10 月 2 日的原检查边界。

[English](claude55-update-2026-10-02.md) · [返回首页](../README.zh-CN.md) · 核对日期：2026-10-02（北京时间）

**判断：仓库扩展为 Awesome Claude 5.5 Videos 有必要。** Sonnet 5.5 已有独立作品；10 月 1–2 日，X 上也出现多位作者称自己正在使用 Fable 5.5 的作品和对照。应当收录这些有价值的原帖，同时保留模型身份的不确定性。

这里的 Fable 5.5 指**作者报告的版本／疑似 Fable 5.1 后台路由**。官方发布信息尚未确认该版本；这不能排除灰度测试。我们的检索也没有核实后台模型 ID。原帖、作品存在与版本身份是三个不同结论。

## 相比 Opus 5.5，大家具体觉得强在哪里？

| 维度 | 最直接的来源 | 能支持的结论与限制 |
|---|---|---|
| 主体与视觉层级 | [@mesmerlord 的同提示 motion graphics 对照](https://x.com/mesmerlord/status/2105758042830549235) | 作者认为两个疑似 Fable 输出都更集中地突出单一主体。作者不是 motion designer，属于同一作者的主观比较。 |
| 节奏、卡点和声音 | [同帖](https://x.com/mesmerlord/status/2105758042830549235)及[作者追加的 Opus 基线](https://x.com/mesmerlord/status/2105766824558174486) | 作者认为 Opus 虽然同为 15 秒，观感更急，声音也较弱；对 beat sync 的判断明确带疑问。尚无逐帧或听觉盲评。 |
| 发布片的整体完成感 | [@mesmerlord 的发布片双版本](https://x.com/mesmerlord/status/2105771088374288692) | 两边参考 Anthropic 的视频；作者更喜欢 Fable 的首轮结果。但没有明确完整的片序与模型对应，评论里也有反对意见，不能把网友猜的“第二条”当已核实标签。 |
| 场景细节与个性化风格 | [@TOPSTR1X 的 Minecraft 模型](https://x.com/TOPSTR1X/status/2105839618872738138)、[@blueemi99 的体素世界](https://x.com/blueemi99/status/2105804692811137242) | 作者认为比自己的 Opus 体验更好。前者提供了 BlockBench MCP 与懂其配色、建模习惯的自定义 skill；后者自己也标记“maybe”。不能归因于裸模型能力。 |
| 连续动作与跨风格一致性 | [@chetaslua 的超人穿越艺术风格](https://x.com/chetaslua/status/2105757136219504862) | 原帖与公开 Artifact 展示一种值得研究的连续变换路径；作者回复称纯代码，无 MCP、skill 或插件。此作品没有配对 Opus 基线，因此支持“能做什么”，暂不支持“强多少”。 |
| 简单提示下的创意发挥 | [@cherry_mx_reds 的圆点短片](https://x.com/cherry_mx_reds/status/2105825930799432073)及[另一条动画](https://x.com/cherry_mx_reds/status/2105816670896009224) | 作者称简短要求带来丰富结果，后一条报告约 15 分钟。未披露完整上下文、全部修改与渲染工程，不能直接标为可复现的一句话制作。 |

**目前最可信的优势线索是编排与时间设计：主体、节奏、音画关系；其次是细节与风格一致性。** 这是我们对上述作者反馈的归纳，不是多模型排名。最直接的 motion 与发布片对照都来自 @mesmerlord，不能当作两个独立测试者。

速度与成本没有形成同样明确的优势。发布片作者在[回复](https://x.com/mesmerlord/status/2105771524825522190)中说 Fable 较慢，且展示的首轮结果还没等它完全结束。[@SPAC89](https://x.com/SPAC89/status/2105783511433318451)比较的是疑似 Fable 5.5 XHigh 与 GPT-6.1 Sol Ultra，两者都约 30 分钟；其约 7% 与 1% 的周额度来自不同订阅档位，不能换算为模型价格比，也不是 Opus 对照。

## 值得直接打开的 Fable 作品

以下是**仅核对来源的新增条目**，不是新增 Hypit 深读案例；模型均为作者归属、后台未核实。

| 作者与原帖 | 制作角色／值得看什么 | 尚缺的证据 |
|---|---|---|
| [@mesmerlord：15 秒动态图形](https://x.com/mesmerlord/status/2105758042830549235) | 两个 Fable 候选输出与另帖 Opus 基线；视觉聚焦、卡点。 | 完整执行记录、统一 effort、全部轮次与账单。 |
| [@mesmerlord：模拟发布片](https://x.com/mesmerlord/status/2105771088374288692) | 同题双版本，参考 Anthropic 影片。作者明确说数字是编造的，不能引用片中指标。 | 后台身份、完整片序标签；允许调用 Codex 生成图片，作者另回复称看起来没有用。 |
| [@chetaslua：超人跨艺术风格](https://x.com/chetaslua/status/2105757136219504862) · [公开 Artifact](https://claude.ai/artifact/7F2XhpmgiuyxHKgQ9Vgr9Q) | 作者称纯代码；保持角色运动同时改变美术风格。 | 完整提示与模型调用记录；本轮未审计 Artifact 源代码。 |
| [@cherry_mx_reds：圆点的故事](https://x.com/cherry_mx_reds/status/2105825930799432073) | 从简单要求扩展为有角色与场景的短片；本轮浏览器检查了原帖及一个视频画面。 | 完整上下文、素材与工具来源、修改次数。 |
| [@cherry_mx_reds：另一条动画](https://x.com/cherry_mx_reds/status/2105816670896009224) | 作者报告约 15 分钟，适合观察简单提示的创意扩展。 | 完整提示上下文、制作过程与后台身份。 |
| [@TOPSTR1X：Minecraft 建模](https://x.com/TOPSTR1X/status/2105839618872738138) | BlockBench MCP + 自定义 Minecraft skill；个性化配色与模型细节。 | 同条件 Opus 输出、调用日志；应作为建模／程序展示看待。 |
| [@blueemi99：体素世界](https://x.com/blueemi99/status/2105804692811137242) | 作者认为细节显著优于 Opus，自行标记版本“maybe”。 | 同条件对照与确切模型身份。 |
| [@Chengzilhy：动作片提示](https://x.com/Chengzilhy/status/2105850801663234374) | 作者说 Fable 写提示，Seedance 2.5 参与出画面；研究镜头指令的作用。 | 完整提示、调用与剪辑过程；不能说 Fable 独立生成最终像素。 |

## Sonnet 5.5 也应进入目录

[官方发布](https://www.anthropic.com/claude-sonnet-5-5)确认 Sonnet 5.5 于 9 月 28 日上线。以下为作者披露，未加入旧统计：

| 原帖 | 用途与生产证据 | 边界 |
|---|---|---|
| [@kevin_t_ngo：彩虹的颜色](https://x.com/kevin_t_ngo/status/2105652774780420607) | 作者称动画每帧由 Sonnet 5.5 的代码绘制。 | 未核实完整代码、音频与执行记录。 |
| [@measure_plan：JavaScript 森林](https://x.com/measure_plan/status/2104634071628337167) | 作者称约 3,000 行 JS / WebGL shaders，实时程序画面与音效，没有外部素材或 3D 模型。 | 这是实时场景预览，不能默认算成剪辑完成的视频。 |
| [@petergyang：StarCraft 关卡及宣传剪辑](https://x.com/petergyang/status/2104736498151256303) | 作者明确使用 Sketchfab 的 SC2 模型与 Suno 音乐；Sonnet 做关卡与 sizzle reel。 | 外部模型资产和音乐均不能算作 Claude 自绘或自作曲。 |
| [@Tim_LB：TinyWorld 同题对照](https://x.com/Tim_LB/status/2104663105837932884) | 作者报告 Sonnet $0.96 / 10.8 分钟，Opus $4.79 / 22.7 分钟，认为质量接近。 | 单次作者实验，不能推广为固定省 80% 或两倍速度。 |
| [@AxtonLiu：五镜头 B-roll 对照](https://x.com/AxtonLiu/status/2105471099891068929) | 作者称卡片、图表、3D 接近，成本约 54%；墨线手绘较弱，Opus 38 轮、Sonnet 24 轮。 | 作者明确是单次实测；更少轮次可能同时省去因果与细节，不能自动等于更高效率。 |

这些作品使仓库扩展到 Claude 5.5 家族有实质内容，也提醒我们按制作任务比较，而不是把全部画风归为同一排行榜。

## 灰度证据怎么读

- [@chetaslua 的路由主张](https://x.com/chetaslua/status/2105733677003292983)、[@Mr_Salio 的试用报告](https://x.com/Mr_Salio/status/2105774088492916757)以及[@kimmonismus 的汇总](https://x.com/kimmonismus/status/2105740195832488447)说明灰度传闻与试用报告确实存在。
- “不开搜索是否认识 Tibo”是社区使用的启发式，**不是后台模型鉴定**。[@EuanSpencer00](https://x.com/EuanSpencer00/status/2105855237018009840)说自己在 Fable 5.1 时就能通过，[@kumouX](https://x.com/kumouX/status/2105849312693588326)也质疑这个推断。输出质量和模型自称版本同样不能独立确认模型身份。
- [原帖评论](https://x.com/rileybrown/status/2105853523862647081)也在追问究竟是猜测还是真实路由。可记录灰度主张，不必等官宣才关注作品；确认具体模型时则需要更直接的证据。

## 本次覆盖与统计边界

本轮通过已有 Mini OpenCLI 会话直接检索 X，保留本地查询和线程收据。四组 Fable 查询分别为精确词 live（30）、广义 Fable + since:2026-09-28 live（50）、精确词 top（50）、精确词 + Opus top（50）；Sonnet 视频 top 返回 30。五组都达到上限，结果有重叠，不能相加作为原创作品数量。广义 Fable 查询含游戏等噪音，top 未限制日期。

另读取 motion、发布片、Minecraft、超人及 B-roll 五个原帖线程；线程也可能截断。本轮浏览器核对了圆点、motion、发布片、超人及 Minecraft 的页面；播放中的截图只帮助确认画面，不构成全片技术审计或音频评分。新增来源与转帖按原帖 ID 区分，不以转帖次数衡量原创作品数量。

[来源账本](../data/claude55-source-review-2026-10-02.csv)记录模型归属、来源类型与限制。本页没有新增 `tile_ok`、原创验证或模型执行验证。**9 月 26 日 Opus 语料、168 条深读案例与图表分母全部保留。**
