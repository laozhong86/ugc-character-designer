# 生图工具路由（2026-10-05 实测，进化时更新本文件）

| 优先 | 工具 | 用法 | 实测状态 | 适用 |
|---|---|---|---|---|
| 1 | `omnimux_image_submit` model=`gpt-image-2.5` operation=`text_to_image` | `dest`=绝对路径（工作区 `ugc-characters/<slug>/out/…png`），`aspectRatio`=`9:16`(全身) / `16:9`(设定表)，`audioTrack: {}`（必填占位） | ✅ live（全身 + 8 格设定表均成功） | 默认主力：全身、设定表、场景 |
| 2 | `image_generate` provider=`gpt` | `size`=`1024x1536`(全身) / `1536x1024`(设定表)，`quality`=`medium`/`high` | ✅ live（全身成功）；偶发 `fetch failed` | 订阅额度出图；失败切 1 |
| 3 | `image_generate` provider=`grok` | 同上 | 未测 | 风格探索/备选 |
| 4 | `flow_image_generate` | ratio=`9:16`，count 1–4 | 未测（需 Flow 登录态） | 一次多候选 |
| — | `omnimux_image_submit` operation=`multi_reference`（gpt-image-2.5 / nano-banana-2 / seedream） | references=[{type:image,pathOrUrl}] | ❌ 网关拒绝："research is draft, not verified" | 状态变化前不要用；每次会话可试 1 次，成功后立即更新本表 |
| — | 画布 `workflow_node_add` image `image-to-image` | 上游 import 节点连线 | 节点创建成功，底层仍 gpt-image-2.5 text_to_image 契约 | 仅当用户希望在画布上管理批量时 |

## 一致性策略（当前没有可用的参考图通道时）

1. **CHARACTER 段即身份**：锁定后把完整 CHARACTER 段存进 `character.json.character_paragraph`，后续所有 prompt 逐字粘贴，不改写。
2. 锚点前置：发型 + 主特征写在第一句后紧接的位置，并在结尾重复一次。
3. 冒烟实测：同一 CHARACTER 段文生图，正面图与设定表人物在发型/眼镜/胡子/服装上高度一致，脸部细节有差异 → 视觉打分时 `ref_match` 不得给 5，除非确实同脸。
4. 用户若需要严格同脸（视频动作迁移），交接包里以**设定表**为唯一参考（正是 B 文 Genjutsu 的输入）。

## 报错处理

- `research is draft, not verified` → 换 text_to_image，不重复同一调用。
- `fetch failed`（image_generate）→ 切 omnimux_image_submit，不同参数重试最多 1 次。
- 配额/渠道离线 → 立即向用户报告真实错误 + 备选工具。
- 永远只在 `mode: live` 且文件落盘后宣称"已生成"；用 `display_file` 展示并**亲眼看图**后再打分。
