import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("update_mlb_state", TOOLS / "update_mlb.py")
UPDATE_MLB = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(UPDATE_MLB)
PAGE = (ROOT / "mlb" / "index.html").read_text(encoding="utf-8")


def game(state: str, detailed: str, away_score=0, home_score=0):
    return {
        "gamePk": 1,
        "officialDate": "2026-08-18",
        "gameDate": "2026-08-19T00:40:00Z",
        "status": {"abstractGameState": state, "detailedState": detailed},
        "teams": {
            "away": {"team": {"name": "Los Angeles Dodgers"}, "score": away_score},
            "home": {"team": {"name": "Colorado Rockies"}, "score": home_score},
        },
        "venue": {"name": "Coors Field"},
        "linescore": {"teams": {"away": {}, "home": {}}},
        "decisions": {},
    }


def build(g):
    return UPDATE_MLB.build_game(
        g,
        "LA 다저스 경기",
        [],
        [],
        box={"teams": {"away": {}, "home": {}}},
        feed={},
    )


def test_scheduled_game_never_generates_final_result_copy():
    result = build(game("Preview", "Scheduled"))

    assert result["status"] == "경기 예정"
    assert result["winner_side"] is None
    assert "승리" not in result["headline"]
    assert "승리투수" not in result["headline"]
    assert result["game_points"] == []
    assert result["opponent_effort"] is None


def test_live_game_never_generates_final_result_copy_or_winner():
    result = build(game("Live", "In Progress", away_score=1, home_score=3))

    assert result["status"] == "경기 진행 중"
    assert result["winner_side"] is None
    assert "승리" not in result["headline"]
    assert "승리투수" not in result["headline"]
    assert result["game_points"] == []
    assert result["opponent_effort"] is None


def test_lineup_member_without_plate_appearance_is_not_a_completed_appearance():
    assert UPDATE_MLB.batter_status({"atBats": 0, "plateAppearances": 0}, "경기 진행 중") == "경기 진행 중"


def test_nonfinal_games_are_rejected_before_publication():
    data = {"team_games": [build(game("Preview", "Scheduled"))]}
    with pytest.raises(ValueError, match="not final"):
        UPDATE_MLB.require_final_report(data)


def test_renderer_uses_game_state_instead_of_hardcoded_result_label():
    assert "const final=g.status==='경기 종료';" in PAGE
    assert "final?'경기 결과':esc(g.status)" in PAGE
    assert "final?`<p class=\"headline\"" in PAGE
    assert "<span class=\"status\">경기 결과</span>" not in PAGE
