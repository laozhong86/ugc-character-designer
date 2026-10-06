#!/usr/bin/env python3
"""Build gallery/taxonomy.md from assets/index.json.

Regenerates the full 170-option element gallery (grouped by category,
one standalone image per element — the same no-composites rule the skill
enforces at runtime). Run after any taxonomy/asset change:

    python3 scripts/build_gallery.py

Output: gallery/taxonomy.md (generated file — do not hand-edit).
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "index.json"
ZH = ROOT / "data" / "zh-labels.json"
OUT = ROOT / "gallery" / "taxonomy.md"

CATEGORY_ORDER = [
    "gender", "ethnicity_origin_base", "age", "skin_tone", "height",
    "body_type", "proportions", "freak_head", "freak_neck",
    "eye_shape", "eye_color", "freak_face", "facial_hair",
    "hair", "hair_colour", "distinctive", "aesthetic", "accessory",
]

TIER_LABEL = {"normal": "Average", "freak": "Bold", "total": "Extreme"}


def zh_of(zh: dict, cat: str, opt_id: str) -> str:
    return (zh.get("options", {}).get(cat, {}).get(opt_id)
            or zh.get("options", {}).get(f"{cat}/{opt_id}") or "")


def cat_zh(zh: dict, cat: str) -> str:
    return zh.get("categories", {}).get(cat, "")


def main() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    zh = json.loads(ZH.read_text(encoding="utf-8")) if ZH.is_file() else {}
    opts = index["options"]

    by_cat: dict[str, list[dict]] = {}
    for key, rec in opts.items():
        by_cat.setdefault(rec["category"], []).append(rec)

    lines: list[str] = [
        "# 元素画廊 · Taxonomy Gallery",
        "",
        f"> 自动生成 · `python3 scripts/build_gallery.py` · 共 {len(opts)} 个元素 · "
        "每个元素一张独立单图（禁止拼图，与运行时规则一致）",
        "",
        "| 类目 | 选项数 |",
        "|---|---|",
    ]
    for cat in CATEGORY_ORDER:
        recs = by_cat.get(cat, [])
        label = recs[0].get("category_label", cat) if recs else cat
        lines.append(f"| [{label} `{cat}`](#{cat}) | {len(recs)} |")
    lines.append("")

    for cat in CATEGORY_ORDER:
        recs = by_cat.get(cat)
        if not recs:
            continue
        label = recs[0].get("category_label", cat)
        zl = cat_zh(zh, cat)
        lines += [
            f"## {label} `{cat}`" + (f" · {zl}" if zl else ""),
            f"<a id=\"{cat}\"></a>",
            "",
            "| 图 | id | 名称 | 档位 |",
            "|---|---|---|---|",
        ]
        for r in recs:
            img = (r.get("image") or {}).get("rel", "")
            name = r.get("label", r["id"])
            z = zh_of(zh, cat, r["id"])
            tiers = " · ".join(TIER_LABEL.get(t, t) for t in r.get("tiers", []))
            bold = " ★" if r.get("bold_only") else ""
            cell = f'<img src="../{img}" width="72">' if img else "—"
            lines.append(f"| {cell} | `{r['id']}` | {name}{(' / ' + z) if z else ''}{bold} | {tiers} |")
        lines.append("")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(opts)} options, {len(by_cat)} categories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
