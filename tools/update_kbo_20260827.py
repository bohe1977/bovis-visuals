#!/usr/bin/env python3
"""Write the reconciled 2026-08-27 KBO final-game report from captured records."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-27", "20260827"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260827&toDate=20260827"
DAUM_IDS = {"20260827NCLG0": 80101144, "20260827HHSK0": 80101142, "20260827OBKT0": 80101145, "20260827SSWO0": 80101146}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(game_id):
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]

def game(game_id, stadium, away, home, a, h, winner, loser, headline, points, effort):
    return {"id": game_id, "stadium": stadium, "start_time": "18:30", "status": "경기 종료", "away": away, "home": home, "away_score": a, "home_score": h, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": None, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(game_id)}

games = [
    game("20260827NCLG0", "잠실", "NC", "LG", 13, 3, "토다", "박시원", "NC가 1회 박민우의 결승타를 시작으로 LG에 13-3 승리", ["NC 선발 토다는 6이닝 8피안타 1사사구 3탈삼진 3실점으로 승리투수가 됐다.", "1회 1사 2루에서 박민우의 중전 적시타가 결승타가 됐고, NC는 20안타로 13득점했다.", "김주원은 5타수 5안타 1타점 3득점, 박민우는 4타수 3안타 3타점 2득점을 기록했다.", "김태훈·류진욱·이준혁이 각 1이닝 무실점으로 리드를 지켰다."], "LG는 천성호가 3타수 2안타 1득점, 손용준이 2타수 2안타 1타점으로 분전했다."),
    game("20260827HHSK0", "문학", "한화", "SSG", 6, 13, "김건우", "조동욱", "SSG가 5회 임근우의 결승타와 안상현의 4타점으로 한화에 13-6 승리", ["SSG 선발 김건우는 5이닝 4피안타 4사사구 4탈삼진 5실점(4자책)으로 승리투수가 됐다.", "5회 1사 2·3루에서 임근우의 좌전 안타가 결승타가 됐다.", "안상현은 5타수 2안타 1홈런 4타점, 전의산은 3타수 2안타 1홈런 3타점 4득점을 기록했다.", "노경은이 1이닝 무실점 홀드를 기록했고 문승원·전영준이 7~8회를 무실점으로 막았다."], "한화는 허인서가 4타수 2안타 1홈런 2타점, 박정현이 솔로 홈런을 기록하며 추격했다."),
    game("20260827OBKT0", "수원", "두산", "KT", 4, 5, "손동현", "이용찬", "KT가 연장 11회 장진혁의 끝내기 홈런으로 두산에 5-4 승리", ["KT 선발 고영표는 7이닝 4피안타 2사사구 6탈삼진 1실점으로 호투했다.", "4-4로 맞선 연장 11회 무사에서 장진혁의 우월 솔로 홈런이 끝내기 결승타가 됐다.", "김상수는 4타수 3안타 2득점, 장진혁은 5타수 1안타 1홈런 1타점 1득점을 기록했다.", "박영현이 2이닝 무실점, 손동현이 ⅔이닝 무실점으로 막고 승리를 챙겼다."], "두산은 양의지가 4타수 2안타 1홈런 3타점, 박준순·박찬호·조수행이 나란히 2안타로 분전했다."),
    game("20260827SSWO0", "고척", "삼성", "키움", 15, 2, "원태인", "하영민", "삼성이 구자욱의 3회 결승타와 디아즈의 만루포로 키움에 15-2 승리", ["삼성 선발 원태인은 6이닝 6피안타 1사사구 7탈삼진 2실점으로 승리투수가 됐다.", "3회 무사 1·3루에서 구자욱의 중전 안타가 결승타가 됐다.", "디아즈는 5타수 2안타 1홈런 5타점, 김지찬은 5타수 3안타 4득점, 김성윤은 4타수 3안타 1타점 2득점을 기록했다.", "임기영·사토시·이승현이 7~9회를 1피안타 무실점으로 마무리했다."], "키움은 김건희가 3타수 2안타, 데이비슨이 4타수 1안타 1타점으로 분전했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "role": "starter", "game_decision": "승", "innings": "6", "hits": 6, "runs": 2, "earned_runs": 2, "walks_hbp": 1, "strikeouts": 7, "home_runs": 0, "pitches": 98, "season_record": "7승 6패", "era": "4.33"},
    {"name": "류현진", "team": "한화", "appeared": False}, {"name": "제레미 비슬리", "team": "롯데", "appeared": False}, {"name": "박세웅", "team": "롯데", "appeared": False}, {"name": "김진욱", "team": "롯데", "appeared": False}, {"name": "김원중", "team": "롯데", "appeared": False}, {"name": "박정민", "team": "롯데", "appeared": False}, {"name": "로드리게스", "team": "롯데", "appeared": False}, {"name": "임찬규", "team": "LG", "appeared": False}, {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": True, "role": "reliever", "game_decision": None, "innings": "2", "hits": 2, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "pitches": 27, "season_record": "6승 0패", "season_saves": 23, "era": "2.28"},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 1, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 0, "avg": "0.291", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 3, "hits": 1, "rbi": 0, "runs": 1, "home_runs": 0, "walks": 0, "strikeouts": 1, "avg": "0.280", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": False},
]
source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · 네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-08-27 편성 5경기 중 롯데-KIA(광주)는 kbo-game CANCELED 및 다음 일정 API gameStatus=CANCEL로 확인되어 제외했다. 나머지 4경기는 kbo-game FINISHED, 네이버 공개 기록 API statusCode=4·스코어, 다음 일정 API gameStatus=END·스코어를 대조해 최종 종료로 확정했다. 종료 4경기 합계 61득점이다. 원태인은 KBO 공식 REVIEW 선발 행과 네이버 기록에서 6이닝 2실점·시즌 7승 6패·ERA 4.33·승을, 박영현은 KBO 공식 REVIEW 구원 행과 네이버 기록에서 2이닝 무실점·시즌 6승 0패 23세이브·ERA 2.28·결정 기록 없음을 대조했다. 류현진·롯데 관심 투수·임찬규는 각 팀 완료 경기의 전체 투수 명단에 없어 등판 없음으로 확인했고, 정해영은 KIA 경기 취소로 등판 기록이 없다. 강백호·노시환의 당일 타격 라인과 시즌 타율은 네이버 기록 API와 KBO REVIEW 기준으로 확인했다. 김도영은 KIA 경기 취소로 출전 기록이 없다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.", "conflicts": []}

assert len(games) == 4 and all(g["status"] == "경기 종료" for g in games)
assert sum(g["away_score"] + g["home_score"] for g in games) == 61
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}
    else:
        assert pitcher["role"] in {"starter", "reliever"}
        assert pitcher["game_decision"] in ({"승", "패", None} if pitcher["role"] == "starter" else {"세이브", "홀드", "블론", None})
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for relative in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8").replace("2026-08-26", DATE).replace("2026.08.26", "2026.08.27").replace("2026년 8월 26일", "2026년 8월 27일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
