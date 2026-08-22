#!/usr/bin/env python3
"""Write the reconciled 2026-08-22 KBO final-game report from captured official/API records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-22", "20260822"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260822&toDate=20260822"
DAUM_IDS = {"20260822HTWO0": 80101122, "20260822SSNC0": 80101126}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


# Only games simultaneously FINISHED (kbo-game), statusCode=4 (Naver), and END (Daum).
games = [
    {
        "id": "20260822HTWO0", "stadium": "고척", "start_time": "18:00", "status": "경기 종료",
        "away": "KIA", "home": "키움", "away_score": 1, "home_score": 3,
        "winner_pitcher": "안우진", "loser_pitcher": "올러", "save_pitcher": "유토",
        "headline": "키움이 안우진의 7이닝 무실점과 서건창의 결승 2타점으로 KIA에 3-1 승리",
        "winner_points": [
            "키움 선발 안우진은 7이닝 4피안타 1사사구 6탈삼진 무실점으로 시즌 3승째를 거뒀다.",
            "3회 1사 2루에서 서건창의 중전 적시타가 결승타가 됐고, 키움은 7회 2점을 보태 3-0으로 달아났다.",
            "서건창은 3타수 2안타 1볼넷 2타점, 김건희는 4타수 2안타 1득점으로 공격을 이끌었다.",
            "원종현이 1이닝 무실점 홀드, 유토가 1이닝 3피안타 1실점으로 시즌 14세이브를 기록했다.",
        ],
        "opponent_effort": "KIA는 올러가 6이닝 4피안타 2사사구 7탈삼진 1실점으로 버텼고, 9회 나성범의 적시타로 영패를 면했다.",
        "sources": sources("20260822HTWO0"),
    },
    {
        "id": "20260822SSNC0", "stadium": "창원", "start_time": "19:00", "status": "경기 종료",
        "away": "삼성", "home": "NC", "away_score": 8, "home_score": 6,
        "winner_pitcher": "이승민", "loser_pitcher": "배재환", "save_pitcher": "김재윤",
        "headline": "삼성이 8회 디아즈의 결승 희생플라이로 NC에 8-6 역전승",
        "winner_points": [
            "삼성 선발 이승현은 2⅔이닝 6피안타 무사사구 1탈삼진 3실점으로 일찍 내려갔고, 이승민이 1이닝 2피안타 무실점으로 시즌 5승째를 챙겼다.",
            "6-6이던 8회 1사 만루에서 디아즈의 좌익수 희생플라이가 결승타가 됐고, 삼성은 9회에도 1점을 보탰다.",
            "김지찬은 5타수 3안타 1볼넷 2타점 2득점, 최형우는 4타수 2안타 1볼넷 3타점, 김태훈은 4타수 2안타 1홈런 2타점 2득점을 기록했다.",
            "장찬희가 ⅔이닝 무실점 홀드, 김재윤이 1⅓이닝 무피안타 무실점으로 시즌 27세이브를 올렸다.",
        ],
        "opponent_effort": "NC는 김형준이 4회 3점 홈런을 포함해 4타수 2안타 4타점으로 맞섰고, 12안타를 치며 6-5 리드를 만들었지만 8회 배재환이 결승점을 내줬다.",
        "sources": sources("20260822SSNC0"),
    },
]

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
    {"name": "정해영", "team": "KIA", "appeared": True, "role": "reliever", "game_decision": None,
     "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 2, "home_runs": 0,
     "season_record": "2승 1패", "season_saves": 2, "era": "6.27"},
    {"name": "박영현", "team": "KT", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": False},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.302", "obp": None, "ops": None},
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-22 편성 5경기 중 KIA-키움과 삼성-NC만 kbo-game FINISHED, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END로 모두 최종 종료를 대조해 수록했다. 한화-LG, 롯데-두산, KT-SSG는 kbo-game CANCELED 및 다음 CANCEL로 확인돼 모든 카드·합계·승부처에서 제외했다. 정해영은 KBO REVIEW 대상 경기와 네이버 투수 목록에서 구원 1이닝 1피안타 무실점 2탈삼진, 결정 기록 없음, 시즌 2승 1패 2세이브·ERA 6.27로 대조했다. 나머지 관심 투수는 완료 경기의 공식·네이버 투수 명단에 없거나 팀 경기가 취소되어 등판 없음으로 기록했다. 김도영은 KBO REVIEW·네이버 타자 명단에서 3타수 무안타 1삼진·시즌 타율 0.302로 대조했고, 한화 타자 두 명은 취소 경기로 출전 없음이다. 다음의 타자 볼넷은 사사구 표기 범위 차이가 있어 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-08-21", DATE).replace("2026.08.21", "2026.08.22").replace("2026년 8월 21일", "2026년 8월 22일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
