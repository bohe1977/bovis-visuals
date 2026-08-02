import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "standards" / "restaurant-map-contract-v1.json"
TEMPLATE = ROOT / "templates" / "restaurant-map-v1.html"


def test_restaurant_map_contract_freezes_data_driven_template_rules():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    assert contract["renderer"]["input"].startswith("Top-level general array")
    assert contract["renderer"]["food_filters"] == "Generate FOOD filter buttons from the active mode's venue categories."
    assert contract["markerLabels"] == {
        "required": True,
        "maxCharacters": 12,
        "uniqueWithinMode": True,
        "railUses": "markerLabel",
        "cardUses": "name",
    }
    assert contract["labelTypography"] == {
        "appliesTo": ["CANDIDATES", "RADIUS", "CLOSEST", "BEST FOR", "DISTANCE", "FOOD"],
        "color": "#343434",
        "fontWeight": 700,
        "fontSize": "11px",
        "fontFamily": "ui-monospace, monospace",
    }
    assert contract["actions"]["savedSourceLabel"] == "레퍼런스"
    assert "reference source URL" in contract["actions"]["savedSourceRule"]
    assert contract["distance"]["placeholderValueForbidden"] == 0
    assert contract["distance"]["unit"] == "m"
    assert contract["actions"]["naverMapSearchTemplate"] == "https://map.naver.com/p/search/{encodeURIComponent(exactVenueName)}?c=15.00,0,0,0,dh"
    assert contract["actions"]["secondaryLabel"] == "검색 링크"
    assert contract["actions"]["naverIntegratedSearchTemplate"] == "https://search.naver.com/search.naver?query={encodeURIComponent(exactVenueName)}"
    assert contract["actions"]["distinctDestinationRule"].startswith("Render both 지도")


def test_canonical_template_keeps_mobile_info_and_menu_contracts():
    template = TEMPLATE.read_text(encoding="utf-8")

    assert ".info { min-height:0; display:block; padding:11px; border:0;" in template
    assert "box-shadow:0 0 0 1px rgba(0,0,0,.06);" in template
    assert ".info { min-height:72px" not in template
    assert ".menu { padding:7px 9px; border-radius:8px; background:#f2f2f2; color:#444; font-size:13px; font-weight:650; }" in template
    menu_contract = json.loads((ROOT / "standards" / "menu-chip-contract-v1.json").read_text(encoding="utf-8"))
    assert menu_contract["cardLimit"] == 3
    assert menu_contract["mobileRendering"] == "Render at most three verified menu chips with normal centered wrapping. Do not shrink chips or use a horizontal swipe rail unless the user explicitly approves it."
    assert "fewer than three" in menu_contract["selection"][-1]
    assert ".menu { padding:5px 8px; font-size:11px; }" not in template


def test_sadang_candidates_have_verified_nonzero_distances():
    sadang = json.loads((ROOT / "data" / "restaurant-guides" / "sadang-station.json").read_text(encoding="utf-8"))
    venues = sadang["general"]

    assert "사당역 좌표" in sadang["config"]["distanceMethod"]
    assert [item["label"] for item in sadang["config"]["distanceFilters"]] == ["전체", "0~100m", "100~300m", "300~500m"]
    assert all(venue["distance"] > 0 and venue["distance"] % 10 == 0 for venue in venues)
    assert all(set(venue["coordinates"]) == {"lat", "lng"} for venue in venues)
