🌐 [中文](README.md) · **English**

> _"Say one sentence. Get back an AI character that can keep shipping content."_

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Agent-Agnostic](https://img.shields.io/badge/Agent-Agnostic-blueviolet)](https://skills.sh/)
[![170 Options](https://img.shields.io/badge/Taxonomy-170%20options-orange)](assets/index.json)

**Say "make me an AI influencer" in your agent, get back a complete character asset pack ready for a short-video pipeline.**

Design original, thumbnail-instantly-recognizable, sustainably-producible AI influencers /
virtual creators / UGC characters: three-line persona → 170-option appearance taxonomy
(3 exaggeration tiers) → full-body character portrait → EDIT face-preserving revisions →
8-panel character sheet → scene first-frames → handoff package. Built-in rule-engine
validation, visual scoring gates (G1–G4), acceptance reports, and a self-evolution ledger.

Core creed: **write the person first, then the face** — one signature hairstyle +
one standout feature + sincere unfashionable outfit + deadpan throughout;
thumbnail recognizability > polish; once a reference is locked, everything defers to it;
original only — never borrow a real face.

[Gallery](#-gallery) · [Install](#install) · [Capabilities](#capabilities) · [Workflow](#s0s8-gated-workflow) · [Repo layout](#repo-layout)

---

## 🎨 Gallery

### Character showcase

<table>
<tr>
<td width="280">
<img src="gallery/characters/jiang-lingyi-fullbody.png" width="260">
</td>
<td valign="top">

**Jiang Lingyi** — female lead of an original costume political-drama short series

- Persona: a 26-year-old peace-marriage princess from a border kingdom;
  she trades her marriage for ceasefire, grain convoys and her people's survival;
  she believes her own dignity is negotiable — her people's lives are not.
- Signature: black center-parted low braided bun + pale-green jade earrings +
  teal robe over apricot dress; a cloth pouch of hometown seeds hidden in her left sleeve.
- Running bit: under pressure, she first smooths her sleeve, then calmly re-asks
  the question that was dodged.
- Full-body gate score **4.37 / 5** (passed first try).

</td>
</tr>
</table>

More in [gallery/README.md](gallery/README.md).

### Element gallery · 170-option taxonomy

18 categories × 170 options, one standalone image per element (composites forbidden) —
26 hairstyles (beehive, lampshade, corkscrews, staircase…), 25 facial features,
8 skin tones, 8 aesthetics. Three exaggeration tiers: Average / Bold / Extreme.

👉 **[Full gallery · gallery/taxonomy.md](gallery/taxonomy.md)** (auto-generated, searchable)

<table>
<tr>
<td><img src="assets/options/hair/hs_beehive.webp" width="110"><br><sub>beehive</sub></td>
<td><img src="assets/options/hair/hs_lampshade.webp" width="110"><br><sub>lampshade</sub></td>
<td><img src="assets/options/hair/hs_softserve.webp" width="110"><br><sub>soft-serve</sub></td>
<td><img src="assets/options/hair/hs_stairs.webp" width="110"><br><sub>staircase</sub></td>
<td><img src="assets/options/hair/hs_sphere.webp" width="110"><br><sub>sphere</sub></td>
<td><img src="assets/options/hair/hs_horns.webp" width="110"><br><sub>horns</sub></td>
</tr>
<tr>
<td><img src="assets/options/distinctive/df_hetero.webp" width="110"><br><sub>heterochromia</sub></td>
<td><img src="assets/options/distinctive/df_gems.webp" width="110"><br><sub>face gems</sub></td>
<td><img src="assets/options/freak_face/ff_nose_1.webp" width="110"><br><sub>nose +1</sub></td>
<td><img src="assets/options/freak_head/head_megachin.webp" width="110"><br><sub>mega chin</sub></td>
<td><img src="assets/options/aesthetic/theatrical.webp" width="110"><br><sub>theatrical</sub></td>
<td><img src="assets/options/aesthetic/y2k.webp" width="110"><br><sub>Y2K</sub></td>
</tr>
</table>

---

## Install

A standard agent skill (`SKILL.md` + `assets/`, `data/`, `references/`, `scripts/`,
`templates/`, `evolution/` — all required). Clone into any skills directory:

```bash
git clone https://github.com/laozhong86/ugc-character-designer.git \
  ~/.agents/skills/ugc-character-designer      # or your agent's skills dir
```

Then just talk to any skills-capable agent:

```
"Make me an AI influencer"
"Random-generate 3 faces, I'm running a TikTok pet-rant account"
"Build an 8-panel character sheet from this locked portrait"
"Swap her hairstyle to a beehive — keep the face identical"
```

Runtime: Python 3.10+ (scripts have zero third-party deps); image output needs any
text-to-image channel (OmniMux hub / gpt-image / etc. — see `references/generation-tools.md`).

## Capabilities

| Capability | Deliverable | Gate |
|---|---|---|
| Random face-gen | 3 candidates (persona + full-body + prompt) | user picks 1 |
| Layered custom face-gen | L1–L6 lock-down (gender→ethnicity→silhouette→features→hair→style); upper locks cascade-filter lower layers | per-layer confirm |
| Character card | `character.json` (bio×3 / vibe / signature / motion personality / drift guard / originality) | **G1** |
| Full-body portrait | 9:16 key art + visual scoring | **G2 ≥3.8** |
| EDIT revision | one-change rerun with verbatim face lock | identity ≥4 |
| 8-panel sheet | 16:9 sheet (5 full-body + 3 close-ups) | **G3 ≥4.0** |
| Scene first-frames | 1–3 × 9:16 UGC frames, same-person verification across scenes | **G4** |
| Handoff package | all anchors needed for video motion transfer + acceptance.md | all green |
| Self-evolution | failure-pattern rollup → rules promoted into `evolution/learnings.md` | ≥2 evidence runs |

## S0→S8 gated workflow

```
S0 face-gen ─→ S1 concept ─→ S2 character card ─→ S3 full-body ─→ S4 EDIT ─→ S5 lock
                                                                              │
S8 delivery ←─ G4 scenes ←─ G3 sheet ←────────────────────────────────────────┘
```

- **Scores come only from actually-viewed generated images** — item-by-item against
  `data/qa-rubric.json`; never score a prompt, never score a file that isn't on disk.
- Failures must carry `failure_tags` (the rubric embeds fix suggestions); the next
  attempt revises the prompt per those suggestions — identical reruns are banned.
- Max 3 distinct attempts per stage; still failing → tell the user the blocker, don't fake it.

## Key mechanisms

### Data-driven, never defaults to localization

A Chinese-language conversation does NOT mean a Chinese character. Ethnicity, style
and tier come from user answers or built-in random weights; unspecified concepts must
span multiple ethnicities (`ugc_taxonomy.py diversity --market global` hard gate).

### Single-element image protocol

Each of the 170 options ships one standalone webp reference
(`assets/options/<category>/<id>.webp`). Display and reference are always per-image —
**composites/contact sheets are forbidden**, they leak wrong elements into generations.

### Lock is law

Once the portrait passes, `ugc_lab.py lock` writes the final CHARACTER paragraph into
`character.json`; every later image (sheet/scene/EDIT) anchors identity to it, and
changes only ever go through the EDIT flow.

### Self-evolution ledger

Every generation: `ugc_lab.py log` → view → `score`; delivery: `accept`;
retro: `evolve` rolls up failure patterns, and with user consent ≥2 evidence runs get
`promote`d into `evolution/learnings.md` — the skill gets sharper the more you use it.

## Hard constraints

- **Original only**: no likeness of real people, celebrities, influencers or copyrighted
  characters; "make it look like X" → declined, original alternative offered.
- Humor comes from styling, posture and attitude; never mock ethnicity, body type,
  gender identity or background.
- No earnings promises; platform incentive terms are governed by official docs.

## Repo layout

```
ugc-character-designer/
├── SKILL.md                # main doc (for agents): S0–S8 gated workflow
├── README.md / README.en.md
├── assets/
│   ├── index.json          # 170-element index (label/fragment/look/tier/image path)
│   └── options/<cat>/<id>.webp   # 170 single-element images + 6 tier cards
├── data/                   # taxonomy.json / visual descriptors / zh labels / QA rubric / rules
├── references/             # method distillation / intake question bank / gen-tool pitfalls / sources
├── scripts/                # ugc_face.py / ugc_taxonomy.py / ugc_lab.py / build_gallery.py
├── templates/              # character card template / prompt library T1–T7
├── evolution/              # learnings.md (proven rules) + ledger.jsonl
└── gallery/                # showcase: character cases + taxonomy.md full element index
```

## Limitations

- **Image quality depends on the text-to-image channel**: multi-reference identity edits
  are still draft on most gateways; identity is preserved via "verbatim CHARACTER
  paragraph + text-to-image", which can drift under extreme settings.
- **No real-person likeness**: any "make it look like <celebrity>" is declined and
  rerouted to an original alternative.
- Cross-panel consistency for Extreme-tier characters in the 8-panel sheet remains
  the hardest case and may need 2–3 iterations.

A skill that turns "an AI character" from a one-off image into a sustainable
production asset — the character owns the difference, the format owns distribution.

## License

[MIT](LICENSE) — free to use, modify and distribute, commercially included.
