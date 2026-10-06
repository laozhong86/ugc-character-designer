# 自进化协议（可审计、有证据、可回滚）

目标 KPI：**首过所需尝试次数**（每阶段第几次生成通过门禁）持续下降；各 `stage|model` 通过率上升。

## 数据流

```
每次生成 → ugc_lab.py log（记录 prompt/模型/输出）
         → 亲眼看图 → ugc_lab.py score（rubric 打分 + failure tags）→ 自动追加 evolution/ledger.jsonl
每个角色交付后 → ugc_lab.py evolve（聚合：失败模式 / 高风险选项 / 模型通过率）
                → 有 ≥2 条证据的模式 → ugc_lab.py promote 写入 evolution/learnings.md
                → 下一次会话开始时 SKILL 要求先读 learnings.md（规则即生效）
```

## 三层进化（从轻到重）

| 层 | 写入位置 | 门槛 | 例子 |
|---|---|---|---|
| L1 经验规则 | `evolution/learnings.md`（append-only） | ≥2 个 run 证据（用户明确要求可 `--force`） | "gpt-image-2.5 设定表第 8 格表情会被抹平 → 写 'clearly different from panel 6'" |
| L2 模板/路由 | `templates/prompt-library.md`、`references/generation-tools.md` | 同一 L1 规则被 ≥3 个角色验证有效 | 把上面那句固化进 T5 模板；某工具从"未测"改"✅" |
| L3 评测标准 | `data/qa-rubric.json`（新增 failure tag / 调权重 / 调 pass_score） | 用户确认 | 新增 `prop_missing` 标签 |

## 规则

1. **证据先行**：没有 ledger 记录支撑的"经验"不写入。每条 learning 必须带 run_id。
2. **append-only + 日期**：learnings 只追加；作废规则写一条 `[deprecated <date>] 原因` 而不是删除。
3. **不改原始数据**：`data/taxonomy.json` 是上游真源，进化不改它；需要补充选项描述 → 写在 learnings 或 prompt-library 的"选项增强词"小节。
4. **回归验证**：修改脚本或 rubric 后必须运行 `python3 scripts/ugc_taxonomy.py selftest` 和 `python3 scripts/selftest_all.py`，全部通过才算完成。
5. **会话结束仪式**：交付角色时，自动跑 `evolve`，把 proposals 简述给用户（1–3 行），征得同意后 promote。
6. **工具状态刷新**：每当某个工具调用的结果与 `generation-tools.md` 记录不符（如 multi_reference 变为可用），立即更新该表并在 learnings 记一条。
