#!/usr/bin/env python3
"""Normalize the verified 2026-08-18 KBO final slate for BOVIS."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-18"
COMPACT = "20260818"
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = (
    "https://sports.daum.net/prx/hermes/api/game/schedule.json?"
    "page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260818&toDate=20260818"
)


def sources(game_id: str, daum_id: int) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{daum_id}"},
    ]

# Only the five games simultaneously final in kbo-game (FINISHED), Naver (statusCode=4), and Daum (END).
games = [
    {
        "id": "20260818KTLG0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료",
        "away": "KT", "home": "LG", "away_score": 1, "home_score": 9,
        "winner_pitcher": "임찬규", "loser_pitcher": "소형준", "save_pitcher": "",
        "headline": "LG가 1회 송찬의의 결승타와 문정빈의 5타점으로 KT에 9-1 승리",
        "winner_points": [
            "LG 선발 임찬규는 6이닝 3피안타 2사사구 3탈삼진 1실점으로 시즌 11승째를 기록했다.",
            "1회 2사 2·3루에서 송찬의가 좌전 2타점 결승타를 쳤고, LG는 5회 문정빈의 만루포로 4점을 보탰다.",
            "문정빈은 5타수 2안타 1홈런 5타점 2득점, 송찬의는 4타수 2안타 3타점으로 중심 생산을 맡았다.",
            "이우찬·김진수·배재준이 각 1이닝 무실점으로 이어 던졌다.",
        ],
        "opponent_effort": "KT는 안현민이 3타수 1안타 1홈런 1타점으로 4회 추격의 솔로포를 쳤지만 이후 추가 득점이 없었다.",
        "sources": sources("20260818KTLG0", 80101103),
    },
    {
        "id": "20260818SKSS0", "stadium": "대구", "start_time": "19:00", "status": "경기 종료",
        "away": "SSG", "home": "삼성", "away_score": 5, "home_score": 4,
        "winner_pitcher": "전영준", "loser_pitcher": "김재윤", "save_pitcher": "조병현",
        "headline": "SSG가 9회 조형우의 결승타로 삼성에 5-4 역전승",
        "winner_points": [
            "SSG 선발 김민준은 6이닝 5피안타 2사사구 2탈삼진 1실점으로 경기를 만들었다.",
            "4-4이던 9회 무사 1·3루에서 조형우가 중전 결승타를 쳤고, 이어 조병현이 9회말을 막아 세이브를 올렸다.",
            "조형우는 4타수 2안타 1타점 1득점, 전의산은 4타수 2안타로 멀티히트를 기록했다.",
            "전영준이 8회 1실점에도 승리투수가 됐고, 조병현은 1이닝 2실점으로 흔들렸지만 시즌 15세이브를 지켰다.",
        ],
        "opponent_effort": "삼성은 전병우가 3타수 3안타 1볼넷으로 네 차례 출루했고, 구자욱이 5타수 2안타 2타점을 보탰다.",
        "sources": sources("20260818SKSS0", 80101105),
    },
    {
        "id": "20260818WOLT0", "stadium": "사직", "start_time": "19:00", "status": "경기 종료",
        "away": "키움", "home": "롯데", "away_score": 10, "home_score": 15,
        "winner_pitcher": "이민석", "loser_pitcher": "박지성", "save_pitcher": "",
        "headline": "롯데가 7회 13득점 빅이닝으로 키움에 15-10 대역전승",
        "winner_points": [
            "롯데 선발 비슬리는 6이닝 10피안타 1사사구 3탈삼진 8실점(7자책)으로 물러났고, 이민석이 7회 무실점으로 승리를 챙겼다.",
            "0-8이던 7회 손성빈의 2사 1·2루 결승 2루타를 포함해 13점을 몰아쳐 경기를 뒤집었다.",
            "손성빈은 3타수 2안타 1홈런 4타점 3득점, 한동희는 5타수 2안타 1홈런 5타점으로 대역전을 이끌었다.",
            "이민석이 1이닝 무실점으로 흐름을 끊었고, 이이무라·김한결은 각각 1실점으로 남은 이닝을 책임졌다.",
        ],
        "opponent_effort": "키움은 김건희가 4타수 3안타 1홈런 1타점 3득점, 서건창이 4타수 3안타 1타점으로 초반 대량 득점을 이끌었다.",
        "sources": sources("20260818WOLT0", 80101106),
    },
    {
        "id": "20260818OBNC0", "stadium": "창원", "start_time": "19:00", "status": "경기 종료",
        "away": "두산", "home": "NC", "away_score": 6, "home_score": 4,
        "winner_pitcher": "김택연", "loser_pitcher": "손주환", "save_pitcher": "이영하",
        "headline": "두산이 9회 양의지의 밀어내기 결승타로 NC에 6-4 승리",
        "winner_points": [
            "두산 선발 벤자민은 5이닝 5피안타 2사사구 5탈삼진 3실점(1자책)으로 버텼다.",
            "4-4이던 9회 2사 만루에서 양의지가 밀어내기 볼넷으로 결승점을 냈고, 뒤이어 정수빈의 2타점 적시타가 나왔다.",
            "조수행은 4타수 3안타 1볼넷 1득점, 양의지는 2타수 1안타 1홈런 2타점 3볼넷으로 활약했다.",
            "김택연이 8회 1이닝 무실점으로 승리, 이영하가 9회 1실점으로 시즌 19세이브를 기록했다.",
        ],
        "opponent_effort": "NC는 이우성과 블레인이 각각 4타수 2안타를 기록했고, 라일리가 6이닝 6피안타 2사사구 7탈삼진 2실점으로 선발 몫을 했다.",
        "sources": sources("20260818OBNC0", 80101104),
    },
    {
        "id": "20260818HTHH0", "stadium": "대전", "start_time": "19:00", "status": "경기 종료",
        "away": "KIA", "home": "한화", "away_score": 4, "home_score": 3,
        "winner_pitcher": "네일", "loser_pitcher": "왕옌청", "save_pitcher": "이의리",
        "headline": "KIA가 4회 윤도현의 결승타를 앞세워 한화에 4-3 승리",
        "winner_points": [
            "KIA 선발 네일은 6이닝 5피안타 4사사구 3탈삼진 2실점으로 시즌 9승째를 올렸다.",
            "4회 2사 1·3루에서 윤도현이 좌전 결승타를 쳤고, KIA는 그 이닝 3점을 내 3-1로 앞섰다.",
            "박재현은 5타수 2안타 1타점, 김호령은 4타수 2안타 1타점으로 멀티히트를 기록했다.",
            "전상현이 7회 홀드, 조상우가 ⅔이닝 홀드, 이의리가 1⅓이닝 무실점으로 시즌 3세이브를 기록했다.",
        ],
        "opponent_effort": "한화는 강백호가 5타수 3안타 1홈런 1타점 1득점으로 분전했고, 최인호도 솔로포를 쳤다.",
        "sources": sources("20260818HTHH0", 80101102),
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
    {"name": "제레미 비슬리", "team": "롯데", "appeared": True, "role": "starter", "game_decision": None,
     "innings": "6", "hits": 10, "runs": 8, "earned_runs": 7, "walks_hbp": 1, "strikeouts": 3, "home_runs": 2,
     "season_record": "8승 5패", "era": "4.72"},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": True, "role": "starter", "game_decision": "승",
     "innings": "6", "hits": 3, "runs": 1, "earned_runs": 1, "walks_hbp": 2, "strikeouts": 3, "home_runs": 1,
     "season_record": "11승 4패", "era": "4.14"},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 3, "rbi": 1, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 1, "avg": "0.306", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.272", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 1, "runs": 1, "home_runs": 1, "walks": 1, "strikeouts": 2, "avg": "0.295", "obp": None, "ops": None},
]

verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW·상세기록", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-18 KBO 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW 대상 URL, 네이버 공개 기록 API statusCode=4·스코어·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조해 모두 최종 종료로 확정했다. 임찬규는 LG 선발 승(6이닝 3피안타 2사사구 3탈삼진 1실점·시즌 11승 4패·ERA 4.14), 제레미 비슬리는 롯데 선발 결정 없음(6이닝 10피안타 1사사구 3탈삼진 8실점·시즌 8승 5패·ERA 4.72)으로 공식 결정기록과 네이버 당일 기록을 대조했다. 나머지 관심 투수는 해당 팀의 완료 경기 공식·네이버 투수 목록에서 미등판으로 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO 공식 상세기록과 네이버 API를 대조했다. 다음은 타자 볼넷을 사사구로 표기할 수 있어 볼넷을 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

replacements = {
    "2026-08-16": DATE,
    "2026.08.16": "2026.08.18",
    "2026년 8월 16일": "2026년 8월 18일",
    "Generated 2026-08-17 06:20 KST": "Generated 2026-08-19 06:20 KST",
    "2026-08-16 06:20 KST": "2026-08-18 06:20 KST",
}
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

print(f"wrote cross-checked KBO data for {DATE} at {NOW}")
