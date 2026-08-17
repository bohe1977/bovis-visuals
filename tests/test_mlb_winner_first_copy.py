import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def game(game_pk: int) -> dict:
    data = json.loads((ROOT / "mlb" / "data.json").read_text(encoding="utf-8"))
    return next(item for item in data["team_games"] if item["game_pk"] == game_pk)


def test_mlb_current_winner_first_copy_uses_korean_names_and_no_score_margin_filler():
    dodgers = game(823912)
    giants = game(823182)

    assert dodgers["headline"] == "로건 헨더슨 7이닝 1실점, 밀워키가 LA 다저스에 6-2 승리"
    assert dodgers["winner_pitcher"] == "로건 헨더슨"
    assert dodgers["loser_pitcher"] == "타릭 스쿠발"
    assert "제이크 바우어스" in " ".join(dodgers["game_points"])
    assert "5회 밀워키 제이크 바우어스의 안타가 결승타가 됐다." in dodgers["game_points"]
    assert dodgers["game_points"][-1] == "채드 패트릭과 애런 애슈비가 1이닝 무실점으로 이어 던졌고, 각각 홀드를 기록했다."

    assert giants["headline"] == "닉 프라소 1이닝 무실점, 콜로라도가 샌프란시스코에 13-7 승리"
    assert giants["winner_pitcher"] == "닉 프라소"
    assert giants["loser_pitcher"] == "샘 헨지스"
    assert "에이다엘 아마도르" in " ".join(giants["game_points"])
    assert giants["game_points"][-1] == "파커 머신스키·지미 허겟·잭 애그노스가 4이닝 무실점으로 이어 던졌고, 파커 머신스키가 홀드를 기록했다."
    assert all("프라소은" not in point and "7.0이닝" not in point for point in dodgers["game_points"] + giants["game_points"])

    for value in (dodgers["headline"], giants["headline"], *dodgers["game_points"], *giants["game_points"]):
        assert "보다" not in value or "앞서 경기를 마무리" not in value
        assert "흐름을 주도" not in value
