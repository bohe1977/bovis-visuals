#!/usr/bin/env python3
"""Build the reconciled 2026-09-05 KBO final-game report from captured records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-05", "20260905"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260905SSLG0": 80101186, "20260905HHLT0": 80101182, "20260905OBSK0": 80101185, "20260905KTHT0": 80101183, "20260905NCWO0": 80101184}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(gid: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "17:00", "status": "경기 종료", "away": away, "home": home,
            "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser,
            "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}


# Narrative statements are confined to reconciled official review rows and Naver record rows.
games = [
    game("20260905SSLG0", "잠실", "삼성", "LG", 4, 3, "김재윤", "이정용", "사토시",
         "삼성이 연장 11회 강민호의 결승타로 LG에 4-3 승리",
         ["삼성 선발 이승현은 5이닝 4피안타 무실점으로 버텼고, 김재윤이 ⅔이닝 무실점으로 승리를 기록했다.",
          "3-3이던 11회 1사 1·2루에서 강민호가 좌전 적시타를 쳐 결승점을 만들었다.",
          "이재현은 4타수 3안타 1타점, 류지혁은 3타수 2안타 2타점, 강민호는 2타수 1안타 1타점으로 공격을 이끌었다.",
          "사토시는 1이닝 무실점으로 시즌 첫 세이브를 올렸다."],
         "LG는 6회 3득점으로 동점을 만들었고, 구본혁이 4타수 1안타 2타점으로 추격에 힘을 보탰지만 연장 11회 실점으로 패했다."),
    game("20260905HHLT0", "사직", "한화", "롯데", 11, 6, "장유호", "박정민", None,
         "한화가 7회 심우준의 결승 2점포를 앞세워 롯데에 11-6 승리",
         ["한화 선발 황준서는 4이닝 5피안타 3실점을 기록했고, 장유호가 1이닝 무실점으로 승리를 챙겼다.",
          "3-3이던 7회 심우준이 좌월 2점 홈런을 쳐 결승타를 기록했고, 한화는 8회 6점을 보태 격차를 벌렸다.",
          "심우준은 5타수 3안타 4타점 3득점, 문현빈은 4타수 3안타 1득점, 노시환은 5타수 2안타 1타점 1득점을 기록했다.",
          "조동욱이 1이닝 무실점 홀드를 올리며 리드를 지켰다."],
         "롯데는 고승민이 4타수 1안타 1홈런 3타점 1득점, 박승욱이 1타수 1안타 2타점을 기록하며 9회 3점을 만회했다."),
    game("20260905OBSK0", "문학", "두산", "SSG", 2, 3, "김민준", "최민석", "조병현",
         "SSG가 전의산의 4회 3점포로 두산에 3-2 승리",
         ["SSG 선발 김민준은 6이닝 4피안타 2실점 5탈삼진으로 승리를 기록했다.",
          "0-0이던 4회 전의산이 1사 1·3루에서 좌중월 3점 홈런을 쳐 결승타를 만들었다.",
          "전의산은 3타수 2안타 1홈런 3타점 1득점으로 팀 득점을 모두 책임졌다.",
          "문승원·김민·전영준이 홀드를 합작했고, 조병현이 1이닝 무실점으로 시즌 18세이브를 올렸다."],
         "두산은 김민석이 3타수 3안타 1타점 1득점으로 분전했고, 4·5회 한 점씩 추격했으나 동점을 만들지 못했다."),
    game("20260905KTHT0", "광주", "KT", "KIA", 3, 6, "양현종", "로건", "전상현",
         "KIA가 5회 역전 뒤 나성범의 8회 2점포로 KT에 6-3 승리",
         ["KIA 선발 양현종은 5이닝 7피안타 3실점 2탈삼진으로 승리를 기록했다.",
          "KIA는 5회 3득점으로 승부를 뒤집었고, 카스트로의 유격수 땅볼이 결승타가 됐다. 8회 나성범의 2점 홈런으로 달아났다.",
          "김선빈은 4타수 2안타 2타점 1득점, 나성범은 4타수 1안타 1홈런 2타점 2득점을 기록했다.",
          "성영탁·곽도규·조상우가 홀드를 합작했고, 전상현이 1⅔이닝 무실점으로 시즌 첫 세이브를 기록했다."],
         "KT는 힐리어드가 5타수 3안타 1홈런 2타점 1득점으로 공격을 이끌었지만, 5회 역전을 허용한 뒤 추가 득점에 실패했다."),
    game("20260905NCWO0", "고척", "NC", "키움", 2, 1, "배재환", "전준표", "전사민",
         "NC가 2회 2득점을 지켜 키움에 2-1 승리",
         ["NC 선발 이재학은 4이닝 1피안타 1실점 4탈삼진을 기록했고, 배재환이 1이닝 무실점으로 승리를 올렸다.",
          "NC는 2회 1사 1·3루에서 이우성의 2루수 땅볼로 결승점을 냈고, 이 이닝에 2점을 뽑아냈다.",
          "김형준은 3타수 1안타 1타점, 박건우는 3타수 1안타 1득점으로 공격에 기여했다.",
          "김진호·신영우·손주환·이용준이 홀드를 이어갔고, 전사민이 1이닝 무실점으로 시즌 9세이브를 기록했다."],
         "키움은 데이비슨이 4타수 2안타, 김웅빈과 권혁빈이 각각 안타를 기록하며 추격했지만 4회 1득점에 그쳤다."),
]

# The watchlist is stable; an inactive pitcher object intentionally carries no extra fields.
pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "1", "hits": 1, "runs": 2, "earned_runs": 2, "walks_hbp": 2, "strikeouts": 0, "home_runs": 1, "pitches": 29, "season_record": "6승 3패", "era": "3.92", "role": "reliever", "game_decision": None},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.288", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 1, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.279", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.300", "obp": None, "ops": None},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text())
daum = json.loads((ART / "daum-schedule.json").read_text())["schedule"][COMPACT]
final_ids = {g["id"] for g in games}
assert final_ids == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 41
for game_data in games:
    gid = game_data["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    official_score = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text())["result"]["recordData"]
    assert official["code"] == "100" and official_score["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == game_data["away_score"] and int(rheb["home"]["r"]) == game_data["home_score"]
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-09-05 KST 편성 5경기는 kbo-game FINISHED, KBO 공식 게임센터 GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료와 스코어를 대조했다. 종료 5경기 합계는 41득점이다. 관심 투수의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 행으로 대조했고, 박정민은 공식 표의 구원·패전 기록을 확인했으나 구원 투수의 game_decision 계약(세이브·홀드·블론만 기록)에 따라 null로 보존했다. 비등판 투수는 해당 팀의 완료 경기 KBO 공식·네이버 투수 목록 부재를 확인해 계약상 name·team·appeared만 보존했다. 관심 타자의 당일 수치는 KBO 공식·네이버 기록으로 대조했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.05", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 5일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
