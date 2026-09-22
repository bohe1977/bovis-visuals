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
    losing_tracked = next(
        (
            game for game in DATA["team_games"]
            if game["status"] == "경기 종료"
            and ((game["section_title"].startswith("LA 다저스") and game["winner_side"] != ("away" if game["away"] == "LA 다저스" else "home"))
                 or (game["section_title"].startswith("샌프란시스코") and game["winner_side"] != ("away" if game["away"] == "샌프란시스코" else "home")))
        ),
        None,
    )
    if losing_tracked is None:
        return  # The final KST slate can legitimately have both tracked teams win.

    winner_team = losing_tracked["away"] if losing_tracked["winner_side"] == "away" else losing_tracked["home"]
    assert "활약, " in losing_tracked["headline"] or "홈런 포함" in losing_tracked["headline"]
    assert winner_team + "가" not in losing_tracked["headline"]


def test_overlapping_tracked_team_game_renders_once_with_dodgers_priority():
    final_games = [game for game in DATA["team_games"] if game["status"] == "경기 종료"]
    game_ids = [game["game_pk"] for game in final_games]
    assert len(game_ids) == len(set(game_ids)), "one MLB game must never create mirrored team cards"
    shared = [game for game in final_games if game["away"] in {"LA 다저스", "샌프란시스코"} and game["home"] in {"LA 다저스", "샌프란시스코"}]
    if shared:
        assert len(shared) == 1
        assert shared[0]["section_title"] == "LA 다저스 경기"


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
        assert any(token in game["headline"] for token in ("에도", "앞세워", "결승타", "홈런 포함", "활약"))
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
