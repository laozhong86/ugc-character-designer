# 生图工具路由（2026-10-15 复测，进化时更新本文件）

**默认顺序：订阅出图 → 云端出图 → 引导安装授权。** 每级失败即降级一次，不原样重跑；降级后仍失败才向用户报告。

| 优先 | 工具 | 用法 | 实测状态 | 适用 |
|---|---|---|---|---|
| 1 · 默认 | `image_generate` provider=`gpt`（未登录自动切 `grok`） | `size`=`1024x1536`(全身) / `1536x1024`(设定表)，`quality`=`high`；**不收落盘目录**，从返回值取路径后拷到工作区 `ugc-characters/<slug>/out/…png` | ✅ live（全身成功）；偶发 `fetch failed` | 默认主力：全身、设定表、场景 |
| 2 · 备用 | `omnimux_image_submit` model=`gpt-image-2.5` operation=`text_to_image` | `dest`=绝对路径（工作区 `ugc-characters/<slug>/out/…png`），`aspectRatio`=`9:16`(全身) / `16:9`(设定表) | ✅ live（全身 + 8 格设定表均成功） | 订阅不可用时接管（未登录 / 额度 / 网络失败） |
| 3 · 兜底 | 引导安装授权（见下节） | 装 OmniMux CLI → `omnimux login` → `login status --verify` | — | 订阅与云端都不可用 |
| — | `omnimux_image_submit` operation=`multi_reference`（gpt-image-2.5 / nano-banana-2 / seedream） | references=[{type:image,pathOrUrl}] | ❌ 网关拒绝："research is draft, not verified" | 状态变化前不要用；每次会话可试 1 次，成功后立即更新本表 |
| — | 画布 `workflow_node_add` image `image-to-image` | 上游 import 节点连线 | 节点创建成功，底层仍 gpt-image-2.5 text_to_image 契约 | 仅当用户希望在画布上管理批量时 |

## 降级判定

- **订阅出图失败**（未登录订阅 / 额度用尽 / `fetch failed` / 渠道离线）→ 立即降级到云端出图，同一提示不重复调用。
- **云端出图失败**（宿主没挂云端通道 / `needs-omnimux` 未登录授权 / 网关拒绝）→ 走下一节，向用户给出安装登录三步。
- 报告口径：只说「哪一级通道、什么原因、下一步要用户做什么」，不复述原始报错文本与堆栈。
- 订阅出图的产物不在工作区：拿到返回路径后必须拷到 `ugc-characters/<slug>/out/<run>.png` 再 `log` + `score`，否则打分门禁找不到图。

## 云端也不可用：引导安装 OmniMux CLI 并登录授权

1. **装**（macOS / Linux）`curl -fsSL https://omnimux.ai/install.sh | bash`；Windows `powershell -c "irm https://omnimux.ai/install.ps1 | iex"`；或 `npm install -g @omnimux/cli`。已有 OmniMux 桌面端可直接用桌面端登录，跳过本步。
2. **登录授权** `omnimux login`（浏览器设备码）→ `omnimux login status --verify` 看到 `verified: true`。
3. **给出图通道的计量密钥** `omnimux tokens`（`tokens copy` 复制，密钥不会打印到屏幕），写进宿主环境变量 `OMNIMUX_API_KEY`。
4. 云端出图还要求宿主挂载 OmniMux 出图通道；CLI 只解决授权与密钥。挂载完成后重试云端出图，仍失败才向用户报告并给替代方案。

## 一致性策略（当前没有可用的参考图通道时）

1. **CHARACTER 段即身份**：锁定后把完整 CHARACTER 段存进 `character.json.character_paragraph`，后续所有 prompt 逐字粘贴，不改写。
2. 锚点前置：发型 + 主特征写在第一句后紧接的位置，并在结尾重复一次。
3. 冒烟实测：同一 CHARACTER 段文生图，正面图与设定表人物在发型/眼镜/胡子/服装上高度一致，脸部细节有差异 → 视觉打分时 `ref_match` 不得给 5，除非确实同脸。
4. 用户若需要严格同脸（视频动作迁移），交接包里以**设定表**为唯一参考（正是 B 文 Genjutsu 的输入）。

## 报错处理

- `research is draft, not verified` → 换 text_to_image，不重复同一调用。
- `fetch failed`（订阅出图）→ 切云端出图，不同参数重试最多 1 次。
- 配额/渠道离线/未登录授权 → 按「降级判定」走下一级；两级都不通时给用户安装登录三步。
- 永远只在 `mode: live` 且文件落盘后宣称"已生成"；用 `display_file` 展示并**亲眼看图**后再打分。
