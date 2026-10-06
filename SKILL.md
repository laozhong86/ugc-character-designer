---
name: ugc-character-designer
description: 设计原创 AI 网红 / UGC 角色并出图 —— 从三句人设、170 项形象分类数据（3 档夸张度）到全身定妆图、EDIT 保脸修改、8 格角色设定表与视频交接包；内置规则引擎校验、视觉打分门禁、验收报告与自进化账本。用于"做一个 AI 网红/虚拟博主/UGC 角色/角色设定表/character sheet/deadpan 梗角色"。
whenToUse: 用户要创建、修改、批量设计 AI 网红或 UGC 角色形象，或需要角色设定表、角色一致性参考、角色视频交接包时。
---

# UGC 角色设计师 Skill

方法论来自两篇高收藏长文的蒸馏（@pounddz deadpan 角色公式 + @arceyul 播放量经济学），数据来自 OmniMux influencer taxonomy。
**核心信条**：先写人，再出脸；一个招牌发型 + 一个突出特征 + 老派真诚着装 + 全程面无表情；缩略图一眼认得出；锁定参考后一切以它为准；原创，绝不借脸。

所有路径相对本 skill 根目录 `<SKILL>`（即本文件所在目录）。脚本用 `python3 <SKILL>/scripts/...` 调用，**在工作区 cwd 下运行**（角色项目写到 `./ugc-characters/<slug>/`，不写进 skill）。

## 开工前（每次会话一次）

1. 读 `evolution/learnings.md`（已证实的经验规则，优先级高于本文默认值）。
2. 按需加载（不要一次全读）：
   - 方法论与原文证据 → `references/research-distillation.md`（原文 `references/sources/`）
   - **S0 捏脸问询流程** → `references/intake-questions.md`（首轮：随机捏脸 / 自定义捏脸；随机走 `ugc_face.py random`，自定义走 6 层 `menu/apply` 分层锁定；不得临场自编）
   - 形象数据怎么选 → `references/taxonomy/guide.md`；查具体选项 → `references/taxonomy/options-table.md`、`scripts/ugc_taxonomy.py find "<词>"` 或 `show <category>`
   - **元素索引**：`assets/index.json`（170 条记录，键 = `<category>/<option_id>`，含 label / fragment / look / 可见档位 / slot / 色值 / 单图路径与类型）。检索只用 `ugc_taxonomy.py get|query|find|refs`，不要整文件读入。
   - **单元素图**：`assets/options/<category>/<option_id>.webp`，一个元素一张独立图（170 选项 + 6 档位图）；色彩类为色卡、age 为文字卡。**禁止拼图/联系表**——展示与参考一律逐张单图。
   - prompt 模板 → `templates/prompt-library.md`
   - 生图工具与已知坑 → `references/generation-tools.md`
   - 打分标准 → `data/qa-rubric.json`；进化规则 → `references/evolution-protocol.md`

## 工作流（阶段门禁，逐阶段推进，不跳级）

| 阶段 | 做什么 | 工具/命令 | 门禁 |
|---|---|---|---|
| S0 捏脸 | **首轮只问：随机捏脸 / 自定义捏脸 / 随机+锁定**。随机 → `ugc_face.py random --count 3 --slug <slug>`（算法组合 + 自动人设 + 系统提示词 → prompt）并直接按返回的 `generate` 出图；自定义 → `ugc_face.py init/menu/apply` 逐层 L1–L6 锁定（每题含默认项 + 随机 + 自定义输入，上层锁定自动过滤/级联下层，如女性不出现胡须），最后 `prompt --slug` | `ask_user_question`、`ugc_face.py` | 随机：选定 1 个候选；自定义：L1–L6 完成且 `prompt` ok |
| S1 概念 | 随机模式已在 S0 产出候选+图，跳过；自定义模式若用户要多个方向，再用 `ugc_taxonomy.py diversity` 校验 3 个变体 | `ugc_taxonomy.py diversity/refs` | 用户选定 |
| S2 角色卡 | `ugc_face.py --slug` 已写好 `character.json`（selection/人设/锚点）；补全或修改后（无项目时 `ugc_lab.py init <slug>`）填 `character.json`（bio×3、vibe、niche、tier、selection、signature、running_bit、motion_personality、drift_guard、originality） | `ugc_lab.py card-check` | **G1** 通过（exit 0） |
| S3 全身定妆 | 用 `ugc_face.py` 产出的 `prompts/fullbody-N.txt`（或 `ugc_taxonomy.py build --mode signature`）→ 必要时细化 → 生图 9:16 → `display_file` 亲眼看 → `log` + `score` | 生图工具（见下） | **G2** ≥3.8 且无 hard_min 失败 |
| S4 EDIT | 用户要改：只改一处，模板 T4；无参考通道时用"逐字 CHARACTER 段 + 改目标字段"重跑并 `--parent` 关联 | 同上 | G2-edit（identity_preserved ≥4） |
| S5 锁定 | 通过的全身图 `ugc_lab.py lock <slug> <run> --role front`；把最终 CHARACTER 段写入 `character.json.character_paragraph` | `ugc_lab.py lock` | 只能锁已通过的 run |
| S6 设定表 | 模板 T5（16:9；第 8 格招牌表情必须与第 6 格明显不同） | 生图 → score → lock `--role sheet` | **G3** ≥4.0，cross_panel_identity/ref_match ≥4 |
| S7 场景（可选） | 1–3 张 9:16 UGC 首帧（模板 T6），验证换场景仍是同一人 | 生图 → score | **G4** |
| S8 交付 | `ugc_lab.py accept <slug>` 生成 `acceptance.md`；输出交接包（T7）；`assets_create` 登记为 `character` 资产（附 front+sheet）；跑 `ugc_lab.py evolve` 并向用户简报 1–3 条进化建议 | `assets_create`、`ugc_lab.py evolve/promote` | 验收全绿 |

**打分纪律**：分数只能来自亲眼看到的生成图（`display_file` 后看图），逐项对照 rubric；绝不凭 prompt 打分，绝不对未落盘的文件打分。失败必须打 `failure_tags`（rubric 里有修复建议），下一次尝试按建议改 prompt——禁止原样重跑。每阶段最多 3 次不同尝试，仍不过 → 向用户说明卡点与选项。

## 生图工具（详见 `references/generation-tools.md`）

1. 主力：`omnimux_image_submit`，`model: gpt-image-2.5`、`operation: text_to_image`、`aspectRatio: 9:16`（设定表 `16:9`）、`dest` 写到 `./ugc-characters/<slug>/out/<run>.png`、`audioTrack: {}`。
2. 订阅备选：`image_generate`（`size: 1024x1536` / 设定表 `1536x1024`，provider gpt→grok）。
3. 多候选：`flow_image_generate`（count 1–4）。
4. `multi_reference` 当前被网关拒绝（draft）；每会话最多试 1 次，成功即更新工具表 + learnings。
工具不收 negative 参数 → 把关键负向改写成正向约束句（见 T3）。

## 硬约束

- **数据驱动、不默认本土化**：对话用中文 ≠ 角色是中国人/做国内梗。族裔、风格、档位来自用户回答或数据内置随机权重；用户未指定时 3 个概念至少覆盖 2 种族裔（全球市场 3 种）。
- 每个概念的发型/面部选项须引用其单图（`refs`），出图 prompt 用 `look` 视觉描述（`build --mode signature` 已自动注入），而不是 2–3 个单词的标签。
- 原创：不做真人/名人/网红/版权角色的相似形象；用户要求"像某某"→ 婉拒并提供原创替代（改 2+ 面部锚点）。
- 幽默来自造型、姿态、态度；绝不嘲弄种族、身材、性别认同、背景。
- 不承诺收益；平台激励计划条款以官方为准；音乐素材需自有/授权。
- 用户的 taxonomy 选择若被规则归一化/冲突 → 明确告诉用户哪条规则、给 2 个替代组合。
- prompt 一律英文、放在 ```prompt-image``` 代码块；对话、说明、报告用中文。

## 脚本速查

```bash
S=<SKILL>/scripts
python3 $S/ugc_face.py random --count 3 [--seed N] [--tier T] [--lock JSON] --slug <slug>   # 随机捏脸 → prompt + 生图参数
python3 $S/ugc_face.py init|menu|apply|prompt --state ugc-characters/<slug>/face-state.json --layer L1..L6   # 分层自定义
python3 $S/ugc_face.py check --sel JSON --tier T                           # 兼容性规则检查
python3 $S/ugc_taxonomy.py list | show hair --tier freak | validate --tier bold --sel '{...}'
python3 $S/ugc_taxonomy.py build --tier bold --sel @sel.json --brief "..." --mode signature
python3 $S/ugc_taxonomy.py random --tier freak --seed 7 --lock '{"hair":["hs_mushroom"]}'
python3 $S/ugc_taxonomy.py get hair/hs_horns distinctive/df_gems         # 按索引键精确取记录 + 单图
python3 $S/ugc_taxonomy.py query --category hair --tier freak --bold-only # 条件筛选（--text/--slot/--fields all）
python3 $S/ugc_taxonomy.py find "horn"  |  refs --sel @sel.json        # 全文检索 / 一组选择对应的全部单图
python3 $S/ugc_taxonomy.py diversity --tier freak --sels '[s1,s2,s3]' --market global   # G0 概念多样性门禁
python3 $S/ugc_lab.py init|card-check|log|score|lock|accept|evolve|promote ...
python3 $S/selftest_all.py   # 改动 skill 后的回归（必须全绿）
```
tier 接受 `normal|freak|total` 或 UI 名 `average|bold|extreme`。
