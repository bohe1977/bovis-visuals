from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "templates" / "restaurant-map-v1.html").read_text(encoding="utf-8")
RENDERER = (ROOT / "scripts" / "render_restaurant_map.py").read_text(encoding="utf-8")


def test_template_uses_approved_sadang_final_shell_not_intermediate_shell():
    assert '<nav class="top">' in TEMPLATE
    assert 'class="brand"' in TEMPLATE
    assert 'class="pill" id="scopePill"' in TEMPLATE
    assert 'font-size:clamp(42px,7vw,78px)' in TEMPLATE
    assert 'font-family:Geist,Arial,"Apple SD Gothic Neo",sans-serif' in TEMPLATE


def test_template_uses_approved_sadang_card_anatomy_and_natural_height():
    assert 'class="card-head"' in TEMPLATE
    assert '.card-head { display:flex;' in TEMPLATE
    assert '.card { min-height:486px;' not in TEMPLATE
    assert 'grid-template-rows:3px 46px 40px' not in TEMPLATE
    assert 'function foodGroup(venue)' in TEMPLATE
    assert "'이자카야/사시미'" in TEMPLATE
    assert 'function conciseSignal(value)' in TEMPLATE
    assert 'margin-top:auto;' in TEMPLATE


def test_renderer_allows_up_to_four_source_backed_menu_signals():
    assert 'if not 1 <= len(evidence) <= 4' in RENDERER
