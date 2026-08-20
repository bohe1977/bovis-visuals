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
    assert 'class="rank">${rank}</div><h2>${escapeHtml(venue.name)}</h2>' in TEMPLATE
    assert '.card-head { display:flex;' not in TEMPLATE
    assert '.card { min-height:486px;' not in TEMPLATE
    assert 'grid-template-rows:3px 46px 40px' not in TEMPLATE
    assert 'function foodGroup(venue)' in TEMPLATE
    assert "'이자카야/사시미'" in TEMPLATE
    assert 'function conciseSignal(value)' in TEMPLATE
    assert '@media (max-width:650px) { .page' in TEMPLATE
    assert '.top { justify-content:center; }' in TEMPLATE
    assert '.pill { display:none; }' in TEMPLATE
    assert 'h1 { margin:18px 0 0; font-size:42px; }' in TEMPLATE
    assert 'h1.long-title { font-size:39px; }' in TEMPLATE
    assert '<h1 class="__TITLE_CLASS__">__TITLE__</h1>' in TEMPLATE
    assert 'min-height:36px' in TEMPLATE
    assert 'padding:0 12px' in TEMPLATE
    assert 'grid-template-rows:3px auto 36px' in TEMPLATE
    assert 'min-height:46px' not in TEMPLATE
    assert 'font-weight:650' in TEMPLATE
    assert 'margin-top:auto;' in TEMPLATE


def test_renderer_rejects_long_card_decision_copy():
    assert 'len(rationale) > 60' in RENDERER
    assert 'rationale must contain at most two short sentences' in RENDERER
    assert 'if not 1 <= len(evidence) <= 4' in RENDERER
