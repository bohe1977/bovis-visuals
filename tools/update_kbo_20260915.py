#!/usr/bin/env python3
"""Build the reconciled 2026-09-15 KBO final-game report from captured records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-15", "20260915"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260915HTSK0": 80108768, "20260915KTHH0": 80108769, "20260915LGNC0": 80108770, "20260915LTSS0": 80108771}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(gid: str) -> list[dict]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "18:30", "status": "경기 종료", "away": away, "home": home, "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}


games = [
    game("20260915LTSS0", "대구", "롯데", "삼성", 3, 7, "사토시", "박정민", None,
         "삼성이 8회 5득점으로 롯데에 7-3 역전승", [
             "삼성 선발 원태인은 5⅔이닝 4피안타 2실점 4탈삼진으로 버텼고, 사토시가 8회 1이닝 무실점으로 승리를 기록했다.",
             "승부처는 3-2로 뒤진 8회였다. 삼성은 이 이닝에 5점을 뽑아 역전에 성공했다.",
             "디아즈는 4타수 3안타 2타점 1득점 1볼넷, 류지혁은 5타수 3안타 2타점 1득점을 기록했다.",
             "장찬희·이승민이 중간을 잇고 사토시가 승리, 김재윤이 9회 무실점으로 마무리했다."],
         "롯데는 나승엽이 4타수 3안타 2타점, 레이예스가 5타수 3안타 1타점으로 분전했고 7회 3-2 리드까지 만들었지만 8회 대량 실점을 막지 못했다."),
    game("20260915HTSK0", "문학", "KIA", "SSG", 3, 6, "김민준", "김태형", "문승원",
         "SSG가 5회 5득점 빅이닝으로 KIA에 6-3 승리", [
             "SSG 선발 김민준은 6이닝 5피안타 3실점 8탈삼진으로 승리를 기록했다.",
             "승부처는 1-3으로 뒤진 5회 5득점이었다. 이 빅이닝으로 SSG가 역전에 성공했다.",
             "고명준은 4타수 3안타 1홈런 3타점 1득점, 에레디아는 4타수 1안타 2타점을 기록했다.",
             "김민·전영준이 각각 1이닝 무실점 홀드, 문승원이 9회 무실점 세이브로 리드를 지켰다."],
         "KIA는 카스트로가 5타수 3안타 1타점, 김선빈이 3타수 2안타 1볼넷으로 분전했지만 5회 역전을 허용한 뒤 추가 득점을 만들지 못했다."),
    game("20260915LGNC0", "창원", "LG", "NC", 3, 2, "카라스코", "송명기", "손주영",
         "LG가 8회 결승 득점으로 NC에 3-2 승리", [
             "LG 선발 카라스코는 5⅔이닝 2피안타 무실점 4탈삼진으로 승리를 기록했다.",
             "승부처는 8회였다. 1-0에서 LG가 1점을 보탠 뒤 NC가 2점을 추격했지만, LG가 8회 추가 1점으로 결승점을 만들었다.",
             "박해민은 3타수 2안타 1타점 1득점 1볼넷, 송찬의는 3타수 1안타 1홈런 1타점 1득점을 기록했다.",
             "고우석이 1⅓이닝 무실점 홀드, 손주영이 1⅔이닝 무실점 세이브로 마무리했다."],
         "NC는 블레인이 3타수 1안타 1홈런 2타점 1득점, 천재환과 김형준이 나란히 2안타를 기록했지만 8회 추격 뒤 동점을 만들지 못했다."),
    game("20260915KTHH0", "대전", "KT", "한화", 13, 3, "고영표", "왕옌청", None,
         "KT가 3회부터 달아나며 한화에 13-3 승리", [
             "KT 선발 고영표는 6이닝 4피안타 무실점 8탈삼진으로 승리를 기록했다.",
             "KT는 2-0으로 앞선 3회 3득점, 5·6회에도 각각 2·4점을 더해 흐름을 완전히 가져왔다.",
             "허경민은 3타수 3안타 1홈런 4타점 2득점 1볼넷, 힐리어드는 4타수 2안타 2홈런 3타점 2득점을 기록했다.",
             "김정운·문용익이 7·8회를 무실점으로 막아 고영표의 승리를 뒷받침했다."],
         "한화는 강백호가 4타수 1안타 1홈런 2타점 1득점, 한지윤이 홈런으로 1타점을 보탰지만 초반 격차를 좁히지 못했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "innings": "5⅔", "hits": 4, "runs": 2, "earned_runs": 2, "walks_hbp": 2, "strikeouts": 4, "home_runs": 0, "pitches": 106, "season_record": "7승 7패", "era": "4.16", "role": "starter", "game_decision": None},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": True, "innings": "6", "hits": 8, "runs": 2, "earned_runs": 2, "walks_hbp": 4, "strikeouts": 2, "home_runs": 0, "pitches": 116, "season_record": "3승 9패", "era": "4.92", "role": "starter", "game_decision": None},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 2, "home_runs": 0, "pitches": 23, "season_record": "1승 5패", "season_saves": 5, "era": "4.79", "role": "reliever", "game_decision": "홀드"},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "⅔", "hits": 2, "runs": 4, "earned_runs": 4, "walks_hbp": 2, "strikeouts": 1, "home_runs": 0, "pitches": 30, "season_record": "6승 4패", "era": "4.47", "role": "reliever", "game_decision": None},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "innings": "0", "hits": 1, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0, "pitches": 4, "season_record": "2승 1패", "season_saves": 2, "era": "6.38", "role": "reliever", "game_decision": None},
    {"name": "박영현", "team": "KT", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 1, "avg": "0.286", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": False},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 40


def official_rows(game_id: str, category: str) -> list[dict]:
    document = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8-sig"))
    assert document["code"] == "100"
    rows = []
    for team in document[category]:
        table = json.loads(team["table"])
        headers = [cell["Text"] for cell in table["headers"][0]["row"]]
        rows.extend(dict(zip(headers, [cell["Text"] for cell in row["row"]])) for row in table["rows"])
    return rows

for g in games:
    gid = g["id"]
    board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    assert board["AWAY_NM"] == g["away"] and board["HOME_NM"] == g["home"]
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
    official_pitchers = official_rows(gid, "arrPitcher")
    naver_pitchers = [x for side in ("away", "home") for x in naver["pitchersBoxscore"][side]]
    for p in pitchers:
        if p["team"] in (g["away"], g["home"]) and not p["appeared"]:
            assert p["name"] not in {x["선수명"] for x in official_pitchers}
            assert p["name"] not in {x["name"] for x in naver_pitchers}
for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}

lt_pitchers = {x["선수명"]: x for x in official_rows("20260915LTSS0", "arrPitcher")}
ht_pitchers = {x["선수명"]: x for x in official_rows("20260915HTSK0", "arrPitcher")}
assert (lt_pitchers["원태인"]["등판"], lt_pitchers["원태인"]["이닝"], lt_pitchers["원태인"]["평균자책점"]) == ("선발", "5 2/3", "4.16")
assert (lt_pitchers["박세웅"]["등판"], lt_pitchers["박세웅"]["이닝"], lt_pitchers["박세웅"]["평균자책점"]) == ("선발", "6", "4.92")
assert (lt_pitchers["김원중"]["결과"], lt_pitchers["김원중"]["세"]) == ("홀드", "5")
assert lt_pitchers["박정민"]["결과"] == "패"
assert (ht_pitchers["정해영"]["등판"], ht_pitchers["정해영"]["이닝"], ht_pitchers["정해영"]["세"]) == ("5.3", "0", "2")

hh_naver = json.loads((ART / "naver-20260915KTHH0.json").read_text(encoding="utf-8"))["result"]["recordData"]
hh_hitters = {x["name"]: x for side in ("away", "home") for x in hh_naver["battersBoxscore"][side]}
assert (hh_hitters["강백호"]["ab"], hh_hitters["강백호"]["hit"], hh_hitters["강백호"]["rbi"], hh_hitters["강백호"]["hr"], hh_hitters["강백호"]["hra"]) == (4, 1, 2, 1, "0.286")
assert "노시환" not in hh_hitters
kia_naver = json.loads((ART / "naver-20260915HTSK0.json").read_text(encoding="utf-8"))["result"]["recordData"]
kia_hitters = {x["name"] for side in ("away", "home") for x in kia_naver["battersBoxscore"][side]}
assert "김도영" not in kia_hitters

source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-09-15 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 40득점이다. 원태인·박세웅·김원중·박정민·정해영의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 원태인·박세웅은 공식 선발 행, 김원중·박정민·정해영은 공식 구원 행으로 확인했다. 김원중의 공식 홀드만 구원 결정 배지로 기록했으며, 구원 박정민의 공식 패전은 계약에 따라 game_decision을 null로 보존했다. 김원중(5)·정해영(2)의 시즌 세이브는 공식·네이버 기록으로 확인했다. 나머지 관심 투수는 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 name·team·appeared만 보존했다. 강백호의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했고, 노시환·김도영은 해당 팀의 전체 타자 명단에 없어 출전 없음으로 기록했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts": []}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.15", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 15일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
