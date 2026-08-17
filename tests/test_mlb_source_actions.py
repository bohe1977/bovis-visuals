from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mlb_game_cards_always_render_three_equal_source_actions():
    html = (ROOT / "mlb" / "index.html").read_text(encoding="utf-8")

    assert "const naverUrl=g.naver_game_id?" in html
    assert "const daumUrl=g.daum_game_id?" in html
    assert "const naverLabel=g.naver_game_id?'네이버 기록':'네이버 일정'" in html
    assert "const daumLabel=g.daum_game_id?'다음 기록':'다음 일정'" in html
    assert 'class="game-sources"' in html


def test_current_mlb_archive_has_same_source_action_contract():
    html = (ROOT / "mlb" / "2026-08-17" / "index.html").read_text(encoding="utf-8")

    assert "const naverUrl=g.naver_game_id?" in html
    assert "const daumUrl=g.daum_game_id?" in html
