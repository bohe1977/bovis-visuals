import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kbo-players" / "data.json"
INDEX = ROOT / "kbo-players" / "index.html"


def test_closer_season_saves_are_present_and_rendered():
    pitchers = json.loads(DATA.read_text(encoding="utf-8"))["pitchers"]
    by_name = {pitcher["name"]: pitcher for pitcher in pitchers}

    assert isinstance(by_name["김원중"]["season_saves"], int)
    assert by_name["김원중"]["season_saves"] == 4
    assert isinstance(by_name["박영현"]["season_saves"], int)
    assert by_name["박영현"]["season_saves"] == 18
    for name in ("김원중", "박영현"):
        assert by_name[name]["season_record"]
        assert by_name[name]["era"]
    player_page = INDEX.read_text(encoding="utf-8")
    integrated_page = (ROOT / "kbo" / "index.html").read_text(encoding="utf-8")
    assert "season_saves" in player_page
    assert "시즌 ${p.season_saves}세이브" in player_page
    assert "시즌 ${p.season_saves}세이브" in integrated_page
