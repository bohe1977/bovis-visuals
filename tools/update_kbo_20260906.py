#!/usr/bin/env python3
"""Build the reconciled 2026-09-06 KBO final-game report from captured records."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-06", "20260906"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260906NCWO0": 80101189, "20260906HHLT0": 80101187, "20260906KTHT0": 80101188, "20260906OBSK0": 80101190, "20260906SSLG0": 80101191}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(gid: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, time, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": time, "status": "경기 종료", "away": away, "home": home,
            "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser,
            "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}


# Narratives are limited to the KBO REVIEW result rows and reconciled Naver box-score rows.
games = [
    game("20260906NCWO0", "고척", "14:00", "NC", "키움", 2, 4, "알칸타라", "구창모", "조영건",
         "키움이 6회 안치홍의 결승 희생플라이로 NC에 4-2 승리",
         ["키움 선발 알칸타라는 7이닝 5피안타 2실점 6탈삼진으로 승리를 기록했다.", "2-2이던 6회 1사 3루에서 안치홍의 좌익수 희생플라이가 결승타가 됐다.", "히우라는 4타수 2안타 2타점, 데이비슨은 3타수 1안타 1홈런 1타점 2득점으로 공격을 이끌었다.", "조영건이 1이닝 무실점으로 시즌 1세이브를 기록했다."],
         "NC는 박건우가 4타수 2안타, 김휘집과 이우성이 각각 1타점을 냈지만 6회 결승점을 내줬다."),
    game("20260906SSLG0", "잠실", "17:00", "삼성", "LG", 10, 4, "후라도", "임찬규", None,
         "삼성이 디아즈의 5회 결승 2루타를 앞세워 LG에 10-4 승리",
         ["삼성 선발 후라도는 5⅔이닝 6피안타 4실점 4탈삼진으로 승리를 기록했다.", "4-4이던 5회 2사 1루에서 디아즈가 좌중간 2루타를 쳐 결승타를 만들었다.", "구자욱은 4타수 3안타 2타점 2득점, 디아즈는 5타수 2안타 3타점, 박승규는 5타수 2안타 2타점을 기록했다.", "사토시가 1이닝 무실점 홀드로 리드를 지켰다."],
         "LG는 신민재가 4타수 2안타 1득점, 구본혁이 4타수 1안타 2타점으로 맞섰지만 5회 이후 격차를 좁히지 못했다."),
    game("20260906HHLT0", "사직", "17:00", "한화", "롯데", 8, 2, "화이트", "로드리게스", None,
         "한화가 문현빈의 5회 결승 2점포로 롯데에 8-2 승리",
         ["한화 선발 화이트는 6이닝 2피안타 2실점 5탈삼진으로 승리를 기록했다.", "3-2이던 5회 1사 1루에서 문현빈이 좌월 2점 홈런을 쳐 결승타가 됐다.", "문현빈은 5타수 3안타 1홈런 2타점 2득점, 페라자는 5타수 4안타 2득점, 노시환은 5타수 2안타 1홈런 2타점을 기록했다.", "박상원·조동욱·장유호가 각각 1이닝 무실점으로 뒤를 막았다."],
         "롯데는 전민재가 4타수 2안타 2타점, 조세진이 4타수 2안타를 기록했지만 팀 6안타에 그쳤다."),
    game("20260906OBSK0", "문학", "17:00", "두산", "SSG", 16, 9, "잭로그", "최민준", None,
         "두산이 박찬호의 3회 결승 2루타와 장단 12안타로 SSG에 16-9 승리",
         ["두산 선발 잭로그는 6이닝 1피안타 1실점 9탈삼진으로 승리를 기록했다.", "3회 2사 3루에서 박찬호의 중견수 2루타가 결승타가 됐다.", "양석환은 4타수 2안타 1홈런 4타점 2득점, 강승호는 1타수 1안타 1홈런 3타점 1득점을 기록했다.", "두산은 7회 강승호의 3점 홈런을 포함해 후반 추가 득점으로 격차를 벌렸다."],
         "SSG는 홍대인이 2타수 2안타 3타점 1득점, 에레디아가 솔로 홈런을 기록하며 추격했다."),
    game("20260906KTHT0", "광주", "17:00", "KT", "KIA", 3, 8, "네일", "대니엘", None,
         "KIA가 카스트로의 3회 결승 2루타와 12안타로 KT에 8-3 승리",
         ["KIA 선발 네일은 6이닝 9피안타 2실점 4탈삼진으로 승리를 기록했다.", "3회 무사 1·2루에서 카스트로가 좌중간 2루타를 쳐 결승타가 됐다.", "카스트로는 4타수 4안타 6타점, 김도영은 4타수 4안타 3득점으로 공격을 이끌었다.", "정해영이 1이닝 1실점 2탈삼진 홀드를 기록했고 성영탁도 홀드를 보탰다."],
         "KT는 김현수가 4타수 2안타 1타점 1득점, 허경민이 4타수 2안타 1득점으로 분전했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "innings": "1", "hits": 2, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 1, "home_runs": 0, "pitches": 20, "season_record": "1승 5패", "season_saves": 5, "era": "5.23", "role": "reliever", "game_decision": None},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "1", "hits": 2, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 2, "home_runs": 1, "pitches": 27, "season_record": "6승 3패", "era": "4.03", "role": "reliever", "game_decision": None},
    {"name": "로드리게스", "team": "롯데", "appeared": True, "innings": "5", "hits": 10, "runs": 5, "earned_runs": 5, "walks_hbp": 1, "strikeouts": 2, "home_runs": 3, "pitches": 105, "season_record": "7승 11패", "era": "4.35", "role": "starter", "game_decision": "패"},
    {"name": "임찬규", "team": "LG", "appeared": True, "innings": "5⅓", "hits": 9, "runs": 7, "earned_runs": 7, "walks_hbp": 3, "strikeouts": 1, "home_runs": 0, "pitches": 87, "season_record": "13승 5패", "era": "4.14", "role": "starter", "game_decision": "패"},
    {"name": "정해영", "team": "KIA", "appeared": True, "innings": "1", "hits": 1, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 2, "home_runs": 0, "pitches": 12, "season_record": "2승 1패", "season_saves": 2, "era": "6.08", "role": "reliever", "game_decision": "홀드"},
    {"name": "박영현", "team": "KT", "appeared": True, "innings": "0", "hits": 2, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0, "pitches": 4, "season_record": "6승 0패", "season_saves": 24, "era": "2.73", "role": "reliever", "game_decision": None},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 1, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 0, "avg": "0.289", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": True, "at_bats": 5, "hits": 2, "rbi": 2, "runs": 1, "home_runs": 1, "walks": 0, "strikeouts": 1, "avg": "0.280", "obp": None, "ops": None},
    {"name": "김도영", "team": "KIA", "appeared": True, "at_bats": 4, "hits": 4, "rbi": 0, "runs": 3, "home_runs": 0, "walks": 1, "strikeouts": 0, "avg": "0.306", "obp": None, "ops": None},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
official_list = json.loads((ART / "official-game-list2.json").read_text(encoding="utf-8-sig"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
final_ids = {g["id"] for g in games}
assert final_ids == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["G_ID"] for g in official_list["game"] if g["GAME_STATE_SC"] == "3" and g["GAME_RESULT_CK"] == 1} == final_ids
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 66
for game_data in games:
    gid = game_data["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    official_score = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert official["code"] == "100" and official_score["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == game_data["away_score"] and int(rheb["home"]["r"]) == game_data["home_score"]
for pitcher in pitchers:
    if not pitcher["appeared"]:
        assert set(pitcher) == {"name", "team", "appeared"}

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status": "KBO 공식 기준 · kbo-game·네이버·다음 대조",
    "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"],
    "details": "2026-09-06 KST 편성 5경기는 kbo-game FINISHED, KBO 공식 게임목록 GAME_STATE_SC=3·GAME_RESULT_CK=1 및 게임센터 GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 최종 종료와 스코어를 대조했다. 종료 5경기 합계는 66득점이다. 관심 투수의 실제 등판 라인·시즌 성적·ERA·세이브는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 선발/구원과 당일 결정은 KBO 공식 결과 기준으로 분류했다. 구원 김원중·박정민·박영현은 공식 세이브·홀드·블론이 없어 game_decision을 null로 보존했다. 비등판 투수는 해당 팀 완료 경기의 KBO 공식·네이버 전체 투수 목록 부재를 확인해 계약상 name·team·appeared만 보존했다. 관심 타자의 당일 수치와 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.",
    "conflicts": [],
}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": NOW, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": NOW, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.06", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 6일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
