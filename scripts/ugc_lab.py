#!/usr/bin/env python3
"""UGC character lab — project scaffolding, verifiable acceptance (QA gates) and self-evolution ledger.

Character projects live in the WORKSPACE (cwd), never inside the skill:
  ugc-characters/<slug>/character.json   # the character card (single source of truth)
  ugc-characters/<slug>/runs/             # one json per generation attempt (prompt, model, output, score)
  ugc-characters/<slug>/refs/             # LOCKED reference images (copied paths recorded in card)

Commands:
  ugc_lab.py init <slug> [--name NAME]                     # scaffold project + empty card
  ugc_lab.py card-check <slug>                             # G1 concept gate (structure, originality, conflicts)
  ugc_lab.py log <slug> --stage S --model M --prompt-file F [--negative-file F] [--output PATH ...] [--parent RUN]
  ugc_lab.py score <slug> <run_id> --scores JSON [--tags t1,t2] [--note TEXT]   # G2/G3/G4 gates from rubric
  ugc_lab.py lock <slug> <run_id> [--role front|sheet|...]  # lock a passed output as reference
  ugc_lab.py accept <slug>                                 # final acceptance report (all gates) -> acceptance.md
  ugc_lab.py evolve [--min 2]                              # mine ledger across projects -> proposals
  ugc_lab.py promote --rule TEXT --evidence RUN_IDS --scope SCOPE   # append a learned rule to evolution/learnings.md
Stages: concept | fullbody | edit | sheet | scene
Exit 0 = pass/ok, 3 = gate failed (report printed), 2 = usage/data error.
"""
import argparse, datetime as dt, glob, json, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import ugc_taxonomy as tx  # noqa: E402

RUBRIC = json.load(open(os.path.join(SKILL, "data", "qa-rubric.json"), encoding="utf-8"))
EVO = os.path.join(SKILL, "evolution")
LEDGER = os.environ.get("UGC_LEDGER") or os.path.join(EVO, "ledger.jsonl")
LEARN = os.path.join(EVO, "learnings.md")


def now(): return dt.datetime.now().astimezone().isoformat(timespec="seconds")
def proj(slug):
    slug = os.path.basename(os.path.normpath(slug.replace("character.json", ""))) if "/" in slug else slug
    return os.path.join(os.getcwd(), "ugc-characters", slug)
def die(msg, code=2): print(msg, file=sys.stderr); sys.exit(code)


def load_card(slug):
    p = os.path.join(proj(slug), "character.json")
    if not os.path.exists(p): die(f"no card at {p}; run init first")
    return json.load(open(p, encoding="utf-8")), p


def save(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh: json.dump(obj, fh, ensure_ascii=False, indent=2)


CARD_TEMPLATE = {
    "slug": "", "name": "", "created_at": "",
    "bio": ["who they are", "what they do", "what they'd have an opinion about"],
    "one_line_vibe": "",
    "niche": "", "platforms": ["tiktok", "instagram", "youtube_shorts", "x"],
    "tier": "freak",
    "selection": {},
    "signature": {"hair": "", "standout_feature": "", "outfit": "", "prop": "", "expression": "deadpan"},
    "running_bit": "",
    "motion_personality": "",
    "palette": [],
    "originality": {"is_original": False, "not_based_on": "no real person / celebrity / copyrighted character"},
    "drift_guard": [],
    "character_paragraph": "",
    "locked_refs": [],
    "status": "concept"
}


def cmd_init(a):
    p = os.path.join(proj(a.slug), "character.json")
    if os.path.exists(p): die(f"exists: {p}")
    card = json.loads(json.dumps(CARD_TEMPLATE))
    card.update(slug=a.slug, name=a.name or a.slug, created_at=now())
    for d in ("runs", "refs"): os.makedirs(os.path.join(proj(a.slug), d), exist_ok=True)
    save(p, card); print(p)


def card_findings(card):
    f = []
    bio = card.get("bio") or []
    if len([s for s in bio if s and s not in CARD_TEMPLATE["bio"]]) < 3: f.append("G1.bio: need >=3 concrete sentences (who / does / opinion)")
    vibe = (card.get("one_line_vibe") or "").strip()
    cjk = sum(1 for ch in vibe if "\u4e00" <= ch <= "\u9fff")
    if len(vibe.split()) < 6 and cjk < 12: f.append("G1.vibe: one-line vibe too thin (>=6 English words or >=12 Chinese chars)")
    sig = card.get("signature") or {}
    for k in ("hair", "standout_feature", "outfit", "prop"):
        if not (sig.get(k) or "").strip(): f.append(f"G1.signature.{k}: missing")
    if (sig.get("expression") or "").lower() not in ("deadpan", "blank", "serious"):
        f.append("G1.signature.expression: house style is deadpan (override only if user asked; set 'expression_override')") if not card.get("expression_override") else None
    if not (card.get("running_bit") or "").strip(): f.append("G1.running_bit: missing (needed for video series)")
    if not card.get("originality", {}).get("is_original"): f.append("G1.originality: must confirm original (no real person/celebrity/IP)")
    if not card.get("niche"): f.append("G1.niche: missing")
    try:
        tier = tx.tier_of(card.get("tier"))
        norm = tx.validate(tier, card.get("selection") or {})
        if not norm.get("hair"): f.append("G1.taxonomy: hair must be selected (signature anchor)")
        if not norm.get("gender"): f.append("G1.taxonomy: gender required")
        dropped = {k: v for k, v in (card.get("selection") or {}).items() if norm.get(k) != v}
        if dropped: f.append(f"G1.taxonomy: options dropped/normalized by rules {dropped} -> fix selection")
    except tx.VErr as e:
        f.append(f"G1.taxonomy: {e.msg}")
    banned = re.compile(r"\b(celebrity|look[- ]?alike|kardashian|taylor swift|elon|mr ?beast|disney|marvel|pokemon|anime character)\b", re.I)
    authored = {k: v for k, v in card.items() if k not in ("originality", "locked_refs", "platforms")}
    blob = json.dumps(authored, ensure_ascii=False)
    if banned.search(blob): f.append("G1.originality: card references a real person/IP keyword -> block or rewrite")
    if not card.get("drift_guard"): f.append("G1.drift_guard: list 2-5 must-keep visual anchors")
    return f


def cmd_card_check(a):
    card, _ = load_card(a.slug)
    f = card_findings(card)
    print(json.dumps({"gate": "G1-concept", "pass": not f, "findings": f}, ensure_ascii=False, indent=1))
    sys.exit(0 if not f else 3)


def run_path(slug, rid): return os.path.join(proj(slug), "runs", f"{rid}.json")


def cmd_log(a):
    card, _ = load_card(a.slug)
    rid = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{a.stage}"
    n = 2
    while os.path.exists(run_path(a.slug, rid)):
        rid = dt.datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{a.stage}-{n}"; n += 1
    prompt = open(a.prompt_file, encoding="utf-8").read() if a.prompt_file else (a.prompt or "")
    neg = open(a.negative_file, encoding="utf-8").read() if a.negative_file else ""
    outs = []
    for o in a.output or []:
        outs.append({"path": o, "exists": os.path.exists(o)})
    run = {"run_id": rid, "slug": a.slug, "stage": a.stage, "model": a.model, "tool": a.tool, "tier": card.get("tier"),
           "selection": card.get("selection"), "prompt": prompt, "negative": neg, "outputs": outs,
           "parent": a.parent, "created_at": now(), "scores": None, "pass": None, "tags": []}
    save(run_path(a.slug, rid), run)
    print(rid)


def gate_for(stage):
    return RUBRIC["stages"].get(stage) or RUBRIC["stages"]["fullbody"]


def cmd_score(a):
    p = run_path(a.slug, a.run_id)
    if not os.path.exists(p): die(f"no run {p}")
    run = json.load(open(p, encoding="utf-8"))
    scores = json.loads(a.scores)
    g = gate_for(run["stage"])
    crit = g["criteria"]
    missing = [c for c in crit if c not in scores]
    if missing: die(f"missing criteria scores: {missing}; required: {list(crit)}")
    total_w = sum(c["weight"] for c in crit.values())
    weighted = sum(scores[k] * crit[k]["weight"] for k in crit) / total_w
    hard_fail = [k for k, c in crit.items() if c.get("hard_min") and scores[k] < c["hard_min"]]
    ok = weighted >= g["pass_score"] and not hard_fail and all(o["exists"] for o in run["outputs"]) and run["outputs"]
    tags = [t.strip() for t in (a.tags or "").split(",") if t.strip()]
    unknown = [t for t in tags if t not in RUBRIC["failure_tags"]]
    run.update(scores=scores, weighted=round(weighted, 2), hard_fail=hard_fail, pass_=bool(ok), tags=tags, note=a.note, scored_at=now())
    run["pass"] = bool(ok); run.pop("pass_", None)
    save(p, run)
    os.makedirs(EVO, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({k: run.get(k) for k in ("run_id", "slug", "stage", "model", "tool", "tier", "selection", "weighted", "pass", "hard_fail", "tags", "note", "scored_at")}, ensure_ascii=False) + "\n")
    rep = {"gate": g["gate"], "run_id": a.run_id, "weighted": round(weighted, 2), "pass_score": g["pass_score"], "hard_fail": hard_fail, "pass": bool(ok)}
    if unknown: rep["warning"] = f"unknown tags (add to rubric failure_tags if recurring): {unknown}"
    if not run["outputs"]: rep["warning_outputs"] = "no output file logged — a gate cannot pass without a real file"
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    sys.exit(0 if ok else 3)


def cmd_lock(a):
    card, cp = load_card(a.slug)
    run = json.load(open(run_path(a.slug, a.run_id), encoding="utf-8"))
    if not run.get("pass"): die("refuse to lock: run has not passed its gate", 3)
    for o in run["outputs"]:
        if not os.path.exists(o["path"]): die(f"missing output {o['path']}")
        card.setdefault("locked_refs", []).append({"path": o["path"], "role": a.role or run["stage"], "run_id": a.run_id, "locked_at": now()})
    card["status"] = {"fullbody": "face_locked", "edit": "face_locked", "sheet": "sheet_locked", "scene": "in_production"}.get(run["stage"], card.get("status"))
    save(cp, card); print(json.dumps({"locked": card["locked_refs"][-len(run['outputs']):], "status": card["status"]}, ensure_ascii=False, indent=1))


def cmd_accept(a):
    card, _ = load_card(a.slug)
    runs = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(proj(a.slug), "runs", "*.json")))]
    best = {}
    for r in runs:
        if r.get("pass"): best.setdefault(r["stage"], r)
    g1 = card_findings(card)
    checks = [
        ("G1 概念卡", not g1, "; ".join(g1) or "ok"),
        ("G2 全身定妆图通过", "fullbody" in best or "edit" in best, (best.get("fullbody") or best.get("edit") or {}).get("run_id", "none")),
        ("G3 角色设定表通过", "sheet" in best, best.get("sheet", {}).get("run_id", "none")),
        ("G3b 已锁定参考图≥2（正面+设定表）", len(card.get("locked_refs", [])) >= 2, str(len(card.get("locked_refs", [])))),
        ("G4 场景一致性≥1", "scene" in best, best.get("scene", {}).get("run_id", "none (optional for image-only delivery)")),
        ("G5 全部输出文件存在", all(os.path.exists(x["path"]) for x in card.get("locked_refs", [])), "checked"),
        ("G6 已写入进化账本", any(json.loads(l)["slug"] == a.slug for l in open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else False, LEDGER),
    ]
    required_ok = all(ok for name, ok, _ in checks if not name.startswith("G4"))
    lines = [f"# 验收报告 · {card.get('name')} ({a.slug})", "", f"- 时间：{now()}", f"- 档位：{card.get('tier')}", f"- 结论：{'✅ 通过' if required_ok else '❌ 未通过'}", "",
             "| 门禁 | 结果 | 证据 |", "|---|---|---|"]
    lines += [f"| {n} | {'✅' if ok else '❌'} | {ev} |" for n, ok, ev in checks]
    lines += ["", "## 生成尝试", "", "| run | stage | model | weighted | pass | tags |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['run_id']} | {r['stage']} | {r.get('model')} | {r.get('weighted')} | {r.get('pass')} | {','.join(r.get('tags') or [])} |" for r in runs]
    first_pass = {s: next((i + 1 for i, r in enumerate([x for x in runs if x['stage'] == s]) if r.get("pass")), None) for s in ("fullbody", "sheet", "scene")}
    lines += ["", f"首过所需尝试次数：{first_pass}（进化 KPI：越低越好）"]
    out = os.path.join(proj(a.slug), "acceptance.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print("\n".join(lines)); print("\n->", out)
    sys.exit(0 if required_ok else 3)


def cmd_evolve(a):
    if not os.path.exists(LEDGER): die("ledger empty — score some runs first")
    rows = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    by_model = defaultdict(lambda: [0, 0]); tag_ctx = defaultdict(Counter); opt_fail = Counter(); opt_all = Counter()
    for r in rows:
        k = f"{r['stage']}|{r.get('model')}"; by_model[k][0] += 1; by_model[k][1] += 1 if r.get("pass") else 0
        for t in r.get("tags") or []:
            tag_ctx[t][f"{r.get('model')}|tier={r.get('tier')}"] += 1
        for c, ids in (r.get("selection") or {}).items():
            for i in ids:
                opt_all[f"{c}:{i}"] += 1
                if not r.get("pass"): opt_fail[f"{c}:{i}"] += 1
    props = []
    for t, ctx in tag_ctx.items():
        for c, n in ctx.items():
            if n >= a.min:
                props.append({"type": "failure_pattern", "tag": t, "context": c, "count": n,
                              "suggest": RUBRIC["failure_tags"].get(t, {}).get("fix", "write a targeted prompt fix")})
    for k, n in opt_fail.items():
        if n >= a.min and n / max(opt_all[k], 1) >= 0.6:
            props.append({"type": "risky_option", "option": k, "fail_rate": round(n / opt_all[k], 2), "n": opt_all[k],
                          "suggest": "add an explicit, concrete descriptor for this option in prompt-recipes, or warn user"})
    stats = {k: {"runs": v[0], "pass_rate": round(v[1] / v[0], 2)} for k, v in by_model.items()}
    learned = open(LEARN, encoding="utf-8").read() if os.path.exists(LEARN) else ""
    props = [p for p in props if (p.get("tag") or p.get("option")) not in learned]
    print(json.dumps({"rows": len(rows), "model_stats": stats, "proposals": props}, ensure_ascii=False, indent=1))


def cmd_promote(a):
    os.makedirs(EVO, exist_ok=True)
    ids = [x.strip() for x in a.evidence.split(",") if x.strip()]
    if len(ids) < 2 and not a.force: die("a learned rule needs >=2 evidence run ids (use --force for user-mandated rules)")
    with open(LEARN, "a", encoding="utf-8") as fh:
        fh.write(f"\n- [{dt.date.today()}] ({a.scope}) {a.rule}  \n  evidence: {', '.join(ids)}\n")
    print("promoted ->", LEARN)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("init"); s.add_argument("slug"); s.add_argument("--name")
    s = sp.add_parser("card-check"); s.add_argument("slug", help="slug only, not a path")
    s = sp.add_parser("log"); s.add_argument("slug"); s.add_argument("--stage", required=True, choices=list(RUBRIC["stages"]) + ["concept"])
    s.add_argument("--model", required=True); s.add_argument("--tool", default=""); s.add_argument("--prompt-file"); s.add_argument("--prompt")
    s.add_argument("--negative-file"); s.add_argument("--output", nargs="*"); s.add_argument("--parent")
    s = sp.add_parser("score"); s.add_argument("slug"); s.add_argument("run_id"); s.add_argument("--scores", required=True); s.add_argument("--tags"); s.add_argument("--note")
    s = sp.add_parser("lock"); s.add_argument("slug"); s.add_argument("run_id"); s.add_argument("--role")
    s = sp.add_parser("accept"); s.add_argument("slug")
    s = sp.add_parser("evolve"); s.add_argument("slug", nargs="?", help="ignored; evolve always aggregates all projects"); s.add_argument("--min", type=int, default=2)
    s = sp.add_parser("promote"); s.add_argument("--rule", required=True); s.add_argument("--evidence", required=True); s.add_argument("--scope", default="global"); s.add_argument("--force", action="store_true")
    a = ap.parse_args()
    {"init": cmd_init, "card-check": cmd_card_check, "log": cmd_log, "score": cmd_score, "lock": cmd_lock,
     "accept": cmd_accept, "evolve": cmd_evolve, "promote": cmd_promote}[a.cmd](a)


if __name__ == "__main__":
    main()
