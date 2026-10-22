🌐 **中文** · [English](README.en.md)

# UGC Character Designer · AI 角色设计

**让你的 Agent，设计有记忆点的原创 AI 角色。**

面向海外短视频创作者的角色设计 Skill：从一句人设出发，确定人物经历、外形和招牌动作，
制作 AI 网红、虚拟博主与 UGC 角色的定妆图、角色设定表和场景参考，为后续图像与视频创作准备资产。

**18 个类目，共 170 个造型选项 · 3 档夸张度 · 随机组合 / 逐层自定义**

先写人，再出脸。让发型、轮廓、穿搭和招牌动作共同表达角色，方便观众在缩略图里认出它。

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](SKILL.md)
[![170 Options](https://img.shields.io/badge/Taxonomy-170%20options-orange)](assets/index.json)

[看设计方向](#设计方向海外角色参考) · [能做什么](#你说它做) · [安装与开始](#安装与首次使用) · [制作流程](#制作流程) · [使用边界](#使用边界)

## 设计方向：海外角色参考

以下素材收集自 [OmniMux「灵感库 → AI 达人」](https://omnimux.ai/influencer)，用来说明本项目关注的海外 AI 网红角色设计方向。
**它们是外部设计参考，不是本 Skill 的生成结果，也不代表角色属于本项目。**

<table>
<tr>
<td width="33%" valign="top"><img src="gallery/overseas/jean-phil.webp" width="250" alt="Jean Phil：铂金波波头、细胡须与棕格西装"><br><strong>Jean Phil · 发型与穿搭</strong><br>铂金波波头、细胡须与棕格西装，建立清晰的视觉锚点。</td>
<td width="33%" valign="top"><img src="gallery/overseas/brigitte-macaron.webp" width="250" alt="Brigitte Macaron：金色短波波头、圆眼镜与淡紫套装"><br><strong>Brigitte Macaron · 配色与配饰</strong><br>金色短波波头、圆眼镜与淡紫套装，让细节共同表达角色。</td>
<td width="33%" valign="top"><img src="gallery/overseas/leopold.webp" width="250" alt="Léopold：橄榄绿帽装、蓬松长发与高筒靴"><br><strong>Léopold · 整体剪影</strong><br>橄榄绿帽装、蓬松长发与高筒靴，让全身造型也有辨识度。</td>
</tr>
</table>

本项目聚焦 TikTok、Reels、Shorts 等海外短视频中的**原创角色设计**：
可以是一本正经的吐槽者、造型鲜明的生活博主，也可以是有固定动作与口头禅的 UGC 人物。
复古穿搭、面无表情是其中一种梗角色配方；角色的表情、气质和服装应服务于具体人设。
当前内置流程以 deadpan 梗角色为主要起点；其他表演方向的验收范围见下方使用边界。

[素材来源](gallery/overseas/SOURCES.md) · [更多角色参考](gallery/README.md) · [浏览 170 项造型元素](gallery/taxonomy.md)

## 你说，它做

| 你的需求 | Skill 帮你完成 |
|---|---|
| “我想做海外 AI 账号，还没想好角色长什么样。” | 随机组合人设与造型，生成候选方向；也可以先锁定部分特征再随机。 |
| “我想自己选轮廓、五官、发型和穿搭。” | 按层选择外形，检查组合冲突，并保留已经确定的选择。 |
| “这个人是谁？为什么观众会记住它？” | 整理三句人设、内容赛道、外形锚点、招牌动作与避免漂移的规则，写入角色卡。 |
| “把选中的方向做成后续出图的参考。” | 生成全身定妆图，确认后再制作 8 格设定表（5 张全身 + 3 张特写）。 |
| “换个造型，尽量保持角色身份。” | 沿用锁定描述修改指定特征，再检查人物身份和未修改部分。 |
| “看看它换个场景还能不能认出来。” | 制作 1–3 张 UGC 场景首帧，复核一致性，整理图片、提示词与验收记录。 |

完整流程的目标交付物：**角色卡 → 全身定妆图 → 8 格设定表 → 场景参考 → 交接包**。
交付以实际生成并通过检查的阶段为准；视频生成与发布由后续工具完成。

## 安装与首次使用

将完整仓库克隆到你的 Agent 支持的 skills 目录，例如：

```bash
git clone https://github.com/laozhong86/ugc-character-designer.git \
  ~/.agents/skills/ugc-character-designer
```

保留 `SKILL.md` 及其 `assets/`、`data/`、`references/`、`scripts/`、`templates/`、`evolution/`
目录。让 Agent 按所用宿主的方式加载此 Skill，然后从一个具体需求开始：

```text
帮我设计一个面向海外短视频的原创 AI 角色。
内容方向是用过分认真的态度点评日常小事。先给我 3 个不同的造型方向。
```

也可以这样开始：

```text
我要逐层选外形，做一个风格鲜明的虚拟生活博主。
保留这个角色的轮廓和发型，换一套适合街头采访的衣服。
基于选定的定妆图，继续做 8 格设定表和两个日常场景。
```

**需要什么：** Python 3.10+（脚本无第三方依赖），以及能加载 Skill、运行脚本和查看图片的 Agent。
实际出图还需要宿主提供可用的生图工具与相应账号或额度；安装 Skill 不会自动获得生图服务。
当前工具路由、OmniMux 接入方式与一致性限制见 [生图工具指南](references/generation-tools.md)。
角色项目默认写入你当前工作区的 `ugc-characters/<slug>/`。

## 制作流程

1. **确定方向。** 从随机组合、逐层自定义或“锁定部分特征后随机”开始，选择角色概念。
2. **先写人物。** 明确经历、内容赛道、性格、外形锚点与招牌动作，检查角色卡。
3. **制作定妆图。** 生成全身图，查看实际图片后检查辨识度、原创性和画面质量；需要时修改。
4. **锁定参考。** 保存通过检查的图片和角色描述，作为后续修改与出图的身份依据。
5. **扩展角色资产。** 制作 8 格设定表，按需增加场景首帧，检查跨图一致性。
6. **整理交接。** 输出角色卡、图片、提示词与验收报告，记录已通过和仍需处理的问题。

### 怎样检查质量

| 阶段 | 检查内容 |
|---|---|
| G1 · 角色卡 | 必填字段、造型组合、人设与原创性声明。 |
| G2 · 定妆图 | 按视觉量表评分，均分至少 3.8/5，并满足单项要求。修改图另查身份保留。 |
| G3 · 8 格设定表 | 均分至少 4.0/5，跨格身份与参考匹配等关键项达到要求。 |
| G4 · 场景参考 | 检查人物换场景后的身份、造型与画面表现。 |

**视觉分数由 Agent 查看实际生成图后逐项判断并录入。** 脚本负责字段、阈值与记录校验，
不自动看图，也不保证审美判断准确。每个阶段最多进行 3 次不同尝试；未通过时说明问题和可选调整。
详细流程见 [SKILL.md](SKILL.md)，评分项见 [质量量表](data/qa-rubric.json)。

### 造型数据与经验记录

- **多种角色方向。** 18 个类目，共 170 个选项，包含发型、面部特征、肤色、配饰和审美风格；
  Average / Bold / Extreme 三档夸张度支持不同强度的设计。中文对话不默认生成中国角色。
- **逐项查看参考。** 每个造型元素有独立参考图，组合时使用视觉描述与兼容规则，避免只靠抽象标签。
- **沿用身份锚点。** 锁定后保存最终角色描述，后续修改、设定表与场景继续引用，并重新看图复核。
- **记录失败经验。** 账本保存生成记录、评分和失败标签；经验规则需要证据支持后才沉淀。
  这是一套复盘机制，质量仍需逐次验证。

## 使用边界

- **表演方向仍有范围。** 当前随机角色卡、signature 提示词与 G1/G2 验收主要适配 deadpan／严肃角色；
  大笑、眨眼等其他表演方向尚未完成完整验收适配，不能仅修改提示词就视为标准流程已支持。
- **一致性依赖生图通道。** 没有可用参考图编辑时，主要沿用角色文字描述生成，脸部细节仍可能漂移；
  换装和 8 格设定表都需要看图复核，Extreme 档尤其如此。
- **公开案例仍有限。** 当前公开的本 Skill 产出是姜令仪的全身定妆图，见下方历史案例；
  首页海外角色均为设计参考，尚未作为本 Skill 的完整生成验收案例。
- **设计原创形象。** 不复刻真人、名人、已有网红或版权角色的相似形象。幽默来自造型、姿态和态度，
  不以种族、身材、性别认同或背景为嘲弄对象。
- **交付角色资产。** 本项目不直接完成视频拍摄、动作迁移、账号运营或发布，也不承诺播放量与收益。

## 案例与方法来源

**历史产出 · 姜令仪。** 一位架空古装权谋短剧角色，现公开一张
[全身定妆图](gallery/characters/jiang-lingyi-fullbody.png)。它用于保留早期角色设计记录；
首页优先展示面向海外短视频的设计方向。更多背景见 [画廊](gallery/README.md)。

方法来自角色设计资料与案例研究，造型数据来自 OmniMux influencer taxonomy：

- [方法论蒸馏与原始资料](references/research-distillation.md)：人设、辨识锚点、动作与角色复用。
- [Jean Phil 案例研究](gallery/case-study-jean-phil.md)：外部角色与传播方式的历史分析，相关数字以原始来源和记录时间为准。
- [造型元素画廊](gallery/taxonomy.md)：170 个选项的单图索引。

## 开发与目录

Agent 的执行入口是 [SKILL.md](SKILL.md)。对话设计见 [问询流程](references/intake-questions.md)，
图像提示词见 [模板库](templates/prompt-library.md)。

<details>
<summary>脚本速查与仓库结构</summary>

脚本路径相对仓库根目录。创建角色时，在目标工作区运行脚本并使用 Skill 的绝对路径，
角色文件会写入当前工作区。以下为命令速查，子命令的参数见各自 `--help`：

```bash
python3 scripts/ugc_face.py --help
python3 scripts/ugc_taxonomy.py find "horn"
python3 scripts/ugc_lab.py --help
python3 scripts/build_gallery.py   # 重建元素画廊
python3 scripts/selftest_all.py    # 数据、规则、阶段门槛与 Skill 引用路径
```

- `ugc_face.py`：随机组合与分层自定义（`random` / `init` / `menu` / `apply` / `prompt`）。
- `ugc_taxonomy.py`：元素检索、组合校验与提示词构建（`find` / `get` / `refs` / `diversity` / `build`）。
- `ugc_lab.py`：角色卡、生成记录、评分、锁定、验收与经验记录（`init` / `card-check` / `log` / `score` / `lock` / `accept` / `evolve` / `promote`）。

```text
ugc-character-designer/
├── SKILL.md                # Agent 执行流程
├── README.md / README.en.md
├── assets/                 # 元素索引与单元素参考图
├── data/                   # 造型数据、视觉描述、评分量表与规则
├── references/             # 方法、问询流程、生图指南与原始来源
├── scripts/                # 组合、校验、记录和画廊工具
├── templates/              # 角色卡与提示词模板
├── evolution/              # 经验规则与运行账本
└── gallery/                # 海外设计参考、历史案例与元素画廊
```

</details>

## License

代码与文档采用 [MIT](LICENSE)。画廊中的外部参考素材保留原作者权利，来源与用途说明见
[画廊](gallery/README.md)。
