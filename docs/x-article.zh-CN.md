# 我把 X 上一千多个 Opus 5.5 视频分了类：大家都拿它做了什么？

Opus 5.5 出来这两天，我的时间线被各种视频刷屏了。我自己也凑了个热闹，让它给我的阅读 App「页读」做了 8 支宣传片（[帖子在这](https://x.com/WangYeruo/status/2103108551799632050)）。

做完我就好奇：别人都在拿它做什么？所以我让 AI agent 在 X 上搜了一整晚，存下 1,104 条相关帖子，下载了里面的视频，去掉重复还剩 1,008 个。每个视频抽 9 帧，交给 Gemini 看图分类，我再随机抽查。其中 786 个判断为作者自己用 Opus 5.5 做的，下面的数字都是这 786 个。

先看我用同样方法做的一支 47 秒小动画，画面也是 Opus 5.5 写代码画的：[视频帖](https://x.com/WangYeruo/status/2103279925960876265)


## 大家拿它做了什么

1. **游戏和交互 demo，184 个。** 最多的一类。[@MengTo 的日式水乡泛舟](https://x.com/MengTo/status/2102760783344189761)、[@edwinarbus 的安提基特拉机械游戏](https://x.com/edwinarbus/status/2102463453176979794)，都是先做出能玩的东西，再录屏。
2. **AI 讲 AI 自己，153 个。** 第二名挺出乎我意料。[@kevin_t_ngo](https://x.com/kevin_t_ngo/status/2102437977435893771) 让一个小女孩问 Claude 爱什么，[@shfred0](https://x.com/shfred0/status/2102495989194236158) 让 Claude 画自己的一生，[@pleometric](https://x.com/pleometric/status/2102572941699354900) 让它想象自己刷 TikTok 会刷到什么。还有大量模型对比。
3. **广告和发布片，119 个。** 比如 [@deedydas 的创业公司发布片](https://x.com/deedydas/status/2102787937482252537)。我给页读做的也算这一类。
4. **科普讲解，99 个。** 点赞最高的两支都在这：[@RyanSael 的相机对焦模拟](https://x.com/RyanSael/status/2102591147927654847)和 [@devteamdrew 的生命与宇宙漫游](https://x.com/devteamdrew/status/2102436464323661880)。
5. **故事短片，85 个。** 比如 [@AndrewOnXYZ 的火星车短片](https://x.com/AndrewOnXYZ/status/2102512879258009818)。
6. **MV，59 个。** [@other__reality](https://x.com/other__reality/status/2102514581684052169) 和 [@donaldjewkes](https://x.com/donaldjewkes/status/2102801274173587569) 的 AI 末日主题 MV 都很火。
7. **纯艺术 33 个，历史 28 个**，比如 [@paji_a 的关原之战 3D 沙盘](https://x.com/paji_a/status/2102581158487945540)。

## 长什么样

- 3D：270 个
- 动态图形、界面风：178 个
- 扁平卡通：131 个
- 像素：50 个
- 手绘线稿：34 个
- 水墨、沙画、油彩：29 个
- 纸片拼贴：29 个
- 生成艺术、数学图解、动漫各十几个

领域和画风搭配起来也有规律：游戏几乎都是 3D；广告和科普偏动态图形；故事短片和 MV 最爱扁平卡通。

## 画面是怎么做出来的

Opus 5.5 本身只输出文字（[官方文档](https://platform.claude.com/docs/en/models/opus-5-5/overview)），画面得靠别的东西画出来。我挑了 152 个回去翻原帖、作者回复、提示词和代码仓库，大多数是 Opus 写代码，浏览器或渲染器一帧一帧画出来，再用 ffmpeg 拼成视频。真正让 Seedance、Kling 这类视频模型出画面的只有 8 个。开源得最完整的是 [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo)，想学可以从它看起。

“一个 prompt 做的”也要打个问号。我比了几条公开的提示词，最短的 172 个字符，最长的 17,664 个字符，还附了参考视频。最火的那条 [12 小时 MV](https://x.com/donaldjewkes/status/2102801469976248500) 提示词有 9,500 多字符，外加原视频、歌曲和整个项目目录。

我自己那 8 支宣传片是 Remotion 写的，返工三四轮，用掉 Claude Code 20 刀订阅一周额度的 22%。上面这支小动画也是同样的做法。

## 说明

- 数据截至 2026 年 9 月 25 日早上。X 搜索有上限，肯定没搜全。
- 分类是 Gemini 看 9 帧加帖子文字判断的，我抽查过，但单个视频可能分错。
- 作者说的耗时和费用大多没法核实。

漏了好作品，欢迎在下面贴给我。
