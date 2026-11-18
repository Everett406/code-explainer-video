# 开源项目分类收藏

核实日期：2026-11-18。这里按用途收藏，不按 Star 数堆榜。参考项目只提供方法和技术证据，不替代本次内容判断。

## 一、Opus 风格与完整案例

### [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)

完整代码电影工具箱。包含大量风格、导演方法、网页逐帧渲染、音频和 FFmpeg 合成工具。适合研究完整视频工程、运镜、时间轴和交付检查。

核心技术是 HTML 页面按时间画帧，再由无头 Chrome 截图。Canvas 2D、Three.js 和 WebGL 都可使用。

许可要分文件看。项目代码主要为 MIT，文档另有 CC BY-NC 与补充许可。不要笼统当作全仓 MIT。

### [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)

15 种 MG 风格，每种都有提示词、源码、成片和评审规则。适合找扁平矢量、贴纸科普、形变、HUD、像素和竖屏花字等参考。

其科普案例使用大画布、照片贴纸、图标、图表和连续运镜。`rubric.md` 适合学习独立评审。

项目自有代码、提示词和文档采用 MIT。第三方素材保留各自许可。

### [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)

大型 Opus 视频提示词索引。按 MG、讲解、3D 和互动作品寻找创意。适合查提示词和原帖，不应当作完整源码库。

部分条目只有作者公开的提示词或结果描述。使用前查看条目说明。

### [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills)

把不同视觉风格拆成独立技能。包含手绘动画和动态文字案例。适合学习技能目录、模板、渲染器和评审流程怎样组合。

仓库标注 MIT。其引用项目和第三方库仍需分别看许可。

### [GODGOD126/opus-5-5-86-styles-in-motion](https://github.com/GODGOD126/opus-5-5-86-styles-in-motion)

面向讲解视频的风格索引和技能工程。包含风格选择、样片、全片和素材归档思路。适合查风格覆盖与工程组织。

仓库未显示明确的标准许可。不要直接再分发其素材；需要复用时先检查仓内声明。

## 二、视频框架与渲染器

### [remotion-dev/remotion](https://github.com/remotion-dev/remotion)

使用 React 和 TypeScript 制作视频。适合新建通用讲解视频、字幕、素材合成和参数化时间轴。也是本技能的默认新工程路线。

Remotion 使用自己的许可，不是 MIT。个人和符合条件的组织可免费使用；其他商业组织先查当前许可。

### [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas)

使用 TypeScript 生成器编写矢量动画，带实时预览编辑器。适合信息图、流程、矢量形变和旁白同步。仓库采用 MIT。

### [ManimCommunity/manim](https://github.com/ManimCommunity/manim)

Python 数学动画框架。适合公式、几何、坐标系和算法推导，不作为所有 MG 视频的默认工具。仓库采用 MIT。

## 三、图标与矢量素材

### [lucide-icons/lucide](https://github.com/lucide-icons/lucide)

本技能的默认图标库。风格统一，提供 SVG 和 React 等用法。普通图标优先从这里选，不要临时手绘。

Lucide 使用 ISC；部分源自 Feather 的图标带 MIT 声明。保留相应许可文本。

### [iconify/icon-sets](https://github.com/iconify/icon-sets)

用于查找其他开源图标集。一个视频仍只选一套主风格，不要混用多套线宽和透视。每个图标集的许可单独核对。

## 选择建议

| 本次需要 | 先看哪里 |
|---|---|
| 完整导演与渲染流程 | lemo-opuscar |
| 科普 MG 和评审规则 | mg-styles-15 |
| 找某个视觉创意 | awesome-opus5-5-videos |
| 学习技能工程结构 | opus-video-skills |
| 浏览更多讲解风格 | opus-5-5-86-styles-in-motion |
| 新建可编辑 MP4 工程 | Remotion |
| 矢量信息动画 | Motion Canvas |
| 数学公式推导 | Manim |
| 统一普通图标 | Lucide |
| 找特定风格图标集 | Iconify |

参考仓库时，先读目录和许可，再读与本次镜头直接相关的文件。不要下载整个素材库后无差别执行，也不要复制原片的题材、品牌和镜头组合。
