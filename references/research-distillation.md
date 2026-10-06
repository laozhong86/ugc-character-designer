# 研究蒸馏：两篇 X 长文 → UGC 角色设计核心要素

来源（2026-10 提取，原文全文见 `references/sources/`）：
- A. @arceyul《HOW TO MAKE YOUR FIRST $10,000 WITH AN AI INFLUENCER》 — 30.9 万浏览 / 1007 收藏
- B. @pounddz《How to ACTUALLY Make Money With The AI Influencer Gold Rush (full blueprint)》 — 16 万浏览 / 1464 收藏（含完整 Claude 角色设计提示词）

## 1. 两篇共识（可信度高）

| # | 要素 | A | B | 落到 Skill 的规则 |
|---|---|---|---|---|
| 1 | **先写人，再出脸** | "Write three sentences before you generate anything" | 概念 = 名字 + 一句话 vibe + 招牌动作 | 概念卡必填 3 句 bio + vibe + running bit（G1 门禁） |
| 2 | **辨识度 = 拥挤信息流里认得出** | "a face you'd recognize in a crowded feed" | "reads instantly at thumbnail size" | 缩略图辨识（thumbnail_read）为硬指标 |
| 3 | **锁定参考图** | "Lock your references … everything uses them" | 设定表 character sheet 作为 Genjutsu 输入 | `lock` 命令；后续一律参考图/编辑模式 |
| 4 | **原创，不借脸** | 程序硬性要求，不用名人/IP | "original person, not a recreation" | originality 硬门槛 ≥4，命中真人/IP 关键词即 block |
| 5 | **动作借爆款，角色做差异** | "The format does the distribution; your character does the differentiation" | 刷爆款 → Genjutsu 替换角色 | 角色卡附 `motion_personality`，供视频阶段选题 |
| 6 | **批量 & 量胜于完美** | 70% 质量日更 > 95% 周更 | 一天可出上百条 | 角色定型后一次规划一周素材；进化目标 = 降低首过尝试次数 |
| 7 | **人设与动作一致** | "Character coherence beats production value" | deadpan 是贯穿笑点 | 场景阶段检查表情/动作与人设一致 |

## 2. B 文独有：可复用的「病毒式 deadpan 角色公式」

1. **一个夸张招牌发型**，缩略图尺寸可读（锅盖头、厚刘海齐波波、地中海秃）。
2. **一个突出面部特征**（八字卷胡、放大眼睛的酒瓶底眼镜、大鼻子、稀疏胡子）。
3. **老派、真诚的着装**，穿得极其认真（粗花呢西装、领结、高腰裤、口袋护套、邮差包）。
4. **全程面无表情**，绝不对镜头眨眼——笑点在于他们把自己当回事。
5. **呆萌古怪，绝不刻薄**：幽默来自造型、姿态、态度，绝不来自嘲弄种族/身材/背景。
6. 每个角色 = 原创个体。

工作协议（已转写进 SKILL.md 工作流）：
1. 先问 2–3 个快问题（vibe / 年龄 / 已想要的特征），或 "surprise me" 直接出 3 个概念；
2. 每个概念：名字、一句话 vibe、发型、脸、服装、一个招牌道具、一个招牌动作/梗；
3. 选中后写全身 prompt（固定格式）；
4. 用户要改：写 **EDIT prompt**——"保持其他完全一致，只改 X"，绝不重写（防丢脸）；
5. 满意后写 **设定表 prompt**：上排 5 个全身视角，下排 3 个特写，附一段每格必须一致的 CHARACTER 段；
6. 每次都给负向词，并加防漂移词；
7. 回复简短，prompt 放可复制代码块。

## 3. A 文独有：运营与经济学（影响设计决策）

- 激励模型：按播放付费（$1/千次）→ 设计目标是**完播与首秒抓力**，而非精致度。
- 首秒决定一切：动作、脸或文字钩子 → 角色正面头像需在首帧可读（scene 门禁的 format_hook、safe_zone）。
- 多平台分发（TikTok / Reels / Shorts / X）→ 角色以 9:16 为主规格。
- 规模化：3–4 个角色、不同垂类、每天多条 → 角色卡需带 `niche`，不同角色之间需**视觉差异**（进化账本可对比已有角色的 hair/palette 避免撞款）。
- 版权：音乐和素材必须自有/授权；角色本身必须原创。
- 编排 > 生成："Orchestration is the part that actually scales you" → 本 Agent 用 ledger + 角色卡做长期编排记忆。

## 4. 与 taxonomy 数据的映射（数据层 ↔ 方法论层）

| 公式要素 | taxonomy 类目 | 说明 |
|---|---|---|
| 招牌发型 | `hair` + `hair_colour` | `category_priority` 也把 hair 放在前 3 位；Bold/Extreme 档解锁 16 种夸张发型（hs_*） |
| 突出面部特征 | `freak_face`(max4, slot 互斥) + `distinctive`(max2) + `facial_hair` + `accessory: acc_glasses` | 选 1 个主特征，别堆满 4 个——辨识度来自"一个"，不是"很多" |
| 老派真诚服装 | `aesthetic`（retro / suits 在随机权重里占 60%） | 用 Character notes 细化面料、颜色、单品 |
| 体型/姿态 | `height` `body_type` `proportions` `freak_neck` | 4 条硬冲突由 CLI 校验 |
| 夸张程度 | tier：normal=Average / freak=Bold / total=Extreme | B 文风格最接近 **Bold**；Extreme 用于漫画式梗角色 |
| 基础身份 | `gender` `ethnicity_origin_base` `age` `skin_tone` `eye_*` | Average 档常显类目：gender/ethnicity/skin/age/eye_color |

注意 `east_asian` 的 fragment 为 "East Asian supermodel, Korean K-Pop idol phenotype"——会把角色推向偶像脸，与 deadpan 呆萌风冲突时，用 Character notes 明确"ordinary, non-idol face"。

## 5. 风险与边界

- 文章中的收益（$10K/月）属于营销叙述，本 Agent 不承诺收益，只负责角色设计质量。
- 「Genjutsu」等第三方工具本工作区不可直接调用；视频阶段输出交接包（角色卡 + 设定表 + 动作人格），或使用本地视频工具（video_generate / omnimux_video_submit 的 image-to-video）。
- 禁止：真人/名人相似、未经许可的肖像、版权角色、基于种族/身材的嘲弄。
