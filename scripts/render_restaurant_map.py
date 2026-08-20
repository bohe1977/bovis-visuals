#!/usr/bin/env python3
"""Render a canonical BOVIS restaurant-map page from validated guide JSON."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "templates" / "restaurant-map-v1.html").read_text(encoding="utf-8")
MENU_KEYS = {"display", "source", "sourceType", "kind"}
VENUE_KEYS = {
    "name", "markerLabel", "distance", "category", "kind", "color", "signal",
    "address", "menuEvidence", "reason", "rationale",
}


def valid_reference_url(value):
    return isinstance(value, str) and re.fullmatch(r"https?://[^\s]+", value) is not None


def validate_address(value):
    if not isinstance(value, str) or "\n" in value or not re.match(r"^서울\s+\S+구\s+.+\d", value):
        fail("address must be one-line Seoul road address with district and building number")


def validate_search_query(venue):
    query = venue.get("searchQuery")
    if query is not None and (not isinstance(query, str) or len(query.strip()) < 3):
        fail("searchQuery must be a specific search phrase of at least three characters")
    if len(venue["name"].strip()) <= 2 and not query:
        fail("short or ambiguous venue names require searchQuery")
CONFIG_KEYS = {
    "title", "description", "eyebrow", "intro", "source", "notice", "markerHelper",
    "distanceFilters",
}
MODE_KEYS = {"label", "radiusLabel", "bestFor", "markerTitle", "quickPicks"}


def fail(message):
    raise SystemExit(message)


def validate_menu_evidence(venue):
    evidence = venue["menuEvidence"]
    if venue.get("dbOnly") and not evidence:
        venue["menus"] = []
        return
    if not 1 <= len(evidence) <= 4 or any(not MENU_KEYS <= set(item) for item in evidence):
        fail("menu evidence must contain 1–4 display/source/sourceType/kind items")
    if any(len(item["display"].strip()) > 12 for item in evidence):
        fail("menu display must be concise (maximum 12 characters) for a one-line mobile chip")
    if any(re.search(r"\b\d+\s*(p|ea|인|인분)\b|\((소|중|대|lunch)\)", item["display"], re.I) for item in evidence):
        fail("menu display still contains count, size, or meal-period copy")
    if sum(item["kind"] == "beverage" for item in evidence) > 1:
        fail("at most one beverage menu signal")
    if any(item["kind"] not in {"food", "beverage"} for item in evidence):
        fail("menu kind must be food or beverage")
    venue["menus"] = [item["display"] for item in evidence]


def validate_mode(mode, venues, mode_config):
    expected_label = "일반 추천" if mode == "general" else "보헤 추천"
    if mode_config.get("label") != expected_label:
        fail(f"{mode} tab label must be {expected_label}")
    if not isinstance(venues, list) or not venues:
        fail(f"{mode} must be a non-empty venue array")
    if not MODE_KEYS <= set(mode_config):
        fail(f"missing modeConfig for {mode}")
    colors, labels, names = [], set(), set()
    for venue in venues:
        if not VENUE_KEYS <= set(venue):
            fail("invalid venue schema")
        label = venue["markerLabel"]
        if not isinstance(label, str) or not label.strip() or len(label) > 12:
            fail("markerLabel must be concise and non-empty (maximum 12 characters)")
        if label in labels:
            fail("markerLabel values must be unique within a mode")
        if venue["name"] in names:
            fail("venue names must be unique within a mode")
        labels.add(label)
        names.add(venue["name"])
        validate_address(venue["address"])
        validate_search_query(venue)
        if mode == "bohe" and not valid_reference_url(venue.get("savedSource")):
            fail("bohe venues require an https savedSource for the reference action")
        if mode == "bohe" and venue.get("dbOnly"):
            fail("bohe venues require verified Naver menu evidence; dbOnly is not allowed")
        colors.append(venue["color"])
        validate_menu_evidence(venue)
    if len(colors) != len(set(colors)):
        fail("candidate accent colors must be unique within each mode")
    quick_picks = mode_config["quickPicks"]
    if not isinstance(quick_picks, list) or not 1 <= len(quick_picks) <= 3:
        fail(f"{mode} quickPicks must contain one to three verified venues")
    for pick in quick_picks:
        if not {"title", "venue", "copy"} <= set(pick) or pick["venue"] not in names:
            fail(f"{mode} quick picks must reference a venue in that mode")


def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def main(input_path, output_path):
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    if not {"config", "modeConfig", "general"} <= set(data):
        fail("missing top-level config, modeConfig, or general")
    config = data["config"]
    if not CONFIG_KEYS <= set(config):
        fail("invalid config schema")
    modes = {"general": data["general"]}
    if data.get("bohe"):
        modes["bohe"] = data["bohe"]
    mode_config = data["modeConfig"]
    if not set(modes) <= set(mode_config):
        fail("missing modeConfig")
    for mode, venues in modes.items():
        validate_mode(mode, venues, mode_config[mode])
    payload = {"config": config, "modeConfig": {mode: mode_config[mode] for mode in modes}, "venues": modes}
    replacements = {
        "__TITLE__": html.escape(config["title"]),
        "__DESCRIPTION__": html.escape(config["description"]),
        "__INTRO__": config["intro"],
        "__PAYLOAD_JSON__": script_json(payload),
    }
    rendered = TEMPLATE
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    if re.search(r"__[A-Z_]+__", rendered):
        fail("unreplaced template token")
    Path(output_path).write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        fail("usage: render_restaurant_map.py INPUT_JSON OUTPUT_HTML")
    main(sys.argv[1], sys.argv[2])
