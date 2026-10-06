#!/usr/bin/env python3
"""UGC character taxonomy CLI — faithful Python port of service/influencer/rules.go
plus the distilled "deadpan signature character" prompt layer.

Usage (run from anywhere; paths resolve relative to the skill root):
  ugc_taxonomy.py list                          # categories overview
  ugc_taxonomy.py show <category> [--tier T]    # options of one category
  ugc_taxonomy.py validate --tier T --sel JSON  # normalize + hard conflicts
  ugc_taxonomy.py build --tier T --sel JSON [--brief TEXT] [--mode base|signature|both]
  ugc_taxonomy.py random --tier T [--seed N] [--lock JSON]
  ugc_taxonomy.py diversity --tier T --sels '[sel1,sel2,sel3]' [--market global|western|regional|cn]
  ugc_taxonomy.py find "<words>" [--tier T]       # search options by id/label/fragment/visual look -> image path
  ugc_taxonomy.py get hair/hs_horns distinctive/df_gems   # exact lookup by index key -> record + single image
  ugc_taxonomy.py query --category hair --tier freak [--bold-only] [--text curl] [--fields all]
  ugc_taxonomy.py refs --sel JSON               # per-option reference images for a selection
  ugc_taxonomy.py reindex                       # regenerate data/option-index.json + options-table.md
  ugc_taxonomy.py selftest                      # port of rules_test.go + data integrity

--sel accepts inline JSON or @path/to/file.json, shape {"category":["option_id",...]}.
Exit code 0 = ok, 2 = validation error (message on stderr as JSON).
"""
import argparse, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "taxonomy.json")
TIERS = ["normal", "freak", "total"]
TIER_ALIAS = {"average": "normal", "bold": "freak", "extreme": "total"}

PROMPT_ORDER = [
    "gender", "ethnicity_origin_base", "age", "skin_tone", "height",
    "body_type", "proportions", "freak_head", "freak_neck", "eye_shape",
    "eye_color", "freak_face", "facial_hair", "hair", "hair_colour",
    "distinctive", "aesthetic", "accessory",
]

with open(DATA, encoding="utf-8") as fh:
    TAX = json.load(fh)
CATS = {c["id"]: c for c in TAX["categories"]}
FRAG = {c: {o["id"]: o["fragment"] for o in arr} for c, arr in TAX["prompt_map"]["categories"].items()}


class VErr(Exception):
    def __init__(self, field, msg):
        super().__init__(msg); self.field = field; self.msg = msg


VIS_PATH = os.path.join(ROOT, "data", "visual-descriptors.json")
VIS = json.load(open(VIS_PATH, encoding="utf-8"))["categories"] if os.path.exists(VIS_PATH) else {}


def asset_rel(cat, oid):
    """Per-option reference image: assets/options/<category>/<option_id>.webp (tier images under 'tier')."""
    return f"assets/options/{cat}/{oid}.webp"


def look(cat, oid):
    return VIS.get(cat, {}).get(oid, {}).get("look")


def tier_of(t):
    t = (t or "normal").lower()
    return TIER_ALIAS.get(t, t)


def opt(cat, oid):
    c = CATS.get(cat)
    if not c: return None
    for o in c["options"]:
        if o["id"] == oid: return o
    return None


def fragment(cat, oid):
    return FRAG.get(cat, {}).get(oid, oid)


def normalize(tier, sel):
    if tier not in TIERS:
        raise VErr("tier", "invalid tier")
    out = {}
    for cat, picks in sel.items():
        c = CATS.get(cat)
        if c is None:
            raise VErr(cat, f'unknown category "{cat}"')
        if isinstance(picks, str): picks = [picks]
        max_n = c.get("max") or 1
        kept = []
        for oid in picks:
            o = opt(cat, oid)
            if o is None:
                raise VErr(cat, f'unknown option "{oid}"')
            if tier not in o["visibleIn"]:
                continue
            if cat == "accessory" and oid == "acc_none":
                kept = [oid]; continue
            if cat == "accessory" and "acc_none" in kept:
                kept = []
            slot = o.get("slot")
            if slot:
                kept = [p for p in kept if (opt(cat, p) or {}).get("slot") != slot]
            if len(kept) >= max_n:
                continue  # Go semantics: cap keeps the FIRST picks
            if oid not in kept:
                kept.append(oid)
        if kept:
            out[cat] = kept
    return out


def has(sel, cat, *ids):
    return any(v in ids for v in sel.get(cat, []))


def conflict(tier, sel):
    if has(sel, "body_type", "body_heavy") and has(sel, "height", "h_tall", "h_very_tall"):
        return "Heavy build cannot be combined with Tall or Very tall."
    if tier != "normal" and has(sel, "body_type", "body_heavy", "body_muscular", "body_ultra") \
            and has(sel, "proportions", "pr_shortlegs", "pr_longlimbs"):
        return "This build cannot be combined with Short legs or Long limbs in this mode."
    if has(sel, "body_type", "body_ultra") and has(sel, "freak_neck", "neck_long"):
        return "Extreme muscular build cannot be combined with Long neck."
    if has(sel, "freak_neck", "neck_long") and has(sel, "freak_face", "ff_teeth_11"):
        return "Long neck cannot be combined with Buck teeth."
    return ""


def validate(tier, sel):
    norm = normalize(tier, sel)
    msg = conflict(tier, norm)
    if msg:
        raise VErr("selection", msg)
    return norm


def tier_lead(tier):
    return {
        "total": "Extreme caricature, exaggerated proportions, full-body character portrait of a",
        "freak": "Stylized, slightly exaggerated, full-body character portrait of a",
    }.get(tier, "Natural, realistic, full-body character portrait of a")


def build_base(tier, sel, brief=""):
    """Exact port of Go BuildPrompt (the product's server-side prompt)."""
    parts = [fragment(c, i) for c in PROMPT_ORDER for i in sel.get(c, [])]
    s = tier_lead(tier)
    if parts: s += " " + ", ".join(parts)
    brief = (brief or "").strip()
    if brief: s += ". " + brief
    return s + ". Studio background, full-body shot, 9:16 composition, high detail, clean lighting."


# ---- distilled signature layer (from @pounddz character-designer system prompt) ----
REALISM = {
    "normal": "Ultra-photorealistic",
    "freak": "Ultra-photorealistic, subtly stylized",
    "total": "Photorealistic caricature with boldly exaggerated yet anatomically coherent",
}
BASE_NEGATIVE = ("cartoon, illustration, 3D render, CGI, plastic skin, airbrushed, overly smooth skin, waxy, "
                 "doll-like, distorted hands, extra fingers, deformed face, asymmetrical eyes, big grin, blurry, "
                 "low resolution, oversaturated, harsh shadows, busy background, cropped feet, cropped head, "
                 "text, watermark, logo")


def _frags(sel, *cats):
    """Signature layer prefers the visual 'look' distilled from the reference image; falls back to the fragment."""
    return [look(c, i) or fragment(c, i) for c in cats for i in sel.get(c, [])]


NOUN = {"female": "woman", "male": "man", "trans_man": "trans man", "trans_woman": "trans woman", "non_binary": "non-binary person"}
AGE = {"adult": "in their late 20s", "mature": "in their late 40s", "senior": "in their late 60s"}  # agent may override with exact age in brief
ETH = {"african": "African", "east_asian": "East Asian", "european": "European", "indian": "South Asian",
       "middle_eastern": "Middle Eastern", "latin_american": "mixed-race Latin American"}


def subject(sel):
    g = (sel.get("gender") or [""])[0]; e = (sel.get("ethnicity_origin_base") or [""])[0]; a = (sel.get("age") or [""])[0]
    s = " ".join(x for x in [ETH.get(e, ""), NOUN.get(g, "person")] if x)
    if e and look("ethnicity_origin_base", e) and look("ethnicity_origin_base", e).lower() != f"{ETH.get(e, '').lower()} facial features":
        s += f" ({look('ethnicity_origin_base', e)})"
    if a:
        pron = {"female": "her", "trans_woman": "her", "male": "his", "trans_man": "his"}.get(g, "their")
        s += " " + AGE[a].replace("their", pron)
    return s


def build_signature(tier, sel, brief=""):
    who = subject(sel)
    build = ", ".join(_frags(sel, "height", "body_type", "proportions", "freak_neck"))
    skin = ", ".join(_frags(sel, "skin_tone"))
    hc = [fragment("hair_colour", i).replace(" hair", "") for i in sel.get("hair_colour", [])]
    hair = ", ".join(_frags(sel, "hair"))
    if hc: hair = f"entirely {hc[0]} hair (every strand {hc[0]}, no other colour): {hair}" if hair else f"{hc[0]} hair"
    face = ", ".join(_frags(sel, "freak_head", "eye_shape", "eye_color", "freak_face", "facial_hair", "distinctive"))
    outfit = ", ".join(_frags(sel, "aesthetic"))
    acc = [f for f in _frags(sel, "accessory") if f != "no accessories"]
    lead = REALISM.get(tier, REALISM["normal"])
    lines = [
        f"{lead} full-body studio portrait of {'an' if who[0].lower() in 'aeio' and not who.startswith('Euro') else 'a'} {who}" + (f", {build}" if build else "") +
        (f", {skin}" if skin else "") + ", standing stiffly upright, arms hanging by the sides, facing the camera. "
        "Plain seamless light-grey studio backdrop, smooth and evenly lit, with a soft natural shadow on the floor.",
        f"Hair: {hair or 'neat signature hairstyle'}, immaculate and slightly too precise, instantly readable at thumbnail size.",
        f"Face: {face + '; ' if face else ''}completely deadpan expression, lips closed, staring directly into the lens.",
        f"Outfit: {outfit or 'earnest, slightly old-fashioned outfit'} worn with total sincerity" +
        (f"; {', '.join(acc)}" if acc else "") + ".",
    ]
    if (brief or "").strip():
        lines.append(f"Character notes: {brief.strip()}")
    lines.append(
        "Photography: shot on a full-frame camera with an 85mm lens at f/8, eye-level, full body head to toe with a "
        "little space around them, 9:16 vertical frame. Soft diffused key light from front left with a large softbox, "
        "gentle fill, subtle rim light. Natural skin texture with visible pores, individual hair strands, fine fabric "
        "texture, realistic creases. True-to-life colour, sharp focus, editorial fashion photography quality.")
    neg = BASE_NEGATIVE
    if tier == "total":
        neg = neg.replace("deformed face, asymmetrical eyes, ", "")  # exaggeration is intended in Extreme
    anchors = [fragment(c, i) for c in ("hair", "hair_colour", "distinctive") for i in sel.get(c, [])]
    keep = ("; drift guard — must keep: " + ", ".join(anchors)) if anchors else ""
    return "\n".join(lines), neg + keep


def labels(sel):
    return [opt(c, i)["label_en"] for c in sorted(sel) for i in sel[c] if opt(c, i)]


# ---- randomize (taxonomy.rules.randomize) ----
def randomize(tier, seed=None, lock=None):
    rnd = random.Random(seed)
    rz = TAX.get("rules", {}).get("randomize", {})
    lock = lock or {}
    for _ in range(200):
        sel = {}
        for cid in PROMPT_ORDER:
            if cid in lock:
                sel[cid] = lock[cid] if isinstance(lock[cid], list) else [lock[cid]]; continue
            c = CATS[cid]
            pool = [o["id"] for o in c["options"] if tier in o["visibleIn"]]
            if cid == "body_type":
                pool = [p for p in pool if p != "body_curvy" and not (tier == "normal" and p == "body_ultra")]
            if cid == "facial_hair" and sel.get("gender", [""])[0] not in ("male", "trans_man"):
                sel[cid] = ["fh_none"]; continue
            weights = rz.get(cid) if isinstance(rz.get(cid), dict) else None
            def pick1(p):
                if weights:
                    r = rnd.random(); acc = 0.0
                    for k, w in weights.items():
                        acc += w
                        if r < acc and k in p: return k
                    rest = [x for x in p if x not in weights] or p
                    return rnd.choice(rest)
                return rnd.choice(p)
            n = 1 if c["max"] <= 1 else rnd.randint(1, min(2, c["max"]))
            if cid in ("proportions", "distinctive") and rnd.random() < 0.5:
                continue  # optional categories: often empty
            picks = []
            for _k in range(n):
                v = pick1(pool)
                if v not in picks: picks.append(v)
            sel[cid] = picks
        try:
            return validate(tier, sel)
        except VErr:
            continue
    raise VErr("random", "could not find a valid random selection")


BOLD_ONLY = {(c["id"], o["id"]) for c in TAX["categories"] for o in c["options"] if "normal" not in o["visibleIn"]}


def diversity(tier, sels, market="global", locked_ethnicity=False):
    """Concept-set gate for S1: distinct anchors, ethnic range, use of the tier's exclusive options."""
    f = []
    norms = []
    for i, s in enumerate(sels):
        try: norms.append(validate(tier, s))
        except VErr as e: f.append(f"concept {i+1}: {e.msg}"); norms.append(s)
    for cat in ("hair", "aesthetic"):
        vals = [tuple(n.get(cat, [])) for n in norms]
        if any(not v for v in vals): f.append(f"every concept needs {cat}")
        elif len(set(vals)) < len(vals): f.append(f"{cat} repeats across concepts: {vals}")
    if not locked_ethnicity:
        eth = {tuple(n.get("ethnicity_origin_base", [])) for n in norms}
        need = 3 if market == "global" else 2
        if len(eth) < min(need, len(norms)): f.append(f"ethnicity range too narrow ({len(eth)} distinct, need {min(need, len(norms))}); do not default every concept to one origin")
    if tier in ("freak", "total"):
        users = sum(1 for n in norms if any((c, i) in BOLD_ONLY for c, ids in n.items() for i in ids))
        if users < min(2, len(norms)): f.append(f"tier={tier} but only {users} concept(s) use Bold/Extreme-only options — the tier is wasted")
    anchors = []
    for n in norms:
        h = n.get("hair", [None])[0]
        anchors.append({"hair": h, "image": asset_rel("hair", h) if h else None})
    return {"pass": not f, "findings": f, "anchors": anchors}


def img_meta(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): return None
    kind = "reference_photo"
    if rel.split("/")[2] in ("skin_tone", "eye_color", "hair_colour"): kind = "color_swatch"
    elif rel.split("/")[2] == "age": kind = "text_card"
    return {"rel": rel, "abs": p, "bytes": os.path.getsize(p), "kind": kind}


def option_record(c, o):
    return {"key": f"{c['id']}/{o['id']}", "category": c["id"], "category_label": c["label_en"], "kind": c["kind"], "max": c["max"],
            "id": o["id"], "label": o["label_en"], "fragment": fragment(c["id"], o["id"]), "look": look(c["id"], o["id"]),
            "card_styling": VIS.get(c["id"], {}).get(o["id"], {}).get("card_styling"),
            "tiers": o["visibleIn"], "bold_only": "normal" not in o["visibleIn"], "slot": o.get("slot"), "swatch": o.get("swatch"),
            "image": img_meta(asset_rel(c["id"], o["id"]))}


def get_option(key):
    cat, _, oid = key.partition("/")
    c = CATS.get(cat)
    o = opt(cat, oid) if c else None
    if not o: raise VErr("key", f"unknown option key {key!r} (format <category>/<option_id>)")
    return option_record(c, o)


def query(category=None, tier=None, text=None, bold_only=False, slot=None):
    out = []
    for c in TAX["categories"]:
        if category and c["id"] != category: continue
        for o in c["options"]:
            if tier and tier not in o["visibleIn"]: continue
            if bold_only and "normal" in o["visibleIn"]: continue
            if slot and o.get("slot") != slot: continue
            r = option_record(c, o)
            if text:
                hay = " ".join(str(r.get(k) or "") for k in ("category", "id", "label", "fragment", "look", "card_styling")).lower()
                if not all(w in hay for w in text.lower().split()): continue
            out.append(r)
    return out


def find(query_text, tier=None):
    return [{"key": r["key"], "label": r["label"], "look": r["look"], "tiers": r["tiers"], "image": r["image"]["abs"] if r["image"] else None}
            for r in query(tier=tier, text=query_text)]


def refs(sel):
    """Absolute per-option reference image paths for a selection (feed to display_file / reference slots)."""
    return [{"key": f"{c}/{i}", "image": os.path.join(ROOT, asset_rel(c, i)), "look": look(c, i)} for c in PROMPT_ORDER for i in sel.get(c, [])]


def parse_sel(s):
    if not s: return {}
    if s.startswith("@"):
        with open(s[1:], encoding="utf-8") as fh: return json.load(fh)
    return json.loads(s)


def cmd_reindex():
    idx = {"tiers": [{"id": o["id"], "label": o["label_en"], "image": asset_rel("tier", o["id"]),
                      "lead": TAX["prompt_map"]["tiers"][o["id"]]} for o in TAX["tier_group"]["options"]],
           "categories": []}
    md = ["# Taxonomy 选项总表（自动生成，勿手改；改 data/taxonomy.json 后运行 `python3 scripts/ugc_taxonomy.py reindex`）", "",
          "图片路径相对 skill 根目录，每个选项一张独立图：`assets/options/<category>/<option_id>.webp`（色彩类为色卡）。`look` = 看图提炼的视觉描述（data/visual-descriptors.json）。`N/B/E` = 选项在 Average(normal)/Bold(freak)/Extreme(total) 三档是否可见。", ""]
    for c in TAX["categories"]:
        md += [f"## {c['id']} — {c['label_en']}（kind={c['kind']}, max={c['max']}）", "",
               "| id | label | fragment | look（视觉描述） | N/B/E | slot | swatch | image |", "|---|---|---|---|---|---|---|---|"]
        cat = {"id": c["id"], "label": c["label_en"], "kind": c["kind"], "max": c["max"], "options": []}
        for o in c["options"]:
            vis = "".join(l if t in o["visibleIn"] else "-" for t, l in zip(TIERS, "NBE"))
            im = asset_rel(c["id"], o["id"]) if os.path.exists(os.path.join(ROOT, asset_rel(c["id"], o["id"]))) else None
            lk = look(c["id"], o["id"]) or ""
            cat["options"].append({"id": o["id"], "label": o["label_en"], "fragment": fragment(c["id"], o["id"]), "look": lk or None,
                                   "visibleIn": o["visibleIn"], "slot": o.get("slot"), "swatch": o.get("swatch"), "image": im})
            md.append(f"| `{o['id']}` | {o['label_en']} | {fragment(c['id'], o['id'])} | {lk} | {vis} | {o.get('slot') or ''} | {o.get('swatch') or ''} | {im or ''} |")
        md.append(""); idx["categories"].append(cat)
    with open(os.path.join(ROOT, "data", "option-index.json"), "w", encoding="utf-8") as fh:
        json.dump(idx, fh, ensure_ascii=False, indent=1)
    assets = {"_doc": "One record per element. Retrieve by key '<category>/<option_id>' (ugc_taxonomy.py get/query/find). Every image is a standalone file containing exactly one element; no composites.",
              "version": TAX.get("version"), "count": 0, "tiers": {}, "options": {}}
    for o in TAX["tier_group"]["options"]:
        assets["tiers"][o["id"]] = {"label": o["label_en"], "lead": TAX["prompt_map"]["tiers"][o["id"]], "image": img_meta(asset_rel("tier", o["id"]))}
    for c in TAX["categories"]:
        for o in c["options"]:
            r = option_record(c, o); r["image"] = r["image"] and {k: v for k, v in r["image"].items() if k != "abs"}
            assets["options"][r["key"]] = r
    assets["count"] = len(assets["options"])
    with open(os.path.join(ROOT, "assets", "index.json"), "w", encoding="utf-8") as fh:
        json.dump(assets, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "references", "taxonomy", "options-table.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print("reindexed", sum(len(c["options"]) for c in idx["categories"]), "options")


def selftest():
    fails = []
    def check(name, cond):
        if not cond: fails.append(name)
    vis = {t: 0 for t in TIERS}; total = 0
    for c in TAX["categories"]:
        for o in c["options"]:
            total += 1
            for v in o["visibleIn"]: vis[v] += 1
    check("counts.categories=18", len(TAX["categories"]) == 18)
    check("counts.options=170", total == 170)
    check("visible 124/167/170", vis == {"normal": 124, "freak": 167, "total": 170})
    # every image localized
    missing = []
    for c in TAX["categories"]:
        for o in c["options"]:
            if not os.path.exists(os.path.join(ROOT, asset_rel(c["id"], o["id"]))): missing.append(f"{c['id']}/{o['id']}")
            if c["kind"] != "color" and c["id"] != "age" and not look(c["id"], o["id"]) and c["id"] not in ("gender", "height", "freak_neck"):
                missing.append(f"look:{c['id']}/{o['id']}")
    check(f"images localized (missing={missing[:5]})", not missing)
    for bad in [("normal", {"nope": ["x"]}), ("normal", {"gender": ["nope"]}), ("notatier", {"gender": ["female"]})]:
        try: normalize(*bad); fails.append(f"reject {bad}")
        except VErr: pass
    n = normalize("normal", {"proportions": ["pr_egg", "pr_shoulders"], "freak_head": ["head_tiny"]})
    check("drop invisible", "pr_egg" not in n.get("proportions", []) and not n.get("freak_head") and "pr_shoulders" in n["proportions"])
    check("acc_none exclusive", normalize("total", {"accessory": ["acc_glasses", "acc_none"]})["accessory"] == ["acc_none"])
    g = normalize("total", {"freak_face": ["fn_fulllips", "ff_lips_3", "fn_freckles"]})["freak_face"]
    check("slot last wins", "fn_fulllips" not in g and "ff_lips_3" in g and "fn_freckles" in g)
    g = normalize("total", {"freak_face": ["fn_eyebags", "fn_mole", "fn_cheekbones", "fn_fulllips", "fn_widemouth"]})["freak_face"]
    check("max cap", len(g) == 4 and g[0] == "fn_eyebags" and g[3] == "fn_widemouth")
    cases = [
        ("normal", {"body_type": ["body_heavy"], "height": ["h_tall"]}, "Heavy build"),
        ("normal", {"body_type": ["body_heavy"], "height": ["h_very_tall"]}, "Heavy build"),
        ("freak", {"body_type": ["body_heavy"], "proportions": ["pr_shortlegs"]}, "Short legs"),
        ("total", {"body_type": ["body_muscular"], "proportions": ["pr_longlimbs"]}, "Long limbs"),
        ("normal", {"body_type": ["body_heavy"], "proportions": ["pr_shortlegs"]}, ""),
        ("total", {"body_type": ["body_ultra"], "freak_neck": ["neck_long"]}, "Long neck"),
        ("total", {"freak_neck": ["neck_long"], "freak_face": ["ff_teeth_11"]}, "Buck teeth"),
        ("total", {"gender": ["male"], "body_type": ["body_muscular"], "height": ["h_tall"]}, ""),
    ]
    for t, s, want in cases:
        try:
            validate(t, s); check(f"conflict {s}", want == "")
        except VErr as e:
            check(f"conflict {s}", want != "" and want in e.msg)
    p = build_base("total", {"gender": ["male"], "hair": ["hair_afro"], "skin_tone": ["st_deep"]})
    check("prompt lead", p.startswith("Extreme caricature, exaggerated proportions, full-body character portrait of a"))
    check("prompt frags", all(f in p for f in ["Male", "afro", "deep brown skin"]))
    check("prompt suffix", p.endswith("Studio background, full-body shot, 9:16 composition, high detail, clean lighting."))
    check("brief", ". freckles, smiling." in build_base("normal", {"gender": ["female"]}, "  freckles, smiling  "))
    for t in TIERS:
        for sd in range(25):
            try: validate(t, randomize(t, sd))
            except VErr as e: fails.append(f"random {t}/{sd}: {e.msg}")
    check("get by key", get_option("hair/hs_horns")["image"]["kind"] == "reference_photo")
    check("query bold-only hair = 16", len(query(category="hair", bold_only=True)) == 16)
    check("query swatch kind", query(category="skin_tone")[0]["image"]["kind"] == "color_swatch")
    d1 = diversity("freak", [{"gender": ["female"], "ethnicity_origin_base": ["east_asian"], "hair": ["hair_bowl"], "aesthetic": ["retro"]}] * 3)
    check("diversity rejects clones", not d1["pass"])
    d2 = diversity("freak", [
        {"gender": ["male"], "ethnicity_origin_base": ["european"], "hair": ["hs_pompadour"], "aesthetic": ["suits"]},
        {"gender": ["female"], "ethnicity_origin_base": ["african"], "hair": ["hs_softserve"], "aesthetic": ["y2k"]},
        {"gender": ["non_binary"], "ethnicity_origin_base": ["indian"], "hair": ["hair_punk"], "aesthetic": ["goth"]}])
    check(f"diversity accepts varied set {d2['findings']}", d2["pass"])
    sig, neg = build_signature("freak", {"hair": ["hair_bowl"], "hair_colour": ["hc_black"], "gender": ["male"]})
    check("signature has deadpan+hair anchor", "deadpan" in sig and "bowl cut" in neg)
    print(json.dumps({"ok": not fails, "failures": fails, "checks_tier_visibility": vis}, ensure_ascii=False))
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("list"); sp.add_parser("reindex"); sp.add_parser("selftest")
    s = sp.add_parser("show"); s.add_argument("category"); s.add_argument("--tier", default="total")
    for name in ("validate", "build"):
        s = sp.add_parser(name); s.add_argument("--tier", default="normal"); s.add_argument("--sel", required=True)
        if name == "build":
            s.add_argument("--brief", default=""); s.add_argument("--mode", default="both", choices=["base", "signature", "both"])
    s = sp.add_parser("random"); s.add_argument("--tier", default="normal"); s.add_argument("--seed", type=int); s.add_argument("--lock", default="")
    s = sp.add_parser("find"); s.add_argument("query"); s.add_argument("--tier")
    s = sp.add_parser("get"); s.add_argument("keys", nargs="+", help="<category>/<option_id> ...")
    s = sp.add_parser("query"); s.add_argument("--category"); s.add_argument("--tier"); s.add_argument("--text"); s.add_argument("--bold-only", action="store_true"); s.add_argument("--slot")
    s.add_argument("--fields", default="key,label,look,tiers,image", help="comma list or 'all'")
    s = sp.add_parser("refs"); s.add_argument("--sel", required=True)
    s = sp.add_parser("diversity"); s.add_argument("--tier", default="freak"); s.add_argument("--sels", required=True, help="JSON list of selections or @file")
    s.add_argument("--market", default="global", choices=["global", "western", "regional", "cn"]); s.add_argument("--locked-ethnicity", action="store_true")
    a = ap.parse_args()
    try:
        if a.cmd == "list":
            for c in TAX["categories"]:
                v = {t: sum(t in o["visibleIn"] for o in c["options"]) for t in TIERS}
                print(f"{c['id']:24} {c['label_en']:22} kind={c['kind']:5} max={c['max']} options={len(c['options'])} N/B/E={v['normal']}/{v['freak']}/{v['total']}")
            print("priority:", ", ".join(TAX["category_priority"]))
        elif a.cmd == "show":
            t = tier_of(a.tier)
            for o in CATS[a.category]["options"]:
                if t in o["visibleIn"]:
                    print(f"{o['id']:16} {o['label_en']:22} -> {fragment(a.category, o['id'])}" + (f"  slot={o['slot']}" if o.get("slot") else "") + (f"  {o['swatch']}" if o.get("swatch") else ""))
        elif a.cmd == "validate":
            t = tier_of(a.tier); n = validate(t, parse_sel(a.sel))
            print(json.dumps({"ok": True, "tier": t, "selection": n, "labels": labels(n)}, ensure_ascii=False, indent=1))
        elif a.cmd == "build":
            t = tier_of(a.tier); n = validate(t, parse_sel(a.sel)); out = {"tier": t, "selection": n}
            if a.mode in ("base", "both"): out["base_prompt"] = build_base(t, n, a.brief)
            if a.mode in ("signature", "both"):
                sig, neg = build_signature(t, n, a.brief); out["signature_prompt"] = sig; out["negative_prompt"] = neg
            print(json.dumps(out, ensure_ascii=False, indent=1))
        elif a.cmd == "random":
            t = tier_of(a.tier); n = randomize(t, a.seed, parse_sel(a.lock))
            print(json.dumps({"tier": t, "selection": n, "labels": labels(n)}, ensure_ascii=False, indent=1))
        elif a.cmd == "get":
            print(json.dumps([get_option(k) for k in a.keys], ensure_ascii=False, indent=1))
        elif a.cmd == "query":
            rows = query(a.category, tier_of(a.tier) if a.tier else None, a.text, a.bold_only, a.slot)
            if a.fields != "all":
                fs = a.fields.split(",")
                rows = [{k: (r[k]["abs"] if k == "image" and r[k] else r[k]) for k in fs} for r in rows]
            print(json.dumps({"count": len(rows), "results": rows}, ensure_ascii=False, indent=1))
        elif a.cmd == "find":
            print(json.dumps(find(a.query, tier_of(a.tier) if a.tier else None), ensure_ascii=False, indent=1))
        elif a.cmd == "refs":
            print(json.dumps(refs(parse_sel(a.sel)), ensure_ascii=False, indent=1))
        elif a.cmd == "diversity":
            r = diversity(tier_of(a.tier), parse_sel(a.sels), a.market, a.locked_ethnicity)
            print(json.dumps(r, ensure_ascii=False, indent=1)); sys.exit(0 if r["pass"] else 3)
        elif a.cmd == "reindex":
            cmd_reindex()
        elif a.cmd == "selftest":
            sys.exit(selftest())
    except VErr as e:
        print(json.dumps({"ok": False, "field": e.field, "error": e.msg}), file=sys.stderr); sys.exit(2)


if __name__ == "__main__":
    main()
