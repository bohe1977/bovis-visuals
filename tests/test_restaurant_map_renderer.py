import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "render_restaurant_map.py"
FIXTURES = ROOT / "tests" / "fixtures"


def render_fixture(tmp_path, fixture_name):
    output = tmp_path / "restaurant-map.html"
    result = subprocess.run(
        [sys.executable, str(RENDERER), str(FIXTURES / fixture_name), str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    return output.read_text(encoding="utf-8")


def test_renderer_renders_general_only_fixture_without_tab_control(tmp_path):
    html = render_fixture(tmp_path, "restaurant-general-only.json")

    assert "테스트역 맛집 지도" in html
    assert '"venues": {"general": [' in html
    assert '"modeConfig": {"general": {' in html
    assert '"bohe":' not in html
    assert 'data-mode="bohe"' not in html


def render_payload(tmp_path, payload):
    input_path = tmp_path / "guide.json"
    output_path = tmp_path / "guide.html"
    input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(RENDERER), str(input_path), str(output_path)], cwd=ROOT, text=True, capture_output=True)


def test_renderer_rejects_non_concise_marker_labels_and_duplicate_mode_colors(tmp_path):
    payload = json.loads((FIXTURES / "restaurant-general-only.json").read_text(encoding="utf-8"))
    payload["general"][0]["markerLabel"] = "가나다라마바사아자차카타파"
    result = render_payload(tmp_path, payload)
    assert result.returncode != 0
    assert "markerLabel must be concise" in result.stderr

    payload["general"][0]["markerLabel"] = "테스트국수"
    payload["general"][1]["color"] = payload["general"][0]["color"]
    result = render_payload(tmp_path, payload)
    assert result.returncode != 0
    assert "candidate accent colors must be unique within each mode" in result.stderr


def test_renderer_embeds_both_modes_as_data_for_synchronized_client_rendering(tmp_path):
    html = render_fixture(tmp_path, "restaurant-general-plus-bohe.json")
    template = (ROOT / "templates" / "restaurant-map-v1.html").read_text(encoding="utf-8")

    assert '"general": [' in html and '"bohe": [' in html
    assert "≤ 500m" in html and "≤ 900m" in html
    assert "일반 레일" in html and "보헤 레일" in html
    assert "일반 파스타" in html and "보헤 버거" in html
    assert "const categories = [...new Map(modeVenues().map" in html
    assert "venue.markerLabel" in template
    assert "<h2>${escapeHtml(venue.name)}</h2>" in template
    assert "?c=15.00,0,0,0,dh" in template
    assert "검색 링크" in template
    assert "function naverPlaceSearchUrl(name) { return `https://search.naver.com/search.naver?query=${encodeURIComponent(name)}`; }" in template
    assert "const query = venue.searchQuery || venue.name; const mapUrl = searchUrl(query); const placeSearchUrl = naverPlaceSearchUrl(query);" in template
    assert "양식/세계음식" not in template and "페레힐" not in template
    assert ".info { min-height:0; display:block; padding:11px; border:0;" in html
    assert ".menu { padding:7px 9px; border-radius:8px; background:#f2f2f2; color:#444; font-size:13px; font-weight:650; }" in html
    assert ".menus { margin:0; gap:7px; flex-wrap:nowrap" not in html
    assert ".stat-label { color:#343434; font:700 11px/1 ui-monospace,monospace; letter-spacing:.08em; }" in html
    assert ".filter-label { color:#343434; text-align:right; font:700 11px/1 ui-monospace,monospace; letter-spacing:.08em; }" in html
    assert ".marker-distance { display:block; color:#181818; font:800 11px/1.25 Geist,Arial,sans-serif; }" in html


def test_renderer_allows_db_only_venue_without_invented_menu_chips(tmp_path):
    payload = json.loads((FIXTURES / "restaurant-general-only.json").read_text(encoding="utf-8"))
    venue = payload["general"][0]
    venue["dbOnly"] = True
    venue["menuEvidence"] = []

    result = render_payload(tmp_path, payload)

    assert result.returncode == 0, result.stderr
    html = (tmp_path / "guide.html").read_text(encoding="utf-8")
    assert "const menus = venue.menus.length" in html


def test_renderer_labels_bohe_source_action_as_reference(tmp_path):
    payload = json.loads((FIXTURES / "restaurant-general-only.json").read_text(encoding="utf-8"))
    payload["general"][0]["savedSource"] = "https://www.instagram.com/p/example/"

    result = render_payload(tmp_path, payload)

    assert result.returncode == 0, result.stderr
    html = (tmp_path / "guide.html").read_text(encoding="utf-8")
    assert ">레퍼런스</a>" in html


def test_renderer_treats_empty_optional_bohe_array_as_general_only(tmp_path):
    html = render_fixture(tmp_path, "restaurant-empty-bohe.json")

    assert '"bohe":' not in html
    assert 'data-mode="bohe"' not in html


def test_renderer_enforces_v2_mode_reference_and_ambiguous_name_rules(tmp_path):
    payload = json.loads((FIXTURES / "restaurant-general-plus-bohe.json").read_text(encoding="utf-8"))
    payload["modeConfig"]["general"]["label"] = "레퍼런스"
    result = render_payload(tmp_path, payload)
    assert result.returncode != 0
    assert "general tab label must be 일반 추천" in result.stderr

    payload = json.loads((FIXTURES / "restaurant-general-plus-bohe.json").read_text(encoding="utf-8"))
    del payload["bohe"][0]["savedSource"]
    result = render_payload(tmp_path, payload)
    assert result.returncode != 0
    assert "bohe venues require an https savedSource" in result.stderr

    payload = json.loads((FIXTURES / "restaurant-general-only.json").read_text(encoding="utf-8"))
    original_name = payload["general"][0]["name"]
    payload["general"][0]["name"] = "마야"
    for pick in payload["modeConfig"]["general"]["quickPicks"]:
        if pick["venue"] == original_name:
            pick["venue"] = "마야"
    result = render_payload(tmp_path, payload)
    assert result.returncode != 0
    assert "short or ambiguous venue names require searchQuery" in result.stderr

    payload["general"][0]["searchQuery"] = "마야 성수"
    result = render_payload(tmp_path, payload)
    assert result.returncode == 0, result.stderr
