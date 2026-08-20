import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "standards" / "mlb-game-card-contract-v1.json").read_text(encoding="utf-8"))
DATA = json.loads((ROOT / "mlb" / "data.json").read_text(encoding="utf-8"))
PAGE = (ROOT / "mlb" / "index.html").read_text(encoding="utf-8")
COLLECTOR = (ROOT / "tools" / "update_mlb.py").read_text(encoding="utf-8")


def test_mlb_contract_declares_kbo_reference_order_and_guardrails():
    assert CONTRACT["scoreboard"]["teamOrder"] == "official-away-home"
    assert CONTRACT["headline"]["perspective"] == "tracked-team"
    assert CONTRACT["headline"]["forbidGenericOpponentFirstResult"] is True
    assert CONTRACT["decisions"]["forbidCombinedDecisionString"] is True
    assert CONTRACT["gamePoints"]["minimumItems"] == 4
    assert CONTRACT["effort"]["team"] == "losing-team"


def test_losing_tracked_team_headline_leads_with_winner_and_omits_winner_team_name():
    giants = next(
        game for game in DATA["team_games"]
        if game["section_title"] == "샌프란시스코 자이언츠 경기" and game["status"] == "경기 종료"
    )

    assert giants["headline"] == "조 아델의 홈런 포함 6타점, 샌프란시스코에 8-1 승리"
    assert "클리블랜드가" not in giants["headline"]
    assert "브라이스 엘드리지의" not in giants["headline"]


def test_mlb_current_final_games_conform_to_contract():
    required = set(CONTRACT["collectorRequiredFields"])
    final_games = [game for game in DATA["team_games"] if game["status"] == "경기 종료"]
    assert final_games
    for game in final_games:
        assert required <= set(game)
        assert game["winner_pitcher"] and game["loser_pitcher"]
        assert len(game["game_points"]) >= CONTRACT["gamePoints"]["minimumItems"]
        losing_team = game["away"] if game["winner_side"] == "home" else game["home"]
        assert game["opponent_label"] == losing_team
        assert any(token in game["headline"] for token in ("에도", "앞세워", "결승타", "홈런 포함"))
        # Headlines must use a verified tracked-team hitter line or a verified decisive play;
        # do not require a home run when the official box score has none.
        assert any(token in game["headline"] for token in ("홈런 포함", "활약", "결승타"))
        assert all("공식 결정" not in item for item in game["game_points"])


def test_mlb_renderer_uses_separated_decisions_and_structured_points_only():
    assert '<div class="record">${g.winner_pitcher?`<span>승 ${esc(g.winner_pitcher)}</span>`' in PAGE
    assert "g.loser_pitcher?`<span>패 ${esc(g.loser_pitcher)}</span>`" in PAGE
    assert "g.save_pitcher?`<span>세 ${esc(g.save_pitcher)}</span>`" in PAGE
    assert "g.game_points.map" in PAGE
    assert "g.pitcher_record?" not in PAGE


def test_collector_generates_tracked_team_headline_and_four_fact_points():
    assert "focus_team='LA 다저스'" in COLLECTOR
    assert "focus_moment=headline_player_moment(focus_leader)" in COLLECTOR
    assert "headline_player_moment" in COLLECTOR
    assert "require_final_report(data)" in COLLECTOR
    assert "'game_points':game_points" in COLLECTOR
    assert "'opponent_label':(focus_team if not focus_won else loser_team)" in COLLECTOR
