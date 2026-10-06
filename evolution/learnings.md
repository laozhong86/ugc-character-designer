# Learnings（append-only，由 ugc_lab.py promote 追加；每次会话开工前必读）

格式：`- [日期] (scope) 规则` + `evidence: run_ids`

## 种子规则（来自 2026-10-05 建设期冒烟测试 · smoke-teacher）

- [2026-10-05] (tool) `omnimux_image_submit` 的 `multi_reference` 操作（gpt-image-2.5 / nano-banana-2）被网关拒绝 "research is draft, not verified"；参考图一致性暂用"逐字 CHARACTER 段 + 文生图"。
  evidence: build-time smoke (2 calls)
- [2026-10-05] (sheet|gpt-image-2.5) 完整 CHARACTER 段 + 两行编号布局，一次即得 5 全身 + 3 特写，跨格一致性高；但第 8 格"招牌表情"与第 6 格几乎相同 → 必须写明 "clearly different from panel 6" 并用强动作词。
  evidence: 20261005-171624-sheet
- [2026-10-05] (fullbody|gpt-image-2) 由 `ugc_taxonomy.py build --mode signature` 生成的结构化 prompt + brief 细化，首次即通过 G2（4.73）。
  evidence: 20261005-171623-fullbody

## 首个真实会话复盘（2026-10-05 · wang-guixiang）

- [2026-10-05] (intake) S0 临场自编问题、未问目标市场 → 3 个概念全部 east_asian + 中国本土梗（居委会/广场舞），且选了 Average 档，taxonomy 的个性空间（16 种夸张发型、25 项面部变形、theatrical/goth/y2k 等风格）基本没用上。规则：S0 必须使用 references/intake-questions.md 固定题库；S1 必须过 `ugc_taxonomy.py diversity`。
  evidence: wang-guixiang S0/S1 transcript (user feedback)
- [2026-10-05] (prompt) taxonomy fragment 只有 2–3 个词，模型按"常见理解"出图，丢失参考照里的夸张造型 → signature prompt 改用 data/visual-descriptors.json 的 look 描述；与用户确认选项时展示 assets/options/<category>/<id>.webp 单图。
  evidence: user feedback + option thumbnail review
