#!/usr/bin/env python3
"""Write the reconciled 2026-08-28 KBO cancellation report from captured sources."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-28", "20260828"
KBO = "https://www.koreabaseball.com"
GAME_IDS = ["20260828WOOB0", "20260828KTSS0", "20260828LGLT0", "20260828SKHT0", "20260828NCHH0"]
DAUM_SCHEDULE = (
    "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo"
    "&seasonKey=2026&fromDate=20260828&toDate=20260828"
)
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"],
    "naver": [f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record" for game_id in GAME_IDS],
    "daum": [DAUM_SCHEDULE],
}

# All scheduled games were cancelled. The report contract intentionally excludes them from games.
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
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": False},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": False},
]
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 스코어보드", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정 API"],
    "details": "2026-08-28 KST 편성 키움-두산, KT-삼성, LG-롯데, SSG-KIA, NC-한화 5경기는 kbo-game에서 모두 CANCELED로 확인했다. 다음 일정 API도 5경기 모두 periodType=\"CANCEL\", gameStatus=\"CANCEL\"로 반환했고, 네이버 공개 기록 API는 각 경기 recordData=null로 반환했다. 따라서 최종 종료 경기는 0경기이며, 취소 경기는 games 배열·카드·스코어·승부처·경기 수·총득점에서 모두 제외했다. 관심 투수는 취소된 팀 경기의 등판 기록이 없어 계약에 따라 name·team·appeared만 보존했고, 관심 타자도 출전 기록이 없다.",
    "conflicts": [],
}

assert all(set(pitcher) == {"name", "team", "appeared"} and not pitcher["appeared"] for pitcher in pitchers)
assert not any(batter["appeared"] for batter in batters)
assert len(GAME_IDS) == 5

(ROOT / "kbo" / "data.json").write_text(
    json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": []}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
(ROOT / "kbo-players" / "data.json").write_text(
    json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-08-27", DATE).replace("2026.08.27", "2026.08.28").replace("2026년 8월 27일", "2026년 8월 28일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO cancellation report for {DATE} at {NOW}")
