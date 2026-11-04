import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_renderer_accepts_sejong_road_address_without_invented_district(tmp_path):
    data = json.loads((ROOT/'tests/fixtures/restaurant-general-only.json').read_text())
    for venue in data['general']:
        venue['address'] = '세종 절재로 194 2층'
    source = tmp_path/'input.json'
    source.write_text(json.dumps(data, ensure_ascii=False))
    result = subprocess.run([sys.executable, str(ROOT/'scripts/render_restaurant_map.py'), str(source), str(tmp_path/'guide.html')], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_renderer_rejects_sejong_without_road_and_building_number(tmp_path):
    data = json.loads((ROOT/'tests/fixtures/restaurant-general-only.json').read_text())
    data['general'][0]['address'] = '세종 중앙타운 근처'
    source = tmp_path/'input.json'
    source.write_text(json.dumps(data, ensure_ascii=False))
    result = subprocess.run([sys.executable, str(ROOT/'scripts/render_restaurant_map.py'), str(source), str(tmp_path/'guide.html')], capture_output=True, text=True)
    assert result.returncode != 0
