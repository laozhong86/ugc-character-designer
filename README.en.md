🌐 [中文](README.md) · **English**

# UGC Character Designer

**Give your Agent a brief. Design an original AI character people can recognize.**

A character-design Skill for creators making short videos for global audiences. Start with a persona,
define their appearance and signature behavior, then build portraits, character sheets and scene
references for AI influencers, virtual creators and UGC characters.

**170 appearance options across 18 categories · 3 exaggeration tiers · Random or guided customization**

Write the person first, then the face. Connect hairstyle, silhouette, outfit and signature actions
so the character stays recognizable in a thumbnail.

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](SKILL.md)
[![170 Options](https://img.shields.io/badge/Taxonomy-170%20options-orange)](assets/index.json)

[Design direction](#design-direction-global-character-references) · [What it does](#you-say-the-skill-helps-you) · [Get started](#installation-and-first-use) · [Workflow](#workflow) · [Limitations](#limitations)

## Design direction: global character references

These images were collected from [OmniMux's Inspiration Library → AI Influencers](https://omnimux.ai/influencer)
to show this project's direction for AI creator character design. **They are external references, not outputs of this Skill.
The featured characters do not belong to this project.**

<table>
<tr>
<td width="33%" valign="top"><img src="gallery/overseas/jean-phil.webp" width="250" alt="Jean Phil: platinum bob, thin mustache and brown checked suit"><br><strong>Jean Phil · Hair and styling</strong><br>A platinum bob, thin mustache and brown checked suit establish clear visual anchors.</td>
<td width="33%" valign="top"><img src="gallery/overseas/brigitte-macaron.webp" width="250" alt="Brigitte Macaron: short blond bob, round glasses and pale lavender suit"><br><strong>Brigitte Macaron · Color and accessories</strong><br>A short blond bob, round glasses and pale lavender suit give the design a coherent identity.</td>
<td width="33%" valign="top"><img src="gallery/overseas/leopold.webp" width="250" alt="Léopold: olive-green hat and outfit, voluminous long hair and tall boots"><br><strong>Léopold · Full-body silhouette</strong><br>An olive-green hat and outfit, voluminous hair and tall boots create a recognizable silhouette.</td>
</tr>
</table>

The focus is **original character design** for TikTok, Reels, Shorts and similar short-video formats:
a straight-faced commentator, a distinctive lifestyle creator, or a UGC persona with recurring gestures
and catchphrases. Retro outfits and deadpan expressions are one recipe for a comedy character;
clothing, expressions and attitude should serve the individual persona. The built-in workflow
currently centers on deadpan characters; see the limitations below for other performance directions.

[Image sources](gallery/overseas/SOURCES.md) · [More character references](gallery/README.md) · [Browse all 170 appearance options](gallery/taxonomy.md)

## You say, the Skill helps you

| Your brief | What the Skill helps you do |
|---|---|
| “I want an AI creator, but I don't know what they should look like.” | Generate character concepts with randomized personas and styling, optionally keeping chosen features fixed. |
| “I want to pick the silhouette, face, hair and outfit myself.” | Choose appearance in layers, check conflicting combinations and retain confirmed choices. |
| “Who is this person, and why would anyone remember them?” | Write a three-line persona, content niche, visual anchors, signature behavior and rules to avoid drift in a character card. |
| “Turn this concept into references for future images.” | Generate a full-body portrait, then an 8-panel character sheet with 5 full-body views and 3 close-ups. |
| “Change the styling while keeping the character recognizable.” | Reuse the locked description, revise the requested features and check identity and unchanged details. |
| “Can I still recognize them in a different setting?” | Create 1–3 UGC scene first-frames, inspect consistency and organize images, prompts and acceptance records. |

The full workflow aims to deliver a **character card → full-body portrait → 8-panel sheet → scene
references → handoff package**. Delivery reflects the stages actually generated and checked;
video generation and publishing happen in downstream tools.

## Installation and first use

Clone the complete repository into a skills directory supported by your Agent, for example:

```bash
git clone https://github.com/laozhong86/ugc-character-designer.git \
  ~/.agents/skills/ugc-character-designer
```

Keep `SKILL.md` and the `assets/`, `data/`, `references/`, `scripts/`, `templates/` and `evolution/`
directories together. Load the Skill through your Agent's host, then start with a concrete brief:

```text
Design an original AI character for short videos aimed at a global audience.
They review everyday things with excessive seriousness. Give me 3 distinct visual directions first.
```

Other starting points:

```text
Let me choose the appearance step by step for a distinctive virtual lifestyle creator.
Keep this character's silhouette and hairstyle; change the outfit for street interviews.
Build an 8-panel character sheet and two everyday scenes from the selected portrait.
```

**Requirements:** Python 3.10+ (scripts have no third-party dependencies) and an Agent that can load
Skills, run scripts and inspect images. Image generation also requires a tool exposed by your host,
with the relevant account access or credits. Installing the Skill does not provide an image service.
See the [image-generation guide](references/generation-tools.md) for current tool routing,
OmniMux setup and consistency limitations. Character projects are written to
`ugc-characters/<slug>/` in your current workspace.

## Workflow

1. **Choose a direction.** Start with random concepts, guided customization or randomization with selected features locked.
2. **Write the person.** Define their background, niche, personality, appearance anchors and signature actions; check the character card.
3. **Make a portrait.** Generate a full-body image, inspect recognition, originality and image quality, then revise when needed.
4. **Lock the reference.** Save the approved portrait and description as identity anchors for later images and revisions.
5. **Expand the assets.** Build an 8-panel sheet and optional scene first-frames; inspect consistency across images.
6. **Prepare the handoff.** Package the card, images, prompts and acceptance report, recording what passed and what still needs work.

### How quality is checked

| Stage | Check |
|---|---|
| G1 · Character card | Required fields, compatible choices, persona and originality declaration. |
| G2 · Full-body portrait | Visual rubric score of at least 3.8/5, with required individual scores. Revisions also check identity preservation. |
| G3 · 8-panel sheet | At least 4.0/5 overall, with required scores for cross-panel identity and reference matching. |
| G4 · Scene references | Identity, styling and image quality after changing the setting. |

**The Agent inspects each generated image and enters its visual judgments.** Scripts validate fields,
thresholds and records; they do not inspect images or guarantee aesthetic quality. Each stage allows
up to 3 different attempts before the Agent explains the issue and available adjustments.
See [SKILL.md](SKILL.md) for the full workflow and the [quality rubric](data/qa-rubric.json) for criteria.

### Appearance data and learning records

- **Multiple character directions.** 170 options across 18 categories cover hairstyles, facial features,
  skin tones, accessories and aesthetics. Average / Bold / Extreme tiers vary the strength of the
  design. A Chinese conversation does not default to a Chinese character.
- **Individual visual references.** Each appearance element has its own reference image. Visual
  descriptions and compatibility rules guide combinations instead of relying only on short labels.
- **Reused identity anchors.** The locked character description carries into revisions, sheets and
  scenes, followed by another visual check.
- **Recorded failures.** The ledger stores generation records, scores and failure tags. Experience
  rules need supporting evidence before promotion; each new result still needs validation.

## Limitations

- **Performance directions have limits.** Random character cards, signature prompts and G1/G2
  acceptance currently focus on deadpan or serious characters. Other expressions, such as broad
  smiles or winks, do not yet have a fully adapted acceptance workflow; changing a prompt alone
  does not establish complete support.
- **Consistency depends on the image tool.** Without a usable reference-image editing channel, the
  workflow mainly reuses a written character description. Facial details can drift. Outfit changes
  and character sheets need visual review, especially at the Extreme tier.
- **Public output evidence is limited.** The currently published Skill output is Jiang Lingyi's
  full-body portrait, linked below. The global character references above have not been presented
  as complete generation-and-acceptance examples of this Skill.
- **Original characters only.** Do not recreate the likeness of real people, celebrities, existing
  influencers or copyrighted characters. Humor comes from styling, posture and attitude, without
  mocking ethnicity, body type, gender identity or background.
- **The deliverable is character assets.** This project does not directly handle video filming,
  motion transfer, account operations or publishing. It promises no view counts or earnings.

## Cases and method sources

**Earlier output · Jiang Lingyi.** An original character for a costume political-drama short series,
with one published [full-body portrait](gallery/characters/jiang-lingyi-fullbody.png). The early design
record remains available; this README leads with the project's direction for global short-video
characters. See the [gallery](gallery/README.md) for context.

The method draws on character-design research and case studies. Appearance data comes from
OmniMux's influencer taxonomy:

- [Method distillation and original sources](references/research-distillation.md): personas, recognition anchors, behavior and character reuse.
- [Jean Phil case study](gallery/case-study-jean-phil.md): historical research into external characters and distribution patterns; figures depend on the original sources and recording dates.
- [Appearance gallery](gallery/taxonomy.md): individual references for all 170 options.

## Development and layout

[SKILL.md](SKILL.md) is the Agent's entry point. See the [intake flow](references/intake-questions.md)
and [prompt library](templates/prompt-library.md) for interaction and image-prompt details.

<details>
<summary>Script reference and repository layout</summary>

Script paths below are relative to the repository root. To create a character, run the script from
the target workspace using its absolute Skill path; character files are written to the current
workspace. Use each script's `--help` for subcommand arguments:

```bash
python3 scripts/ugc_face.py --help
python3 scripts/ugc_taxonomy.py find "horn"
python3 scripts/ugc_lab.py --help
python3 scripts/build_gallery.py   # rebuild the appearance gallery
python3 scripts/selftest_all.py    # data, rules, stage thresholds and Skill reference paths
```

- `ugc_face.py`: random concepts and layered customization (`random` / `init` / `menu` / `apply` / `prompt`).
- `ugc_taxonomy.py`: lookup, compatibility checks and prompt building (`find` / `get` / `refs` / `diversity` / `build`).
- `ugc_lab.py`: cards, generation records, scoring, locking, acceptance and learning records (`init` / `card-check` / `log` / `score` / `lock` / `accept` / `evolve` / `promote`).

```text
ugc-character-designer/
├── SKILL.md                # Agent execution workflow
├── README.md / README.en.md
├── assets/                 # option index and individual reference images
├── data/                   # appearance data, visual descriptions, rubric and rules
├── references/             # methods, intake flow, generation guide and sources
├── scripts/                # combination, validation, logging and gallery tools
├── templates/              # character card and prompt templates
├── evolution/              # experience rules and run ledger
└── gallery/                # global design references, earlier output and appearance gallery
```

</details>

## License

Code and documentation are [MIT](LICENSE). External reference media retain their original owners'
rights; see the [gallery](gallery/README.md) for sources and usage notes.
