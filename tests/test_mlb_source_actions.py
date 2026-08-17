from pathlib import Path
import json

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


def test_20260817_giants_game_uses_actual_naver_and_daum_records_in_korean():
    data = json.loads((ROOT / "mlb" / "2026-08-17" / "data.json").read_text(encoding="utf-8"))
    game = next(game for game in data["team_games"] if game["game_pk"] == 823182)

    assert game["away"] == "콜로라도"
    assert game["naver_game_id"] == "20260817COSF0"
    assert game["daum_game_id"] == 80105159
    assert game["naver_verified"] is True
    assert game["daum_verified"] is True
