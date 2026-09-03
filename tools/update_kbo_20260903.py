#!/usr/bin/env python3
"""Write the reconciled 2026-09-03 KBO final-game report from captured primary records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-03", "20260903"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260903HHKT0": 80101172, "20260903LGOB0": 80101174, "20260903LTSS0": 80101175, "20260903SKWO0": 80101176}
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


# The KBO official game-list/API is the baseline. Narrative facts below are limited to the reconciled official/Naver box lines.
games = [
    game("20260903HHKT0", "수원", "한화", "KT", 11, 13, "오원석", "김서현", "박영현",
         "KT가 난타전 끝에 한화를 13-11로 제압",
         ["KT 선발 고영표가 3이닝 7실점으로 일찍 물러났지만 오원석이 3이닝 2피안타 1사사구 3탈삼진 무실점으로 승리를 기록했다.",
          "KT는 1회 3점 뒤 3~6회 매 이닝 득점으로 추격해 역전했고, 8회 3득점으로 13-8까지 달아났다.",
          "안현민은 3타수 2안타 2홈런 5타점 2득점, 오윤석은 4타수 3안타 2타점 2득점, 허경민은 4타수 2안타 1타점 2득점을 기록했다.",
          "손동현이 1이닝 무실점 홀드를 올렸고, 박영현은 1⅓이닝 3실점(2자책)으로 시즌 24세이브를 기록했다."],
         "한화는 노시환이 5타수 3안타 1타점 2득점, 김태연이 4타수 2안타 1홈런 3타점 3득점으로 끝까지 추격했다."),
    game("20260903LGOB0", "잠실", "LG", "두산", 1, 0, "박시원", "곽빈", "손주영",
         "LG가 오스틴의 4회 솔로포로 두산에 1-0 승리",
         ["LG 선발 박시원은 5이닝 2피안타 2사사구 2탈삼진 무실점으로 승리를 기록했다.",
          "0-0이던 4회 오스틴이 중월 솔로 홈런을 쳐 결승점을 만들었다.",
          "오스틴은 4타수 2안타 1홈런 1타점 1득점으로 팀의 유일한 득점을 책임졌다.",
          "이우찬·김진수·김영우가 각각 홀드를 기록했고, 손주영이 1이닝 무실점으로 시즌 26세이브를 올렸다."],
         "두산은 김민석이 4타수 3안타를 기록했고, 곽빈이 7이닝 3피안타 1실점 8탈삼진으로 버텼지만 패했다."),
    game("20260903LTSS0", "대구", "롯데", "삼성", 3, 2, "비슬리", "장찬희", "이이무라",
         "롯데가 8회 결승점을 내 삼성에 3-2 승리",
         ["롯데 선발 제레미 비슬리는 7이닝 3피안타 1사사구 9탈삼진 2실점으로 승리를 기록했다.",
          "롯데는 6회 2득점으로 2-2 동점을 만든 뒤 8회 1득점으로 승부를 갈랐다.",
          "황성빈은 4타수 3안타 2득점, 나승엽은 4타수 2안타 1타점, 한동희는 4타수 1안타 1홈런 2타점 1득점을 기록했다.",
          "박정민이 1이닝 무실점 홀드, 최준용이 ⅓이닝 무실점 홀드, 이이무라가 ⅔이닝 무실점으로 시즌 첫 세이브를 올렸다."],
         "삼성은 원태인이 6이닝 7피안타 7탈삼진 2실점으로 막았고, 디아즈가 4타수 2안타로 분전했다."),
    game("20260903SKWO0", "고척", "SSG", "키움", 2, 3, "박진형", "전영준", None,
         "키움이 9회 끝내기 득점으로 SSG에 3-2 승리",
         ["키움 선발 박준현은 5이닝 3피안타 4사사구 8탈삼진 1실점으로 승패 없이 물러났다.",
          "키움은 1회 2점을 냈고, 9회 SSG가 동점을 만든 뒤 말 공격에서 1점을 보태 끝내기 승리를 만들었다.",
          "추재현은 4타수 3안타 2타점 1득점, 김웅빈은 4타수 2안타 1타점으로 공격을 이끌었다.",
          "김선기·박지성·유토·조영건이 홀드를 합작했고, 박진형은 1이닝 1실점으로 승리를 기록했다."],
         "SSG는 정준재와 에레디아가 각각 5타수 2안타 1타점을 기록하며 9회 동점을 만들었지만 끝내기 실점으로 패했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "innings": "6", "hits": 7, "runs": 2, "earned_runs": 2, "walks_hbp": 0, "strikeouts": 7, "home_runs": 1, "pitches": 95, "season_record": "7승 6패", "era": "4.26", "role": "starter", "game_decision": None},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": True, "innings": "7", "hits": 3, "runs": 2, "earned_runs": 2, "walks_hbp": 1, "strikeouts": 9, "home_runs": 0, "pitches": 94, "season_record": "9승 5패", "era": "4.68", "role": "starter", "game_decision": "승"},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "pitches": 14, "season_record": "6승 2패", "era": "3.59", "role": "reliever", "game_decision": "홀드"},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": True, "innings": "1⅓", "hits": 2, "runs": 3, "earned_runs": 2, "walks_hbp": 2, "strikeouts": 0, "home_runs": 1, "pitches": 38, "season_record": "6승 0패", "season_saves": 24, "era": "2.56", "role": "reliever", "game_decision": "세이브"},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 1, "rbi": 0, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.285", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 3, "rbi": 1, "runs": 2, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.276", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": False},
]

# Structural and three-surface checks before mutating the live report.
kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
official_list = json.loads((ART / "official-game-list.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
final_ids = {g["id"] for g in games}
assert final_ids == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["G_ID"] for g in official_list["game"] if g["GAME_STATE_SC"] == "3" and g["GAME_RESULT_CK"] == 1} == final_ids
assert any(g["G_ID"] == "20260903HTNC0" and g["CANCEL_SC_NM"] == "우천취소" for g in official_list["game"])
assert all(g["gameStatus"] == "END" for g in daum if g["gameId"] in DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 35
for g in games:
    gid = g["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    scoreboard = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert official["code"] == "100" and scoreboard["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
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
    "details": "2026-09-03 KST 편성 5경기 중 KIA-NC는 KBO 공식 GAME_STATE_SC=4·우천취소, kbo-game CANCELED, 다음 gameStatus=CANCEL로 대조돼 모든 카드·합계·승부처에서 제외했다. 나머지 4경기는 kbo-game FINISHED, KBO 공식 게임목록 GAME_STATE_SC=3·GAME_RESULT_CK=1 및 게임센터 상세기록 API(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료와 스코어를 대조했다. 종료 4경기 합계는 35득점이다. 관심 투수의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 행으로, 역할 및 당일 승·홀드·세이브는 KBO 공식 기준으로 대조했다. 비등판 투수는 완료 경기의 공식·네이버 투수 목록 부재 또는 팀 경기 취소를 확인해 계약상 name·team·appeared만 보존했다. 관심 타자는 KBO 공식·네이버 기록으로 대조했으며, 김도영은 우천취소 경기로 출전 없음이다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-09-02", DATE).replace("2026.09.02", "2026.09.03").replace("2026년 9월 2일", "2026년 9월 3일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
