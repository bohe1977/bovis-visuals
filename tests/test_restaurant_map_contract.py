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
