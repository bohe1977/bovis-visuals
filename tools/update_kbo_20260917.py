#!/usr/bin/env python3
"""Build the reconciled 2026-09-17 KBO final-game report from captured records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-17", "20260917"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260917SKNC0": 80108776, "20260917WOHT0": 80108777}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(gid: str) -> list[dict]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {
        "id": gid, "stadium": stadium, "start_time": "18:30", "status": "경기 종료",
        "away": away, "home": home, "away_score": away_score, "home_score": home_score,
        "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save,
        "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid),
    }


games = [
    game("20260917WOHT0", "광주", "키움", "KIA", 0, 2, "곽도규", "박준현", "이의리",
         "KIA가 7회 한준수의 결승 2루타로 키움에 2-0 승리", [
             "KIA 선발 올러는 6이닝 3피안타 3사사구 5탈삼진 무실점으로 호투했고, 곽도규가 ⅔이닝 무실점으로 승리를 기록했다.",
             "승부처는 7회 2사 1루였다. 한준수가 우익수 방면 2루타를 쳐 공식 결승타를 기록했고, KIA가 그 이닝 2점을 냈다.",
             "한준수는 4타수 2안타 1타점, 카스트로는 4타수 3안타 1타점, 나성범은 3타수 2안타 1볼넷을 기록했다.",
             "조상우가 ⅔이닝 무실점 홀드, 이의리가 9회 1이닝 무실점 3탈삼진 세이브로 마무리했다."],
         "키움은 안우진이 6이닝 5피안타 3사사구 4탈삼진 무실점으로 버텼고 서건창이 4타수 2안타를 기록했지만, 7회 2사 뒤 실점한 뒤 타선이 끝내 득점하지 못했다."),
    game("20260917SKNC0", "창원", "SSG", "NC", 2, 1, "이로운", "손주환", "전영준",
         "SSG가 8회 박성한의 결승타로 NC에 2-1 승리", [
             "SSG 선발 이로운은 7이닝 6피안타 무사사구 5탈삼진 1실점으로 승리를 기록했다.",
             "1-1이던 8회 2사 2루에서 박성한의 우전 안타가 공식 결승타가 됐다.",
             "고명준은 5회 라일리에게 시즌 11호 솔로 홈런을 쳤고, 박성한은 4타수 1안타 1타점으로 결승타를 만들었다.",
             "김민이 8회 1이닝 무실점 홀드, 전영준이 9회 1이닝 무실점 세이브를 기록했다."],
         "NC는 라일리가 7이닝 2피안타 2사사구 8탈삼진 1실점으로 호투했고 박건우가 4타수 2안타 1득점, 김형준이 3타수 2안타로 분전했지만 8회 결승점을 내줬다."),
]

# The approved watchlist is preserved. All teams with games were checked against complete
# official and Naver pitcher/hitter lists; no watchlist player appeared.
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
    {"name": "강백호", "team": "한화", "appeared": False},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": False},
]


def official_rows(game_id: str, category: str) -> list[dict]:
    document = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8-sig"))
    assert document["code"] == "100"
    rows = []
    for team in document[category]:
        table = json.loads(team["table"])
        headers = [cell["Text"] for cell in table["headers"][0]["row"]]
        rows.extend(dict(zip(headers, [cell["Text"] for cell in row["row"]])) for row in table["rows"])
    return rows


def official_hitter_names(game_id: str) -> set[str]:
    document = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8-sig"))
    assert document["code"] == "100"
    return {
        row["row"][2]["Text"]
        for team in document["arrHitter"]
        for row in json.loads(team["table1"])["rows"]
        if len(row["row"]) >= 3
    }


kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 5

for g in games:
    gid = g["id"]
    board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    assert (board["AWAY_NM"], board["HOME_NM"]) == (g["away"], g["home"])
    rheb = naver["scoreBoard"]["rheb"]
    assert (int(rheb["away"]["r"]), int(rheb["home"]["r"])) == (g["away_score"], g["home_score"])
    official_pitchers = {x["선수명"] for x in official_rows(gid, "arrPitcher")}
    naver_pitchers = {x["name"] for side in ("away", "home") for x in naver["pitchersBoxscore"][side]}
    official_hitters = official_hitter_names(gid)
    naver_hitters = {x["name"] for side in ("away", "home") for x in naver["battersBoxscore"][side]}
    for p in pitchers:
        if p["team"] in (g["away"], g["home"]):
            assert not p["appeared"] and p["name"] not in official_pitchers | naver_pitchers
    for b in batters:
        if b["team"] in (g["away"], g["home"]):
            assert not b["appeared"] and b["name"] not in official_hitters | naver_hitters

for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-09-17 KST 편성 2경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 2경기 합계는 5득점이다. 관심 투수 가운데 KIA 정해영은 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 name·team·appeared만 보존했다. 나머지 관심 투수의 팀은 해당 날짜에 경기하지 않아 동일 계약 객체만 보존했다. 김도영은 KIA의 KBO 공식·네이버 전체 타자 명단에 없어 출전 없음으로 기록했으며, 강백호·노시환의 팀은 해당 날짜에 경기하지 않았다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.17", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 17일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
