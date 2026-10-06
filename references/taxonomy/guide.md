# Taxonomy 使用指南（按需加载）

数据真源：`data/taxonomy.json`（18 类目 × 170 选项 × 3 档位，来自 OmniMux service/influencer，Higgsfield 反向分类）。
- 总表（含 fragment / 可见档位 / slot / 色值 / 本地图）：`references/taxonomy/options-table.md`
- 机器索引：`data/option-index.json`
- 元素索引：`assets/index.json`（键 `<category>/<option_id>` → label/fragment/look/tiers/slot/swatch/image{rel,bytes,kind}）；检索 `ugc_taxonomy.py get|query|find|refs`
- 单元素图：`assets/options/<category>/<option_id>.webp`，每个元素一张独立图（138 原始参考照 + 29 色卡 + 3 年龄文字卡 + 6 档位图）；不提供也不使用拼图
- 视觉描述：`data/visual-descriptors.json`——逐张看图提炼的"实际长相"，fragment 只有 2–3 个词（如 "beehive"），look 写出图里的样子（"towering 60s beehive"）；signature prompt 自动使用 look
- 规则引擎原始 Go 实现：`data/rules.go.txt`（CLI 为其忠实移植，`selftest` 覆盖原 rules_test.go 全部用例）

## 档位（tier）

| id | UI 名 | 可见选项 | prompt lead | 何时用 |
|---|---|---|---|---|
| normal | Average | 124 | Natural, realistic | 可信"真人博主"、带货 UGC、生活方式 |
| freak | Bold | 167 | Stylized, slightly exaggerated | **deadpan 爆款梗角色默认档**（B 文风格） |
| total | Extreme | 170 | Extreme caricature | 漫画式夸张、meme 角色；需注意不嘲弄身体 |

## 规则（CLI 自动执行，但设计时要提前避开）

硬冲突（4 条）：
1. `body_heavy` × `h_tall`/`h_very_tall`
2. 非 normal 档：`body_heavy|body_muscular|body_ultra` × `pr_shortlegs|pr_longlimbs`
3. `body_ultra` × `neck_long`
4. `neck_long` × `ff_teeth_11`（龅牙）

归一化：
- 不在当前档可见的选项被静默丢弃 → 设计时看 N/B/E 列；
- `acc_none` 独占；
- `freak_face` 同 slot 互斥（marks/cheeks/eyes/lips/brows/nose/ears/teeth/chin/forehead），后选替换先选；
- 每类 `max` 封顶，超出的**后选**被丢弃（保留先选）。

## 设计启发（把数据变成"辨识度"）

1. **一个主锚点**：hair（含 15 个 Bold+ 夸张发型 hs_*）是缩略图辨识第一来源；`category_priority` = gender → body_type → hair → hair_colour → aesthetic。
2. **一个次锚点**：从 `freak_face` / `distinctive` / `facial_hair` / `acc_glasses` 里只选 1 个"主特征"，其余最多 1–2 个小细节。堆 4 个 freak_face 会稀释辨识度。
3. **色彩对比**：hair_colour 与 aesthetic 服装主色形成对比（例：ginger × mustard 是同色系——可行但需要眼镜/领结做第二色点）。
4. **服装 = 年代感 + 真诚**：`retro`/`suits` 最贴 B 文公式（随机权重也偏向二者）；用 brief 写具体单品与面料。
5. **参考图自带的风格基调**：所有选项照都是同一套美学——白底正面对称构图、面无表情、单色高饱和服装、一个夸张特征、编辑级真实皮肤。这正是这套数据"有个性"的来源；概念与 prompt 应延续它，而不是滑向"日常美颜网红"。
6. **ethnicity 片段风险**：`east_asian` 片段是 "supermodel, K-Pop idol phenotype"，会偶像化；做呆萌角色时 brief 加 "ordinary everyday face, not idol-like"。
6. **体型不当笑点**：heavy / potbelly / egg 等选项可以用，但幽默必须来自造型与态度，绝不来自身体本身（rubric: stereotype_risk）。
7. **gender**：trans/non-binary 选项按用户意愿尊重呈现，不作为笑点。
8. **看图方式**：逐张 `display_file` 单图，每次只展示与当前决策相关的 3–6 个元素。
9. **随机灵感**：`ugc_taxonomy.py random --tier freak --seed N --lock '{"hair":["hs_mushroom"]}'` 遵循数据内置随机权重（male 0.67、suits 0.4、retro 0.2、lampshade 0.2；facial_hair 仅 male/trans_man）。

## 类目速览

| 类目 | max | 说明 |
|---|---|---|
| gender | 1 | female / male / trans_man / trans_woman / non_binary |
| ethnicity_origin_base | 1 | african / east_asian / european / indian / middle_eastern / latin_american(UI: Mixed) |
| age | 1 | adult / mature(Middle-aged) / senior |
| skin_tone | 1 | 8 色（带 swatch） |
| height | 1 | average / tall / very_tall |
| body_type | 1 | slim / athletic / muscular / curvy / heavy / ultra |
| proportions | 2 | longlimbs / shortlegs / shoulders / waist；Bold+：egg / potbelly |
| freak_head | 1 | oval / long / round / square / heart；Bold+：tiny / forehead；Extreme：ancient / herojaw / megachin |
| freak_neck | 1 | normal / short；Bold+：column / long |
| eye_shape | 1 | 11 种，Bold+ 解锁 close / wide / uneven / huge |
| eye_color | 1 | 8 色 |
| freak_face | 4 | 25 个，slot 互斥 |
| facial_hair | 1 | 8 种，Bold+：pushbroom / braid |
| hair | 1 | 26 种，10 个全档 + 16 个 Bold+ 夸张款 |
| hair_colour | 1 | 13 色 |
| distinctive | 2 | 14 个（异色瞳、面部纹身、鼻中隔环、金牙套、精灵耳…） |
| aesthetic | 1 | retro / sporty / y2k / theatrical / goth / suits / streetstyle / casual |
| accessory | 3 | none(独占) / glasses / headphones / jewelry / hat / bag |
