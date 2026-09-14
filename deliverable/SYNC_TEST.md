# SYNC_TEST — 方向 1（agent → 本机）测试标记

- 时间：2026-09-14（UTC）
- 分支：`arena/01a04caf-image-to-editable-pptx`
- 写入者：Arena 会话 `01a04caf`（image-to-editable-pptx）

如果你在本机 `.\sync.ps1` 之后能看到这个文件，
说明 **agent → 本机** 方向的同步链路是通的 ✅

本仓库的交付物在 `examples/fig3-mechanism-map/`：

| 文件 | 说明 |
| --- | --- |
| `fig3_mechanism_map.pptx` | 可编辑 PPT（227 个原生对象） |
| `fig3_mechanism_map.svg` | 可编辑矢量 SVG |
| `fig3_page_ir.json` | PageIR 中间表示 |
| `build_fig3.py` | 可复现生成脚本 |

`.\download.ps1 -Set final` 会把 `deliverable\` 和 `examples\fig3-mechanism-map\`
一起镜像到本机 `<仓库名>_out` 目录。

下一步（方向 2 测试）：你本机随便改一个文件 → `.\push.ps1 "test: local -> arena"`
→ 回到这里说"我推了"，我跑一次 agent-sync，回执 `results\sync\last_sync.md`
里就会列出你的提交。
