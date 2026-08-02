#!/usr/bin/env python3
"""Render a BOVIS restaurant-map page only from the v1 template and a data JSON."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
template = (root / "templates/restaurant-map-v1.html").read_text(encoding="utf-8")
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
required = {"title", "eyebrow", "intro", "source", "markerTitle", "notice", "venues"}
missing = required - data.keys()
if missing: raise SystemExit(f"missing: {sorted(missing)}")
venues = data["venues"]
if not venues or any(not {"name","markerLabel","distance","category","kind","color","signal","address","menuEvidence","reason","rationale"} <= set(v) for v in venues):
    raise SystemExit("invalid venue schema")
colors = [v["color"] for v in venues]
if len(colors) != len(set(colors)): raise SystemExit("candidate accent colors must be unique")
for venue in venues:
    evidence = venue["menuEvidence"]
    if not 1 <= len(evidence) <= 4 or any(not {"display","source","sourceType","kind"} <= set(item) for item in evidence):
        raise SystemExit("menu evidence must contain 1–4 display/source/sourceType/kind items")
    if any(re.search(r"\b\d+\s*(p|ea|인|인분)\b|\((소|중|대|lunch)\)", item["display"], re.I) for item in evidence):
        raise SystemExit("menu display still contains count, size, or meal-period copy")
    drinks = [item for item in evidence if item["kind"] == "beverage"]
    if len(drinks) > 1:
        raise SystemExit("at most one beverage menu signal")
    if any(item["kind"] not in {"food", "beverage"} for item in evidence):
        raise SystemExit("menu kind must be food or beverage")
    venue["menus"] = [item["display"] for item in evidence]
replacements = {"__TITLE__":data["title"],"__EYEBROW__":data["eyebrow"],"__INTRO__":data["intro"],"__SOURCE__":data["source"],"__MARKER_TITLE__":data["markerTitle"],"__NOTICE__":data["notice"],"__VENUES_JSON__":json.dumps(venues,ensure_ascii=False)}
for key,value in replacements.items(): template = template.replace(key,value)
if re.search(r'__[A-Z_]+__',template): raise SystemExit("unreplaced template token")
Path(sys.argv[2]).write_text(template,encoding="utf-8")
