# 10 月 11 日更新：素材、分工与修改过程

[首页](../README.zh-CN.md) · [完整目录](library.zh-CN.md) · [English](maintenance-2026-10-11.md)

新增 **30 条来源帖**，其中 **6 条涉及 Haiku**。其中五段预览已做九帧取样。收录时间是本轮发现日期，并不表示这些作品均在今天发布。来源帖不等于独立影片。

## 值得带回制作流程的三件事

- **先列输入和分工。** [西湖宣传片](https://x.com/shengtang135754/status/2108934243636408790)让 Haiku 处理素材、配音和字幕；[Follow the Crumbs](https://x.com/sarit69976/status/2109072935998681436)由多个图像、视频和音乐工具共同完成。
- **记录修正，才能解释“一条提示”。** [Opus 与九个 Sonnet](https://x.com/agito20211021/status/2108852733792891379)的文章转视频包括内部返工；[另一支作品集短片](https://x.com/MaciejPoczek/status/2108924468110176457)明确用了七十一条消息。
- **可控的三维流程仍有制作成本。** [3d-product 的固定版本说明](https://github.com/nicceasy/3d-product/blob/b7e2025cbcb33ffd9625cd21ad506343b8b6e83d/README.md)列出九天制作、四 GPU、人工阶段决策与外部素材。公开技能提供流程，不能据此把整支片的时间和成本归零。

## 五段取样预览

| 预览与原帖 | 取样观察 |
|---|---|
| [<img src="../assets/claude55-2026-10-11/2108934243636408790.jpg" width="240" alt="西湖素材剪辑宣传片">](https://x.com/shengtang135754/status/2108934243636408790)<br>西湖素材剪辑宣传片 · 107.067 s | 取样可见风景素材、章节角标和中文字幕。未独立核实地理位置与素材许可。 |
| [<img src="../assets/claude55-2026-10-11/2108951077991362922.jpg" width="240" alt="Thermal Courier 游戏预告对照">](https://x.com/jeffbruchado/status/2108951077991362922)<br>Thermal Courier 游戏预告对照 · 15.061 s | 取样可见上下排列的两版气球场景、模型与费用标签、变化的地形和预告文字。 |
| [<img src="../assets/claude55-2026-10-11/2108852733792891379.jpg" width="240" alt="九个场景工人的文章转视频">](https://x.com/agito20211021/status/2108852733792891379)<br>九个场景工人的文章转视频 · 61.419 s | 取样可见竖屏日文文字、图表、数字与照片场景。取得的预览为六十一点四一九秒。 |
| [<img src="../assets/claude55-2026-10-11/2108912164253602187.jpg" width="240" alt="Low Tide Shuffle 节奏游戏">](https://x.com/blueemi99/status/2108912164253602187)<br>Low Tide Shuffle 节奏游戏 · 30.059 s | 取样可见 Low Tide Shuffle 的四条海豹轨道、变化的提示与分数标记。 |
| [<img src="../assets/claude55-2026-10-11/2108018789468250448.jpg" width="240" alt="Braun PS550 产品片与 3d-product 技能">](https://x.com/nicceasy/status/2108018789468250448)<br>Braun PS550 产品片与 3d-product 技能 · 97.963 s | 取样可见唱盘、唱臂与房间，从局部特写变化到不同光线的较宽景别。 |

每段预览均由 ffprobe 探测，再用 ffmpeg 快速定位取得九帧人工查看，五段均有音轨。这里只能确认取样画面；完整播放、音画同步、模型调用和音乐来源未独立验证。这些预览不进入九月二十六日冻结的文件级统计。

## 新增来源

| 原帖 | 模型／制作角色 | 制作说明 |
|---|---|---|
| [西湖素材剪辑宣传片](https://x.com/shengtang135754/status/2108934243636408790) · @shengtang135754 | Haiku 5.5 + Pixabay footage + Volcengine narration | 作者报告费用四元，公开了素材检索、逐段配音计时、章节角标、字幕和音乐要求。这是已有素材的编辑流程。 取样可见风景素材、章节角标和中文字幕。未独立核实地理位置与素材许可。 |
| [作者指出翅膀缺陷的蜜蜂](https://x.com/letdarky/status/2108936071409000539) · @letdarky | Haiku 5.5 | 作者称 Max 档约六分钟完成，并明确指出部分翅膀表现不对。 |
| [蜜蜂对照的 Sonnet 后续](https://x.com/letdarky/status/2108992110598697376) · @letdarky | Sonnet 5.5 / Haiku 5.5 | 同一作者补充 Sonnet Max 的蜜蜂结果，并更喜欢这一版；未给出 Sonnet 的实测耗时。 |
| [发光软杆对照](https://x.com/noclipepe/status/2109076746524045447) · @noclipepe | Haiku 5.5 / GPT-6 Luna / Gemini 3.8 Flash | 作者比较变刚度软杆：Haiku Medium 为三十一分二十五秒、约零点六九美元；Luna Medium 为十分三十六秒、约零点一六美元；Gemini High 为四分钟、约零点一美元。档位标签不同，物理正确性未验证。 |
| [Thermal Courier 游戏预告对照](https://x.com/jeffbruchado/status/2108951077991362922) · @jeffbruchado | Opus 5.5 / Sonnet 5.5 | 作者称画面与声音均写在一个 HTML 文件内，没有外部素材。Opus 为四十七分三十四秒、六百六十二行、估算七点四七美元；Sonnet 为四十四分二十八秒、一千三百四十三行、估算四点八九美元。原帖展示两版预告对照。 取样可见上下排列的两版气球场景、模型与费用标签、变化的地形和预告文字。 |
| [Chroma Sweep 画廊潜入预告](https://x.com/jeffbruchado/status/2109041668595069182) · @jeffbruchado | Opus 5.5 / Sonnet 5.5 | 作者让两个模型完成相同的光线投射游戏与预告任务，报告耗时分别为五十二分二十五秒、五十一分十二秒，估算 API 费用分别为七点二九、五点三六美元。 |
| [End of Humanity：叙事与生成镜头分工](https://x.com/nonodigitalart/status/2109038670611100001) · @nonodigitalart | Sonnet 5.5 narrative + Google Flow / Omni Flash video | 作者明确由 Sonnet 写叙事，由 Google Flow 中的 Omni Flash 生成视频，披露了不同模型的制作分工。 |
| [After Effects 粒子插件原型](https://x.com/learson_move/status/2108906894379344339) · @learson_move | Sonnet 5.5 + After Effects + DeepGlow | 作者称 Sonnet 编写了粒子插件原型，并搭配 DeepGlow；还需微调。原帖有三段预览，本条只核对来源。 |
| [九个场景工人的文章转视频](https://x.com/agito20211021/status/2108852733792891379) · @agito20211021 | Opus 5.5 lead + Sonnet 5.5 scene workers + external media tools | 作者由 Opus 负责策划、台本和设计，九个 Sonnet 并行制作场景，搭配 HyperFrames、Gemini 音乐与配音、Whisper 和生成图片。披露的内部修正包括误读演出指令、八十四秒缩至六十一秒，以及导出后的淡出处理。 取样可见竖屏日文文字、图表、数字与照片场景。取得的预览为六十一点四一九秒。 |
| [Follow the Crumbs 多工具短片](https://x.com/sarit69976/status/2109072935998681436) · @sarit69976 | Opus 5.5 direction/editing + Magnific + Seedance 2.5 + ElevenLabs | 作者将故事、台本、工具调用和剪辑归于 Claude；角色使用 Magnific，镜头使用 Higgsfield 上的 Seedance，音乐使用 ElevenLabs。 |
| [韩文日代码动画](https://x.com/danialnamkr/status/2109070380711481599) · @danialnamkr | Opus 5.5 | 作者称这段韩文主题动画由 Opus 写代码完成，没有使用视频模型。本次没有核实片中的历史陈述。 |
| [可交互的江户切子玻璃](https://x.com/mizugame_22/status/2109067132839579693) · @mizugame_22 | Opus 5.5 + Three.js | 作者描述了 Three.js 交互体验：选择纹样并点击后，玻璃出现刻纹，阴影中出现光纹，还能通过链接分享。 |
| [Falcon 9 着陆可视化](https://x.com/konstantinsaifo/status/2109061641027678483) · @konstantinsaifo | Opus 5.5 | 作者报告约六小时、五十九美元 API 费用，使用地形和发动机参数制作着陆可视化，并提供点火时机控制。所述输入不能证明仿真准确。 |
| [想象版 Starbase 海岸扩展](https://x.com/konstantinsaifo/status/2109059572619002267) · @konstantinsaifo | Opus 5.5 | 作者明确说明场址布局为想象版本、间距有压缩，且建立在已有引擎之上。回复给出 V2 约两小时七分钟、三百五十次工具调用、五十一美元；另加十九美元制作光照、烟尘和音乐。 |
| [一百八十四种 SwiftUI 文字动画](https://x.com/amos_gyamfi/status/2109056620831649927) · @amos_gyamfi | Opus 5.5 + human SwiftUI seed examples | 作者先制作两个示例，再让 Opus 扩展一百八十二种。公开 MIT 仓库确认了总量与人工示例的来源。 |
| [Low Tide Shuffle 节奏游戏](https://x.com/blueemi99/status/2108912164253602187) · @blueemi99 | Opus / creator-reported Fable 5.5 | 作者将游戏和声音归于 Opus 与 Fable 5.5，并提供可玩链接。未独立核实 Opus 版本与 Fable 后台身份。 取样可见 Low Tide Shuffle 的四条海豹轨道、变化的提示与分数标记。 |
| [清明上河图虹桥场景](https://x.com/AISuperDomain/status/2108878175531110875) · @AISuperDomain | creator-reported Fable 5.5 | 发帖者将可探索的虹桥场景标为 Fable 5.5，并描述了视角切换。没有披露完整制作输入或后台身份。 |
| [Braun PS550 产品片与 3d-product 技能](https://x.com/nicceasy/status/2108018789468250448) · @nicceasy | Opus 5.5 + scripted 3D rendering + external assets/audio | 作者描述了由人导演的三维流程。固定版本 README 写明示范片花了九天、使用四块 GPU，并在五个阶段需要人工决策；也列出授权布景、Midjourney 标签图、外部音效与 Suno 音乐。 取样可见唱盘、唱臂与房间，从局部特写变化到不同光线的较宽景别。 |
| [以参考视频为输入的动画技能](https://x.com/ishuagra02/status/2108250410221781009) · @ishuagra02 | Opus 5.5 + video-by-reference skill | 作者发布研究参考视频画面、声音、剪辑与节奏的流程。回复要求附参考视频，也说明原始 Claude 会话未保存。公开流程并非原始制作记录的完整副本。 |
| [十一个可组合视频制作技能](https://x.com/eazymoney888/status/2107876636133847244) · @eazymoney888 | Opus 5.5 within an assistant-coordinated video workflow | 作者链接到 MIT 技能包，覆盖素材索引、台本、分镜、动画、配音字幕计时和交付。README 明确方法与检查工具之外，还要自行配置媒体工具和模型账号。 |
| [完成已有的未完剪辑](https://x.com/DTM_lab/status/2107108897521897547) · @DTM_lab | Opus 5.5 | 作者称把公开动效文章及其引用整理成技能，再用来重剪、卡点和完成已有短片。 |
| [在 Devin 中迭代完成的动画](https://x.com/Screeendev/status/2108333562462408823) · @Screeendev | Opus 5.5 in Devin | 作者将视频归于 Devin 中的 Opus High，并明确说明对部分动画和转场做过迭代。 |
| [钓鱼游戏预告](https://x.com/Blushneyy/status/2108644023330390194) · @Blushneyy | Opus 5.5 + Blender | 作者报告为已有游戏制作 Blender 预告，花费九十三美元、七小时。这个数字不包含先前的游戏开发；其他输入以作者线程披露为准。 |
| [Haiku 跑酷游戏首次结果不佳](https://x.com/nabendu82/status/2108523368701993395) · @nabendu82 | Haiku 5.5 / Sonnet 5.5 / Opus 5.5 comparison | 作者报告 Haiku 在此前相同跑酷任务中的结果不佳。回复说明测试只用一条提示、没有后续修改；最终发布的网站版本选用 Sonnet，并用 Blender 替换了跑步角色。 |
| [经过七十一条消息的作品集短片](https://x.com/MaciejPoczek/status/2108924468110176457) · @MaciejPoczek | Opus 5.5 | 作者报告第一支动画作品集短片用了七十一条消息。这说明成片本身不足以证明只用过一条提示。 |
| [分工生成并放大的音乐视频](https://x.com/atomtanstudio/status/2107990511164559839) · @atomtanstudio | Opus 5.5 + GPT Image 2.5 + MiniMax H3 + Topaz | 作者披露了 Opus 与技能、GPT Image 生图、本地 MiniMax H3 生视频、Topaz 放大的分工。使用的歌曲是已有录音。 |
| [Desmodus 画面与人工音效分工](https://x.com/RogerKernel/status/2108226472607690903) · @RogerKernel | Opus 5.5 + Remotion + professional sound effects | 作者说明关联发布片的画面使用 Opus、Remotion 与技能，音效由专业人员制作。 |
| [Prison Break 动画](https://x.com/VulKan42069/status/2106425412712804791) · @VulKan42069 | Sonnet 5.5 + Blender | 作者称只发了一条提示、没有追加提示，约一小时和五千八百五十万 token 完成 Blender 动画。帖子同时给出订阅额度百分比与美元数字，但没有统一计费口径。 |
| [摩托车材质对照](https://x.com/ziwenxu_/status/2107943956709339177) · @ziwenxu_ | Haiku 5.5 / Sonnet 5.5 / GPT-6 Luna + Blender | 作者向三个模型给出相同 Blender 摩托车材质任务，报告 Haiku 十二分钟、四万三角面；Luna 四十分钟、十二点三万；Sonnet 三十五分钟、十七点五万。面数描述工作量，不能当作画质评分。 |
| [带费用披露的脑腐剪辑](https://x.com/blueemi99/status/2107459553369760024) · @blueemi99 | creator-reported Fable 5.5 | 作者将剪辑短片归于 Fable 5.5，并报告二十五美元费用。输入素材、运行耗时和后台身份没有完整披露。 |

## 检索范围与缺口

十组检索中，九组成功并各返回五十行，共 450 行；一组 Haiku 流程检索在 OpenCLI 内部六十秒超时，原任务状态未知，没有重试。另读取四个作者线程，返回 111 行，其中两个达到五十行。纳入引用帖并去重后，共保留 629 个候选 ID。

按响应中的实际时间字段核对，0 行落在请求的日期窗口外。所有成功搜索均达到返回上限，因此不能说明近期帖子已经收尽。重复转述、新闻、无关演示和证据不足的条目没有全部收录；候选表保留了处理结果。

[来源账本](../data/claude55-source-review-2026-10-11.csv) · [搜索覆盖](../data/claude55-search-coverage-2026-10-11.csv) · [候选处理](../data/claude55-candidate-audit-2026-10-11.csv) · [静帧出处](../assets/claude55-2026-10-11/frames.csv)

[制作方式分析](workflow-analysis.zh-CN.md) · [开源制作资源](production-resources.zh-CN.md) · [统一目录](library.zh-CN.md)
