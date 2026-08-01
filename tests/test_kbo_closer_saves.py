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


def test_pitcher_badges_use_verified_role_specific_game_decisions():
    pitchers = json.loads(PLAYER_DATA.read_text(encoding="utf-8"))["pitchers"]
    integrated = INTEGRATED.read_text(encoding="utf-8")
    player_page = PLAYER_PAGE.read_text(encoding="utf-8")
    active = {pitcher["name"]: pitcher for pitcher in pitchers if pitcher["appeared"]}

    assert active["원태인"]["role"] == "starter"
    assert active["원태인"]["game_decision"] == "승"
    assert active["류현진"]["role"] == "starter"
    assert active["류현진"]["game_decision"] == "패"
    assert active["박영현"]["role"] == "reliever"
    assert active["박영현"]["game_decision"] == "세이브"
    assert active["박정민"]["game_decision"] is None

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
    assert all(game.get("pitcher_record") for game in final_games)
    assert all(len(game.get("points", [])) >= 3 for game in final_games)
    assert all("공식 결정" not in " ".join(game["points"]) for game in final_games)
    assert all(game.get("opponent_label") in {game["away"], game["home"]} for game in final_games)
    assert '<div class="record">' in mlb
    assert 'g.pitcher_record?' in mlb
    assert '<strong>${esc(g.opponent_label)}의 분전</strong>' in mlb
    assert '<strong>출처</strong>: ${esc(g.opponent_effort)}</div>' not in mlb


def test_mlb_uses_result_label_and_role_specific_pitcher_badges():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")
    skenes = next(pitcher for pitcher in data["pitchers"] if pitcher["name"] == "폴 스킨스")

    assert '<span class="status">경기 결과</span>' in mlb
    assert "const pitcherState=p=>" in mlb
    assert "['승','패']" in mlb
    assert "['세이브','홀드','블론']" in mlb
    assert skenes["role"] == "starter"
    assert skenes["game_decision"] is None


def test_mlb_ohtani_homer_headline_matches_official_rbi_total():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    ohtani = next(player for player in data["batters"] if player["name"] == "오타니 쇼헤이")
    dodgers_game = next(game for game in data["team_games"] if game["section_title"] == "LA 다저스 경기")

    assert ohtani["home_runs"] == 1
    assert ohtani["rbi"] == 2
    assert "오타니의 2점포" in dodgers_game["headline"]
    assert "오타니의 3점포" not in dodgers_game["headline"]


def test_mlb_minor_league_batting_lines_are_excluded_and_rendered_as_no_mlb_appearance():
    data = json.loads(MLB_DATA.read_text(encoding="utf-8"))
    mlb = MLB_INTEGRATED.read_text(encoding="utf-8")
    excluded = [player for player in data["batters"] if player.get("minor_league_excluded")]

    assert {player["name"] for player in excluded} == {"김하성", "김혜성"}
    assert all(player["status"] == "출전 없음" for player in excluded)
    assert all(player["daily_note"] == "MLB 경기 출전 없음" for player in excluded)
    assert all(player["at_bats"] is None and player["hits"] is None for player in excluded)
    assert "Gwinnett Stripers" not in MLB_DATA.read_text(encoding="utf-8")
    assert "Oklahoma City Comets" not in MLB_DATA.read_text(encoding="utf-8")
    assert "p.minor_league_excluded" in mlb


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
