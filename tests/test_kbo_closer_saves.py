import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYER_DATA = ROOT / "kbo-players" / "data.json"
GAME_DATA = ROOT / "kbo" / "data.json"
INTEGRATED = ROOT / "kbo" / "index.html"
PLAYER_PAGE = ROOT / "kbo-players" / "index.html"


def test_kbo_report_excludes_canceled_games_from_data_and_display():
    games = json.loads(GAME_DATA.read_text(encoding="utf-8"))["games"]
    page = INTEGRATED.read_text(encoding="utf-8")

    assert len(games) == 3
    assert all(game["status"] == "경기 종료" for game in games)
    assert "경기 취소" not in GAME_DATA.read_text(encoding="utf-8")
    assert "const finalGames=gdata.games.filter(g=>g.status==='경기 종료');" in page
    assert "#metric-games').textContent=finalGames.length" in page
    assert "#metric-runs').textContent=finalGames.reduce" in page


def test_inactive_pitchers_have_status_only_and_active_closers_have_compact_season_line():
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
    assert "p.season_saves!==undefined?` · 시즌" not in integrated
    assert "p.season_saves!==undefined?` · 시즌" not in player_page

    assert "class=\"season-record\"" in integrated
    assert "${p.season_record} · ${p.season_saves}세이브" in integrated
    assert "<span>시즌 성적</span>" in integrated
    assert "strong.season-record{font-size:17px" in integrated
    assert "strong.season-record.compact{font-size:13px" in integrated
    assert "el.scrollWidth>el.clientWidth" in integrated
    assert "addEventListener?.('resize',fitSeasonRecords)" in integrated
    assert "${p.season_record} · ${p.season_saves}세이브" in player_page
    assert "'시즌 성적','season-record'" in player_page
    assert ".stat b.season-record{font-size:inherit" in player_page
    assert ".stat b.season-record.compact{font-size:13px" in player_page
