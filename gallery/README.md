# 画廊 · Gallery

三个区：**产出案例**（本 skill 真实出图）· **行业对标**（外部参考，定目标水位）· **元素画廊**（170 项 taxonomy 单图索引）。

---

## 产出案例 · `characters/`

本 skill 验收通过的角色。每个角色一组文件：`<slug>-fullbody.png`（定妆图）、
`<slug>-sheet.png`（8 格设定表）、`<slug>-scene-*.png`（场景首帧）。

| 角色 | 定妆 | 赛道 | 档位 | G2 评分 |
|---|---|---|---|---|
| [姜令仪 jiang-lingyi](characters/jiang-lingyi-fullbody.png) | <img src="characters/jiang-lingyi-fullbody.png" width="120"> | 架空古装权谋短剧 | Average | 4.37 |

> 新角色验收后把图拷到这里并登记本表。

---

## 行业对标 · `references/`

外部优秀 AI influencer 的角色设定表与定妆图（Higgsfield AI Influencer 等，via X）。
**非本 skill 产出**——收集目的是校准目标水位：什么样的设定表才算"缩略图一眼可辨"。
来源归原作者所有，仅作研究参考。

### 8 格设定表对标（5 全身 + 3 特写，同一角色多角度）

| | | |
|---|---|---|
| <img src="references/sheet-mushroom-hat-man.jpg" width="240"><br><sub>蘑菇帽 + 背心马靴：招牌发型极简化</sub> | <img src="references/sheet-yapper-kid.jpg" width="240"><br><sub>螺旋桨帽 + 标语 T：一件单品讲完人设</sub> | <img src="references/sheet-blonde-bob-suit.jpg" width="240"><br><sub>金色波波头 + 细格子西装</sub> |
| <img src="references/sheet-lavender-suit-mustache.jpg" width="240"><br><sub>薰衣草西装 + 姜色碗盖头 + 翘胡</sub> | <img src="references/sheet-bald-curls-mustache.jpg" width="240"><br><sub>光头两绺卷 + 大八字胡：极简强记忆</sub> | <img src="references/sheet-emo-bodybuilder.jpg" width="240"><br><sub>遮眼长发 + 肌肉体型反差</sub> |
| <img src="references/sheet-leather-coat-woman.jpg" width="240"><br><sub>银白盘发 + 黑皮大衣：冷感权威</sub> | | |

**共同规律**（正是本 skill 的设计信条）：一个夸张招牌发型 + 一个突出特征 +
老派真诚着装 + 面无表情；全身 5 视角 + 特写 3 视角的版式统一。

### 全身定妆图对标（9:16，灰/白纯色背景棚拍）

| | | | |
|---|---|---|---|
| <img src="references/fullbody-gothic-lolita.png" width="180"><br><sub>哥特洛丽塔：全黑 + 十字架 + 厚底靴</sub> | <img src="references/fullbody-techwear-man.png" width="180"><br><sub>银灰短发 + 全黑机能束带</sub> | <img src="references/fullbody-brown-check-suit.webp" width="180"><br><sub>金色波波头 + 棕格西装</sub> | <img src="references/fullbody-lavender-flare.webp" width="180"><br><sub>薰衣草喇叭裤套装 + 领巾</sub> |
| <img src="references/fullbody-safari-khaki.jpg" width="180"><br><sub>猎装卡其 + 贝雷帽 + 皮马靴</sub> | <img src="references/fullbody-hippie-fringe.jpg" width="180"><br><sub>嬉皮流苏背心 + 和平符 + 扎染喇叭裤</sub> | | |

---

## 元素画廊 · `taxonomy.md`

170 个形象选项的完整单图索引，由 `scripts/build_gallery.py` 从
`assets/index.json` 自动生成——**不要手改**，改数据后重新生成。

👉 [taxonomy.md](taxonomy.md)
