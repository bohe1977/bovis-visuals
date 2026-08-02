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
    assert contract["actions"]["naverMapSearchTemplate"] == "https://map.naver.com/p/search/{encodeURIComponent(exactVenueName)}?c=15.00,0,0,0,dh"
    assert contract["actions"]["secondaryLabel"] == "검색 링크"
    assert contract["actions"]["naverIntegratedSearchTemplate"] == "https://search.naver.com/search.naver?query={encodeURIComponent(exactVenueName)}"
    assert contract["actions"]["distinctDestinationRule"].startswith("Render both 지도")


def test_canonical_template_keeps_mobile_info_and_menu_contracts():
    template = TEMPLATE.read_text(encoding="utf-8")

    assert ".info { min-height:0; display:block; padding:11px; border:0;" in template
    assert "box-shadow:0 0 0 1px rgba(0,0,0,.06);" in template
    assert ".info { min-height:72px" not in template
    assert ".menu { padding:7px 9px; border-radius:8px; background:#f2f2f2; color:#444; font-size:13px; font-weight:650; white-space:nowrap; }" in template
    assert ".menu { padding:5px 8px; font-size:11px; }" not in template
