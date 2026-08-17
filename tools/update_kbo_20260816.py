#!/usr/bin/env python3
"""Normalize cross-checked 2026-08-16 KBO final results for BOVIS."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-16"
COMPACT = "20260816"
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = (
    "https://sports.daum.net/prx/hermes/api/game/schedule.json?"
    "page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260816&toDate=20260816"
)


def sources(game_id: str, daum_id: int) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{daum_id}"},
    ]


# kbo-game FINISHED + KBO official/ Naver statusCode=4 + Daum END only.
games = [
    {
        "id": "20260816SKLG0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료",
        "away": "SSG", "home": "LG", "away_score": 6, "home_score": 0,
        "winner_pitcher": "아빌라", "loser_pitcher": "카라스코", "save_pitcher": "",
        "headline": "SSG가 아빌라의 7이닝 무실점과 5회 집중타로 LG에 6-0 승리",
        "winner_points": [
            "SSG 선발 아빌라는 7이닝 4피안타 2사사구 8탈삼진 무실점으로 시즌 4승째를 올렸다.",
            "0-0이던 5회 1사 2·3루에서 정준재가 중전 결승 2타점 적시타를 쳤고, SSG는 그 이닝에 4점을 냈다.",
            "한유섬은 4타수 3안타 1홈런 2타점, 마드리스는 3타수 2안타 1홈런 1타점 2득점으로 장타를 보탰다.",
            "전영준과 이건욱이 각각 1이닝 무실점으로 이어 던져 팀 완봉을 마무리했다.",
        ],
        "opponent_effort": "LG는 신민재가 4타수 2안타를 기록했고 카라스코가 5⅓이닝 8피안타 8탈삼진 5실점으로 버텼지만 득점권 타선이 막혔다.",
        "sources": sources("20260816SKLG0", 80101100),
    },
    {
        "id": "20260816OBHT0", "stadium": "광주", "start_time": "19:00", "status": "경기 종료",
        "away": "두산", "home": "KIA", "away_score": 1, "home_score": 2,
        "winner_pitcher": "올러", "loser_pitcher": "곽빈", "save_pitcher": "이의리",
        "headline": "KIA가 박재현의 3회 솔로포와 올러의 호투로 두산에 2-1 승리",
        "winner_points": [
            "KIA 선발 올러는 7이닝 4피안타 무사사구 6탈삼진 1실점으로 시즌 11승째를 기록했다.",
            "박재현이 3회 곽빈을 상대로 우월 솔로 홈런을 쳐 1-1 균형을 깼고, 결승타는 공식 기록상 없었다.",
            "박재현은 4타수 2안타 1홈런 1타점 1득점, 김도영은 4타수 2안타 2루타를 기록했다.",
            "전상현이 8회 홀드, 이의리가 9회 1⅓이닝 무실점으로 시즌 2세이브를 올렸다.",
        ],
        "opponent_effort": "두산은 안재석과 조수행이 각각 2안타를 쳤고, 곽빈은 7이닝 7피안타 5탈삼진 2실점(1자책)으로 퀄리티스타트를 남겼다.",
        "sources": sources("20260816OBHT0", 80101099),
    },
    {
        "id": "20260816WOKT0", "stadium": "수원", "start_time": "19:00", "status": "경기 종료",
        "away": "키움", "home": "KT", "away_score": 2, "home_score": 6,
        "winner_pitcher": "로건", "loser_pitcher": "김성민", "save_pitcher": "박영현",
        "headline": "KT가 최원준의 6회 결승타와 박영현의 세이브로 키움에 6-2 승리",
        "winner_points": [
            "KT 선발 로건은 6이닝 6피안타 4사사구 4탈삼진 2실점으로 시즌 4승째를 거뒀다.",
            "2-2이던 6회 2사 1·2루에서 최원준이 중전 결승타를 쳐 균형을 깼고, KT는 그 이닝 3점을 냈다.",
            "최원준은 5타수 4안타 2타점, 안현민은 5타수 2안타 1홈런 2타점으로 중심 타선을 이끌었다.",
            "김민수·전용주·우규민이 홀드를 나눠 챙겼고, 박영현이 1⅓이닝 무실점으로 시즌 22세이브를 기록했다.",
        ],
        "opponent_effort": "키움은 추재현이 2타수 2안타 1타점 2볼넷으로 4차례 출루했고, 박찬혁도 3타수 2안타 1볼넷으로 맞섰다.",
        "sources": sources("20260816WOKT0", 80101101),
    },
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}

# Park Younghyun closed KT's win; all other watched pitchers did not appear.
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
    {"name": "박영현", "team": "KT", "appeared": True, "role": "reliever", "game_decision": "세이브",
     "innings": "1 ⅓", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 2, "strikeouts": 1, "home_runs": 0,
     "season_record": "6승 0패", "season_saves": 22, "era": "2.30"},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": False},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 2, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.296", "obp": None, "ops": None},
]

verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW·상세기록", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-16 KBO 예정 5경기 중 한화-삼성과 NC-롯데는 취소되어 제외했다. 나머지 3경기는 kbo-game FINISHED, KBO 공식 게임센터 상세기록, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조했다. 박영현은 KT전 공식·네이버 투수 목록에서 1⅓이닝 무피안타 2사사구 1탈삼진 무실점, 세이브, 시즌 22세이브로 확인했다. 나머지 관심 투수는 완료된 경기의 공식·네이버 투수 목록에서 모두 미등판으로 확인했다. 김도영의 4타수 2안타·1삼진·시즌 타율 0.296은 KBO 공식 상세기록과 네이버 API에서 대조했다. 다음은 타자 볼넷을 사사구로 표기할 수 있어 해당 필드는 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

replacements = {
    "2026-08-15": DATE,
    "2026.08.15": "2026.08.16",
    "2026년 8월 15일": "2026년 8월 16일",
    "Generated 2026-08-16 06:20 KST": "Generated 2026-08-17 06:20 KST",
    "2026-08-15 06:20 KST": "2026-08-16 06:20 KST",
}
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

print(f"wrote cross-checked KBO data for {DATE} at {NOW}")
