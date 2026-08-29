#!/usr/bin/env python3
"""Write the reconciled 2026-08-29 KBO report from captured official/Naver/Daum records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / ".artifacts" / "kbo-2026-08-29"
DATE, COMPACT = "2026-08-29", "20260829"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260829&toDate=20260829"
DAUM_IDS = {"20260829KTSS0": 80101152, "20260829LGLT0": 80101153, "20260829NCHH0": 80101154, "20260829SKHT0": 80101155, "20260829WOOB0": 80101156}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


def game(game_id, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": game_id, "stadium": stadium, "start_time": "18:00", "status": "경기 종료", "away": away, "home": home, "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(game_id)}


games = [
    game("20260829WOOB0", "잠실", "키움", "두산", 2, 7, "곽빈", "안우진", None,
         "두산이 안재석의 멀티 홈런과 곽빈의 6이닝으로 키움에 7-2 승리",
         ["두산 선발 곽빈은 6이닝 5피안타 3사사구 8탈삼진 2실점으로 시즌 11승째를 기록했다.", "1-2로 뒤진 5회 2사 1루에서 안재석의 우중월 투런포가 공식 결승타가 됐다.", "안재석은 4타수 3안타 2홈런 4타점, 김대한은 솔로포를 기록했다.", "타카다가 7회 1이닝 무실점 홀드, 김택연·이영하가 8~9회를 무실점으로 막았다."],
         "키움은 3회 서건창의 3루타와 추재현의 적시 2루타로 2점을 먼저 냈고, 권혁빈이 2안타로 분전했다."),
    game("20260829KTSS0", "대구", "KT", "삼성", 2, 4, "페덱", "로건", "김재윤",
         "삼성이 페덱의 6이닝 무실점과 구자욱의 1회 결승타로 KT에 4-2 승리",
         ["삼성 선발 페덱은 6이닝 6피안타 2사사구 7탈삼진 무실점으로 승리투수가 됐다.", "1회 1사 2루 구자욱의 우전 적시타가 공식 결승타가 됐고, 삼성은 1·2·4·5회에 한 점씩 보탰다.", "구자욱은 3타수 2안타 2타점, 김영웅은 4타수 2안타 1타점을 기록했다.", "김태훈·이승현이 7~8회를 무실점으로 잇고 김재윤이 9회 2실점에도 시즌 29세이브를 올렸다."],
         "KT는 9회 오윤석의 2점 홈런으로 추격했고 안현민·유준규가 나란히 2안타를 기록했다."),
    game("20260829LGLT0", "사직", "LG", "롯데", 8, 3, "카라스코", "김진욱", None,
         "LG가 5회 5득점 빅이닝으로 롯데를 8-3으로 제압",
         ["LG 선발 카라스코는 6이닝 5피안타 1사사구 4탈삼진 3실점으로 시즌 3승째를 챙겼다.", "2회 2사 만루에서 박해민의 밀어내기 볼넷이 공식 결승타가 됐고, LG는 5회 5득점으로 격차를 벌렸다.", "송찬의는 4타수 3안타 2타점, 오스틴은 5타수 2안타 2타점, 박해민은 2타점을 냈다.", "LG 불펜은 우강훈·케네디·유영찬이 7회를 무실점으로 막고 마무리했다."],
         "롯데는 한동희가 6회 솔로 홈런, 레이예스·손성빈이 각각 1타점을 올리며 추격했다."),
    game("20260829SKHT0", "광주", "SSG", "KIA", 1, 2, "조상우", "문승원", None,
         "KIA가 연장 10회 박정우의 끝내기 안타로 SSG에 2-1 승리",
         ["KIA 선발 올러는 6이닝 3피안타 1사사구 9탈삼진 1실점, SSG 선발 아빌라는 7이닝 4피안타 1사사구 6탈삼진 무실점으로 팽팽히 맞섰다.", "1-1이던 연장 10회 1사 만루에서 박정우의 중전 안타가 공식 끝내기 결승타가 됐다.", "박재현은 5타수 2안타 1타점 1득점, 김호령·나성범은 각각 2안타를 기록했다.", "KIA는 곽도규·성영탁·조상우가 연장까지 무실점으로 이어 던져 승리를 지켰다."],
         "SSG는 6회 박성한의 적시타로 먼저 앞섰고 정준재가 5타수 2안타로 분전했다."),
    game("20260829NCHH0", "대전", "NC", "한화", 11, 4, "라일리", "박준영", None,
         "NC가 김주원의 결승포와 3홈런으로 한화에 11-4 승리",
         ["NC 선발 라일리는 6이닝 2피안타 4사사구 4탈삼진 2실점으로 시즌 6승째를 거뒀다.", "3회 1사에서 김주원의 우월 솔로포가 공식 결승타가 됐고, NC는 4회 5득점으로 달아났다.", "김형준은 3타수 2안타 1홈런 4타점, 김주원은 4타수 2안타 1홈런 3타점, 김휘집도 홈런을 기록했다.", "이용준·손주환·김재열이 7~9회를 무실점으로 막았다."],
         "한화는 박정현과 유민이 각각 2점 홈런을 기록하며 4득점했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": True, "role": "starter", "game_decision": "패", "innings": "4 ⅓", "hits": 9, "runs": 7, "earned_runs": 7, "walks_hbp": 2, "strikeouts": 4, "home_runs": 0, "pitches": 88, "season_record": "6승 6패", "era": "3.75"},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "role": "reliever", "game_decision": None, "innings": "0", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 0, "home_runs": 0, "pitches": 7, "season_record": "2승 1패", "season_saves": 2, "era": "6.00"},
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.289", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.278", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 2, "strikeouts": 1, "avg": "0.303", "obp": None, "ops": None},
]

# KBO's own dynamic box-score API is the baseline. Naver's public record is the independent numeric cross-check.
def official_pitcher_rows(game_id: str) -> dict[str, list[str]]:
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8"))
    rows = {}
    for team in doc["arrPitcher"]:
        for record in json.loads(team["table"])["rows"]:
            cells = [cell["Text"] for cell in record["row"]]
            rows[cells[0]] = cells
    return rows

for g in games:
    naver = json.loads((ART / f"naver-{g['id']}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    board = naver["scoreBoard"]["rheb"]
    assert naver["gameInfo"]["statusCode"] == "4"
    assert int(board["away"]["r"]) == g["away_score"] and int(board["home"]["r"]) == g["home_score"]
    assert json.loads((ART / f"official-GetScoreBoardScroll-{g['id']}.json").read_text(encoding="utf-8"))["code"] == "100"

official_rows = {g["id"]: official_pitcher_rows(g["id"]) for g in games}
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}
        continue
    found = []
    for g in games:
        naver = json.loads((ART / f"naver-{g['id']}.json").read_text(encoding="utf-8"))["result"]["recordData"]
        for side in ("away", "home"):
            for row in naver["pitchersBoxscore"][side]:
                if row["name"] == pitcher["name"]:
                    found.append(row)
                    official = official_rows[g["id"]][pitcher["name"]]
                    # The official table labels starters as 선발; a reliever row carries its entry point (e.g. 10.8).
                    assert (official[1] == "선발") == (pitcher["role"] == "starter")
                    assert official[2].replace("&nbsp;", "") == (pitcher["game_decision"] or "")
                    assert official[6].replace(" 1/3", " ⅓") == pitcher["innings"]
                    assert int(official[10]) == pitcher["hits"] and int(official[13]) == pitcher["strikeouts"] and int(official[14]) == pitcher["runs"]
                    assert row["era"] == pitcher["era"] and row["w"] == int(pitcher["season_record"].split("승")[0])
    assert len(found) == 1

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-29 KST 5경기는 kbo-game FINISHED, KBO 공식 게임센터 동적 상세기록 API(code=100), 네이버 공개 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)를 대조해 모두 최종 종료로 확정했다. 종료 5경기 합계 44득점이다. 관심 투수 중 김진욱은 KBO 공식 선발·패 행과 네이버 행에서 4⅓이닝 9피안타 2사사구 4탈삼진 7실점·시즌 6승 6패·ERA 3.75를, 정해영은 KBO 공식 구원 행과 네이버 행에서 0이닝 1피안타 1사사구 무실점·당일 결정 없음·시즌 2승 1패 2세이브·ERA 6.00을 확인했다. 나머지 관심 투수는 각 팀 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 계약상 name·team·appeared만 보존했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록에서 대조했다. 다음은 타자의 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

assert len(games) == 5 and all(g["status"] == "경기 종료" for g in games)
assert sum(g["away_score"] + g["home_score"] for g in games) == 44
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8").replace("2026-08-28", DATE).replace("2026.08.28", "2026.08.29").replace("2026년 8월 28일", "2026년 8월 29일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
