import importlib.util
import io
import json
import re
import sys
from pathlib import Path
from urllib.error import URLError
from unittest.mock import patch

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
        ("Alec Burleson", "알렉 벌레슨"),
        ("Blake Snell", "블레이크 스넬"),
        ("Blake Treinen", "블레이크 트라이넨"),
        ("Edwin Díaz", "에드윈 디아스"),
        ("Tristan Beck", "트리스탄 벡"),
        ("Zebby Matthews", "제비 매튜스"),
        ("Brooks Lee", "브룩스 리"),
        ("Bo Bichette", "보 비셋"),
        ("Bobby Miller", "바비 밀러"),
        ("Brandon Williamson", "브랜든 윌리엄슨"),
        ("Emmet Sheehan", "에밋 시한"),
        ("George Soriano", "조지 소리아노"),
        ("Harry Ford", "해리 포드"),
        ("Jonathan Pintaro", "조너선 핀타로"),
        ("Nate Lavender", "네이트 라벤더"),
        ("Tobias Myers", "토바이어스 마이어스"),
        ("Will Dion", "윌 디온"),
        ("Will Smith", "윌 스미스"),
        ("Brandon Eisert", "브랜든 아이서트"),
        ("Jared Triolo", "재러드 트리올로"),
        ("Joshua Báez", "조슈아 바에스"),
        ("Khristian Curtis", "크리스천 커티스"),
        ("Luke Weaver", "루크 위버"),
        ("Juan Soto", "후안 소토"),
        ("Tomoyuki Sugano", "스가노 도모유키"),
        ("Mookie Betts", "무키 베츠"),
        ("Max Muncy", "맥스 먼시"),
        ("Yohan Ramírez", "요한 라미레스"),
        ("Andrew Knizner", "앤드루 니즈너"),
        ("Shohei Ohtani", "오타니 쇼헤이"),
        ("Evan Phillips", "에번 필립스"),
        ("Bryce Eldridge", "브라이스 엘드리지"),
        ("Jo Adell", "조 아델"),
        ("Framber Valdez", "프램버 발데스"),
        ("Seth Halvorsen", "세스 할보르센"),
        ("Luis Gastelum", "루이스 가스텔럼"),
        ("Michael McGreevy", "마이클 맥그리비"),
        ("Ramón Urías", "라몬 우리아스"),
        ("Ryan Fernandez", "라이언 페르난데스"),
        ("Thomas Saggese", "토머스 사제시"),
        ("Camilo Doval", "카밀로 도발"),
        ("Mason Montgomery", "메이슨 몽고메리"),
        ("Rafael Flores Jr.", "라파엘 플로레스 주니어"),
        ("Gordon Graceffo", "고든 그라세포"),
        ("Justin Bruihl", "저스틴 브루일"),
        ("Riley O'Brien", "라일리 오브라이언"),
        ("Ryne Stanek", "라인 스타넥"),
        ("Spencer Horwitz", "스펜서 호위츠"),
        ("Jackson Kent", "잭슨 켄트"),
        ("James Wood", "제임스 우드"),
        ("Kodai Senga", "센가 고다이"),
        ("Mark Vientos", "마크 비엔토스"),
        ("Nolan McLean", "놀런 맥린"),
        ("Robert Stock", "로버트 스톡"),
        ("Ryan Gusto", "라이언 구스토"),
        ("Agustín Ramírez", "아구스틴 라미레스"),
        ("Robbie Ray", "로비 레이"),
        ("Mason Miller", "메이슨 밀러"),
        ("Dustin Harris", "더스틴 해리스"),
        ("Yuki Matsui", "마쓰이 유키"),
        ("Adrian Morejon", "아드리안 모레혼"),
        ("Bradgley Rodriguez", "브래들리 로드리게스"),
        ("Freddy Fermin", "프레디 페르민"),
    ],
)
def test_known_rendered_mlb_names_are_localized(english: str, korean: str):
    assert UPDATE_MLB.ko_person(english) == korean


def test_mlb_api_retries_a_transient_timeout(monkeypatch):
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

    with patch.object(UPDATE_MLB.urllib.request, "urlopen", side_effect=[URLError("timeout"), Response(b'{"ok": true}')]) as request:
        monkeypatch.setattr(UPDATE_MLB.time, "sleep", lambda _seconds: None)
        assert UPDATE_MLB.get("https://example.test") == {"ok": True}
        assert request.call_count == 2


def test_juan_soto_is_batter_watchlist_before_song_seong_mun():
    assert ("후안 소토", 665742, "batter") in UPDATE_MLB.PLAYER_SPECS
    batter_names = [name for name, _pid, role in UPDATE_MLB.PLAYER_SPECS if role == "batter"]
    assert batter_names.index("후안 소토") == batter_names.index("송성문") - 1


def test_unknown_person_name_uses_korean_reading_fallback_and_records_provenance():
    unknown = "Nova Quell"
    UPDATE_MLB.FALLBACK_PLAYER_KO.pop(unknown, None)

    rendered = UPDATE_MLB.ko_person(unknown)

    assert rendered
    assert re.fullmatch(r"[가-힣 ]+", rendered)
    assert UPDATE_MLB.FALLBACK_PLAYER_KO[unknown] == rendered


def test_unknown_team_name_fails_generation_instead_of_leaking_english():
    with pytest.raises(ValueError, match="Missing Korean team-name mapping"):
        UPDATE_MLB.ko_team("Unmapped Club")


def test_washington_nationals_team_name_is_localized():
    assert UPDATE_MLB.ko_team("Washington Nationals") == "워싱턴"


def test_miami_marlins_team_name_is_localized():
    assert UPDATE_MLB.ko_team("Miami Marlins") == "마이애미"


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
