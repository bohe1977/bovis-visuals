import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("update_mlb", TOOLS / "update_mlb.py")
UPDATE_MLB = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(UPDATE_MLB)


@pytest.mark.parametrize(
    ("english", "korean"),
    [
        ("Blake Snell", "블레이크 스넬"),
        ("Tomoyuki Sugano", "스가노 도모유키"),
        ("Mookie Betts", "무키 베츠"),
        ("Shohei Ohtani", "오타니 쇼헤이"),
        ("Evan Phillips", "에번 필립스"),
        ("Bryce Eldridge", "브라이스 엘드리지"),
        ("Jo Adell", "조 아델"),
    ],
)
def test_known_rendered_mlb_names_are_localized(english: str, korean: str):
    assert UPDATE_MLB.ko_person(english) == korean


def test_unknown_person_name_fails_generation_instead_of_leaking_english():
    with pytest.raises(ValueError, match="Missing Korean player-name mapping"):
        UPDATE_MLB.ko_person("Unmapped Player")


def test_20260818_archive_has_no_english_player_names_in_user_copy():
    data = json.loads((ROOT / "mlb" / "2026-08-18" / "data.json").read_text(encoding="utf-8"))
    player_copy = []
    for game in data["team_games"]:
        player_copy.extend(
            value
            for value in [
                game.get("winner_pitcher"),
                game.get("loser_pitcher"),
                game.get("save_pitcher"),
                game.get("pitcher_record"),
                game.get("headline"),
                game.get("opponent_effort"),
                *game.get("game_points", []),
            ]
            if value
        )
    latin_name = re.compile(r"\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)+\b")
    assert not [text for text in player_copy if latin_name.search(text)]
