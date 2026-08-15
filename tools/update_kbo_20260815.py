#!/usr/bin/env python3
"""Normalize cross-checked 2026-08-15 KBO final results for BOVIS."""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-15"
COMPACT = DATE.replace("-", "")
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = (
    "https://sports.daum.net/prx/hermes/api/game/schedule.json?"
    "page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260815&toDate=20260815"
)


def sources(game_id: str, daum_id: int) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{daum_id}"},
    ]


# Only completed games are deliberately included.
games = [
    {
        "id": "20260815SKLG0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료",
        "away": "SSG", "home": "LG", "away_score": 1, "home_score": 4,
        "winner_pitcher": "김진수", "loser_pitcher": "김건우", "save_pitcher": "손주영",
        "headline": "LG가 문정빈의 6회 결승 홈런을 앞세워 SSG에 4-1 승리",
        "winner_points": [
            "LG 선발 박시원은 4이닝 4피안타 1사사구 5탈삼진 1실점, 이우찬은 1⅔이닝 무실점으로 뒤를 받쳤다.",
            "문정빈이 6회 무사에서 중월 솔로포로 결승타를 만들었고, LG는 8회 박동원의 2점 홈런으로 격차를 벌렸다.",
            "오스틴은 4타수 3안타 1득점, 문정빈은 3타수 1안타 1홈런 1타점, 박동원은 4타수 1안타 2타점을 기록했다.",
            "김진수가 1⅓이닝 무실점으로 승리를 챙겼고 우강훈이 홀드, 손주영이 1⅓이닝 무실점으로 시즌 23세이브를 기록했다.",
        ],
        "opponent_effort": "SSG는 한유섬이 3타수 1안타 1홈런 1타점으로 5회 선제점을 만들었고, 김건우가 6이닝 5피안타 9탈삼진 2실점으로 버텼다.",
        "sources": sources("20260815SKLG0", 80101095),
    },
    {
        "id": "20260815HHSS0", "stadium": "대구", "start_time": "19:00", "status": "경기 종료",
        "away": "한화", "home": "삼성", "away_score": 6, "home_score": 11,
        "winner_pitcher": "배찬승", "loser_pitcher": "이상규", "save_pitcher": "",
        "headline": "삼성이 6~8회 9득점으로 한화에 11-6 승리",
        "winner_points": [
            "삼성은 선발 양창섭 조기 강판 뒤 이승현이 5⅔이닝 2피안타 7탈삼진 1실점으로 긴 이닝을 책임졌다.",
            "6회 최형우의 3점 홈런으로 흐름을 바꾼 뒤, 7회 구자욱의 결승 좌전 안타를 포함해 3점을 더해 8-6으로 달아났다.",
            "구자욱은 5타수 3안타 1홈런 5타점, 최형우는 4타수 3안타 1홈런 3타점, 박승규는 3타수 2안타 2타점 3득점을 올렸다.",
            "배찬승이 1⅓이닝 무실점으로 승리를 기록했고, 이승민이 마지막 1이닝을 무실점으로 마무리했다.",
        ],
        "opponent_effort": "한화는 7회 페라자의 2점 홈런과 채은성·허인서의 솔로포 등으로 4점을 만회했고, 이원석이 4타수 2안타 2득점을 기록했다.",
        "sources": sources("20260815HHSS0", 80101092),
    },
    {
        "id": "20260815NCLT0", "stadium": "사직", "start_time": "19:00", "status": "경기 종료",
        "away": "NC", "home": "롯데", "away_score": 5, "home_score": 8,
        "winner_pitcher": "이이무라", "loser_pitcher": "김진호", "save_pitcher": "최준용",
        "headline": "롯데가 고승민의 7회 결승 3점 홈런으로 NC에 8-5 승리",
        "winner_points": [
            "롯데 선발 박세웅은 6⅔이닝 9피안타 무사사구 2탈삼진 4실점(2자책)을 기록했다.",
            "7회 고승민이 무사 1·2루에서 우월 3점 홈런으로 결승타를 만들며 7-3으로 달아났다.",
            "고승민은 3타수 1안타 1홈런 3타점, 한동희는 4타수 3안타 2타점, 안중열은 4타수 4안타 1타점으로 공격을 이끌었다.",
            "이이무라가 1⅓이닝 1실점으로 승리했고 최요한이 홀드, 최준용이 1이닝 무실점으로 시즌 15세이브를 올렸다.",
        ],
        "opponent_effort": "NC는 13안타를 기록했고 안중열이 4타수 4안타 1타점, 천재환이 4타수 3안타, 박민우가 5타수 2안타 2득점으로 분전했다.",
        "sources": sources("20260815NCLT0", 80101093),
    },
    {
        "id": "20260815OBHT0", "stadium": "광주", "start_time": "19:00", "status": "경기 종료",
        "away": "두산", "home": "KIA", "away_score": 1, "home_score": 6,
        "winner_pitcher": "양현종", "loser_pitcher": "최승용", "save_pitcher": "",
        "headline": "KIA가 박재현의 2회 결승 2루타를 앞세워 두산에 6-1 승리",
        "winner_points": [
            "KIA 선발 양현종은 6이닝 6피안타 3사사구 4탈삼진 1실점으로 승리를 기록했다.",
            "박재현이 2회 1사 1·2루에서 중견수 쪽 2루타로 결승타를 만들었고, KIA는 1~4회 매 이닝 득점으로 주도권을 잡았다.",
            "카스트로는 5타수 3안타 1타점, 박재현은 5타수 2안타 2타점, 김도영은 4타수 1안타 1홈런 1타점 2득점을 기록했다.",
            "전상현·조상우·이의리가 각각 1이닝을 맡아 1피안타 무실점 계투를 완성했다.",
        ],
        "opponent_effort": "두산은 김대한이 5타수 3안타 1득점, 박준순이 3타수 1안타 1타점을 기록했고 최승용은 3⅔이닝 7피안타 4자책으로 패전했다.",
        "sources": sources("20260815OBHT0", 80101094),
    },
    {
        "id": "20260815WOKT0", "stadium": "수원", "start_time": "19:00", "status": "경기 종료",
        "away": "키움", "home": "KT", "away_score": 10, "home_score": 5,
        "winner_pitcher": "하영민", "loser_pitcher": "오원석", "save_pitcher": "",
        "headline": "키움이 박찬혁의 1회 결승 3점 홈런으로 KT에 10-5 승리",
        "winner_points": [
            "키움 선발 하영민은 6이닝 7피안타 2사사구 4탈삼진 4실점(2자책)으로 승리를 기록했다.",
            "박찬혁이 1회 1사 1·2루에서 좌월 3점 홈런으로 결승타를 만들었고, 키움은 3회 5득점으로 리드를 넓혔다.",
            "박찬혁은 4타수 2안타 1홈런 3타점 2득점, 김건희는 5타수 1안타 2타점, 안치홍은 2타수 1안타 1홈런 2타점을 기록했다.",
            "박지성·김선기가 각각 1이닝 무실점, 유토가 ⅔이닝 무실점으로 리드를 지켰다.",
        ],
        "opponent_effort": "KT는 최원준이 5타수 3안타 1타점, 김현수가 5타수 2안타 1타점, 안현민이 5타수 1안타 2타점으로 추격했으나 초반 8실점이 컸다.",
        "sources": sources("20260815WOKT0", 80101096),
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
    {"name": "박세웅", "team": "롯데", "appeared": True, "role": "starter", "game_decision": None,
     "innings": "6 ⅔", "hits": 9, "runs": 4, "earned_runs": 2, "walks_hbp": 0, "strikeouts": 2, "home_runs": 0, "pitches": 76, "season_record": "2승 7패", "era": "4.77"},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None,
     "innings": "0", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0, "pitches": 5, "season_record": "1승 4패", "season_saves": 5, "era": "4.35"},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 1, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.302", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 3, "hits": 1, "rbi": 0, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 0, "avg": "0.272", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 1, "runs": 2, "home_runs": 1, "walks": 1, "strikeouts": 1, "avg": "0.294", "obp": None, "ops": None},
]

verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW·상세기록", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-15 KBO 정규시즌 5경기는 모두 최종 종료했다. kbo-game FINISHED 상태, KBO 공식 게임센터 REVIEW 대상 URL, 네이버 공개 기록 API의 statusCode=4·스코어·박스스코어, 다음 일정 API의 gameStatus=END·스코어를 대조했다. 관심 투수의 등판·당일 기록·시즌 승패·ERA는 네이버 당일 기록을 KBO 공식 게임센터 대상으로 대조했고, 선발/구원과 당일 결정 기록은 공식 게임센터 결정기록을 기준으로 분류했다. 박세웅은 선발·결정 없음, 김원중은 구원·결정 없음이다. 김원중의 시즌 세이브는 네이버 당일 기록의 s=5로 확인했다. 타자 시즌 OBP·OPS는 별도 대조하지 않아 넣지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(
    json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
(ROOT / "kbo-players" / "data.json").write_text(
    json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-08-14", DATE).replace("2026.08.14", "2026.08.15")
    text = text.replace("2026년 8월 14일", "2026년 8월 15일")
    text = text.replace("Generated 2026-08-15 06:20 KST", "Generated 2026-08-16 06:20 KST")
    path.write_text(text, encoding="utf-8")

print(f"wrote cross-checked KBO data for {DATE} at {NOW}")
