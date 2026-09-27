# 14 个对照案例：相似画面，不同制作链

这 14 例是从[168 条人工深读案例](../data/cases.csv)中**有目的地挑选**的，覆盖七种制作路径。它们不是随机样本，不能用来估计各路径占比、给作品排质量名次，或比较模型总体能力。“作者称”表示公开自述；公开提示词只证明提出过要求，不等于执行日志。“九帧可见”只针对可取得的 X 预览 MP4，不能验收整段运动、音质、事实准确性、隐藏工具调用或最高画质母版。字段和取样边界见[案例表说明](case-index-guide.zh-CN.md)与[调查方法](methodology.zh-CN.md)。

以下 14 张小图各取自对应案例的 X 预览视频单帧；点击图片前往创作者原帖。小图仅帮助辨认风格，不用于判断全片运动、声音或画质；原画面权利仍属于创作者。

## 程序二维绘图与动效

两条都呈插画外观：一条有与成片对应的公开动画工程，另一条明确使用外部生成的静图和语音。

### 蚂蚁群落：有对应工程

<a href="https://x.com/hanifproduktif/status/2102742924148830211"><img src="../assets/case-thumbnails/2102742924148830211.webp" width="320" loading="lazy" alt="原帖预览单帧截图：蚂蚁群落：有对应工程"></a>

- **原帖：**[@hanifproduktif](https://x.com/hanifproduktif/status/2102742924148830211)。
- **Opus 角色与输入（作者披露）：**利用蚂蚁 rig、场景规则和声音脚本，以 Node Canvas 逐帧绘图，再用 FFmpeg 合成。
- **公开工程或提示词：**作者链接了[含对应蚂蚁短片源码的项目](https://github.com/buildwithhanif/claude-animation-skill)，其中有抽帧检查和可复用动画规则。
- **九帧可见：**蚂蚁由草图变成彩色角色、搬叶进入地下群落，最后出现代码主题片尾；画面和时长与工程对应。
- **不能推出：**公开工程无法还原 Claude 对话、逐行代码作者，也不能验收全片音轨听感。

### 纸艺解说：外部静图与 TTS

<a href="https://x.com/so_ainsight/status/2103117547776163845"><img src="../assets/case-thumbnails/2103117547776163845.webp" width="320" loading="lazy" alt="原帖预览单帧截图：纸艺解说：外部静图与 TTS"></a>

- **原帖：**[@so_ainsight](https://x.com/so_ainsight/status/2103117547776163845)。
- **Opus 角色与输入（作者披露）：**作者称代理用 11 张外部生成静图、四段 Gemini TTS 语音，经 HTML/JS 逐帧截图合成动画，并修改铅笔位置和气泡溢出。
- **公开工程或提示词：**[后续任务帖](https://x.com/so_ainsight/status/2103119227192225926)允许 gpt-image-2.5 与 Gemini TTS；深读记录中没有对应源工程或运行日志。
- **九帧可见：**纸张纹理、人物、电脑、铅笔和日文字幕。
- **不能推出：**九帧无法核验所称素材数量、修改顺序或语音质量。

## 知识讲解

两条都把知识拆成图解步骤：一条依赖现有说明书，另一条据作者说由 JavaScript 绘图。

### 家具安装：说明书转教程

<a href="https://x.com/deedydas/status/2103174501345493197"><img src="../assets/case-thumbnails/2103174501345493197.webp" width="320" loading="lazy" alt="原帖预览单帧截图：家具安装：说明书转教程"></a>

- **原帖：**[@deedydas](https://x.com/deedydas/status/2103174501345493197)。
- **Opus 角色与输入（作者披露）：**简短委托要求根据 IKEA 安装说明书制作三维配音教程。
- **公开工程或提示词：**公开了委托文字；深读记录中未取得原说明书和执行日志。
- **九帧可见：**零件编号、警示、简单三维面板、说明书小图和步骤标号；取样画面出现“第 5／48 步”。
- **不能推出：**需要逐步对照原说明书才能验收安装准确性，九帧也不能判断旁白质量。

### 浏览器原理：JavaScript 图解

<a href="https://x.com/addyosmani/status/2103009037164110327"><img src="../assets/case-thumbnails/2103009037164110327.webp" width="320" loading="lazy" alt="原帖预览单帧截图：浏览器原理：JavaScript 图解"></a>

- **原帖：**[@addyosmani](https://x.com/addyosmani/status/2103009037164110327)。
- **Opus 角色与输入（作者披露）：**作者称 Opus 用 JavaScript 逐帧绘图，并说这类 demo 多数是 one-shot。
- **公开工程或提示词：**深读案例依据作者原帖与回复；尚未核查对应源代码仓库。
- **九帧可见：**画面依次涉及 DNS／HTTP、DOM、页面绘制和布局。
- **不能推出：**不能由九帧验证全部技术讲解、这条视频是否恰好属于 one-shot，或抽样帧之间的运动流畅度。

## 三维与实时图形

两条都有三维渲染外观：水面案例可核公开 WebGL 工程，鹈鹕案例的渲染器仍属作者自述。

### Clearwater：可检查的浏览器渲染

<a href="https://x.com/Aurelien_Gz/status/2102786378282987591"><img src="../assets/case-thumbnails/2102786378282987591.webp" width="320" loading="lazy" alt="原帖预览单帧截图：Clearwater：可检查的浏览器渲染"></a>

- **原帖：**[@Aurelien_Gz](https://x.com/Aurelien_Gz/status/2102786378282987591)。
- **Opus 角色与输入（作者披露）：**作者归因于 Opus 制作 WebGL2 浅水场景，并说提供过参考视频。
- **公开工程或提示词：**[对应的 Clearwater 工程](https://github.com/Aureliengmz/clearwater)记录着色器、FFT 波浪、涟漪，以及嵌入页面的生成石子贴图。
- **九帧可见：**浅水场景里的镜头与涟漪变化。
- **不能推出：**预览不能证明物理准确性或 one-shot；“运行时不拉取素材”也不等于源码中没有视觉资产。

### 骑车鹈鹕：未公开源码的代码渲染主张

<a href="https://x.com/AxtonLiu/status/2103119648271290566"><img src="../assets/case-thumbnails/2103119648271290566.webp" width="320" loading="lazy" alt="原帖预览单帧截图：骑车鹈鹕：未公开源码的代码渲染主张"></a>

- **原帖：**[@AxtonLiu](https://x.com/AxtonLiu/status/2103119648271290566)。
- **Opus 角色与输入（作者披露）：**作者称开放式委托让 Opus 写出 GPU 光线步进渲染器，鹈鹕、自行车、栈桥、海、天空及音乐均由代码计算，没有外部模型、贴图或音频。
- **公开工程或提示词：**可见委托和制作说法；深读案例未见源码或运行日志。
- **九帧可见：**约 38 秒的 X 预览里，夕阳栈桥上有骑车鹈鹕，下方是水面。
- **不能推出：**九帧无法核验渲染器、每帧 40 次采样、零外部素材或母版画质。

## 现有素材改编

两条看起来都是完整视频，但既有人物表演、产品资产和人工导演意图是重要输入。

### 真人口播重绘：保留原表演

<a href="https://x.com/AxtonLiu/status/2102827887732932956"><img src="../assets/case-thumbnails/2102827887732932956.webp" width="320" loading="lazy" alt="原帖预览单帧截图：真人口播重绘：保留原表演"></a>

- **原帖：**[@AxtonLiu](https://x.com/AxtonLiu/status/2102827887732932956)。
- **Opus 角色与输入（作者披露）：**作者提供 83 秒真人口播原片，要求保留原声、字幕和片长，并增加圆形说话者画中画及配合概念的线稿插画。
- **公开工程或提示词：**深读案例中的流程证据是作者说明；未取得可编辑工程。
- **九帧可见：**反复出现的圆形人物画中画、手绘图解和字幕。
- **不能推出：**这属于已有原片条件下的改编；作者所称无人干预及整段声画同步尚未独立核验。

### Social SDK 发布片：产品代码与品牌系统

<a href="https://x.com/leodev/status/2102781872107659270"><img src="../assets/case-thumbnails/2102781872107659270.webp" width="320" loading="lazy" alt="原帖预览单帧截图：Social SDK 发布片：产品代码与品牌系统"></a>

- **原帖：**[@leodev](https://x.com/leodev/status/2102781872107659270)。
- **Opus 角色与输入（作者披露）：**[后续七点说明](https://x.com/leodev/status/2102897952587133299)称 Opus 5.5 主做、Fable 5.1 协助难段；作者提供产品代码库、动画组件、落地页、品牌系统和每段展示要求。
- **公开工程或提示词：**作者说明从 Remotion 转到 HyperFrames，且经历多轮调整；深读记录中未见完整工程或模型调用日志。
- **九帧可见：**聊天界面、文档、应用画面和 Social SDK 品牌收尾。
- **不能推出：**根帖本身未交代完整流程，预览也不能分辨每个镜头由哪一模型或渲染器完成。

## 外部视频模型编排

两条都是 Opus 负责组织生产、外部模型提供运动画面的例子，但上游参考不同。

### 音乐视频：音乐、镜头与剪辑服务

<a href="https://x.com/jantijssen/status/2102861462461124755"><img src="../assets/case-thumbnails/2102861462461124755.webp" width="320" loading="lazy" alt="原帖预览单帧截图：音乐视频：音乐、镜头与剪辑服务"></a>

- **原帖：**[@jantijssen](https://x.com/jantijssen/status/2102861462461124755)。
- **Opus 角色与输入（作者披露）：**作者称 Opus 写歌并导演 MV，Suno v6 制作音乐、Seedance 2.5 制作视频片段、Tesseract 剪辑。
- **公开工程或提示词：**原帖交代了工具分工；深读记录中没有服务调用日志或可编辑工程。
- **九帧可见：**复古电视与拼贴风格、表演者、流行字卡和重复出现的“SLOP-TV”标识。
- **不能推出：**画面不能核验具体服务调用，也不能把某些像素直接归功于 Opus。

### Blender 草模：参考视频到 Seedance

<a href="https://x.com/OriSilver/status/2102817977812824335"><img src="../assets/case-thumbnails/2102817977812824335.webp" width="320" loading="lazy" alt="原帖预览单帧截图：Blender 草模：参考视频到 Seedance"></a>

- **原帖：**[@OriSilver](https://x.com/OriSilver/status/2102817977812824335)。
- **Opus 角色与输入（作者披露）：**作者称提供镜头参考片；Opus 经 MaxFusion MCP 取样，在 Blender 中制作机位与走位草模，再把草模和作者角色交给 Seedance 2.5。
- **公开工程或提示词：**原帖描述了这条三段式制作链；深读时未核查参考原片、Blender 工程或服务日志。
- **九帧可见：**X 预览上下分屏，上方近写实人物与下方低模／卡通草模在构图上对应。
- **不能推出：**公开分屏片长不是 Blender 草模母版片长；画面不能核验所称取样帧率，也不能说上方真人感画面由 Opus 直接渲染。

## 应用与游戏录屏

两条预览记录的是交互环境：一条有详细代码委托，另一条明确披露了大量人工制作的三维资产。

### 平台游戏：详细 Canvas 委托

<a href="https://x.com/iannuttall/status/2102685186919932404"><img src="../assets/case-thumbnails/2102685186919932404.webp" width="320" loading="lazy" alt="原帖预览单帧截图：平台游戏：详细 Canvas 委托"></a>

- **原帖：**[@iannuttall](https://x.com/iannuttall/status/2102685186919932404)。
- **Opus 角色与输入（作者披露）：**作者要求制作受《波斯王子》启发的单文件 HTML／原生 JS Canvas 游戏，包含操作、机关、战斗和灯光。
- **公开工程或提示词：**[详细提示词](https://x.com/iannuttall/status/2102685189558190087)公开；作者所称一次人类委托、约 35 分钟没有对应运行日志。
- **九帧可见：**横向卷轴游戏录屏中有 HUD、战斗、门机关和菜单。
- **不能推出：**录屏不能证明完整关卡都可玩、敌方行为正确、代码归属，或所借鉴美术元素的授权状态。

### Roblox 场景：人工制作的资产

<a href="https://x.com/NiloTechInc/status/2102741813719138661"><img src="../assets/case-thumbnails/2102741813719138661.webp" width="320" loading="lazy" alt="原帖预览单帧截图：Roblox 场景：人工制作的资产"></a>

- **原帖：**[@NiloTechInc](https://x.com/NiloTechInc/status/2102741813719138661)。
- **Opus 角色与输入（作者披露）：**作者称人在 Nilo 中制作动画、服饰和三维资产，Opus 在 Roblox Studio 中编排镜头和预告片。
- **公开工程或提示词：**原帖披露了分工；深读案例没有可编辑场景或详细提示词。
- **九帧可见：**短录屏呈现 Roblox 风格人物及编辑器场景，并有 Nilo／Opus 标记。
- **不能推出：**录屏不能证明 Opus 制作了人物资产，也不能把编辑器画面当成已验收的完整成片。

## 比较或制作路径未确定

一条本来就是双模型对比；另一条是完整发布片，但公开提示词、交付画面和事先存在的仓库各自回答不同问题。

### 鲁布·戈德堡机关：自报成本与时间

<a href="https://x.com/leogao25/status/2102544078927741369"><img src="../assets/case-thumbnails/2102544078927741369.webp" width="320" loading="lazy" alt="原帖预览单帧截图：鲁布·戈德堡机关：自报成本与时间"></a>

- **原帖：**[@leogao25](https://x.com/leogao25/status/2102544078927741369)。
- **Opus 角色与输入（作者披露）：**作者称 Opus 5.5 与 GPT-6 Astra 接受同一物理机关任务，并报告不同的耗时与费用。
- **公开工程或提示词：**原帖有对比说法和费用表；深读记录中没有同口径运行日志或账单。
- **九帧可见：**木质／绿色机关分屏及费用字卡；这不是两支独立原片的全片验收。
- **不能推出：**一组自报对比不能建立普遍的模型质量、速度或价格排名。

### Opus 发布片：委托目标与已发布预览

<a href="https://x.com/marcthecreatorr/status/2103133462798483752"><img src="../assets/case-thumbnails/2103133462798483752.webp" width="320" loading="lazy" alt="原帖预览单帧截图：Opus 发布片：委托目标与已发布预览"></a>

- **原帖：**[@marcthecreatorr](https://x.com/marcthecreatorr/status/2103133462798483752)。
- **Opus 角色与输入（作者披露）：**作者称用一条提示词、14 分钟和 $3.98 制作了 Canvas 手绘风品牌发布片。
- **公开工程或提示词：**[提示词截图](https://x.com/marcthecreatorr/status/2103133477600206925)要求短于 30 秒并禁用 skills／MCP。[视频 skill 仓库的一次提交](https://github.com/Changroro/code-video/commit/e60a7d54e80215ca3b34302cb65cfab3e0b18f8c)早于发帖，但仓库存在不能证明本片是否调用了它。
- **九帧可见：**约 32 秒的 X 预览含手绘感图形、品牌信息和片尾卡。
- **不能推出：**提示词不是执行记录；已发布预览长于目标时长，费用、耗时、数据准确性和 skill 使用情况均未独立核验。
