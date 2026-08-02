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
if not venues or any(not {"name","distance","category","kind","color","signal","address","menus","reason","rationale"} <= set(v) for v in venues):
    raise SystemExit("invalid venue schema")
colors = [v["color"] for v in venues]
if len(colors) != len(set(colors)): raise SystemExit("candidate accent colors must be unique")
if any(len(v["menus"]) > 4 for v in venues): raise SystemExit("maximum four menu chips")
replacements = {"__TITLE__":data["title"],"__EYEBROW__":data["eyebrow"],"__INTRO__":data["intro"],"__SOURCE__":data["source"],"__MARKER_TITLE__":data["markerTitle"],"__NOTICE__":data["notice"],"__VENUES_JSON__":json.dumps(venues,ensure_ascii=False)}
for key,value in replacements.items(): template = template.replace(key,value)
if re.search(r'__[A-Z_]+__',template): raise SystemExit("unreplaced template token")
Path(sys.argv[2]).write_text(template,encoding="utf-8")
