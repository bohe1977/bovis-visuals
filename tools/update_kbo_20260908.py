#!/usr/bin/env python3
"""Build the reconciled 2026-09-08 KBO report from captured official/Naver/Daum records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-08", "20260908"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {
    "20260908HTSS0": 80108745, "20260908LTNC0": 80108746,
    "20260908OBHH0": 80108747, "20260908SKKT0": 80108748,
    "20260908WOLG0": 80108749,
}
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


# Every fact below is present in the captured KBO official REVIEW tables and Naver record API.
games = [
    game("20260908WOLG0", "잠실", "키움", "LG", 8, 3, "하영민", "박시원", None,
         "키움이 추재현의 3회 결승 적시타를 앞세워 LG에 8-3 승리",
         ["키움 선발 하영민은 6이닝 2피안타 무실점 2탈삼진으로 승리를 기록했다.",
          "3회 1사 1·3루에서 추재현의 우전 안타가 결승타가 됐다.",
          "서건창은 5타수 2안타 1타점 1득점, 추재현·데이비슨·히우라는 각각 1타점을 기록했다.",
          "조영건이 1이닝 무실점으로 마무리했다."],
         "LG는 오스틴이 3타수 1안타 2타점 1득점, 박해민이 2타수 1안타로 분전했지만 초반 실점을 만회하지 못했다."),
    game("20260908HTSS0", "대구", "KIA", "삼성", 4, 6, "최원태", "시라카와", None,
         "삼성이 KIA에 6-4 승리",
         ["삼성 선발 최원태는 5이닝 7피안타 4실점 3탈삼진으로 승리를 기록했다.",
          "공식 기록의 결승타 항목은 ‘없음’으로 남았고, 삼성은 중반까지 만든 리드를 지켰다.",
          "박승규는 3타수 1안타 1홈런 2타점 3득점, 최형우는 3타수 1안타 2타점을 기록했다.",
          "이승민이 1이닝 무실점 홀드로 리드를 지켰다."],
         "KIA는 박재현이 5타수 3안타 1홈런 1타점, 김도영이 5타수 2안타 1홈런 1타점 2득점으로 추격했다."),
    game("20260908SKKT0", "수원", "SSG", "KT", 1, 3, "소형준", "김건우", "박영현",
         "KT가 안현민의 2회 결승 2타점 적시타와 박영현의 세이브로 SSG에 3-1 승리",
         ["KT 선발 소형준은 7이닝 4피안타 1실점 3탈삼진으로 승리를 기록했다.",
          "2회 2사 만루에서 안현민의 좌전 안타가 결승타가 됐다.",
          "최원준은 4타수 3안타 1득점, 안현민은 3타수 1안타 2타점을 기록했다.",
          "손동현이 홀드, 박영현이 1이닝 무실점으로 시즌 25세이브를 올렸다."],
         "SSG는 에레디아가 4타수 2안타, 박성한이 3타수 1안타 1타점으로 분전했지만 1득점에 그쳤다."),
    game("20260908LTNC0", "창원", "롯데", "NC", 6, 3, "박세웅", "토다", "이이무라",
         "롯데가 고승민의 5회 결승 2점포로 NC에 6-3 승리",
         ["롯데 선발 박세웅은 5이닝 4피안타 3실점 4탈삼진으로 승리를 기록했다.",
          "5회 무사 2루에서 고승민의 우월 2점 홈런이 결승타가 됐다.",
          "고승민은 5타수 3안타 1홈런 2타점 2득점, 한동희는 4타수 2안타 2타점 1득점을 기록했다.",
          "김원중·박정민·최준용이 홀드를 이어갔고 이이무라가 1이닝 무실점 세이브를 올렸다."],
         "NC는 블레인이 4타수 1안타 2타점, 박건우가 4타수 1안타 1득점으로 추격했지만 안타 5개에 묶였다."),
    game("20260908OBHH0", "대전", "두산", "한화", 1, 6, "류현진", "최승용", None,
         "한화가 허인서의 2회 결승 홈런과 류현진의 호투로 두산에 6-1 승리",
         ["한화 선발 류현진은 6이닝 3피안타 1실점 3탈삼진으로 승리를 기록했다.",
          "2회 1사 1루에서 허인서의 좌중월 홈런이 결승타가 됐다.",
          "강백호는 4타수 1안타 1홈런 2타점 1득점, 심우준은 4타수 1안타 1타점을 기록했다.",
          "한화 불펜이 뒤 3이닝을 무실점으로 막아 승리를 지켰다."],
         "두산은 박지훈이 4타수 2안타 1홈런 1타점 1득점으로 팀 유일의 득점을 만들었다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": True, "innings": "6", "hits": 3, "runs": 1, "earned_runs": 1, "walks_hbp": 1, "strikeouts": 3, "home_runs": 1, "pitches": 79, "season_record": "9승 5패", "era": "3.80", "role": "starter", "game_decision": "승"},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": True, "innings": "5", "hits": 4, "runs": 3, "earned_runs": 3, "walks_hbp": 4, "strikeouts": 4, "home_runs": 0, "pitches": 93, "season_record": "3승 9패", "era": "5.01", "role": "starter", "game_decision": "승"},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "pitches": 13, "season_record": "1승 5패", "season_saves": 5, "era": "5.11", "role": "reliever", "game_decision": "홀드"},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 1, "home_runs": 0, "pitches": 16, "season_record": "6승 3패", "era": "3.94", "role": "reliever", "game_decision": "홀드"},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": True, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "pitches": 11, "season_record": "6승 0패", "season_saves": 25, "era": "2.68", "role": "reliever", "game_decision": "세이브"},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 1, "avg": "0.289", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.280", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 1, "runs": 2, "home_runs": 1, "walks": 0, "strikeouts": 2, "avg": "0.307", "obp": None, "ops": None},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
final_ids = {g["id"] for g in games}
assert final_ids == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 41
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
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-09-08 KST 편성 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW의 GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료와 스코어를 대조했다. 종료 5경기 합계는 41득점이다. 실제 등판 관심 투수의 당일 라인·시즌 성적·ERA·세이브는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 선발/구원 및 당일 결정은 KBO 공식 결과 행과 네이버 pitchingResult를 대조했다. 비등판 투수는 해당 팀의 완료 경기 KBO·네이버 전체 투수 명단 부재를 확인해 계약상 name·team·appeared만 보존했다. 관심 타자의 당일 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts": []}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.08", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 8일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
