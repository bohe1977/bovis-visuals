#!/usr/bin/env python3
"""Write reconciled 2026-08-23 KBO final-game report from captured records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-23", "20260823"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260823&toDate=20260823"
DAUM_IDS = {"20260823HTWO0": 80101127, "20260823KTSK0": 80101128, "20260823LGHH0": 80101129, "20260823LTOB0": 80101130, "20260823SSNC0": 80101131}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


# All five games were simultaneously kbo-game FINISHED, Naver statusCode=4, and Daum END.
games = [
    {"id": "20260823HTWO0", "stadium": "고척", "start_time": "14:00", "status": "경기 종료", "away": "KIA", "home": "키움", "away_score": 7, "home_score": 8, "winner_pitcher": "이강준", "loser_pitcher": "이의리", "save_pitcher": None,
     "headline": "키움이 9회 김재현의 끝내기 만루포로 KIA에 8-7 승리",
     "winner_points": ["키움 선발 전준표는 5이닝 3피안타 5사사구 무탈삼진 2실점으로 버텼고, 이강준이 1이닝 1피안타 무실점으로 시즌 첫 승을 기록했다.", "7-7이던 9회 2사 만루에서 김재현의 좌월 만루 홈런이 결승타가 됐다.", "데이비슨은 5타수 3안타 1홈런 4타점 2득점, 서건창과 추재현은 나란히 3안타를 쳤다.", "키움 불펜은 9회 이강준이 무실점으로 마무리했다."],
     "opponent_effort": "KIA는 박재현이 5타수 3안타 2타점, 김태군이 3타수 2안타 1홈런 2타점으로 추격했고 김도영도 솔로포를 보탰지만 9회 이의리가 끝내기 홈런을 허용했다.", "sources": sources("20260823HTWO0")},
    {"id": "20260823KTSK0", "stadium": "문학", "start_time": "19:00", "status": "경기 종료", "away": "KT", "home": "SSG", "away_score": 3, "home_score": 1, "winner_pitcher": "로건", "loser_pitcher": "아빌라", "save_pitcher": "박영현",
     "headline": "KT가 로건의 6이닝 무실점과 박영현의 세이브로 SSG에 3-1 승리",
     "winner_points": ["KT 선발 로건은 6이닝 4피안타 무사사구 7탈삼진 무실점으로 시즌 5승째를 올렸다.", "1회 2사 2·3루에서 김현수의 2타점 2루타가 결승타가 됐다.", "권동진은 3타수 3안타 1타점, 힐리어드는 4타수 2안타 1득점을 기록했다.", "스기모토가 1⅔이닝 무실점 홀드했고, 박영현은 1⅓이닝 2피안타 1실점으로 시즌 23세이브를 기록했다."],
     "opponent_effort": "SSG는 9회 에레디아의 솔로 홈런으로 영패를 면했고, 선발 아빌라는 7이닝 8피안타 2사사구 7탈삼진 3실점으로 버텼다.", "sources": sources("20260823KTSK0")},
    {"id": "20260823LGHH0", "stadium": "대전", "start_time": "19:00", "status": "경기 종료", "away": "LG", "home": "한화", "away_score": 12, "home_score": 3, "winner_pitcher": "카라스코", "loser_pitcher": "박준영", "save_pitcher": None,
     "headline": "LG가 1회부터 앞서며 한화에 12-3 승리",
     "winner_points": ["LG 선발 카라스코는 6이닝 5피안타 3사사구 3탈삼진 3실점(2자책)으로 시즌 2승째를 거뒀다.", "1회 2사 1·2루에서 문보경의 좌익수 2루타가 결승타가 됐고, 문정빈의 1회 3점포와 송찬의의 2회 3점포로 초반 격차를 벌렸다.", "송찬의는 4타수 2안타 1홈런 4타점, 문정빈은 5타수 1안타 1홈런 3타점, 신민재는 4타수 2안타 2득점을 올렸다.", "LG 불펜은 케네디·김영우·손주영이 마지막 3이닝을 무실점으로 막았다."],
     "opponent_effort": "한화는 문현빈이 4타수 3안타 1타점, 한지윤이 4타수 1안타 2타점으로 분전했지만 선발 박준영이 1⅔이닝 8실점으로 무너졌다.", "sources": sources("20260823LGHH0")},
    {"id": "20260823LTOB0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료", "away": "롯데", "home": "두산", "away_score": 1, "home_score": 3, "winner_pitcher": "곽빈", "loser_pitcher": "박세웅", "save_pitcher": "이영하",
     "headline": "두산이 곽빈의 7이닝 무실점에 힘입어 롯데에 3-1 승리",
     "winner_points": ["두산 선발 곽빈은 7이닝 1피안타 2사사구 8탈삼진 무실점으로 시즌 10승째를 올렸다.", "3회 무사 2루에서 박찬호의 좌익수 2루타가 결승타가 됐다.", "안재석은 4타수 3안타 1타점, 박찬호는 4타수 2안타 1타점 1득점으로 공격을 이끌었다.", "타카다가 ⅔이닝 무실점 홀드, 이영하가 1이닝 무실점으로 시즌 20세이브를 기록했다."],
     "opponent_effort": "롯데는 박세웅이 6이닝 9피안타 무사사구 5탈삼진 3실점(2자책)으로 버텼고, 8회 전민재의 볼넷과 상대 폭투로 1점을 만회했다.", "sources": sources("20260823LTOB0")},
    {"id": "20260823SSNC0", "stadium": "창원", "start_time": "19:00", "status": "경기 종료", "away": "삼성", "home": "NC", "away_score": 2, "home_score": 1, "winner_pitcher": "페덱", "loser_pitcher": "라일리", "save_pitcher": "김재윤",
     "headline": "삼성이 박계범의 6회 결승포로 NC에 2-1 승리",
     "winner_points": ["삼성 선발 페덱은 8이닝 3피안타 무사사구 7탈삼진 1실점으로 시즌 3승째를 기록했다.", "1-1이던 6회 1사에서 박계범의 좌월 솔로 홈런이 결승타가 됐다.", "박계범은 3타수 1안타 1홈런 1타점 1득점, 김지찬은 4타수 1안타 1득점을 기록했다.", "김재윤이 1이닝 1피안타 1사사구 무실점으로 시즌 28세이브를 올렸다."],
     "opponent_effort": "NC는 라일리가 8이닝 3피안타 1사사구 12탈삼진 2실점으로 호투했고 박민우가 4타수 2안타 1득점으로 맞섰지만 한 점 차를 뒤집지 못했다.", "sources": sources("20260823SSNC0")},
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False}, {"name": "류현진", "team": "한화", "appeared": False}, {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": True, "role": "starter", "game_decision": "패", "innings": "6", "hits": 9, "runs": 3, "earned_runs": 2, "walks_hbp": 0, "strikeouts": 5, "home_runs": 0, "season_record": "2승 8패", "era": "4.68"},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "⅔", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "season_record": "1승 4패", "season_saves": 5, "era": "4.28"},
    {"name": "박정민", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 3, "home_runs": 0, "season_record": "6승 2패", "season_saves": 1, "era": "3.76"},
    {"name": "로드리게스", "team": "롯데", "appeared": False}, {"name": "임찬규", "team": "LG", "appeared": False}, {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": True, "role": "reliever", "game_decision": "세이브", "innings": "1⅓", "hits": 2, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 1, "home_runs": 1, "season_record": "6승 0패", "season_saves": 23, "era": "2.37"},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 0, "avg": "0.298", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.276", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 1, "runs": 1, "home_runs": 1, "walks": 1, "strikeouts": 1, "avg": "0.301", "obp": None, "ops": None},
]
source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · 네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-08-23 편성 5경기는 kbo-game FINISHED, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조해 모두 최종 종료로 확정했다. 관심 투수의 등판·당일 라인·시즌 승패·ERA와 박영현·김원중·박정민의 시즌 세이브는 KBO 공식 REVIEW와 네이버 기록을 대조했다. 박세웅은 KBO 공식 선발·패전, 박영현은 KBO 공식 구원·세이브로 분류했으며 김원중·박정민은 구원 등판이나 공식 세이브·홀드·블론이 없어 결정 기록을 null로 기록했다. 미등판 투수는 해당 팀의 완료 경기 KBO·네이버 전체 투수 목록에서 부재함을 확인했다. 강백호·노시환·김도영 타격 라인과 시즌 타율은 KBO REVIEW와 네이버 API에서 대조했다. 다음의 타자 볼넷은 사사구 표기 범위 차이가 있어 독립 일치값으로 주장하지 않았다.", "conflicts": []}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8").replace("2026-08-22", DATE).replace("2026.08.22", "2026.08.23").replace("2026년 8월 22일", "2026년 8월 23일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
