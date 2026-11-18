# code-explainer-video

用代码策划、制作、检查和导出讲解视频与 MG 动画的 Skill。把选题、脚本或用户素材变成可编辑的视频工程，默认交付 H.264 MP4。

## 能做什么

- 根据一句主题生成旁白、分镜和统一时间轴。
- 新建 Remotion + React + TypeScript 视频工程。
- 改造具有 `render(t)` 或 `renderAt(t)` 接口的 Opus 风格 HTML 工程。
- 优先使用用户提供的图片、视频、录音、字体和数据。
- 使用统一图标库、专业运镜和有内容因果的转场。
- 通过关键帧、联系表、连续帧条、完整预览和技术检查反复验收。

## 使用方式

在支持 `SKILL.md` 的 Agent 环境中，将本仓库作为技能目录使用。也可以将本目录打包为 `.skill` 后导入支持该格式的环境。

示例请求：

```text
做一个讲解【主题】的视频，使用代码实现，渲染 MP4。
```

开始制作、改造或审片前，执行者必须先读：

1. `references/core-playbook.md`
2. `references/review.md`

## 默认约定

- 中文讲解，1920×1080，30 fps。
- 添加同步旁白字幕，默认不生成配音。
- 默认使用 Lucide 图标。
- 保留源码、时间轴和本地素材。
- 先检查和返修，再交付最终 MP4。

用户另有要求时，以用户要求为准。

## 目录

```text
SKILL.md
references/
  core-playbook.md      # 强制阅读的导演、渲染和迭代方法
  prompt-template.md    # 可复用的完整制作提示词
  repositories.md       # 已核实的开源项目分类索引
  review.md             # 多轮检查、返修和最终验收
scripts/
  inspect_media.py      # 素材盘点与 JSON 清单
  check_video.py        # MP4 参数、解码和黑帧检查
```

## 检查脚本

盘点素材：

```bash
python3 scripts/inspect_media.py <素材路径> --json asset-manifest.json
```

检查成片：

```bash
python3 scripts/check_video.py <成片.mp4> --width 1920 --height 1080 --fps 30 --codec h264 --decode --blackdetect
```

音视频检查依赖 FFmpeg 和 ffprobe。图片尺寸读取优先使用 Pillow。

## 方法来源

核心方法提炼自以下真实项目，并在 `references/repositories.md` 中按用途分类：

- [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)
- [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)
- [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills)
- [GODGOD126/opus-5-5-86-styles-in-motion](https://github.com/GODGOD126/opus-5-5-86-styles-in-motion)
- [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)

参考或复用外部项目时，分别核对代码、文档、提示词和素材许可。
