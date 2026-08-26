import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "render_restaurant_map", ROOT / "scripts" / "render_restaurant_map.py"
)
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


def test_restaurant_renderer_accepts_one_line_busan_road_address():
    RENDERER.validate_address("부산 동구 중앙대로 206")
