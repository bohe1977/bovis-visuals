#!/usr/bin/env python3
"""Write the reconciled 2026-08-30 KBO report from captured official/Naver/Daum records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / ".artifacts" / "kbo-2026-08-30"
DATE, COMPACT = "2026-08-30", "20260830"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260830&toDate=20260830"
DAUM_IDS = {"20260830NCHH0": 80101159, "20260830WOOB0": 80101161}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


def game(game_id, stadium, away, home, away_score, home_score, winner, loser, headline, points, effort):
    return {
        "id": game_id, "stadium": stadium, "start_time": "18:00", "status": "경기 종료",
        "away": away, "home": home, "away_score": away_score, "home_score": home_score,
        "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": None,
        "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(game_id),
    }


# Only final games enter this array. KT-삼성, LG-롯데, SSG-KIA were cancelled and are deliberately absent.
games = [
    game("20260830WOOB0", "잠실", "키움", "두산", 1, 15, "최민석", "전준표",
         "두산이 1회 6득점과 홈런 3방으로 키움에 15-1 대승",
         [
             "두산 선발 최민석은 6이닝 6피안타 1사사구 5탈삼진 1실점으로 승리투수가 됐다.",
             "두산은 1회 6득점으로 먼저 달아난 뒤 4·5·6·8회에도 득점해 격차를 벌렸다.",
             "안재석은 3타수 2안타 1홈런 2타점 3득점, 세베리노는 3타수 2안타 1홈런 3타점, 오명진은 대타 홈런으로 3타점을 기록했다.",
             "박치국·윤태호·박신지가 7~9회를 합계 3이닝 무실점으로 막았다.",
         ],
         "키움은 데이비슨의 6회 솔로 홈런과 이형종의 2안타로 영봉패를 면했다."),
    game("20260830NCHH0", "대전", "NC", "한화", 10, 7, "전사민", "김서현",
         "NC가 연장 10회 3득점으로 한화를 10-7로 제압",
         [
             "NC 선발 테일러는 5이닝 6피안타 3사사구 5탈삼진 5실점, 한화 선발 황준서는 3이닝 7피안타 1사사구 2탈삼진 4실점을 기록했다.",
             "7-7로 맞선 연장 10회 NC가 3득점하며 승부를 갈랐고, 전사민이 1⅓이닝 무실점으로 승리투수가 됐다.",
             "천재환은 5타수 2안타 4타점, 박건우는 5타수 2안타 1홈런 1타점, 블레인은 홈런 포함 2타점을 기록했다.",
             "NC 불펜은 신영우·이용준·배재환·손주환·전사민이 5이닝 무실점으로 이어 던졌다.",
         ],
         "한화는 강백호가 3타수 1안타 1홈런 2타점 1득점, 노시환이 5타수 1안타 2타점으로 추격을 이끌었다."),
]

# Strict inactive-pitcher contract: no season or explanatory fields are permitted.
pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 3, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 1, "walks": 2, "strikeouts": 1, "avg": "0.289", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 0, "avg": "0.277", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": False},
]


def official_pitchers(game_id: str) -> dict[str, list[str]]:
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8-sig"))
    assert doc["code"] == "100"
    rows = {}
    for team in doc["arrPitcher"]:
        for record in json.loads(team["table"])["rows"]:
            values = [cell["Text"] for cell in record["row"]]
            rows[values[0]] = values
    return rows


# Cross-check final state, score and all requested individual player rows.
naver_records = {}
official_rows = {}
for entry in games:
    gid = entry["id"]
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    naver_records[gid] = naver
    assert naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == entry["away_score"]
    assert int(rheb["home"]["r"]) == entry["home_score"]
    official_rows[gid] = official_pitchers(gid)

# Official KBO row is the baseline for the starter/decision and Naver confirms the same row and season AVG.
assert official_rows["20260830WOOB0"]["최민석"][1:3] == ["선발", "승"]
assert official_rows["20260830WOOB0"]["전준표"][1:3] == ["선발", "패"]
assert official_rows["20260830NCHH0"]["전사민"][2] == "승"
naver_han = naver_records["20260830NCHH0"]["battersBoxscore"]["home"]
by_name = {row["name"]: row for row in naver_han}
for name, expected in {"강백호": (3, 1, 2, 1, 1, 2, 1, "0.289"), "노시환": (5, 1, 2, 1, 0, 0, 0, "0.277")}.items():
    row = by_name[name]
    assert (row["ab"], row["hit"], row["rbi"], row["run"], row["hr"], row["bb"], row["kk"], row["hra"]) == expected
for pitcher in pitchers:
    assert set(pitcher) == {"name", "team", "appeared"} and pitcher["appeared"] is False

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [item["sources"][0]["url"] for item in games],
    "naver": [f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record" for gid in ["20260830WOOB0", "20260830KTSS0", "20260830LGLT0", "20260830SKHT0", "20260830NCHH0"]],
    "daum": [DAUM_SCHEDULE] + [item["sources"][2]["url"] for item in games],
}
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-30 KST 편성 5경기를 대조했다. 키움-두산과 NC-한화는 kbo-game FINISHED, KBO 공식 게임센터 상세기록 API(code=100), 네이버 공개 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료를 확인해 games 배열에 넣었다. KT-삼성·LG-롯데·SSG-KIA는 kbo-game CANCELED 및 다음 일정 API periodType/gameStatus=CANCEL로 확인해 모든 카드·스코어·승부처·경기 수·총득점에서 제외했다. 종료 2경기 합계 33득점이다. 관심 투수 11명은 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없거나 팀 경기가 취소돼 name·team·appeared만 보존했다. 강백호와 노시환은 KBO 공식 타자표 및 네이버 행에서 당일 타격 라인·시즌 타율을 대조했고, 김도영은 KIA 경기 취소로 출전 없음이다. 다음은 타자의 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

assert len(games) == 2 and all(item["status"] == "경기 종료" for item in games)
assert sum(item["away_score"] + item["home_score"] for item in games) == 33
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8").replace("2026-08-29", DATE).replace("2026.08.29", "2026.08.30").replace("2026년 8월 29일", "2026년 8월 30일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
