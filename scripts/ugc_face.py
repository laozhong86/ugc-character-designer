#!/usr/bin/env python3
"""UGC 捏脸引擎（face builder）—— 随机捏脸 + 分层自定义捏脸，共用同一套兼容性规则与权重模型。

随机捏脸（一次出结果）:
  ugc_face.py random [--seed N] [--tier T] [--lock JSON] [--count K] [--slug SLUG] [--market global|western|regional|cn]
    -> 种子可复现的组合 + 自动人设 + 生图 prompt/negative + 生图调用参数；--slug 时写入项目（character.json / face-state.json / prompts/）

分层自定义捏脸（多轮锁定）:
  ugc_face.py layers                                   # 列出 6 个层级及其类目
  ugc_face.py init  --state S.json [--tier T]          # 新建空状态
  ugc_face.py menu  --state S.json --layer L1          # 本层菜单：已按上层锁定过滤的选项 + 默认项 + 随机 + 自定义；含"为何隐藏"
  ugc_face.py apply --state S.json --layer L1 --answers JSON   # 写入本层答案，自动级联剔除下游冲突
  ugc_face.py prompt --state S.json [--slug SLUG]      # 汇总 → 生图 prompt（可落项目）
  ugc_face.py check --sel JSON [--tier T]              # 仅跑兼容性规则

answers 值格式（每个类目一个键）:
  "default" | "random" | "<option_id>" | ["id1","id2"]（多选类目）
  {"custom": "中文描述", "en": "english prompt phrase"}   # 自定义输入；能匹配到选项则自动映射，否则作为自定义描述注入 prompt
  {"id": "fh_beard", "override": true}                    # 用户明确要求时越过"软规则"（硬冲突与档位可见性不可越过）
Exit 0 ok · 2 usage/data error · 3 rule violation
"""
import argparse, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import ugc_taxonomy as tx  # noqa: E402

ZH = json.load(open(os.path.join(SKILL, "data", "zh-labels.json"), encoding="utf-8"))
TIERS = ["normal", "freak", "total"]


def zh_cat(c): return ZH["categories"].get(c, c)
def zh_opt(c, i): return ZH["options"].get(f"{c}/{i}", i)
def img(c, i): return os.path.join(SKILL, tx.asset_rel(c, i))


# ───────────────────────── 分层定义 ─────────────────────────
LAYERS = [
    ("L1", "身份基础", ["tier", "gender", "ethnicity_origin_base", "age"]),
    ("L2", "身体", ["skin_tone", "height", "body_type", "proportions"]),
    ("L3", "风格与发型", ["aesthetic", "hair", "hair_colour"]),
    ("L4", "脸部轮廓", ["freak_head", "freak_neck", "eye_shape", "eye_color"]),
    ("L5", "面部特征与细节", ["freak_face", "facial_hair", "distinctive", "accessory"]),
    ("L6", "人设与确认", ["persona"]),
]
LAYER_OF = {c: lid for lid, _, cats in LAYERS for c in cats}
ORDER = [c for _, _, cats in LAYERS for c in cats if c not in ("tier", "persona")]

# ───────────────────────── 兼容性规则（分层锁定的核心）─────────────────────────
TALL_HAIR = {"hs_beehive", "hs_softserve", "hs_horns", "hs_corkscrews", "hs_stairs", "hs_sphere", "hair_afro", "hs_mouse",
             "hair_punk", "hs_hedgehog", "hs_wings", "hs_sidecoil", "hs_pompadour"}
BROW_OPTS = {("freak_face", "fn_thickbrows"), ("freak_face", "ff_brows_5"), ("freak_face", "ff_brows_6"), ("freak_face", "ff_brows_7"),
             ("distinctive", "df_bleached"), ("distinctive", "df_slits"), ("distinctive", "df_scar")}
# 软规则：(名称, 说明, 判定函数(sel, cat, oid) -> 冲突则返回原因字符串)


def _has(sel, c, *ids): return any(i in ids for i in sel.get(c, []))


def soft_rules(sel, cat, oid):
    g = (sel.get("gender") or [None])[0]
    if cat == "facial_hair" and oid != "fh_none" and g and g not in ("male", "trans_man"):
        return f"性别={zh_opt('gender', g)}，胡须类默认隐藏（数据规则：仅男性/跨性别男性）"
    if cat == "hair_colour" and _has(sel, "hair", "hair_bald"):
        return "光头无需发色"
    if (cat, oid) == ("accessory", "acc_hat") and any(h in TALL_HAIR for h in sel.get("hair", [])):
        return f"帽子会盖住招牌发型（{zh_opt('hair', sel['hair'][0])}）"
    if cat == "hair" and oid in TALL_HAIR and _has(sel, "accessory", "acc_hat"):
        return "已选棒球帽，高耸发型会被遮住"
    if (cat, oid) in BROW_OPTS and _has(sel, "distinctive", "df_nobrows"):
        return "已选无眉，眉毛相关选项不适用"
    if (cat, oid) == ("distinctive", "df_nobrows") and any(_has(sel, c, i) for c, i in BROW_OPTS):
        return "已选眉毛相关特征，不能再无眉"
    teeth = {("distinctive", "df_grill"), ("distinctive", "df_braces"), ("freak_face", "ff_teeth_10"), ("freak_face", "ff_teeth_11")}
    if (cat, oid) in teeth:
        others = [(c, i) for c, i in teeth if (c, i) != (cat, oid) and _has(sel, c, i)]
        if (cat, oid) == ("distinctive", "df_grill") and others: return "金牙套会盖住其它牙齿特征"
        if ("distinctive", "df_grill") in others: return "已选金牙套"
        if (cat, oid) == ("distinctive", "df_braces") and ("distinctive", "df_grill") in others: return "已选金牙套"
    if (cat, oid) == ("distinctive", "df_elf") and (_has(sel, "freak_face", "ff_ears_8", "ff_ears_9")):
        return "已选耳朵特征，与精灵耳冲突"
    if cat == "freak_face" and oid in ("ff_ears_8", "ff_ears_9") and _has(sel, "distinctive", "df_elf"):
        return "已选精灵耳"
    if cat == "proportions":
        if oid == "pr_waist" and (_has(sel, "body_type", "body_heavy") or _has(sel, "proportions", "pr_egg", "pr_potbelly")):
            return "细腰与壮硕/蛋形/啤酒肚矛盾"
        if oid in ("pr_egg", "pr_potbelly") and _has(sel, "proportions", "pr_waist"): return "已选细腰"
        if oid == "pr_shortlegs" and _has(sel, "proportions", "pr_longlimbs"): return "已选超长四肢"
        if oid == "pr_longlimbs" and _has(sel, "proportions", "pr_shortlegs"): return "已选短腿"
    if (cat, oid) == ("body_type", "body_heavy") and _has(sel, "proportions", "pr_waist"):
        return "已选细腰"
    BODY_PROP = {"body_ultra": {"pr_egg", "pr_potbelly", "pr_waist", "pr_shortlegs", "pr_longlimbs"},
                 "body_muscular": {"pr_egg", "pr_potbelly"}, "body_curvy": {"pr_potbelly", "pr_egg"}, "body_slim": {"pr_potbelly"}}
    if cat == "proportions":
        b = first(sel, "body_type")
        if b and oid in BODY_PROP.get(b, set()): return f"与体型「{zh_opt('body_type', b)}」视觉矛盾"
    if cat == "body_type" and any(p in BODY_PROP.get(oid, set()) for p in sel.get("proportions", [])):
        return "与已选身材比例视觉矛盾"
    return None


def hard_rules(sel, cat, oid, tier):
    o = tx.opt(cat, oid)
    if o is None: return "未知选项"
    if tier and tier not in o["visibleIn"]:
        return f"{zh_opt('tier', tier)} 档不可见（需 {'/'.join(zh_opt('tier', t) for t in o['visibleIn'])}）"
    trial = {k: list(v) for k, v in sel.items()}
    if tx.CATS[cat]["max"] <= 1: trial[cat] = [oid]
    else: trial[cat] = list(dict.fromkeys(trial.get(cat, []) + [oid]))
    msg = tx.conflict(tier or "total", trial)
    if msg: return "数据硬冲突：" + msg
    return None


LAYER_RANK = {l: n for n, (l, _, _) in enumerate(LAYERS)}


def upstream(sel, cat):
    """Layered locking: a choice is only constrained by choices in the same or earlier layers.
    Later-layer picks that conflict are cascade-removed, never block an upstream change."""
    r = LAYER_RANK[LAYER_OF[cat]]
    return {k: v for k, v in sel.items() if k in LAYER_OF and LAYER_RANK[LAYER_OF[k]] <= r}


def allowed(sel, cat, oid, tier, overrides=(), layered=True):
    """Returns (ok, reason, kind)."""
    if layered: sel = upstream(sel, cat)
    r = hard_rules(sel, cat, oid, tier)
    if r: return False, r, "hard"
    if f"{cat}/{oid}" in overrides: return True, None, None
    r = soft_rules(sel, cat, oid)
    if r: return False, r, "soft"
    return True, None, None


def check_selection(sel, tier, overrides=()):
    """Every pick validated against all other picks; returns list of violations."""
    out = []
    for c in ORDER:
        for i in sel.get(c, []):
            rest = {k: [x for x in v if not (k == c and x == i)] for k, v in sel.items()}
            ok, why, kind = allowed(rest, c, i, tier, overrides, layered=True)
            if not ok: out.append({"key": f"{c}/{i}", "zh": f"{zh_cat(c)}={zh_opt(c, i)}", "reason": why, "kind": kind})
    try: tx.validate(tier, sel)
    except tx.VErr as e: out.append({"key": "selection", "reason": e.msg, "kind": "hard"})
    return out


# ───────────────────────── 权重模型（随机与默认项共用）─────────────────────────
DATA_RZ = tx.TAX.get("rules", {}).get("randomize", {})
ETH_SKIN = {"african": {"st_deep": 3, "st_ebony": 3, "st_brown": 2}, "east_asian": {"st_porcelain": 2, "st_fair": 3, "st_light": 2},
            "european": {"st_porcelain": 2, "st_fair": 3, "st_light": 2}, "indian": {"st_tan": 2, "st_brown": 3, "st_olive": 1},
            "middle_eastern": {"st_olive": 3, "st_tan": 2, "st_light": 1}, "latin_american": {"st_tan": 3, "st_olive": 2, "st_brown": 2, "st_light": 1}}
ETH_EYE = {"european": {"eye_blue": 3, "eye_green": 2, "eye_grey": 2, "eye_hazel": 2, "eye_brown": 2, "eye_ice_blue": 1},
           "latin_american": {"eye_brown": 3, "eye_hazel": 2, "eye_amber": 1, "eye_green": 1}}
EYE_DEFAULT = {"eye_brown": 3, "eye_black": 2, "eye_hazel": 1, "eye_amber": 1}
ETH_EYESHAPE = {"east_asian": {"es_monolid": 2, "es_almond": 1, "es_hooded": 1}}
AGE_HAIRCOL = {"senior": {"hc_grey": 4, "hc_white": 4}, "mature": {"hc_grey": 1.5}}
STYLE_HAIR = {"retro": ["hair_mullet", "hs_pompadour", "hs_beehive", "hair_bowl", "hs_dome", "hs_lampshade", "hs_shelf"],
              "goth": ["hair_long", "hair_bowl", "hs_horns", "hs_lampshade", "hs_corkscrews", "hair_punk"],
              "y2k": ["hair_pigtails", "hs_mouse", "hs_wings", "hs_hedgehog", "hair_long", "hs_sidecoil"],
              "sporty": ["hair_buzz", "hair_mullet", "hair_short", "hair_braids", "hs_hedgehog"],
              "suits": ["hair_short", "hair_bowl", "hair_bald", "hs_stairs", "hs_tufts", "hs_mushroom"],
              "theatrical": ["hs_beehive", "hs_softserve", "hs_horns", "hs_corkscrews", "hs_sphere", "hs_wings"],
              "streetstyle": ["hair_braids", "hair_afro", "hair_punk", "hs_hedgehog", "hair_buzz", "hs_sphere"],
              "casual": ["hair_short", "hair_long", "hs_dome", "hair_afro", "hs_mushroom", "hair_mullet"]}
STYLE_HAIRCOL = {"goth": {"hc_black": 3, "hc_platinum": 2, "hc_white": 1}, "y2k": {"hc_pink": 2, "hc_platinum": 2, "hc_blonde": 2, "hc_lilac": 1},
                 "retro": {"hc_ginger": 2, "hc_chestnut": 2, "hc_blonde": 1, "hc_red": 1}, "theatrical": {"hc_red": 2, "hc_white": 2, "hc_ginger": 1},
                 "streetstyle": {"hc_blue": 1, "hc_green": 1, "hc_platinum": 1, "hc_black": 1}, "sporty": {"hc_blonde": 1, "hc_black": 1},
                 "suits": {"hc_black": 2, "hc_darkbrown": 2}, "casual": {"hc_darkbrown": 2, "hc_chestnut": 1}}
STYLE_ACC = {"suits": {"acc_glasses": 2}, "y2k": {"acc_jewelry": 2, "acc_bag": 1}, "streetstyle": {"acc_headphones": 2, "acc_hat": 2, "acc_bag": 1},
             "sporty": {"acc_headphones": 1, "acc_hat": 1}, "retro": {"acc_glasses": 2, "acc_bag": 1}, "goth": {"acc_jewelry": 2},
             "theatrical": {"acc_jewelry": 1}, "casual": {"acc_bag": 1, "acc_hat": 1}}
FEM_HAIR = {"hair_long", "hair_pigtails", "hs_beehive", "hair_braids", "hs_lampshade", "hs_mouse", "hs_wings", "hs_shelf", "hs_corkscrews", "hs_sidecoil", "hs_softserve"}
MASC_HAIR = {"hair_short", "hair_buzz", "hair_bald", "hair_bowl", "hair_mullet", "hair_punk", "hs_tufts", "hs_stairs", "hs_hedgehog", "hs_mushroom"}
EXAG_CATS = {"hair", "freak_face", "freak_head", "eye_shape", "facial_hair", "proportions", "freak_neck"}
TIER_W = {"normal": 0.3, "freak": 0.5, "total": 0.2}
AGE_W = {"adult": 0.6, "mature": 0.25, "senior": 0.15}


def first(sel, c): return (sel.get(c) or [None])[0]


def strong(cat, oid):
    """Counts against the exaggeration budget: anything that reads as a 'signature' at thumbnail size."""
    o = tx.opt(cat, oid)
    if not o: return False
    if "normal" not in o["visibleIn"]: return True
    if cat in ("freak_face", "distinctive", "proportions"): return True
    if cat == "facial_hair": return oid not in ("fh_none", "fh_stubble")
    if cat == "hair": return oid in TALL_HAIR or oid in {"hair_bald", "hair_bowl", "hair_mullet", "hair_braids", "hair_pigtails", "hair_buzz"}
    return (cat, oid) in {("body_type", "body_ultra"), ("body_type", "body_heavy"), ("height", "h_very_tall"), ("eye_shape", "es_huge")}


BUDGET = {"normal": 3, "freak": 4, "total": 5}


def weight(sel, cat, oid, tier, randomizing=False):
    """Affinity of an option given what is already locked (all > 0 so nothing is impossible, just less likely)."""
    w = 1.0
    eth, g, age, sty = first(sel, "ethnicity_origin_base"), first(sel, "gender"), first(sel, "age"), first(sel, "aesthetic")
    if cat == "skin_tone" and eth: w = ETH_SKIN.get(eth, {}).get(oid, 0.0 if randomizing else 0.05)
    if cat == "eye_color": w = (ETH_EYE.get(eth) or EYE_DEFAULT).get(oid, 0.2)
    if cat == "eye_shape" and eth in ETH_EYESHAPE: w *= ETH_EYESHAPE[eth].get(oid, 1)
    if cat == "hair_colour":
        w = 1.0
        if age in AGE_HAIRCOL: w *= AGE_HAIRCOL[age].get(oid, 0.5 if age == "senior" else 1)
        if sty in STYLE_HAIRCOL: w *= STYLE_HAIRCOL[sty].get(oid, 0.6)
    if cat == "hair":
        if sty and oid in STYLE_HAIR.get(sty, []): w *= 3
        if g in ("female", "trans_woman") and oid in FEM_HAIR: w *= 1.5
        if g in ("male", "trans_man") and oid in MASC_HAIR: w *= 1.5
        if oid == "hs_lampshade": w *= 1.5  # data randomize boost
    if cat == "accessory" and sty: w *= STYLE_ACC.get(sty, {}).get(oid, 1)
    if randomizing and (cat, oid) == ("accessory", "acc_hat"): w *= 0.3  # hats hide the hair anchor
    if cat == "age": w = AGE_W.get(oid, 1)
    if cat == "aesthetic": w = {"suits": 4, "retro": 2}.get(oid, 4 / 6)  # data: suits .4 retro .2 rest share .4
    if cat == "gender": w = {"male": 0.67, "female": 0.33}.get(oid, 0.0)
    if randomizing and cat == "body_type" and oid == "body_curvy": w = 0.0  # data randomize excludes curvy
    if tier in ("freak", "total") and cat in EXAG_CATS:
        o = tx.opt(cat, oid)
        if "normal" not in o["visibleIn"]: w *= 2.5
        if tier == "total" and o["visibleIn"] == ["total"]: w *= 1.5
    return w


def candidates(sel, cat, tier, overrides=()):
    ok, hidden = [], []
    for o in tx.CATS[cat]["options"]:
        a, why, kind = allowed(sel, cat, o["id"], tier, overrides)
        (ok if a else hidden).append((o["id"], why, kind))
    return [i for i, _, _ in ok], [{"key": f"{cat}/{i}", "zh": zh_opt(cat, i), "reason": why, "kind": kind} for i, why, kind in hidden]


def wchoice(rnd, items, weights):
    tot = sum(weights)
    if tot <= 0: return rnd.choice(items)
    r = rnd.random() * tot; acc = 0
    for it, w in zip(items, weights):
        acc += w
        if r < acc: return it
    return items[-1]


# ───────────────────────── 随机捏脸算法 ─────────────────────────
def sample(seed=None, tier=None, lock=None, market="global"):
    seed = seed if seed is not None else random.randrange(1, 10**9)
    rnd = random.Random(seed)
    lock = {k: (v if isinstance(v, list) else [v]) for k, v in (lock or {}).items()}
    tier = tx.tier_of(tier) if tier else (lock.pop("tier", [None])[0] or wchoice(rnd, TIERS, [TIER_W[t] for t in TIERS]))
    sel = {}

    used = [0]

    def pick(cat, n=1, optional=False):
        if cat in lock:
            sel[cat] = lock[cat]; used[0] += sum(strong(cat, i) for i in lock[cat]); return
        picks = []
        for _ in range(n):
            pool, _h = candidates({**sel, cat: picks} if picks else sel, cat, tier)
            pool = [p for p in pool if p not in picks]
            if cat == "body_type" and tier == "normal": pool = [p for p in pool if p != "body_ultra"]
            if used[0] >= BUDGET[tier]:
                pool = [p for p in pool if not strong(cat, p)]
                if optional and not pool: break
            ws = [weight(sel, cat, p, tier, randomizing=True) for p in pool]
            if not pool or sum(ws) <= 0: break
            c = wchoice(rnd, pool, ws); picks.append(c); used[0] += strong(cat, c)
        if picks: sel[cat] = picks

    # 顺序 = 先身份，再风格与招牌发型（锚点优先占用预算），再身体，最后脸部细节
    pick("gender"); pick("ethnicity_origin_base"); pick("age"); pick("skin_tone")
    pick("aesthetic"); pick("hair"); pick("hair_colour")
    pick("height"); pick("body_type")
    if rnd.random() < 0.35: pick("proportions", optional=True)
    pick("freak_head"); pick("freak_neck"); pick("eye_shape"); pick("eye_color")
    pick("freak_face", 1 if (tier == "normal" and rnd.random() < 0.7) else 2, optional=True)
    if first(sel, "gender") in ("male", "trans_man") and rnd.random() < 0.55: pick("facial_hair", optional=True)
    if first(sel, "gender") not in ("male", "trans_man") or not sel.get("facial_hair"): sel["facial_hair"] = ["fh_none"]
    if rnd.random() < (0.4 if tier == "normal" else 0.6): pick("distinctive", optional=True)
    if rnd.random() < 0.5: pick("accessory", optional=True)
    # 招牌锚点保障：至少一个缩略图可读的突出特征
    if used[0] == 0 and "distinctive" not in lock: pick("distinctive")
    sel = {k: v for k, v in sel.items() if v}
    sel = tx.validate(tier, sel)
    return seed, tier, sel


# ───────────────────────── 自动人设（随机模式用）─────────────────────────
ARCHETYPES = [
    {"role": "substitute geography teacher", "does": "reviews European capitals they have never visited, with a pointer and a laminated map", "opinion": "correct map projections", "niche": "travel & geography comedy", "prop": "laminated world map", "bit": "unrolls the map at the worst possible moment", "styles": ["retro", "suits"]},
    {"role": "gym equipment reviewer", "does": "tests every machine at the gym and clearly resents all of them", "opinion": "the moral failings of treadmills", "niche": "fitness reviews", "prop": "clipboard and stopwatch", "bit": "gives every machine 2/10 without blinking", "styles": ["sporty", "casual"]},
    {"role": "retired synchronized swimmer", "does": "judges office chairs like an Olympic panel", "opinion": "posture as a moral issue", "niche": "product reviews", "prop": "judge scorecards", "bit": "holds up a scorecard after every sit", "styles": ["sporty", "retro"]},
    {"role": "Victorian ghost-tour guide", "does": "reviews modern apps as if they were haunted artefacts", "opinion": "the soul-stealing nature of notifications", "niche": "tech reviews", "prop": "brass lantern", "bit": "blows out the lantern when an app disappoints", "styles": ["theatrical", "goth"]},
    {"role": "1970s game-show host", "does": "reviews supermarket snacks as if each were the grand prize", "opinion": "the decline of crunch", "niche": "food reviews", "prop": "gold handheld microphone", "bit": "announces every price like a jackpot", "styles": ["retro", "suits"]},
    {"role": "haunted-mansion butler", "does": "rates fast food with silver-service solemnity", "opinion": "the proper temperature of fries", "niche": "food reviews", "prop": "silver serving cloche", "bit": "lifts the cloche to reveal a single nugget", "styles": ["goth", "suits"]},
    {"role": "pop star who never left 2003", "does": "reviews today's gadgets against their flip phone", "opinion": "ringtones as high art", "niche": "tech nostalgia", "prop": "glittery flip phone", "bit": "snaps the flip phone shut to end every verdict", "styles": ["y2k"]},
    {"role": "corporate compliance officer", "does": "audits playgrounds, picnics and birthday parties", "opinion": "unregulated fun", "niche": "deadpan sketch comedy", "prop": "lanyard badge and clipboard", "bit": "issues a formal warning to a swing", "styles": ["suits", "casual"]},
    {"role": "medieval town herald", "does": "announces trivial daily news with full ceremony", "opinion": "the importance of proclamations", "niche": "news comedy", "prop": "parchment scroll and tiny trumpet", "bit": "toots the trumpet before every non-event", "styles": ["theatrical"]},
    {"role": "opera diva", "does": "does grocery hauls with tragic intensity", "opinion": "the drama of discounted vegetables", "niche": "lifestyle & haul", "prop": "folding lace fan", "bit": "snaps the fan open at every price tag", "styles": ["theatrical", "retro"]},
    {"role": "sneaker monk", "does": "reviews streetwear drops in a whisper", "opinion": "the sacredness of unworn soles", "niche": "fashion & sneakers", "prop": "pristine sneaker box", "bit": "bows to the box before opening it", "styles": ["streetstyle"]},
    {"role": "night-shift security guard", "does": "reviews vending-machine snacks at 3 a.m.", "opinion": "loyalty to one specific crisp flavour", "niche": "food reviews", "prop": "heavy flashlight", "bit": "interrogates each snack under the flashlight", "styles": ["casual", "streetstyle"]},
    {"role": "90s aerobics instructor", "does": "teaches office productivity as a cardio routine", "opinion": "the healing power of step class", "niche": "self-help parody", "prop": "neon step board", "bit": "counts '5, 6, 7, 8' before answering email", "styles": ["sporty", "y2k"]},
    {"role": "museum curator", "does": "presents everyday rubbish as priceless artefacts", "opinion": "the cultural value of receipts", "niche": "deadpan comedy", "prop": "white cotton gloves", "bit": "places objects on a velvet cushion", "styles": ["suits", "retro"]},
    {"role": "vampire accountant", "does": "reviews sunscreens with grave professionalism", "opinion": "SPF ratings", "niche": "beauty reviews", "prop": "leather-bound ledger", "bit": "files every product under 'acceptable losses'", "styles": ["goth"]},
    {"role": "tax auditor", "does": "reviews cafés by itemising everything", "opinion": "the true cost of oat milk", "niche": "food & café reviews", "prop": "printing calculator", "bit": "tears off the receipt tape as a verdict", "styles": ["suits", "casual"]},
    {"role": "birdwatcher", "does": "documents city pigeons as rare species", "opinion": "pigeon hierarchy", "niche": "nature parody", "prop": "oversized binoculars", "bit": "whispers the Latin name of every pigeon", "styles": ["casual", "retro"]},
    {"role": "elevator-music DJ", "does": "remixes viral songs into lift music", "opinion": "the calming power of smooth jazz", "niche": "music comedy", "prop": "tiny keytar", "bit": "drops the beat that never drops", "styles": ["streetstyle", "y2k"]},
    {"role": "fashion-week critic", "does": "reviews supermarket outfits with runway severity", "opinion": "beige as a moral choice", "niche": "fashion commentary", "prop": "tiny notepad and fountain pen", "bit": "lowers sunglasses to deliver one-word verdicts", "styles": ["goth", "suits", "y2k"]},
    {"role": "motivational speaker with zero motivation", "does": "gives life advice in a total monotone", "opinion": "the overrated nature of trying", "niche": "self-help parody", "prop": "podium microphone", "bit": "ends every talk with an unenthusiastic fist pump", "styles": ["suits", "casual"]},
]
NAMES = {"african": ["Tobi Okafor", "Amara Nwosu", "Kwame Asante", "Zuri Mensah"], "east_asian": ["Rin Takeda", "Jun Park", "Mei Lan", "Haru Sato"],
         "european": ["Ambrose Pell", "Nora Vint", "Dex Halloran", "Greta Lund"], "indian": ["Ravi Menon", "Priya Iyer", "Arjun Rao", "Leela Das"],
         "middle_eastern": ["Karim Haddad", "Layla Nassar", "Omar Farouk", "Yasmin Aziz"], "latin_american": ["Mateo Rivas", "Lucía Quay", "Diego Soto", "Marisol Vega"]}
AGE_WORD = {"adult": "late-20s", "mature": "late-40s", "senior": "late-60s"}


def persona(rnd, sel):
    sty = first(sel, "aesthetic")
    pool = [a for a in ARCHETYPES if sty in a["styles"]] or ARCHETYPES
    a = rnd.choice(pool)
    name = rnd.choice(NAMES.get(first(sel, "ethnicity_origin_base"), sum(NAMES.values(), [])))
    age = AGE_WORD.get(first(sel, "age"), "late-20s")
    return {"name": name, "archetype": a["role"],
            "one_line_vibe": f"a {age} {a['role']} who {a['does']}",
            "bio": [f"{name} is a {age} {a['role']}.", f"They {a['does']}.", f"They have very strong opinions about {a['opinion']}."],
            "niche": a["niche"], "prop": a["prop"], "running_bit": a["bit"]}


# ───────────────────────── prompt 组装（系统风格提示词 + 参数）─────────────────────────
def compose(tier, sel, pers=None, customs=None):
    notes = []
    if pers:
        notes.append(f"Signature prop: {pers['prop']}. Character: {pers['one_line_vibe']}.")
    for c, v in (customs or {}).items():
        if v.get("en"): notes.append(f"{c.replace('_', ' ')}: {v['en']}")
    sig, neg = tx.build_signature(tier, sel, " ".join(notes))
    return sig, neg


def summary(tier, sel, customs=None):
    rows = [{"category": "tier", "zh": zh_cat("tier"), "value": zh_opt("tier", tier), "key": f"tier/{tier}", "image": img("tier", tier)}]
    for c in ORDER:
        for i in sel.get(c, []):
            rows.append({"category": c, "zh": zh_cat(c), "value": zh_opt(c, i), "key": f"{c}/{i}", "look": tx.look(c, i), "image": img(c, i)})
    for c, v in (customs or {}).items():
        rows.append({"category": c, "zh": zh_cat(c), "value": "自定义：" + v.get("custom", ""), "key": None, "en": v.get("en")})
    return rows


def gen_call(prompt, dest):
    return {"tool": "omnimux_image_submit", "args": {"model": "gpt-image-2.5", "operation": "text_to_image", "aspectRatio": "9:16",
                                                      "prompt": prompt, "dest": dest, "audioTrack": {}},
            "fallback": {"tool": "image_generate", "args": {"prompt": prompt, "size": "1024x1536", "quality": "high"}}}


def anchors_of(sel):
    return [tx.fragment(c, i) for c in ("hair", "hair_colour", "distinctive", "facial_hair") for i in sel.get(c, []) if i != "fh_none"][:5]


def write_project(slug, tier, sel, pers, prompt, neg, state=None):
    root = os.path.join(os.getcwd(), "ugc-characters", slug)
    for d in ("runs", "refs", "out", "prompts"): os.makedirs(os.path.join(root, d), exist_ok=True)
    cp = os.path.join(root, "character.json")
    card = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else {}
    look = lambda c: tx.look(c, first(sel, c)) if first(sel, c) else ""
    standout = next((tx.look(c, i) for c in ("distinctive", "freak_face", "facial_hair") for i in sel.get(c, []) if i != "fh_none"), "") or look("freak_head")
    card.update({"slug": slug, "name": (pers or {}).get("name", card.get("name", slug)), "tier": tier, "selection": sel,
                 "signature": {"hair": " ".join(x for x in [look("hair"), tx.fragment("hair_colour", first(sel, "hair_colour")) if first(sel, "hair_colour") else ""] if x),
                               "standout_feature": standout, "outfit": look("aesthetic"), "prop": (pers or {}).get("prop", card.get("signature", {}).get("prop", "")),
                               "expression": "deadpan"},
                 "drift_guard": anchors_of(sel), "status": card.get("status", "concept"),
                 "originality": {"is_original": True, "not_based_on": "random taxonomy composite; no real person / celebrity / IP"}})
    if pers:
        card.update(bio=pers["bio"], one_line_vibe=pers["one_line_vibe"], niche=pers["niche"], running_bit=pers["running_bit"],
                    motion_personality=card.get("motion_personality") or "stiff, deliberate, minimal movement; deadpan reactions")
    card.setdefault("created_at", tx_now()); card.setdefault("platforms", ["tiktok", "instagram", "youtube_shorts", "x"]); card.setdefault("locked_refs", [])
    json.dump(card, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    n = len([f for f in os.listdir(os.path.join(root, "prompts")) if f.startswith("fullbody")]) + 1
    pf = os.path.join(root, "prompts", f"fullbody-{n}.txt"); nf = os.path.join(root, "prompts", f"fullbody-{n}.neg.txt")
    open(pf, "w", encoding="utf-8").write(prompt); open(nf, "w", encoding="utf-8").write(neg)
    if state is not None: json.dump(state, open(os.path.join(root, "face-state.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return {"card": cp, "prompt_file": pf, "negative_file": nf, "dest": os.path.join(root, "out", f"fullbody-{n}.png")}


def tx_now():
    import datetime as dt
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# ───────────────────────── 自定义捏脸：状态 / 菜单 / 应用 ─────────────────────────
def load_state(p):
    if not os.path.exists(p): raise SystemExit(f"no state {p}; run init")
    return json.load(open(p, encoding="utf-8"))


def save_state(p, s):
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    json.dump(s, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def default_for(sel, cat, tier, pool):
    """Highest-affinity option; categories without any preference default to 'random'."""
    if cat == "facial_hair": return "fh_none" if "fh_none" in pool else (pool[0] if pool else "random")
    if cat in ("proportions", "distinctive"): return "none"
    if cat == "accessory": return "acc_none" if "acc_none" in pool else "none"
    if cat == "freak_neck": return "neck_normal" if "neck_normal" in pool else "random"
    if cat == "height": return "h_average" if "h_average" in pool else "random"
    if cat in ("gender", "ethnicity_origin_base"): return "random"
    if cat == "age": return "adult"
    ws = {p: weight(sel, cat, p, tier) for p in pool}
    if not ws: return "random"
    best = max(ws.values())
    tops = [p for p, w in ws.items() if w == best]
    return tops[0] if len(tops) == 1 else "random"


def menu(state, layer, top=8):
    lid = layer.upper()
    lay = next((l for l in LAYERS if l[0] == lid), None)
    if not lay: raise SystemExit(f"unknown layer {layer}; use {[l[0] for l in LAYERS]}")
    tier = state.get("tier"); sel = state["selection"]; ov = state.get("overrides", [])
    qs = []
    for cat in lay[2]:
        if cat == "persona":
            qs.append({"id": "persona", "zh": "人设", "type": "text", "question": "这个角色是谁、做什么内容、招牌梗是什么？（可留空 → 自动生成人设）",
                       "default": "auto", "fields": ["name", "one_line_vibe", "niche", "prop", "running_bit"]}); continue
        if cat == "tier":
            qs.append({"id": "tier", "zh": zh_cat("tier"), "multi": False, "max": 1, "default": "freak",
                       "options": [{"value": t, "zh": zh_opt("tier", t), "image": img("tier", t),
                                    "note": {"normal": "124 个选项可用，隐藏全部夸张发型/面部变形", "freak": "167 个选项，解锁 16 种夸张发型（推荐）", "total": "170 个全开，漫画级夸张"}[t]} for t in TIERS],
                       "extra": [{"value": "random", "zh": "随机"}]}); continue
        if not tier and LAYER_OF[cat] != "L1": qs.append({"id": cat, "blocked": "先在 L1 锁定夸张档位"}); continue
        tier_eff = tier or "total"
        if cat == "hair_colour" and first(sel, "hair") == "hair_bald":
            qs.append({"id": cat, "zh": zh_cat(cat), "skipped": "光头，无需发色"}); continue
        if cat == "facial_hair" and first(sel, "gender") not in (None, "male", "trans_man") and "facial_hair" not in [k.split('/')[0] for k in ov]:
            qs.append({"id": cat, "zh": zh_cat(cat), "skipped": f"性别={zh_opt('gender', first(sel, 'gender'))}，胡须已锁定为无（如用户明确要求可 override）", "locked_value": "fh_none"}); continue
        others = {k: v for k, v in sel.items() if k != cat}
        pool, hidden = candidates(others, cat, tier_eff, ov)
        ranked = sorted(pool, key=lambda p: -weight(others, cat, p, tier_eff))
        d = default_for(others, cat, tier_eff, pool)
        c = tx.CATS[cat]
        shown = ranked[:top]
        if d not in ("random", "none") and d not in shown: shown = [d] + shown[:top - 1]
        q = {"id": cat, "zh": zh_cat(cat), "multi": c["max"] > 1, "max": c["max"], "default": d,
             "options": [{"value": p, "zh": zh_opt(cat, p), "look": tx.look(cat, p), "image": img(cat, p), "swatch": tx.opt(cat, p).get("swatch"),
                          "slot": tx.opt(cat, p).get("slot"), "recommended": p == d} for p in shown],
             "more": [p for p in ranked if p not in shown],
             "extra": [{"value": "random", "zh": "随机（按已锁定条件加权）"}, {"value": "custom", "zh": "自定义输入"}] + ([{"value": "none", "zh": "不选"}] if c["max"] > 1 else []),
             "hidden": hidden}
        if cat == "freak_face": q["note"] = "同一部位（鼻/唇/眉/耳/牙/下巴…）只能选一个，最多 4 个；建议 1–2 个形成招牌"
        qs.append(q)
    return {"layer": lid, "title": lay[1], "tier": tier, "locked": summary(tier, sel, state.get("customs")) if tier else [], "questions": qs}


def resolve_custom(cat, text):
    hits = []
    for o in tx.CATS[cat]["options"]:
        zh = zh_opt(cat, o["id"]); en = " ".join([o["id"], o["label_en"], tx.fragment(cat, o["id"]), tx.look(cat, o["id"]) or ""]).lower()
        if zh and (zh in text or text in zh): hits.append(o["id"])
        elif any(w and len(w) > 2 and w in en for w in text.lower().split()): hits.append(o["id"])
    return hits


def apply(state, layer, answers):
    lid = layer.upper()
    lay = next((l for l in LAYERS if l[0] == lid), None)
    if not lay: raise SystemExit(f"unknown layer {layer}")
    sel = state["selection"]; ov = state.setdefault("overrides", []); customs = state.setdefault("customs", {}); log = []
    rnd = random.Random(state.setdefault("seed", random.randrange(1, 10**9)) + len(state.get("history", [])))
    if "tier" in answers:
        t = answers["tier"]; t = wchoice(rnd, TIERS, [TIER_W[x] for x in TIERS]) if t in ("random", "default") and t == "random" else ("freak" if t == "default" else tx.tier_of(t))
        if t not in TIERS: raise SystemExit("invalid tier")
        state["tier"] = t; log.append(f"档位 = {zh_opt('tier', t)}")
    tier = state.get("tier")
    for cat in lay[2]:
        if cat in ("tier",) or cat not in answers: continue
        v = answers[cat]
        if cat == "persona":
            state["persona"] = None if v in ("auto", "default", "", None) else v; continue
        if not tier and LAYER_OF[cat] != "L1": raise SystemExit("lock tier first (L1)")
        c = tx.CATS[cat]; others = {k: vv for k, vv in sel.items() if k != cat}
        tier = tier or "total"
        pool, _ = candidates(others, cat, tier, ov)
        vals = v if isinstance(v, list) else [v]
        picks = []
        for x in vals:
            if isinstance(x, dict) and "custom" in x:
                hits = [h for h in resolve_custom(cat, x["custom"]) if h in pool]
                if len(hits) == 1 and not x.get("keep_custom"):
                    picks.append(hits[0]); log.append(f"{zh_cat(cat)}：自定义「{x['custom']}」匹配到选项 {zh_opt(cat, hits[0])}")
                else:
                    customs[cat] = {"custom": x["custom"], "en": x.get("en", "")}
                    log.append(f"{zh_cat(cat)}：自定义描述「{x['custom']}」" + ("" if x.get("en") else "（缺英文 en，prompt 将无法使用——请补充）") + (f"；相近选项 {[zh_opt(cat, h) for h in hits]}" if hits else ""))
                continue
            if isinstance(x, dict) and x.get("override"):
                key = f"{cat}/{x['id']}"
                if key not in ov: ov.append(key)
                pool, _ = candidates(others, cat, tier, ov); x = x["id"]; log.append(f"{zh_cat(cat)}：用户明确要求，越过软规则")
            if x == "none": picks = []; continue
            if x == "default": x = default_for(others, cat, tier, pool)
            if x in ("none",): continue
            if x == "random":
                cand = [p for p in pool if p not in picks]
                if cat == "facial_hair" and first(sel, "gender") not in ("male", "trans_man"): cand = ["fh_none"]
                x = wchoice(rnd, cand, [weight(others, cat, p, tier) for p in cand]) if cand else None
                if not x: continue
            if x not in pool:
                o = tx.opt(cat, x)
                if not o: raise SystemExit(f"unknown option {cat}/{x}")
                ok, why, kind = allowed(others, cat, x, tier, ov)
                print(json.dumps({"ok": False, "error": f"{zh_cat(cat)}={zh_opt(cat, x)} 不可选：{why}", "kind": kind,
                                  "hint": "软规则可用 {\"id\":..., \"override\": true} 越过" if kind == "soft" else "换一个选项"}, ensure_ascii=False))
                sys.exit(3)
            picks.append(x)
        if cat == "facial_hair" and first(sel, "gender") not in (None, "male", "trans_man") and not any(k.startswith("facial_hair/") for k in ov):
            picks = ["fh_none"]
        picks = list(dict.fromkeys(picks))[: c["max"]]
        if picks: sel[cat] = picks
        else: sel.pop(cat, None)
        if picks: log.append(f"{zh_cat(cat)} = {'、'.join(zh_opt(cat, p) for p in picks)}")
    # 级联：重新检查所有已选项，剔除被新锁定条件判为不兼容的
    removed = []
    for _ in range(12):
        bad = check_selection(sel, tier or "total", ov) if tier else []
        bad = [b for b in bad if b["key"] != "selection"]
        if not bad: break
        bad.sort(key=lambda b: LAYER_RANK[LAYER_OF[b["key"].split("/")[0]]])
        b = bad[-1]; c, i = b["key"].split("/")
        if LAYER_OF.get(c) == lid and c in answers: break  # 本层刚选的冲突交给用户
        sel[c] = [x for x in sel.get(c, []) if x != i]
        if not sel[c]: sel.pop(c)
        removed.append(f"{b['zh']}（{b['reason']}）")
    if first(sel, "gender") not in (None, "male", "trans_man") and not any(k.startswith("facial_hair/") for k in ov) and sel.get("facial_hair", ["fh_none"]) != ["fh_none"]:
        removed.append(f"胡须={zh_opt('facial_hair', first(sel, 'facial_hair'))}（性别改变）"); sel["facial_hair"] = ["fh_none"]
    state.setdefault("history", []).append({"layer": lid, "answers": answers})
    state.setdefault("done_layers", [])
    if lid not in state["done_layers"]: state["done_layers"].append(lid)
    nxt = next((l[0] for l in LAYERS if l[0] not in state["done_layers"]), None)
    return {"ok": True, "applied": log, "cascade_removed": removed, "next_layer": nxt, "locked": summary(tier, sel, customs) if tier else []}


# ───────────────────────── CLI ─────────────────────────
def out(o, code=0):
    print(json.dumps(o, ensure_ascii=False, indent=1)); sys.exit(code)


def parse(s):
    if not s: return {}
    if s.startswith("@"): return json.load(open(s[1:], encoding="utf-8"))
    return json.loads(s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("random"); r.add_argument("--seed", type=int); r.add_argument("--tier"); r.add_argument("--lock", default="")
    r.add_argument("--count", type=int, default=1); r.add_argument("--slug"); r.add_argument("--market", default="global")
    sp.add_parser("layers")
    i = sp.add_parser("init"); i.add_argument("--state", required=True); i.add_argument("--tier")
    m = sp.add_parser("menu"); m.add_argument("--state", required=True); m.add_argument("--layer", required=True); m.add_argument("--top", type=int, default=8)
    a = sp.add_parser("apply"); a.add_argument("--state", required=True); a.add_argument("--layer", required=True); a.add_argument("--answers", required=True)
    p = sp.add_parser("prompt"); p.add_argument("--state", required=True); p.add_argument("--slug")
    c = sp.add_parser("check"); c.add_argument("--sel", required=True); c.add_argument("--tier", default="total")
    args = ap.parse_args()

    if args.cmd == "layers":
        out([{"layer": l, "title": t, "categories": [{"id": x, "zh": zh_cat(x) if x != "persona" else "人设"} for x in cats]} for l, t, cats in LAYERS])
    if args.cmd == "random":
        base = args.seed if args.seed is not None else random.randrange(1, 10**9)
        results, seen = [], set()
        s = base
        while len(results) < max(1, args.count) and s < base + 200:
            seed, tier, sel = sample(s, args.tier, parse(args.lock), args.market); s += 1
            sig = (first(sel, "hair"), first(sel, "aesthetic"))
            if args.count > 1 and sig in seen: continue
            seen.add(sig)
            pers = persona(random.Random(seed), sel)
            prompt, neg = compose(tier, sel, pers)
            res = {"seed": seed, "tier": tier, "selection": sel, "summary": summary(tier, sel), "persona": pers, "prompt": prompt, "negative": neg,
                   "violations": check_selection(sel, tier)}
            if args.slug:
                slug = args.slug if args.count == 1 else f"{args.slug}-{len(results) + 1}"
                st = {"mode": "random", "seed": seed, "tier": tier, "selection": sel, "persona": pers, "customs": {}, "overrides": []}
                files = write_project(slug, tier, sel, pers, prompt, neg, st)
                res.update(slug=slug, files=files, generate=gen_call(prompt, files["dest"]))
            else:
                res["generate"] = gen_call(prompt, "<abs path>/ugc-characters/<slug>/out/fullbody-1.png")
            results.append(res)
        out(results[0] if args.count == 1 else {"count": len(results), "candidates": results})
    if args.cmd == "init":
        st = {"mode": "custom", "seed": random.randrange(1, 10**9), "tier": tx.tier_of(args.tier) if args.tier else None,
              "selection": {}, "customs": {}, "overrides": [], "persona": None, "done_layers": [], "history": []}
        save_state(args.state, st); out({"ok": True, "state": os.path.abspath(args.state), "next_layer": "L1"})
    if args.cmd == "menu":
        out(menu(load_state(args.state), args.layer, args.top))
    if args.cmd == "apply":
        st = load_state(args.state); res = apply(st, args.layer, parse(args.answers)); save_state(args.state, st); out(res)
    if args.cmd == "prompt":
        st = load_state(args.state)
        tier, sel = st.get("tier"), st["selection"]
        if not tier: out({"ok": False, "error": "tier not locked"}, 3)
        viol = check_selection(sel, tier, st.get("overrides", []))
        if viol: out({"ok": False, "violations": viol}, 3)
        pers = st.get("persona") or persona(random.Random(st["seed"]), sel)
        if isinstance(pers, dict) and "one_line_vibe" in pers and "prop" not in pers: pers.setdefault("prop", "")
        prompt, neg = compose(tier, sel, pers if pers.get("prop") is not None else None, st.get("customs"))
        res = {"ok": True, "tier": tier, "selection": sel, "summary": summary(tier, sel, st.get("customs")), "persona": pers, "prompt": prompt, "negative": neg,
               "missing_en": [c for c, v in st.get("customs", {}).items() if not v.get("en")]}
        if args.slug:
            files = write_project(args.slug, tier, sel, pers, prompt, neg, st); res.update(files=files, generate=gen_call(prompt, files["dest"]))
        out(res)
    if args.cmd == "check":
        sel = parse(args.sel); t = tx.tier_of(args.tier); v = check_selection(sel, t); out({"ok": not v, "violations": v}, 0 if not v else 3)


if __name__ == "__main__":
    main()
