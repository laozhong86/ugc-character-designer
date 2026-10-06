#!/usr/bin/env python3
"""Skill-wide regression: data integrity, taxonomy engine, lab gates (in a temp dir, isolated ledger), docs links.
Run after ANY change to scripts / rubric / templates. Exit 0 = all green."""
import json, os, re, subprocess, sys, tempfile

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
fails = []


def run(args, cwd=None, env=None, expect=0):
    p = subprocess.run([PY] + args, cwd=cwd, env=env, capture_output=True, text=True)
    if p.returncode != expect:
        fails.append(f"{' '.join(args[:3])} exit={p.returncode} want={expect}: {p.stderr.strip()[:200] or p.stdout.strip()[:200]}")
    return p


tx = os.path.join(SKILL, "scripts", "ugc_taxonomy.py")
lab = os.path.join(SKILL, "scripts", "ugc_lab.py")

# 1. taxonomy engine
r = run([tx, "selftest"])
if '"ok": true' not in r.stdout: fails.append("taxonomy selftest not ok")
run([tx, "validate", "--tier", "normal", "--sel", '{"body_type":["body_heavy"],"height":["h_tall"]}'], expect=2)
b = run([tx, "build", "--tier", "extreme", "--sel", '{"gender":["female"],"hair":["hs_softserve"],"hair_colour":["hc_pink"]}'])
try:
    d = json.loads(b.stdout)
    assert d["base_prompt"].startswith("Extreme caricature") and "soft-serve" in d["signature_prompt"]
except Exception as e:
    fails.append(f"build output: {e}")

f = run([tx, "find", "soft-serve"])
if "hair/hs_softserve.webp" not in f.stdout: fails.append("find did not return per-option asset path")
run([tx, "diversity", "--tier", "freak", "--sels", json.dumps([{"gender": ["female"], "ethnicity_origin_base": ["east_asian"], "hair": ["hair_bowl"], "aesthetic": ["retro"]}] * 3)], expect=3)
for c in json.load(open(os.path.join(SKILL, "data", "option-index.json")))["categories"]:
    for o in c["options"]:
        if not o.get("image") or not os.path.exists(os.path.join(SKILL, o["image"])): fails.append(f"index image missing {c['id']}/{o['id']}")

# 1b. face engine (random + layered custom)
face = os.path.join(SKILL, "scripts", "ugc_face.py")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import ugc_face as uf
for sd in range(300):
    seed, t, sel = uf.sample(sd)
    if uf.check_selection(sel, t): fails.append(f"random seed {sd} violates rules"); break
    if sel["gender"][0] not in ("male", "trans_man") and sel.get("facial_hair", ["fh_none"]) != ["fh_none"]: fails.append(f"seed {sd}: beard on {sel['gender']}"); break
if uf.sample(123) != uf.sample(123): fails.append("random not reproducible by seed")
_, _, locked = uf.sample(5, tier="freak", lock={"gender": ["female"], "aesthetic": ["goth"]})
if locked["gender"] != ["female"] or locked["aesthetic"] != ["goth"]: fails.append("lock ignored")
with tempfile.TemporaryDirectory() as tmp:
    stp = os.path.join(tmp, "s.json")
    run([face, "init", "--state", stp])
    run([face, "apply", "--state", stp, "--layer", "L1", "--answers", '{"tier":"freak","gender":"female","ethnicity_origin_base":"random","age":"default"}'])
    m = json.loads(run([face, "menu", "--state", stp, "--layer", "L5"]).stdout)
    fhq = [q for q in m["questions"] if q["id"] == "facial_hair"][0]
    if "skipped" not in fhq: fails.append("female: facial_hair not locked in L5 menu")
    run([face, "apply", "--state", stp, "--layer", "L5", "--answers", '{"facial_hair":"fh_beard"}'], expect=3)
    run([face, "apply", "--state", stp, "--layer", "L2", "--answers", '{"height":"h_tall","body_type":"body_heavy"}'], expect=3)
    r = json.loads(run([face, "apply", "--state", stp, "--layer", "L3", "--answers", '{"aesthetic":"goth","hair":{"custom":"恶魔角"},"hair_colour":"default"}']).stdout)
    if json.load(open(stp))["selection"].get("hair") != ["hs_horns"]: fails.append("custom text not mapped to option")
    run([face, "apply", "--state", stp, "--layer", "L5", "--answers", '{"accessory":["acc_hat"]}'], expect=3)
    run([face, "apply", "--state", stp, "--layer", "L1", "--answers", '{"gender":"male"}'])
    run([face, "apply", "--state", stp, "--layer", "L5", "--answers", '{"facial_hair":"fh_pushbroom"}'])
    c = json.loads(run([face, "apply", "--state", stp, "--layer", "L1", "--answers", '{"gender":"female"}']).stdout)
    if not any("胡须" in x for x in c["cascade_removed"]): fails.append("gender change did not cascade-remove beard")
    for L in ("L2", "L4", "L6"):
        run([face, "apply", "--state", stp, "--layer", L, "--answers", json.dumps({c: "default" for c in dict((l, cs) for l, _, cs in uf.LAYERS)[L]} if L != "L6" else {"persona": "auto"})], cwd=tmp)
    pr = json.loads(run([face, "prompt", "--state", stp, "--slug", "t-custom"], cwd=tmp).stdout)
    if not pr.get("ok") or "devil horns" not in pr["prompt"]: fails.append("custom prompt missing anchor")
    rr = json.loads(run([face, "random", "--seed", "9", "--count", "2", "--slug", "t-rand"], cwd=tmp).stdout)
    if rr["count"] != 2 or not all(os.path.exists(c["files"]["prompt_file"]) for c in rr["candidates"]): fails.append("random --slug did not write projects")

# 2. lab gates in temp workspace
with tempfile.TemporaryDirectory() as tmp:
    env = dict(os.environ, UGC_LEDGER=os.path.join(tmp, "ledger.jsonl"))
    img = os.path.join(tmp, "fake.png"); open(img, "wb").write(b"\x89PNG\r\n")
    run([lab, "init", "t1"], cwd=tmp, env=env)
    run([lab, "card-check", "t1"], cwd=tmp, env=env, expect=3)
    cp = os.path.join(tmp, "ugc-characters", "t1", "character.json"); c = json.load(open(cp))
    c.update(bio=["Nora is a 34-year-old retired synchronized swimmer.", "She reviews office chairs with Olympic seriousness.", "She believes posture is a moral issue."],
             one_line_vibe="a retired synchronized swimmer who judges office chairs like an Olympic panel",
             niche="deadpan product reviews", tier="freak",
             selection={"gender": ["female"], "hair": ["hs_lampshade"], "hair_colour": ["hc_platinum"], "aesthetic": ["sporty"]},
             signature={"hair": "platinum lampshade bob", "standout_feature": "nose clip worn at all times", "outfit": "vintage team tracksuit", "prop": "judge scorecards", "expression": "deadpan"},
             running_bit="holds up a scorecard after every sit", drift_guard=["platinum lampshade bob", "nose clip"])
    c["originality"]["is_original"] = True; json.dump(c, open(cp, "w"))
    run([lab, "card-check", "t1"], cwd=tmp, env=env)
    # conflict must fail G1
    c["selection"].update(body_type=["body_heavy"], height=["h_tall"]); json.dump(c, open(cp, "w"))
    run([lab, "card-check", "t1"], cwd=tmp, env=env, expect=3)
    del c["selection"]["body_type"], c["selection"]["height"]; json.dump(c, open(cp, "w"))
    rid = run([lab, "log", "t1", "--stage", "fullbody", "--model", "m", "--prompt", "p", "--output", img], cwd=tmp, env=env).stdout.strip()
    good = '{"thumbnail_read":5,"selection_fidelity":5,"deadpan_sincerity":4,"photoreal_texture":4,"framing":5,"anatomy":4,"originality_safety":5}'
    run([lab, "score", "t1", rid, "--scores", good], cwd=tmp, env=env)
    run([lab, "lock", "t1", rid], cwd=tmp, env=env)
    rid2 = run([lab, "log", "t1", "--stage", "sheet", "--model", "m", "--prompt", "p", "--output", img], cwd=tmp, env=env).stdout.strip()
    run([lab, "score", "t1", rid2, "--scores", '{"layout":5,"cross_panel_identity":3,"ref_match":5,"photoreal_texture":5,"anatomy":5}', "--tags", "panel_inconsistency"], cwd=tmp, env=env, expect=3)
    run([lab, "lock", "t1", rid2], cwd=tmp, env=env, expect=3)  # refuse locking failed run
    run([lab, "accept", "t1"], cwd=tmp, env=env, expect=3)       # no sheet yet
    rid3 = run([lab, "log", "t1", "--stage", "sheet", "--model", "m", "--prompt", "p2", "--output", img, "--parent", rid2], cwd=tmp, env=env).stdout.strip()
    run([lab, "score", "t1", rid3, "--scores", '{"layout":5,"cross_panel_identity":5,"ref_match":4,"photoreal_texture":5,"anatomy":5}'], cwd=tmp, env=env)
    run([lab, "lock", "t1", rid3], cwd=tmp, env=env)
    run([lab, "accept", "t1"], cwd=tmp, env=env)
    run([lab, "log", "t1", "--stage", "fullbody", "--model", "m", "--prompt", "p"], cwd=tmp, env=env)  # no output
    ev = run([lab, "evolve", "--min", "1"], cwd=tmp, env=env)
    if "panel_inconsistency" not in ev.stdout: fails.append("evolve did not surface failure pattern")

# 3. docs: every relative path mentioned in SKILL.md exists
skill_md = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
for ref in set(re.findall(r"`((?:references|templates|data|scripts|evolution|assets)/[^`\s]+?)`", skill_md)):
    if "<" in ref or "*" in ref: continue
    if not os.path.exists(os.path.join(SKILL, ref)): fails.append(f"SKILL.md references missing path {ref}")
if not skill_md.startswith("---\nname: ugc-character-designer\n"): fails.append("SKILL.md frontmatter name")

print(json.dumps({"ok": not fails, "failures": fails}, ensure_ascii=False, indent=1))
sys.exit(0 if not fails else 1)
