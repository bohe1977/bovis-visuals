import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "standards" / "restaurant-map-contract-v1.json"
SEONGSU = ROOT / "2026-08-02-seongsu-station-restaurants" / "index.html"
PORTAL = ROOT / "index.html"
SADANG = ROOT / "2026-08-03-sadang-db-second-round" / "index.html"


def test_curation_is_the_standard_label_for_db_source_actions():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    seongsu = SEONGSU.read_text(encoding="utf-8")
    sadang = SADANG.read_text(encoding="utf-8")

    assert contract["actions"]["savedSourceLabel"] == "큐레이션"
    assert 'href="${venue.savedSource}">큐레이션</a>' in seongsu
    assert ">큐레이션</a>" in sadang
    assert "저장 원문" not in seongsu
    assert "저장 원문" not in sadang


def test_seongsu_page_has_standardized_addresses_and_both_modes():
    seongsu = SEONGSU.read_text(encoding="utf-8")
    portal = PORTAL.read_text(encoding="utf-8")

    assert "general: [" in seongsu and "bohe: [" in seongsu
    assert seongsu.count("savedSource:") == 4
    assert seongsu.count("address:'서울 성동구 ") == 13
    assert "일반 추천" in seongsu and "보헤 추천" in seongsu
    assert "2026-08-02-seongsu-station-restaurants/" in portal
    assert "보헤 큐레이션 4곳" in portal


def test_seongsu_mobile_info_boxes_match_the_reference_natural_height_rule():
    seongsu = SEONGSU.read_text(encoding="utf-8")

    assert ".info { min-height:0; display:block; padding:11px; border:0;" in seongsu
    assert "box-shadow:0 0 0 1px rgba(0,0,0,.06);" in seongsu
    assert ".info { min-height:72px" not in seongsu
    assert ".info b { font-size:9px; }" not in seongsu
    assert ".info span { font-size:12px; }" not in seongsu


def test_seongsu_menu_tags_keep_the_reference_size_on_mobile():
    seongsu = SEONGSU.read_text(encoding="utf-8")

    assert ".menu { padding:7px 9px; border-radius:8px; background:#f2f2f2; color:#444; font-size:13px; font-weight:650; }" in seongsu
    assert ".menu { padding:5px 8px; font-size:11px; }" not in seongsu
