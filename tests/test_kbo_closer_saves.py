import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYER_DATA = ROOT / "kbo-players" / "data.json"
GAME_DATA = ROOT / "kbo" / "data.json"
INTEGRATED = ROOT / "kbo" / "index.html"
PLAYER_PAGE = ROOT / "kbo-players" / "index.html"
MLB_INTEGRATED = ROOT / "mlb" / "index.html"
MLB_DATA = ROOT / "mlb" / "data.json"


def test_kbo_report_excludes_canceled_games_from_data_and_display():
    games = json.loads(GAME_DATA.read_text(encoding="utf-8"))["games"]
    page = INTEGRATED.read_text(encoding="utf-8")

    assert len(games) == 3
    assert all(game["status"] == "경기 종료" for game in games)
    assert all((game["away"], game["home"]) not in {("NC", "두산"), ("KT", "KIA")} for game in games)
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


def test_pitcher_badges_use_verified_role_specific_game_decisions():
    pitchers = json.loads(PLAYER_DATA.read_text(encoding="utf-8"))["pitchers"]
    integrated = INTEGRATED.read_text(encoding="utf-8")
    player_page = PLAYER_PAGE.read_text(encoding="utf-8")
    active = {pitcher["name"]: pitcher for pitcher in pitchers if pitcher["appeared"]}

    assert active["로드리게스"]["role"] == "starter"
    assert active["로드리게스"]["game_decision"] == "승"
    assert active["김원중"]["role"] == "reliever"
    assert active["김원중"]["game_decision"] == "세이브"
    assert active["김원중"]["season_saves"] == 5

    for page in (integrated, player_page):
        assert "const pitcherState=p=>" in page
        assert "['승','패']" in page
        assert "['세이브','홀드','블론']" in page
        assert "game_decision" in page


def test_game_card_uses_result_label_mono_meta_and_outside_winner_badge_order():
    page = INTEGRATED.read_text(encoding="utf-8")

    assert '<span class="status">경기 결과</span>' in page
    assert '.status,.venue{font:600 11px/1.3 "Geist Mono",ui-monospace,monospace' in page
    assert '<div class="team away">${aw?' in page
    assert "<span class=\"team-name\">${esc(g.away)}</span>" in page


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


def test_mlb_game_note_uses_losing_team_effort_like_kbo():
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")

    assert '<strong>${esc(g.opponent_label)}의 분전</strong>: ${esc(g.opponent_effort)}</div>' in mlb
    assert '<strong>출처</strong>: ${esc(g.opponent_effort)}</div>' not in mlb


def test_mlb_game_cards_match_kbo_game_content_hierarchy():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")

    final_games = [game for game in data["team_games"] if game["status"] == "경기 종료"]
    assert final_games
    assert all(game.get("winner_pitcher") and game.get("loser_pitcher") for game in final_games)
    assert all(len(game.get("game_points", [])) >= 4 for game in final_games)
    assert all("공식 결정" not in " ".join(game["game_points"]) for game in final_games)
    assert all(game.get("opponent_label") in {game["away"], game["home"]} for game in final_games)
    assert '<div class="record">${g.winner_pitcher?`<span>승 ${esc(g.winner_pitcher)}</span>`' in mlb
    assert "g.game_points.map" in mlb
    assert '<strong>${esc(g.opponent_label)}의 분전</strong>' in mlb
    assert '<strong>출처</strong>: ${esc(g.opponent_effort)}</div>' not in mlb


def test_mlb_uses_result_label_and_role_specific_pitcher_badges():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")

    assert '<span class="status">경기 결과</span>' in mlb
    assert "const pitcherState=p=>" in mlb
    assert "['승','패']" in mlb
    assert "['세이브','홀드','블론']" in mlb
    assert "metric(p.game_decision" not in mlb
    assert "metric(p.decision" not in mlb
    assert "metric(p.daily_walks_hbp,'4사구')" in mlb

    # Role-specific decision fixtures: only the allowed decision may render.
    fixtures = [
        {"role": "starter", "game_decision": "승", "visible": True},
        {"role": "starter", "game_decision": "패", "visible": True},
        {"role": "starter", "game_decision": None, "visible": False},
        {"role": "reliever", "game_decision": "세이브", "visible": True},
        {"role": "reliever", "game_decision": "홀드", "visible": True},
        {"role": "reliever", "game_decision": "블론", "visible": True},
        {"role": "reliever", "game_decision": None, "visible": False},
    ]
    for fixture in fixtures:
        decision = fixture["game_decision"]
        visible = bool(decision) and (
            (fixture["role"] == "starter" and decision in {"승", "패"})
            or (fixture["role"] == "reliever" and decision in {"세이브", "홀드", "블론"})
        )
        assert visible is fixture["visible"]

    for pitcher in data["pitchers"]:
        if pitcher["appeared"]:
            assert pitcher["role"] in {"starter", "reliever"}
            assert pitcher["game_decision"] in {"승", "패", "세이브", "홀드", "블론", None}
        elif pitcher.get("minor_league_excluded"):
            assert pitcher["status"] == "출전 없음"
            assert pitcher["daily_note"] == "MLB 경기 출전 없음"
        else:
            assert set(pitcher) == {"name", "team", "mlbam_id", "appeared", "status"}


def test_mlb_current_batting_line_and_team_result_are_normalized_from_official_data():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    ohtani = next(player for player in data["batters"] if player["name"] == "오타니 쇼헤이")
    dodgers_game = next(game for game in data["team_games"] if game["section_title"] == "LA 다저스 경기")

    assert ohtani["mlbam_id"] == 660271
    assert ohtani["status"] in {"출전", "비출전", "팀 경기 없음"}
    assert dodgers_game["status"] == "경기 종료"
    assert dodgers_game["winner_pitcher"]
    assert len(dodgers_game["game_points"]) >= 4


def test_mlb_minor_league_batting_lines_are_excluded_and_rendered_as_no_mlb_appearance():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")
    excluded = [player for player in data["batters"] if player.get("minor_league_excluded")]

    assert "김혜성" in {player["name"] for player in excluded}
    assert all(player["status"] == "출전 없음" for player in excluded)
    assert all(player["daily_note"] == "MLB 경기 출전 없음" for player in excluded)
    assert all(player["at_bats"] is None and player["hits"] is None for player in excluded)
    assert "Gwinnett Stripers" not in MLB_DATA.read_text(encoding="utf-8")
    assert "Oklahoma City Comets" not in MLB_DATA.read_text(encoding="utf-8")
    assert "p.minor_league_excluded" in mlb


def test_mlb_current_report_marks_minor_league_pitcher_go_woosuk_as_no_mlb_appearance():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")
    go = next(player for player in data["pitchers"] if player["name"] == "고우석")

    assert go["minor_league_excluded"] is True
    assert go["status"] == "출전 없음"
    assert go["daily_note"] == "MLB 경기 출전 없음"
    assert "const inactivePitcherRows=inactivePitchers.map(p=>p.minor_league_excluded?" in mlb
    assert "cache:'no-store'" in mlb
    assert "data.json?rev=20260805-minor-pitcher" in mlb


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
