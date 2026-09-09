#!/usr/bin/env python3
"""Build the reconciled 2026-09-09 KBO final-game report from captured records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-09", "20260909"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260909KTSS0": 80108750, "20260909LGHH0": 80108751, "20260909NCHT0": 80108752, "20260909SKOB0": 80108753}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(gid: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "18:30", "status": "경기 종료", "away": away, "home": home,
            "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser,
            "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}


# Narratives are restricted to official REVIEW result rows and reconciled Naver box-score rows.
games = [
    game("20260909SKOB0", "잠실", "SSG", "두산", 1, 0, "이로운", "곽빈", "조병현",
         "SSG가 박성한의 3회 결승 적시타와 이로운의 호투로 두산에 1-0 승리",
         ["SSG 선발 이로운은 6⅔이닝 2피안타 무실점 9탈삼진으로 승리를 기록했다.",
          "3회 2사 2루에서 박성한의 우전 안타가 결승타가 됐다.",
          "박성한은 3타수 2안타 1타점, 에레디아·김재환도 각각 안타를 기록했다.",
          "김민·전영준이 홀드를 이어갔고 조병현이 1이닝 무실점으로 시즌 19세이브를 올렸다."],
         "두산은 곽빈이 7이닝 5피안타 1실점 9탈삼진으로 버텼고 김재환·정수빈이 안타를 쳤지만 득점하지 못했다."),
    game("20260909KTSS0", "대구", "KT", "삼성", 2, 0, "고영표", "원태인", "박영현",
         "KT가 김현수의 6회 결승 2점포와 고영표의 무실점 호투로 삼성에 2-0 승리",
         ["KT 선발 고영표는 6이닝 5피안타 무실점 7탈삼진으로 승리를 기록했다.",
          "6회 2사 1루에서 김현수의 우월 2점 홈런이 결승타가 됐다.",
          "김현수는 4타수 1안타 1홈런 2타점, 안현민은 4타수 3안타를 기록했다.",
          "손동현이 홀드, 박영현이 1이닝 무실점 3탈삼진으로 시즌 26세이브를 올렸다."],
         "삼성은 원태인이 6이닝 5피안타 2실점 3탈삼진으로 버텼고 최형우가 4타수 2안타를 기록했지만 영봉패를 당했다."),
    game("20260909NCHT0", "광주", "NC", "KIA", 5, 4, "송명기", "황동하", "류진욱",
         "NC가 블레인의 멀티 홈런을 앞세워 KIA에 5-4 승리",
         ["NC 선발 송명기는 5이닝 2피안타 1실점 7탈삼진으로 승리를 기록했다.",
          "2회 무사에서 블레인의 좌월 홈런이 결승타가 됐다.",
          "블레인은 4타수 2안타 2홈런 3타점 2득점, 김주원은 3타수 1안타 1홈런 2타점을 기록했다.",
          "신영우·김진호·손주환·전사민이 홀드를 이어갔고 류진욱이 ⅓이닝 무실점으로 시즌 4세이브를 올렸다."],
         "KIA는 하주석이 4타수 2안타 2홈런 2타점 2득점으로 추격했고 9회에도 1점을 냈지만 동점에는 닿지 못했다."),
    game("20260909LGHH0", "대전", "LG", "한화", 3, 19, "왕옌청", "카라스코", None,
         "한화가 허인서의 4회 결승타와 한지윤의 만루포로 LG에 19-3 대승",
         ["한화 선발 왕옌청은 6이닝 7피안타 1실점 1탈삼진으로 승리를 기록했다.",
          "4회 무사 만루에서 허인서의 좌전 안타가 결승타가 됐다.",
          "허인서는 5타수 3안타 4타점, 한지윤은 8회 만루 홈런으로 1타수 1안타 4타점, 문현빈은 3타수 2안타 3득점을 기록했다.",
          "한화는 8회 한지윤의 만루포를 포함해 10득점하며 승부를 갈랐다."],
         "LG는 박해민과 오스틴이 각각 4타수 2안타, 홍창기가 2타수 1안타 2타점으로 분전했지만 마운드가 19실점했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "innings": "6", "hits": 5, "runs": 2, "earned_runs": 2, "walks_hbp": 1, "strikeouts": 3, "home_runs": 1, "pitches": 108, "season_record": "7승 7패", "era": "4.20", "role": "starter", "game_decision": "패"},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 1, "home_runs": 0, "pitches": 20, "season_record": "2승 1패", "season_saves": 2, "era": "5.93", "role": "reliever", "game_decision": None},
    {"name": "박영현", "team": "KT", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 3, "home_runs": 0, "pitches": 16, "season_record": "6승 0패", "season_saves": 26, "era": "2.63", "role": "reliever", "game_decision": "세이브"},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 3, "hits": 1, "rbi": 0, "runs": 2, "home_runs": 0, "walks": 2, "strikeouts": 0, "avg": "0.289", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 4, "hits": 2, "rbi": 1, "runs": 1, "home_runs": 0, "walks": 1, "strikeouts": 0, "avg": "0.282", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 1, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 0, "avg": "0.306", "obp": None, "ops": None},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
final_ids = {g["id"] for g in games}
assert final_ids == {g["id"] for g in kbo_game if g["status"] == "FINISHED"}
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 34
for g in games:
    gid = g["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    score = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert official["code"] == "100" and score["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}

source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-09-09 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW의 GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료와 스코어를 대조했다. 종료 4경기 합계는 34득점이다. 실제 등판 관심 투수의 당일 라인·시즌 성적·ERA·세이브는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 선발/구원 및 당일 결정은 KBO 공식 결과 행과 네이버 pitchingResult를 대조했다. 비등판 투수는 해당 팀 완료 경기의 KBO 공식·네이버 전체 투수 명단 부재를 확인해 계약상 name·team·appeared만 보존했다. 관심 타자의 당일 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts": []}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.09", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 9일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
