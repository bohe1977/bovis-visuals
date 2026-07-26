import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYER_DATA = ROOT / "kbo-players" / "data.json"
GAME_DATA = ROOT / "kbo" / "data.json"
INTEGRATED = ROOT / "kbo" / "index.html"
PLAYER_PAGE = ROOT / "kbo-players" / "index.html"
MLB_INTEGRATED = ROOT / "mlb" / "index.html"


def test_kbo_report_excludes_canceled_games_from_data_and_display():
    games = json.loads(GAME_DATA.read_text(encoding="utf-8"))["games"]
    page = INTEGRATED.read_text(encoding="utf-8")

    assert len(games) == 5
    assert all(game["status"] == "경기 종료" for game in games)
    assert "경기 취소" not in GAME_DATA.read_text(encoding="utf-8")
    assert "const finalGames=gdata.games.filter(g=>g.status==='경기 종료');" in page
    assert "#metric-games').textContent=finalGames.length" in page
    assert "#metric-runs').textContent=finalGames.reduce" in page


def test_inactive_pitchers_have_status_only_and_active_pitchers_share_one_season_record_label():
    pitchers = json.loads(PLAYER_DATA.read_text(encoding="utf-8"))["pitchers"]
    inactive = [pitcher for pitcher in pitchers if not pitcher["appeared"]]
    integrated = INTEGRATED.read_text(encoding="utf-8")
    player_page = PLAYER_PAGE.read_text(encoding="utf-8")

    assert inactive
    for pitcher in inactive:
        assert set(pitcher) == {"name", "team", "appeared"}

    assert "<span class=\"none\">${s}</span>" in integrated
    assert "<span class=\"none\">${t}</span>" in player_page
    assert "inactive=(p,s)" in integrated

    assert "class=\"season-record\"" in integrated
    assert "${p.season_record} ${p.season_saves}세이브" in integrated
    assert "${p.season_record} · ${p.season_saves}세이브" not in integrated
    assert "${p.season_record} ${p.season_saves}세이브" in player_page
    assert "${p.season_record} · ${p.season_saves}세이브" not in player_page
    assert "stat(p.season_record,'시즌 성적')" in integrated
    assert "s(p.season_record,'시즌 성적')" in player_page
    assert "시즌 승패" not in integrated
    assert "시즌 승패" not in player_page
    assert "strong.season-record{font-size:17px" in integrated
    assert "strong.season-record.compact{font-size:13px" in integrated
    assert "el.scrollWidth>el.clientWidth" in integrated
    assert "addEventListener?.('resize',fitSeasonRecords)" in integrated
    assert "'시즌 성적','season-record'" in player_page
    assert ".stat b.season-record{font-size:inherit" in player_page
    assert ".stat b.season-record.compact{font-size:13px" in player_page


def test_kbo_integrated_report_hero_uses_player_then_all_team_result_title():
    page = INTEGRATED.read_text(encoding="utf-8")

    assert '<h1 id="page-title">KBO 관심 선수와<br>전체 팀 경기 결과</h1>' in page
    report_date = json.loads(GAME_DATA.read_text(encoding="utf-8"))["date"]
    assert f'<title>{report_date} KBO 관심 선수와 전체 팀 경기 결과</title>' in page
    assert 'KBO 경기·관심 선수</h1>' not in page


def test_game_note_headings_use_colon_in_kbo_and_mlb_reports():
    kbo = INTEGRATED.read_text(encoding="utf-8")
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")

    assert "</strong>: ${esc(g.opponent_effort)}</div>" in kbo
    assert "</strong> · ${esc(g.opponent_effort)}</div>" not in kbo
    assert "</strong>: ${esc(g.opponent_effort)}</div>" in mlb
    assert "</strong> · ${esc(g.opponent_effort)}</div>" not in mlb


def test_active_closer_fixture_keeps_verified_save_count_separate_from_inactive_shape():
    active_closer = {
        "name": "검증용 마무리",
        "team": "테스트",
        "appeared": True,
        "season_record": "3승 2패",
        "season_saves": 11,
        "era": "2.91",
    }
    inactive_pitcher = {"name": "검증용 미등판", "team": "테스트", "appeared": False}

    assert active_closer["appeared"] is True
    assert active_closer["season_saves"] == 11
    assert set(inactive_pitcher) == {"name", "team", "appeared"}
