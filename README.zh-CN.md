# Awesome Claude Opus 5.5 Videos

[English](README.md) · 独立维护的、带原帖来源的精选列表与研究档案。

这份仓库收录**使用 Claude Opus 5.5 参与制作**的视频，并追问模型究竟负责哪一步。它不把“Opus 做视频”一律理解成模型直接生成视频像素，也不以成片外观猜测渲染器。

**更新截点：X 最后一次成功检索为 2026 年 9 月 25 日 22:47（北京时间），文件快照整理于 23:21。**共保存 49 组查询回执，48 次成功，另有一次中文检索遇到限流。语料有 1,242 条去重候选帖，其中 1,156 条有 MP4、共 1,180 个附件；Hypit 0.2.3 已对全部附件做媒体探测和九帧取样，SHA-256 去重后有 1,138 个不同文件。人工回读并整理了 160 条来源案例。候选含比较、转载和检索噪音，因此这些数字都不是 X 全站原创影片数，也不是各制作路径的占比。[检索覆盖与失败记录](docs/search-coverage.zh-CN.md)和[冻结快照](data/corpus-snapshot.json)保留了边界。

![Opus 5.5 视频的常见制作路径](assets/opus55-video-paths.png)

## 大家做了什么、长什么样

> 9 月 25 日增量更新：视觉模型 Gemini 3.8 Flash 根据九帧和帖文，对 1,138 个不同 MP4 作了领域／画风分类；它把 767 条判为“yes”、126 条判为“likely”与 Opus 有关。893 是**分类器判断**，不是经过逐项验证的原创数。每个视频仅取一个主领域和主画风，分类器用于整理主题与外观，**没有预测爆款概率**。数据见 [`data/domain-style.csv`](data/domain-style.csv)。已发布的 [X 长文](https://x.com/WangYeruo/article/2103278277536485482)与[47 秒视频版](https://x.com/WangYeruo/status/2103279925960876265)保留早上那一版截点。

![按领域分装的视频罐](assets/domains-jars.png)

下表只统计被判为 Opus 相关的 893 个“yes／likely”文件；每个文件只计一个主领域和主画风。

| 领域 | 数量 | 例子 |
|---|---:|---|
| 游戏和交互 demo | 207 | [@MengTo 日式水乡泛舟](https://x.com/MengTo/status/2102760783344189761) |
| AI 讲 AI 自己 | 167 | [@kevin_t_ngo 小女孩问 Claude 爱什么](https://x.com/kevin_t_ngo/status/2102437977435893771) |
| 广告和发布片 | 138 | [@deedydas 创业公司发布片](https://x.com/deedydas/status/2102787937482252537) |
| 科普讲解 | 116 | [@RyanSael 相机对焦模拟](https://x.com/RyanSael/status/2102591147927654847) |
| 故事短片 | 97 | [@AndrewOnXYZ 火星车短片](https://x.com/AndrewOnXYZ/status/2102512879258009818) |
| MV | 67 | [@other__reality](https://x.com/other__reality/status/2102514581684052169) |
| 艺术 | 36 | [@majidmanzarpour 像素巫师](https://x.com/majidmanzarpour/status/2102476258948927543) |
| 历史人文 | 34 | [@paji_a 关原之战 3D 沙盘](https://x.com/paji_a/status/2102581158487945540) |
| 梗、数据可视化和其他 | 31 | |

画风：3D 297、动态图形/界面 222、扁平卡通 141、像素 52、手绘 38、纸片拼贴 35、水墨沙画油彩 31、生成艺术 20、动漫 19、数学图解 15、写实 14、真人 5、复古终端/ASCII 4。游戏多为 3D；广告和科普偏动态图形；故事短片和 MV 较常用扁平卡通。每条只有一个主领域和主画风，可另有一个次要画风。

有条文明 Top 结果在采集时获 42,836 个赞，但 136.5 秒 MP4 与一条后来标注“Opus 5.5”的[转帖](https://x.com/_IamAlam/status/2103494816055345491)逐字节相同；较早的[原帖](https://x.com/IterIntellectus/status/2103212539895017864)只说“Claude”，没有给出版本。我们保留两条候选记录，但没有将该片列为已核实案例。互动量不能证明作者身份或模型版本。

## 先看六种路径

| 路径 | 代表案例 | 读它时要问什么 |
|---|---|---|
| **程序逐帧绘图** | [蚂蚁群落片与匹配源码](https://x.com/hanifproduktif/status/2102742924148830211)、[纸雕夜景与制作工程](https://x.com/makwired/status/2103008945220567166) | 画面是 Canvas／SVG／浏览器程序输出的吗？音轨或素材是否另有来源？ |
| **知识讲解** | [Manim 导数课](https://x.com/LinearUncle/status/2103128559174971663)、[VAE 数学片](https://x.com/ng169onX/status/2103183904563998809) | 旁白谁生成？公式与知识有没有独立核对？ |
| **三维与实时图形** | [Clearwater 与 WebGL 源码](https://x.com/Aurelien_Gz/status/2102786378282987591)、[建筑爆炸图](https://x.com/zdkiel_labs/status/2102722754172850310) | 是实时程序录屏、Blender 渲染，还是外部视频模型？ |
| **现有素材改编** | [83 秒真人口播线稿重制](https://x.com/AxtonLiu/status/2102827887732932956)、[13 条 take 挑剪](https://x.com/gregpr07/status/2102984873351037161)、[长委托 MV](https://x.com/donaldjewkes/status/2102801274173587569) | 原视频、音乐、产品代码库与人工表演贡献了什么？ |
| **外部视频模型编排** | [Opus＋Seedance](https://x.com/abxxai/status/2102775755646337530)、[多模型无限放大拼贴](https://x.com/koldo2k/status/2103129343253778767) | Opus 是写分镜／调度，还是实际出画面像素？ |
| **应用或游戏录屏** | [捡罐模拟器与在线演示](https://x.com/masaya_1980/status/2103115017755500561)、[交互海岛](https://x.com/Acemation_/status/2103150350211354966) | 交付物是 MP4 电影，还是可玩的程序及其录屏？ |

## 9 月 25 日新增案例

| 作品 | 为什么值得看、有哪些边界 |
|---|---|
| [15 秒简历 showreel - @ajith_io](https://x.com/ajith_io/status/2103449416325890146) | 作者公开了简短的 motion-design 提示词；九帧显示动态图形和片尾字卡。没有公开源工程，同一时段也出现多个相近的提示词变体。 |
| [中秋剪纸拼贴 - @NFT_Chen](https://x.com/NFT_Chen/status/2103380404791333144) | 作者说给了脚本和音乐，Nano Banana Pro 生成背景与纸纹，再用 p5.js／p5.brush 做动效、Node 合成音效。39.3 秒样片展现一只猫给月亮补缺口。 |
| [2076 年机器人故事 - @Hesamation](https://x.com/Hesamation/status/2103457566978162901) | 作者称故事、动画、音乐和音效都由 Opus 5.5 制作，视频用 JavaScript 编码。87.6 秒九帧呈现机器人在空城中的短篇叙事；音频与源码未独立核查。 |
| [手绘感动画 - @mablesjoseph](https://x.com/mablesjoseph/status/2103465246014746943) | 作者称用代码画笔触并合成音效，同时公开说不是 one-shot：163 次调用、约 6 小时 45 分、约 1.5 小时人工参与。这些 token、费用和时间数字均为自述。 |
| [白俄罗斯鸡尾酒教程 - @Sarut0biSasuke](https://x.com/Sarut0biSasuke/status/2103418429248069973) | 作者公开完整 prompt，并称提供手绘参考图后，一次提示生成 HTML／SVG／JavaScript 动画。Hypit 测得 X 预览为 30 秒；1080p 母版与酒谱准确性未核。 |
| [阿拉伯语配音动漫试播集 - @sbalhatlani](https://x.com/sbalhatlani/status/2103475507471806929) | 作者称 8 分 33 秒试播集有 211 个镜头、300 多张生成图、11 个角色、70 条阿拉伯语配音和 16 段音乐。Hypit 实测 X 预览 513.3 秒；制作统计和音质仍是作者口径。 |
| [Claude Code 会话回顾片 - @shneural](https://x.com/shneural/status/2103472385563459833) | 作者称 Opus 把 Claude Code 工作过程制成 56.3 秒视频，涉及 Python、Blender、音乐和 900 帧渲染；92 分钟、API 标价等价 81 美元均未拿到日志或账单核验。 |
| [JEV＋Opus 实时视觉器 - @TheViableEdge](https://x.com/TheViableEdge/status/2103494684374900862) | 作者称用 Opus 5.5 与 JEV 做实时图表、动效和主题切换，考虑用作社媒短片叠层。56.5 秒内容是工具演示录屏；JEV 的具体分工未披露，也没展示完整短片。 |

首页英文版的[精选案例](README.md#code-drawn-2d-and-motion-graphics)只挑制作路径和证据有代表性的作品。想筛选全部深读案例，请看[160 条公开索引](data/cases.csv)及[字段说明](docs/case-index-guide.zh-CN.md)。

## 研究材料

- [完整中文报告](docs/report.zh-CN.md)与[适合 X Article 的版本](docs/x-article.zh-CN.md)。
- [88 例提示词与制作条件矩阵](docs/prompt-matrix.zh-CN.md)、[七类可复用提示词模板](docs/prompt-playbook.zh-CN.md)。
- [方法和证据等级](docs/methodology.zh-CN.md)、[49 组查询回执](docs/search-coverage.zh-CN.md)、[MP4 文件属性](docs/media-profile.zh-CN.md)、[冻结计数](data/corpus-snapshot.json)。

本仓库不转载创作者的 MP4、音乐或完整第三方提示词，也不分发原始抓取记录与本地九帧图。案例说明区分**创作者披露**、**公开工程佐证**和**Hypit 对预览 MP4 的独立观察**。九帧无法验收全片运动、音质、知识正确性或隐藏调用。

欢迎按 [CONTRIBUTING.md](CONTRIBUTING.md) 提交原作者帖子、提示词来源、工程链接或更正。原创文字、标注和图示按 [CC BY 4.0](LICENSE) 开放；第三方内容权利仍归原权利人，详见 [THIRD_PARTY.md](THIRD_PARTY.md)。
