# Prompt 模板库（蒸馏自 @pounddz 原版 + taxonomy 适配）

所有 prompt 一律英文（生图模型对英文最稳）；与用户沟通用中文。占位符 `[...]` 必须全部填满，禁止把占位符原样发给模型。

## T1 · 概念提案卡（中文对话输出，每个概念一张）

```
【概念 A】名字：___  一句话 vibe：___（具体到年代/职业/自我认知的反差）
三句人设：1) 他是谁 2) 他做什么 3) 他对什么有强烈意见
招牌发型：___（taxonomy: hair=___, hair_colour=___）
突出特征：___（freak_face / distinctive / facial_hair / acc_glasses）
老派真诚服装：___（aesthetic=___）  招牌道具：___
招牌动作/梗：___    动作人格：___    档位：Average / Bold / Extreme
差异化：与已有角色相比，缩略图上靠什么一眼区分
```

## T2 · 全身定妆图（FULL-BODY，首选由 CLI 生成后再润色）

`python3 scripts/ugc_taxonomy.py build --tier <tier> --sel '<json>' --brief '<细节>' --mode signature`

手写格式（CLI 不足时）：
```
Ultra-photorealistic full-body studio portrait of a [BUILD] [ETHNICITY] [man/woman] in their [AGE], standing [POSTURE], arms [ARM POSITION], facing the camera. Plain seamless light-grey studio backdrop, smooth and evenly lit, with a soft natural shadow on the floor beneath them.
Hair: [ONE EXAGGERATED SIGNATURE HAIRSTYLE — shape, length, parting, fringe], [COLOUR], immaculate and slightly too precise.
Face: [FACIAL HAIR]; [GLASSES]; [FACIAL FEATURES]; completely deadpan expression, [EXPRESSION DETAIL], staring directly into the lens.
Outfit: [OLD-FASHIONED EARNEST OUTFIT — every garment, colour, fabric, fit], [SHIRT], [TIE/BOW TIE], [SHOES], [ONE PROP].
Photography: shot on a full-frame camera with an 85mm lens at f/8, eye-level, full body in frame head to toe with a little space around them, 9:16 vertical. Soft diffused key light from front left with a large softbox, gentle fill, subtle rim light. Natural skin texture with visible pores, individual hair strands, fine fabric texture, realistic creases, reflections on glasses and shoes. True-to-life colour, sharp focus, editorial fashion photography quality.
```

档位措辞：
- Average(normal)：保持 "Ultra-photorealistic"，加 "natural proportions"。
- Bold(freak)："Ultra-photorealistic, subtly stylized"——B 文爆款风格的默认档。
- Extreme(total)："Photorealistic caricature with boldly exaggerated yet anatomically coherent [feature]"，夸张特征要写尺度词（"oversized chin twice normal size"）。

## T3 · 负向词

```
cartoon, illustration, 3D render, CGI, plastic skin, airbrushed, overly smooth skin, waxy, doll-like, distorted hands, extra fingers, deformed face, asymmetrical eyes, big grin, blurry, low resolution, oversaturated, harsh shadows, busy background, cropped feet, cropped head, text, watermark, logo
```
- Extreme 档移除 `deformed face, asymmetrical eyes`（夸张是有意的；es_uneven/ff_ears_9 等不对称选项同理）。
- 防漂移（drift guard）：负向不能"要求保留"，所以把 must-keep 锚点**写进正向**（Hair 行首 + Character notes 再说一次），负向只放会替换锚点的词，例如锅盖头角色负向加 `side part, slicked back hair, long hair`。
- 工具不支持 negative 参数时（image_generate / omnimux_image_submit），把关键负向改写为正向约束句：“mouth closed and neutral; plain grey backdrop only”。

## T4 · EDIT 修改（保脸，绝不重写）

```
Using the reference image, keep the exact same person: identical face, skin, freckles, hair shape and colour, glasses, facial hair, body proportions, outfit, pose, lighting, background and framing. Change ONLY: [one specific change]. Everything else must remain pixel-faithful to the reference.
```
- 一次只改一处；改两处 = 两次 EDIT。
- 如果当前工具没有可用的参考图通道 → 告知用户，改用"全文 CHARACTER 段 + 只改动目标字段"的文生图重跑，并在 run 中标记 `identity_drift` 风险。

## T5 · 角色设定表（CHARACTER SHEET）

```
Create a professional character reference sheet of the exact same [man/woman/person] from the reference image, keeping face, skin, body shape, hair, glasses, facial hair and outfit identical in every panel. Ultra-photorealistic studio photography, plain seamless light-grey background in every panel, consistent soft diffused lighting throughout.
LAYOUT: two rows on one wide image.
Top row – five full-body panels, head to toe, same scale, [POSE from motion_personality], arms by the sides:
1. Front view  2. Three-quarter front view  3. Side profile view  4. Three-quarter back view  5. Back view
Bottom row – three large chest-up close-ups:
6. Front headshot, deadpan and blank, eyes straight into the lens
7. Three-quarter headshot, same deadpan
8. Front headshot, SIGNATURE EXPRESSION: [e.g. one eyebrow raised high in quiet disapproval — clearly different from panel 6]
CHARACTER (must match exactly in every panel):
[完整 CHARACTER 段：体型年龄 → 皮肤 → 发型（形状/长度/分缝/刘海/颜色）→ 眼镜 → 胡须 → 脸型特征 → 服装逐件 → 道具位置]
QUALITY: 85mm lens, sharp focus in every panel, natural skin texture with visible pores, fine hair strands, realistic fabric texture. Accurate, consistent colours across all panels. Clean thin white dividing lines between panels, no text, no labels.
```
- 冒烟验证（2026-10-05）：gpt-image-2.5 纯文生图 + 完整 CHARACTER 段即可得到高一致的 8 格表；但第 8 格"招牌表情"被抹平 → 必须写"clearly different from panel 6"并给强动作词。
- 比例 16:9（omnimux_image_submit aspectRatio）或 1536x1024（image_generate）。

## T6 · 场景/UGC 首帧（视频交接用）

```
Vertical 9:16 smartphone UGC frame of the exact same character from the reference sheet ([3 个 drift-guard 锚点]). [SCENE: 真实地点 + 时间光线]. [ACTION: 招牌动作 / 爆款格式的第一拍]. Face in the upper-middle third, clear of the bottom caption area. Handheld phone look, natural light, slight grain, deadpan expression.
```
- 首帧必须满足 A 文"第一秒决定一切"：动作 / 脸 / 文字钩子三选一明确存在。

## T7 · 交接包（给视频阶段 / Genjutsu 类动作迁移）

```
角色：___   slug：___   档位：___
锁定参考：front=___  sheet=___
drift guard：___
动作人格：___   招牌梗：___
推荐爆款格式（3 个）：___（格式负责分发，角色负责差异）
平台：TikTok / Reels / Shorts / X（9:16）
版权提示：音乐与素材须自有或授权
```
