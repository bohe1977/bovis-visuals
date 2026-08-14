#!/usr/bin/env python3
"""Normalize the verified 2026-08-14 KBO final slate for the BOVIS data contract."""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-14"
COMPACT = DATE.replace("-", "")
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"


def sources(game_id: str, daum_id: int) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{daum_id}"},
    ]


games = [
    {
        "id": "20260814HHSS0", "stadium": "대구", "start_time": "19:00", "status": "경기 종료",
        "away": "한화", "home": "삼성", "away_score": 5, "home_score": 8,
        "winner_pitcher": "최원태", "loser_pitcher": "짐머맨", "save_pitcher": "김재윤",
        "headline": "삼성이 4~6회 8득점으로 한화에 8-5 승리",
        "winner_points": [
            "삼성 선발 최원태는 5⅔이닝 5피안타 2사사구 6탈삼진 1실점으로 승리를 기록했다.",
            "4회 구자욱의 선제 홈런을 시작으로 5회 3점, 6회 4점을 보태 8-0까지 달아난 구간이 승부처였다.",
            "구자욱은 5타수 5안타 2홈런 3타점 2득점, 이재현은 4타수 2안타 1홈런 2타점 2득점을 올렸다.",
            "이승현·이승민이 홀드를 기록했고 김재윤이 1이닝 무실점으로 시즌 26세이브를 기록했다.",
        ],
        "opponent_effort": "한화는 8회 4점을 만회했고 강백호가 5타수 2안타 1홈런 1타점, 박정현이 대타 홈런으로 3타점을 올리며 추격했다.",
        "sources": sources("20260814HHSS0", 80101087),
    },
    {
        "id": "20260814NCLT0", "stadium": "사직", "start_time": "19:00", "status": "경기 종료",
        "away": "NC", "home": "롯데", "away_score": 9, "home_score": 8,
        "winner_pitcher": "임지민", "loser_pitcher": "김원중", "save_pitcher": "김태훈",
        "headline": "NC가 9회 3득점으로 롯데의 끝내기 추격을 9-8로 막았다",
        "winner_points": [
            "NC 선발 토다는 5이닝 9피안타 2사사구 2탈삼진 2실점을 기록했다.",
            "NC는 9회 3점을 더해 9-6으로 달아났고, 롯데의 9회 2득점 추격을 한 점 차로 막아냈다.",
            "박건우는 5타수 3안타 3타점, 천재환은 2타수 1안타 1홈런 2타점 2득점, 김주원은 홈런 포함 3득점을 기록했다.",
            "김진호가 ⅔이닝 홀드, 임지민이 1이닝 2실점으로 승리, 김태훈이 ⅓이닝 무실점으로 시즌 1세이브를 기록했다.",
        ],
        "opponent_effort": "롯데는 19안타를 치고 9회 2점을 더했으며 레이예스가 6타수 5안타 2타점, 한동희가 6타수 3안타 1홈런 2타점으로 분전했다.",
        "sources": sources("20260814NCLT0", 80101088),
    },
    {
        "id": "20260814OBHT0", "stadium": "광주", "start_time": "19:00", "status": "경기 종료",
        "away": "두산", "home": "KIA", "away_score": 10, "home_score": 4,
        "winner_pitcher": "잭로그", "loser_pitcher": "황동하", "save_pitcher": "",
        "headline": "두산이 1회 4득점으로 주도권을 잡아 KIA에 10-4 승리",
        "winner_points": [
            "두산 선발 잭로그는 6이닝 6피안타 3사사구 7탈삼진 2실점으로 승리했다.",
            "두산은 1회 4득점으로 앞서 나간 뒤 3회 2점, 7회 2점을 추가해 격차를 벌렸다.",
            "박찬호는 4타수 3안타 3타점, 정수빈은 4타수 2안타 3타점, 양의지는 3타수 2안타 2타점을 기록했다.",
            "타카다·김정우·이용찬이 각각 1이닝을 맡아 리드를 지켰다.",
        ],
        "opponent_effort": "KIA는 나성범이 4타수 2안타 1홈런 3타점, 김호령이 4타수 2안타 1홈런 1타점으로 장타를 만들며 맞섰다.",
        "sources": sources("20260814OBHT0", 80101089),
    },
    {
        "id": "20260814SKLG0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료",
        "away": "SSG", "home": "LG", "away_score": 5, "home_score": 3,
        "winner_pitcher": "전영준", "loser_pitcher": "김진성", "save_pitcher": "조병현",
        "headline": "SSG가 8회 김재환의 결승 2점 홈런으로 LG에 5-3 승리",
        "winner_points": [
            "SSG 선발 최민준은 5⅔이닝 2피안타 1사사구 3탈삼진 2실점으로 버텼다.",
            "8회 김재환이 2점 홈런을 쳐 2-2 균형을 깨고 결승점을 만들었다.",
            "김재환은 4타수 1안타 1홈런 2타점, 최지훈은 4타수 3안타, 박성한은 4타수 2안타 2득점을 기록했다.",
            "전영준이 1이닝 무실점으로 승리, 문승원이 홀드, 조병현이 1이닝 1실점으로 시즌 5세이브를 기록했다.",
        ],
        "opponent_effort": "LG는 9회 문정빈의 솔로 홈런으로 한 점 차까지 좁혔고 송찬의와 오스틴도 각각 1타점씩 보탰다.",
        "sources": sources("20260814SKLG0", 80101090),
    },
    {
        "id": "20260814WOKT0", "stadium": "수원", "start_time": "19:00", "status": "경기 종료",
        "away": "키움", "home": "KT", "away_score": 3, "home_score": 8,
        "winner_pitcher": "전용주", "loser_pitcher": "배동현", "save_pitcher": "",
        "headline": "KT가 6회 4득점으로 키움을 8-3으로 꺾었다",
        "winner_points": [
            "KT 선발 고영표는 5⅓이닝 3피안타 3사사구 8탈삼진 3실점을 기록했다.",
            "KT는 6회 4점을 뽑아 2-3 열세를 6-3으로 뒤집었고, 안현민의 만루 유격수 땅볼이 결승타가 됐다.",
            "최원준은 5타수 3안타 2타점 2득점, 김현수는 3타수 2안타 1타점, 힐리어드는 3타수 1안타 2타점을 기록했다.",
            "전용주가 ⅔이닝 무실점으로 승리했고 주권이 1이닝 무실점 홀드를 기록했다.",
        ],
        "opponent_effort": "키움은 데이비슨이 4타수 1안타 1홈런 2타점으로 6회 추격의 불씨를 살렸고 권혁빈이 4타수 2안타를 기록했다.",
        "sources": sources("20260814WOKT0", 80101091),
    },
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": True, "role": "starter", "game_decision": None, "innings": "5", "hits": 8, "runs": 6, "earned_runs": 6, "walks_hbp": 3, "strikeouts": 5, "home_runs": 2, "pitches": 85, "season_record": "5승 5패", "era": "3.46"},
    {"name": "김원중", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "0", "hits": 1, "runs": 3, "earned_runs": 3, "walks_hbp": 2, "strikeouts": 0, "home_runs": 0, "pitches": 9, "season_record": "1승 4패", "season_saves": 5, "era": "4.35"},
    {"name": "박정민", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 2, "home_runs": 0, "pitches": 24, "season_record": "5승 2패", "season_saves": 1, "era": "4.10"},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 1, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 1, "avg": "0.303", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 0, "runs": 1, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.272", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.294", "obp": None, "ops": None},
]

verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW·상세기록", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-14 KBO 정규시즌 5경기는 모두 최종 종료했다. kbo-game FINISHED 상태, KBO 공식 게임센터 대상 URL, 네이버 공개 기록 API의 statusCode=4·스코어·박스스코어, 다음 일정 API의 gameStatus=END·스코어를 대조했다. 관심 투수의 등판·당일 기록·시즌 승패·ERA는 네이버 당일 기록을 KBO 공식 게임센터 대상으로 대조했으며, 선발/구원 및 당일 결정 기록은 KBO 공식 기준으로 분류했다. 김원중은 공식 패전이나 구원투수의 화면 배지는 세이브·홀드·블론만 허용하는 계약에 따라 game_decision은 null로 기록했다. 타자 시즌 OBP·OPS는 대조하지 않아 넣지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-08-13", DATE, text)
    text = re.sub(r"2026\.08\.13", "2026.08.14", text)
    text = text.replace("2026년 8월 12일", "2026년 8월 14일").replace("2026년 8월 13일", "2026년 8월 14일")
    text = re.sub(r"Generated 2026-08-14 06:20 KST", "Generated 2026-08-15 06:20 KST", text)
    path.write_text(text, encoding="utf-8")

print(f"wrote verified KBO data for {DATE} at {NOW}")
