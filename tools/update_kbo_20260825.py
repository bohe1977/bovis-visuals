#!/usr/bin/env python3
"""Write the reconciled 2026-08-25 KBO final-game report from captured official records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-25", "20260825"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260825&toDate=20260825"
DAUM_IDS = {
    "20260825HHSK0": 80101132,
    "20260825LTHT0": 80101133,
    "20260825NCLG0": 80101134,
    "20260825OBKT0": 80101135,
    "20260825SSWO0": 80101136,
}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


# Only games confirmed final on all three collection surfaces are included.  The tied game is final,
# not a cancellation, and is retained with neither winning nor losing pitcher.
games = [
    {
        "id": "20260825NCLG0", "stadium": "잠실", "start_time": "18:30", "status": "경기 종료",
        "away": "NC", "home": "LG", "away_score": 4, "home_score": 5,
        "winner_pitcher": "케네디", "loser_pitcher": "전사민", "save_pitcher": None,
        "headline": "LG가 연장 10회 홍창기의 끝내기 안타로 NC에 5-4 승리",
        "winner_points": [
            "LG 선발 톨허스트는 6이닝 5피안타 2사사구 2탈삼진 2실점을 기록했고, 케네디가 연장 10회 1이닝 2피안타 1실점으로 승리를 챙겼다.",
            "4-4이던 10회 2사 만루에서 홍창기의 우중간 안타가 끝내기 결승타가 됐다.",
            "오스틴은 5타수 4안타 1홈런 3타점으로 8회 동점 3점포를 쳤고, 송찬의도 5타수 1안타 1타점 1득점을 기록했다.",
            "LG 불펜은 김진수의 1이닝 무실점 뒤 케네디가 마지막 위기를 넘겼다."
        ],
        "opponent_effort": "NC는 테일러가 6이닝 2피안타 2사사구 5탈삼진 무실점으로 호투했고, 박건우가 5타수 2안타 1득점으로 연장까지 추격했지만 끝내기 안타를 막지 못했다.",
        "sources": sources("20260825NCLG0"),
    },
    {
        "id": "20260825HHSK0", "stadium": "문학", "start_time": "18:30", "status": "경기 종료",
        "away": "한화", "home": "SSG", "away_score": 1, "home_score": 7,
        "winner_pitcher": "김민", "loser_pitcher": "화이트", "save_pitcher": None,
        "headline": "SSG가 6회 최지훈의 결승타를 앞세워 한화에 7-1 승리",
        "winner_points": [
            "SSG 선발 김민준은 5이닝 4피안타 2사사구 6탈삼진 1실점을 기록했고, 김민이 1이닝 무실점으로 승리투수가 됐다.",
            "1-1이던 6회 무사 1·2루에서 최지훈의 우중간 안타가 결승타가 됐다.",
            "에레디아는 5타수 2안타 2타점, 최지훈은 4타수 2안타 1타점 1득점으로 공격을 이끌었다.",
            "이건욱·전영준·서진용이 7~9회를 무실점으로 지켰다."
        ],
        "opponent_effort": "한화는 문현빈이 3타수 2안타 1홈런 1타점 1득점, 노시환이 3타수 3안타로 분전했지만 화이트가 5이닝 4실점하며 흐름을 내줬다.",
        "sources": sources("20260825HHSK0"),
    },
    {
        "id": "20260825LTHT0", "stadium": "광주", "start_time": "18:30", "status": "경기 종료",
        "away": "롯데", "home": "KIA", "away_score": 5, "home_score": 8,
        "winner_pitcher": "조상우", "loser_pitcher": "김원중", "save_pitcher": None,
        "headline": "KIA가 9회 이호연의 끝내기 만루포로 롯데에 8-5 승리",
        "winner_points": [
            "KIA 선발 시라카와는 4⅔이닝 7피안타 1사사구 5탈삼진 5실점을 기록했고, 조상우가 1이닝 2피안타 무실점으로 승리를 올렸다.",
            "5-5이던 9회 2사 만루에서 이호연의 우월 만루 홈런이 끝내기 결승타가 됐다.",
            "나성범은 5타수 3안타 1타점, 김도영은 4타수 2안타 1득점으로 출루를 이끌었고 이호연은 1타수 1안타 4타점을 기록했다.",
            "성영탁이 1⅔이닝 무실점으로 중간을 지켰고 조상우가 9회를 막았다."
        ],
        "opponent_effort": "롯데는 비슬리가 5⅔이닝 9피안타 4사사구 4탈삼진 4실점을 기록했고, 레이예스가 4타수 2안타 1타점·손성빈이 4타수 2안타 2타점으로 맞섰지만 9회 김원중이 끝내기 홈런을 허용했다.",
        "sources": sources("20260825LTHT0"),
    },
    {
        "id": "20260825OBKT0", "stadium": "수원", "start_time": "18:30", "status": "경기 종료",
        "away": "두산", "home": "KT", "away_score": 3, "home_score": 1,
        "winner_pitcher": "최민석", "loser_pitcher": "소형준", "save_pitcher": "이영하",
        "headline": "두산이 양의지의 6회 결승포와 이영하의 세이브로 KT에 3-1 승리",
        "winner_points": [
            "두산 선발 최민석은 6이닝 6피안타 1사사구 5탈삼진 1실점으로 시즌 12승째를 기록했다.",
            "1-1이던 6회 1사에서 양의지의 좌월 솔로 홈런이 결승타가 됐다.",
            "정수빈은 4타수 2안타 1홈런 1타점 2득점, 양의지는 4타수 1안타 1홈런 1타점 1득점을 기록했다.",
            "김택연·타카다가 나란히 1이닝 무실점 홀드했고, 이영하는 1이닝 1피안타 2탈삼진 무실점으로 시즌 21세이브를 올렸다."
        ],
        "opponent_effort": "KT는 소형준이 6이닝 5피안타 3사사구 6탈삼진 2실점으로 버텼고, 김현수가 4타수 2안타 1타점으로 유일한 득점을 만들었지만 역전에는 닿지 못했다.",
        "sources": sources("20260825OBKT0"),
    },
    {
        "id": "20260825SSWO0", "stadium": "고척", "start_time": "18:30", "status": "경기 종료",
        "away": "삼성", "home": "키움", "away_score": 3, "home_score": 3,
        "winner_pitcher": None, "loser_pitcher": None, "save_pitcher": None,
        "headline": "삼성과 키움이 연장 11회까지 3-3으로 비겼다",
        "winner_points": [
            "삼성 선발 보스는 6이닝 7피안타 무사사구 8탈삼진 2실점, 키움 선발 알칸타라는 6이닝 3피안타 2사사구 8탈삼진 1실점을 기록했다.",
            "승부가 연장 11회까지 이어졌지만 어느 팀도 결승점을 내지 못해 무승부로 끝났다.",
            "삼성은 구자욱이 4타수 2안타 2타점, 디아즈가 4타수 1안타 1홈런 1타점을 기록했다.",
            "삼성 김재윤과 키움 윤석원은 각각 마지막 1이닝을 무실점으로 막아 균형을 지켰다."
        ],
        "opponent_effort": "키움은 서건창이 5타수 1안타 1홈런 1타점 2득점, 데이비슨이 5타수 2안타로 분전했고 유토가 ⅔이닝 무실점으로 연장 위기를 넘겼다.",
        "sources": sources("20260825SSWO0"),
    },
]

# Inactive pitchers intentionally contain only the three contract fields.
pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": True, "role": "starter", "game_decision": None,
     "innings": "5⅔", "hits": 9, "runs": 4, "earned_runs": 4, "walks_hbp": 4, "strikeouts": 4, "home_runs": 1,
     "season_record": "8승 5패", "era": "4.80"},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "role": "reliever", "game_decision": None,
     "innings": "⅔", "hits": 3, "runs": 4, "earned_runs": 4, "walks_hbp": 1, "strikeouts": 1, "home_runs": 1,
     "season_record": "1승 5패", "season_saves": 5, "era": "5.09"},
    {"name": "박정민", "team": "롯데", "appeared": False},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "role": "reliever", "game_decision": None,
     "innings": "1⅓", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0,
     "season_record": "2승 1패", "season_saves": 2, "era": "6.05"},
    {"name": "박영현", "team": "KT", "appeared": False},
]

batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.294", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 3, "hits": 3, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 1, "strikeouts": 0, "avg": "0.281", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 2, "rbi": 0, "runs": 1, "home_runs": 0, "walks": 1, "strikeouts": 0, "avg": "0.303", "obp": None, "ops": None},
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · 네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-08-25 편성 5경기는 kbo-game FINISHED, KBO 공식 게임목록 GAME_STATE_SC=3·GAME_RESULT_CK=1, 네이버 공개 기록 API statusCode=4, 다음 일정 API gameStatus=END·스코어를 대조해 모두 최종 종료로 확정했다. 관심 투수의 등판 여부·당일 라인·시즌 승패·ERA·세이브는 KBO 공식 REVIEW 표와 네이버 기록 API에서 대조했다. 비슬리는 공식 선발 행(결정 기록 없음), 김원중·정해영은 공식 구원 행으로 확인했다. 김원중의 공식 표상 패전은 구원투수 UI 계약에 따라 game_decision에 기록하지 않았고, 공식 세이브·홀드·블론도 없어 null로 기록했다. 미등판 투수는 해당 팀의 완료 경기 KBO·네이버 전체 투수 목록에서 부재함을 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO REVIEW와 네이버 API에서 대조했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}

# Data-contract checks protect against stale or incomplete manual preparation.
assert len(games) == 5 and all(g["status"] == "경기 종료" for g in games)
assert sum(g["away_score"] + g["home_score"] for g in games) == 40
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}
    else:
        assert pitcher["role"] in {"starter", "reliever"}
        allowed = {"승", "패", None} if pitcher["role"] == "starter" else {"세이브", "홀드", "블론", None}
        assert pitcher["game_decision"] in allowed

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old in ("2026-08-23", "2026.08.23", "2026년 8월 23일"):
        new = DATE if "-" in old else ("2026.08.25" if "." in old else "2026년 8월 25일")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
