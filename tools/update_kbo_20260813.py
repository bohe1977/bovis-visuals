#!/usr/bin/env python3
"""Normalize verified 2026-08-13 KBO results into the BOVIS report data contract."""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-13"
DATE_COMPACT = DATE.replace("-", "")
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")

KBO = "https://www.koreabaseball.com"
OFFICIAL_SCOREBOARD = f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={DATE_COMPACT}"


def source_urls(game_id: str, naver_id: str, daum_id: int) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={DATE_COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{naver_id}/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{daum_id}"},
    ]


games = [
    {
        "id": "20260813HHOB0", "stadium": "잠실", "start_time": "19:00", "status": "경기 종료",
        "away": "한화", "home": "두산", "away_score": 6, "home_score": 9,
        "winner_pitcher": "최민석", "loser_pitcher": "류현진", "save_pitcher": "이영하",
        "headline": "두산이 3회 3득점 포함 초반 공세로 한화에 9-6 승리",
        "winner_points": [
            "두산 선발 최민석은 5이닝 6피안타 2실점(2자책) 3탈삼진으로 시즌 10승째를 거뒀다.",
            "두산은 1~4회 8점을 뽑아 주도권을 잡았고, 3회 3득점이 승부의 분수령이 됐다.",
            "두산은 양의지가 4타수 2안타 1홈런 3타점 2득점, 박찬호가 4타수 3안타 1타점으로 공격을 이끌었다.",
            "김택연이 1⅔이닝 무실점 홀드, 이영하가 1이닝 무실점으로 시즌 18세이브를 기록했다.",
        ],
        "opponent_effort": "한화는 7회 3득점으로 추격했고 페라자가 5타수 2안타 1홈런 1타점, 노시환이 5타수 1안타 1홈런 2타점으로 분전했다.",
        "sources": source_urls("20260813HHOB0", "20260813HHOB02026", 80101082),
    },
    {
        "id": "20260813LTSK0", "stadium": "문학", "start_time": "19:00", "status": "경기 종료",
        "away": "롯데", "home": "SSG", "away_score": 11, "home_score": 0,
        "winner_pitcher": "로드리게스", "loser_pitcher": "타케다", "save_pitcher": "",
        "headline": "롯데가 13안타·4홈런과 완봉 계투로 SSG에 11-0 승리",
        "winner_points": [
            "롯데 선발 로드리게스는 6이닝 5피안타 1볼넷 5탈삼진 무실점으로 시즌 7승째를 거뒀다.",
            "롯데는 3회 3득점, 4회 4득점으로 일찌감치 승기를 잡았다.",
            "롯데는 황성빈이 4타수 2안타 1타점, 나승엽이 5타수 1안타 1타점으로 타선을 이끌었고 팀이 4홈런을 기록했다.",
            "박정민·이민석·박세진이 각각 1이닝 무실점으로 완봉을 완성했다.",
        ],
        "opponent_effort": "SSG는 선발 타케다가 5이닝 10피안타 9실점으로 고전했지만, 박성한이 2타수 1안타 1볼넷으로 출루하며 팀 타선에서 분전했다.",
        "sources": source_urls("20260813LTSK0", "20260813LTSK02026", 80101085),
    },
    {
        "id": "20260813SSHT0", "stadium": "광주", "start_time": "19:00", "status": "경기 종료",
        "away": "삼성", "home": "KIA", "away_score": 9, "home_score": 8,
        "winner_pitcher": "김재윤", "loser_pitcher": "조상우", "save_pitcher": "",
        "headline": "삼성이 9회 2득점으로 KIA에 9-8 역전승",
        "winner_points": [
            "삼성 선발 원태인은 5⅔이닝 9피안타 6실점으로 물러났고, 김재윤이 1⅔이닝 무실점으로 시즌 6승째를 거뒀다.",
            "삼성은 9회 2점을 올려 7-8 열세를 뒤집으며 결승점을 만들었다.",
            "삼성은 이재현이 5타수 2안타 3타점 1득점, 디아즈가 5타수 2안타 1타점 2득점으로 공격을 이끌었다.",
            "성영탁이 1⅓이닝 무실점 홀드를 기록했고, 김재윤이 마지막 1⅔이닝을 막아 역전승을 지켰다.",
        ],
        "opponent_effort": "KIA는 김선빈이 5타수 3안타 3타점 3득점, 김도영이 3타수 1안타 1타점 1득점 2볼넷으로 활약했으나 9회 리드를 지키지 못했다.",
        "sources": source_urls("20260813SSHT0", "20260813SSHT02026", 80101086),
    },
    {
        "id": "20260813KTNC0", "stadium": "창원", "start_time": "19:00", "status": "경기 종료",
        "away": "KT", "home": "NC", "away_score": 5, "home_score": 6,
        "winner_pitcher": "이용준", "loser_pitcher": "손동현", "save_pitcher": "임지민",
        "headline": "NC가 7회 3득점으로 흐름을 바꿔 KT에 6-5 승리",
        "winner_points": [
            "NC 선발 테일러는 7이닝 5피안타 4실점 6탈삼진을 기록했고, 이용준이 ⅔이닝 무실점으로 승리를 챙겼다.",
            "NC는 7회 3득점으로 2-4 열세를 뒤집어 결승점을 만들었다.",
            "NC는 김주원이 3타수 1안타 1홈런 1타점 2득점, 박건우가 4타수 2안타 2타점으로 타선을 이끌었다.",
            "이용준이 ⅔이닝 무실점으로 흐름을 끊었고, 임지민이 ⅔이닝 무실점으로 시즌 6세이브를 올렸다.",
        ],
        "opponent_effort": "KT는 강백호가 5타수 1안타 2득점, 황재균이 4타수 2안타 1홈런 2타점으로 맞섰고 8회 1점을 더했으나 동점에는 닿지 못했다.",
        "sources": source_urls("20260813KTNC0", "20260813KTNC02026", 80101083),
    },
    {
        "id": "20260813LGWO0", "stadium": "고척", "start_time": "19:00", "status": "경기 종료",
        "away": "LG", "home": "키움", "away_score": 13, "home_score": 6,
        "winner_pitcher": "톨허스트", "loser_pitcher": "알칸타라", "save_pitcher": "",
        "headline": "LG가 5회 8득점 빅이닝으로 키움에 13-6 승리",
        "winner_points": [
            "LG 선발 톨허스트는 6이닝 11피안타 6실점 9탈삼진으로 시즌 10승째를 거뒀다.",
            "LG는 5회 8득점으로 2-4 열세를 단숨에 뒤집어 승부를 갈랐다.",
            "LG는 오스틴이 5타수 3안타 1홈런 4타점 2득점, 박해민이 5타수 1안타 3타점으로 대량 득점을 이끌었다.",
            "이우찬·김영우·이정용이 나란히 1이닝 무실점으로 남은 3이닝을 막았다.",
        ],
        "opponent_effort": "키움은 서건창이 4타수 2안타 1홈런 2타점, 송성문이 5타수 2안타 2타점으로 초반 리드를 만들었지만 5회 대량 실점을 막지 못했다.",
        "sources": source_urls("20260813LGWO0", "20260813LGWO02026", 80101084),
    },
]

player_sources = {
    "kbo_official": [OFFICIAL_SCOREBOARD] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={DATE_COMPACT}&toDate={DATE_COMPACT}"] + [g["sources"][2]["url"] for g in games],
}

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "role": "starter", "game_decision": None, "innings": "5 ⅔", "hits": 9, "runs": 6, "earned_runs": 6, "walks_hbp": 2, "strikeouts": 2, "home_runs": 0, "pitches": 87, "season_record": "6승 5패", "era": "4.44"},
    {"name": "류현진", "team": "한화", "appeared": True, "role": "starter", "game_decision": "패", "innings": "3 ⅓", "hits": 9, "runs": 8, "earned_runs": 7, "walks_hbp": 2, "strikeouts": 3, "home_runs": 1, "pitches": 71, "season_record": "8승 4패", "era": "3.91"},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": False},
    {"name": "박정민", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 2, "home_runs": 0, "pitches": 10, "season_record": "5승 2패", "era": "4.21"},
    {"name": "로드리게스", "team": "롯데", "appeared": True, "role": "starter", "game_decision": "승", "innings": "6", "hits": 5, "runs": 0, "earned_runs": 0, "walks_hbp": 1, "strikeouts": 5, "home_runs": 0, "pitches": 80, "season_record": "7승 8패", "era": "3.81"},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "role": "reliever", "game_decision": None, "innings": "0 ⅓", "hits": 2, "runs": 3, "earned_runs": 3, "walks_hbp": 1, "strikeouts": 0, "home_runs": 1, "pitches": 17, "season_record": "2승 1패", "season_saves": 2, "era": "6.62"},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 1, "rbi": 0, "runs": 2, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.301", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 1, "rbi": 2, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 2, "avg": "0.272", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 3, "hits": 1, "rbi": 1, "runs": 1, "home_runs": 0, "walks": 2, "strikeouts": 0, "avg": "0.297", "obp": None, "ops": None},
]

kbo_data = {"date": DATE, "generated_at": NOW, "source_urls": player_sources, "games": games}
player_data = {
    "report_date": DATE, "generated_at": NOW,
    "verification": {
        "status": "KBO 공식 기준 · 네이버·다음 대조",
        "sources": ["KBO 공식 게임센터 REVIEW·상세기록", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
        "details": "2026-08-13 KBO 정규시즌 5경기가 모두 최종 종료했다. kbo-game FINISHED 상태, KBO 공식 게임센터 대상 경기, 네이버 공개 기록 API의 statusCode=4·스코어·박스스코어, 다음 일정 API의 gameStatus=END·스코어를 대조했다. 관심 투수의 등판·이닝·피안타·4사구·탈삼진·자책·시즌 승패·ERA는 네이버 당일 투수 기록을 KBO 공식 게임센터 대상 URL과 대조했다. 선발/구원 및 당일 승·패·세이브·홀드는 KBO 공식 결정 기록을 기준으로 기록했으며, 네이버 wls로 재확인했다. 정해영은 구원 등판·결정 없음이며 시즌 2세이브를 공식·네이버 기록으로 확인했다. 타자 시즌 OBP·OPS는 교차확인되지 않아 넣지 않았다.",
        "conflicts": [],
    },
    "pitchers": pitchers, "batters": batters, "source_urls": player_sources,
}

(ROOT / "kbo" / "data.json").write_text(json.dumps(kbo_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps(player_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for html_path in [ROOT / "kbo" / "index.html", ROOT / "kbo-players" / "index.html"]:
    text = html_path.read_text(encoding="utf-8")
    text = text.replace("2026-08-12", DATE).replace("2026.08.12", "2026.08.13")
    text = text.replace("2026-08-13 15:43", "2026-08-14 06:20")
    html_path.write_text(text, encoding="utf-8")

print(f"wrote KBO data for {DATE} at {NOW}")
