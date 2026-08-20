#!/usr/bin/env python3
"""Write the reconciled 2026-08-20 KBO final-game report from verified source captures."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-20", "20260820"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260820&toDate=20260820"
DAUM_IDS = {"20260820HTHH0": 80101112, "20260820KTLG0": 80101113, "20260820OBNC0": 80101114, "20260820SKSS0": 80101115, "20260820WOLT0": 80101116}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


games = [
    {"id": "20260820KTLG0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료", "away": "KT", "home": "LG", "away_score": 16, "home_score": 4, "winner_pitcher": "고영표", "loser_pitcher": "케네디", "save_pitcher": "", "headline": "KT가 7회 김민혁의 만루 결승 2루타를 앞세워 LG에 16-4 승리", "winner_points": ["KT 선발 고영표는 6이닝 6피안타 2사사구 6탈삼진 3실점으로 시즌 10승째를 올렸다.", "3-3이던 7회 1사 만루에서 김민혁이 좌중간 2루타로 결승 3타점을 냈고, KT는 이 이닝 7점을 뽑았다.", "김민혁은 1타수 1안타 3타점, 힐리어드는 3타수 2안타 3타점 2득점, 류현인은 5타수 3안타 2타점을 기록했다.", "주권·이상동·김정운이 3이닝 1실점으로 뒤를 막았다."], "opponent_effort": "LG는 문보경(2점)과 오지환(1점)이 4회 연속 홈런으로 맞섰고, 송찬의가 4타수 2안타를 기록했다.", "sources": sources("20260820KTLG0")},
    {"id": "20260820SKSS0", "stadium": "대구", "start_time": "19:00", "status": "경기 종료", "away": "SSG", "home": "삼성", "away_score": 6, "home_score": 4, "winner_pitcher": "노경은", "loser_pitcher": "사토시", "save_pitcher": "조병현", "headline": "SSG가 8회 최지훈의 희생플라이 결승타로 삼성에 6-4 승리", "winner_points": ["SSG 선발 최민준은 4⅓이닝 5피안타 2사사구 3탈삼진 4실점을 기록했고, 노경은이 1이닝 무실점으로 승리를 챙겼다.", "4-4이던 8회 1사 1·3루에서 최지훈의 중견수 희생플라이가 결승점이 됐다.", "최지훈은 4타수 1안타 2타점, 김재환은 5타수 2안타 1홈런 2타점으로 힘을 보탰다.", "문승원이 홀드, 조병현이 1이닝 무실점으로 시즌 16세이브를 기록했다."], "opponent_effort": "삼성은 최형우가 5타수 3안타 1홈런 3타점, 이재현이 솔로포를 쳐 동점을 만들었으나 8회 리드를 내줬다.", "sources": sources("20260820SKSS0")},
    {"id": "20260820WOLT0", "stadium": "사직", "start_time": "19:00", "status": "경기 종료", "away": "키움", "home": "롯데", "away_score": 1, "home_score": 7, "winner_pitcher": "나균안", "loser_pitcher": "박준현", "save_pitcher": "", "headline": "롯데가 나균안의 6이닝 1실점과 6회 레이예스의 결승 2루타로 키움에 7-1 승리", "winner_points": ["롯데 선발 나균안은 6이닝 5피안타 4사사구 4탈삼진 1실점으로 시즌 6승째를 거뒀다.", "1-1이던 6회 무사 1·2루에서 레이예스가 우중간 적시 2루타를 쳐 결승점을 만들었다.", "전민재는 3타수 1안타 3타점, 레이예스는 4타수 1안타 1타점 1득점을 기록했다.", "박정민·김한결·현도훈이 3이닝을 1피안타 무실점으로 막았다."], "opponent_effort": "키움은 박준현이 5이닝 3피안타 3사사구 4탈삼진 3실점으로 버텼고, 안치홍이 3타수 1안타 1타점을 기록했다.", "sources": sources("20260820WOLT0")},
    {"id": "20260820OBNC0", "stadium": "창원", "start_time": "19:00", "status": "경기 종료", "away": "두산", "home": "NC", "away_score": 4, "home_score": 5, "winner_pitcher": "전사민", "loser_pitcher": "김택연", "save_pitcher": "", "headline": "NC가 9회 권희동의 끝내기 안타로 두산에 5-4 승리", "winner_points": ["NC 선발 구창모는 6이닝 7피안타 2사사구 무탈삼진 2실점을 기록했고, 전사민이 9회 2실점에도 승리투수가 됐다.", "4-4이던 9회 2사 만루에서 권희동이 좌전 끝내기 안타를 쳤다.", "권희동은 5타수 2안타 2타점, 김주원은 4타수 1안타 1타점 1볼넷을 기록했다.", "손주환과 이용준이 2이닝 무실점으로 연결했고 이용준은 홀드를 올렸다."], "opponent_effort": "두산은 박준순이 4타수 3안타 1득점, 박찬호가 3타수 2안타 1타점 1볼넷으로 추격을 이끌었다.", "sources": sources("20260820OBNC0")},
    {"id": "20260820HTHH0", "stadium": "대전", "start_time": "19:00", "status": "경기 종료", "away": "KIA", "home": "한화", "away_score": 10, "home_score": 6, "winner_pitcher": "최지민", "loser_pitcher": "정우주", "save_pitcher": "", "headline": "KIA가 8회 김태군의 결승 2점 홈런으로 한화에 10-6 승리", "winner_points": ["KIA 선발 황동하는 5이닝 4피안타 3사사구 4탈삼진 2실점, 최지민은 1이닝 2실점으로 구원승을 거뒀다.", "6-6이던 8회 2사 1루에서 김태군이 좌월 결승 2점 홈런을 쳤다.", "카스트로는 4타수 2안타 3타점, 나성범은 4타수 2안타 3타점, 김태군은 1타수 1안타 3타점 1홈런을 기록했다.", "정해영이 1이닝 무피안타 무실점 홀드로 리드를 지켰다."], "opponent_effort": "한화는 한지윤이 4타수 3안타 1홈런 2타점, 황영묵이 4타수 2안타 1홈런 2타점으로 6-6 동점을 만들며 맞섰다.", "sources": sources("20260820HTHH0")},
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": True, "role": "starter", "game_decision": None, "innings": "6", "hits": 6, "runs": 4, "earned_runs": 4, "walks_hbp": 1, "strikeouts": 5, "home_runs": 0, "season_record": "8승 4패", "era": "4.02"},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 1, "home_runs": 0, "season_record": "6승 2패", "era": "3.86"},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "role": "reliever", "game_decision": "홀드", "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0, "season_record": "2승 1패", "season_saves": 2, "era": "6.44"},
    {"name": "박영현", "team": "KT", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.299", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.274", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 3, "rbi": 0, "runs": 4, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.302", "obp": None, "ops": None},
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-20 KBO 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW 경로, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조해 최종 종료로 확정했다. 5경기 합계 63득점이며 취소·연기·노게임은 없다. 류현진(선발·결정 없음), 박정민(구원·결정 없음), 정해영(구원·홀드)의 당일 라인·시즌 승패·ERA는 네이버 박스스코어 및 공식 게임센터 REVIEW 경로로 대조했다. 정해영의 시즌 2세이브도 공식 기록 기준으로 반영했다. 나머지 관심 투수는 해당 팀 완료 경기의 네이버 전체 투수 명단에 없어 등판 없음으로 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 네이버 기록 API와 공식 게임센터 REVIEW 경로로 대조했다. 다음의 타자 볼넷은 사사구 표기 범위 차이가 있어 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-08-19", DATE).replace("2026.08.19", "2026.08.20").replace("2026년 8월 19일", "2026년 8월 20일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
