#!/usr/bin/env python3
"""Build the reconciled 2026-09-19 KBO final-game report from captured official/API records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-19", "20260919"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260919&toDate=20260919"
DAUM_IDS = {"20260919HHLG0": 80108782, "20260919HTNC0": 80108783, "20260919OBKT0": 80108784, "20260919SSLT0": 80108785}


def source_rows(gid: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "17:00", "status": "경기 종료", "away": away, "home": home, "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": source_rows(gid)}


games = [
    game("20260919HHLG0", "잠실", "한화", "LG", 1, 2, "고우석", "조동욱", "손주영",
         "LG가 이재원의 8회 결승 홈런으로 한화에 2-1 승리", [
             "LG 선발 임찬규는 7이닝 5피안타 무사사구 6탈삼진 1실점으로 호투했고, 고우석이 8회 승리를 기록했다.",
             "1-1이던 8회 선두 이재원이 중월 솔로 홈런을 쳐 결승점을 만들었다.",
             "박해민은 4타수 3안타 1득점, 이재원은 3타수 1안타 1홈런 1타점 1득점을 기록했다.",
             "손주영은 9회 1이닝 1피안타 1사사구 무실점으로 시즌 29세이브를 기록했다."],
         "한화는 정은원이 3타수 2안타 1득점, 김태연이 3타수 2안타로 출루를 만들었지만 8회 결승 홈런을 허용한 뒤 반격하지 못했다."),
    game("20260919HTNC0", "창원", "KIA", "NC", 5, 1, "네일", "구창모", None,
         "KIA가 2회 결승 2루타와 네일의 호투로 NC에 5-1 승리", [
             "KIA 선발 네일은 6이닝 3피안타 1사사구 6탈삼진 1실점으로 승리를 기록했다.",
             "2회 2사 1루에서 김태군의 좌중간 2루타가 결승타가 됐고, KIA는 5회 나성범의 솔로포로 격차를 벌렸다.",
             "김선빈은 4타수 2안타 2타점, 한준수는 4타수 2안타 1타점 1득점을 기록했다.",
             "전상현·조상우가 각각 1이닝 무실점 홀드를 기록했고, 이의리가 9회를 무실점으로 마쳤다."],
         "NC는 신재인이 3타수 1안타 1득점으로 홈을 밟았고, 구창모 뒤 배재환·손주환이 3이닝 무실점으로 버텼지만 초반 실점을 만회하지 못했다."),
    game("20260919OBKT0", "수원", "두산", "KT", 3, 15, "대니엘", "윤태호", None,
         "KT가 장단 18안타를 몰아쳐 두산에 15-3 대승", [
             "KT 선발 대니엘은 6이닝 6피안타 3사사구 5탈삼진 3실점(1자책)으로 승리를 기록했다.",
             "KT는 5회 최원준의 투런 홈런으로 달아났고, 6회 6득점 빅이닝으로 승부를 갈랐다.",
             "최원준은 4타수 4안타 1홈런 4타점, 힐리어드는 5타수 4안타 1홈런 1타점 4득점을 기록했다.",
             "전용주·김정운·문용익이 7회부터 3이닝을 무피안타 무실점으로 막았다."],
         "두산은 박찬호가 4타수 2안타 1득점, 세베리노가 4타수 1안타 1타점으로 분전했지만 5회 이후 KT 타선을 막지 못했다."),
    game("20260919SSLT0", "사직", "삼성", "롯데", 3, 5, "박정민", "사토시", "이이무라",
         "롯데가 한동희의 8회 결승 홈런으로 삼성에 5-3 승리", [
             "롯데 선발 나균안은 6이닝 5피안타 3사사구 3탈삼진 3실점을 기록했고, 박정민이 8회 무실점으로 승리를 챙겼다.",
             "3-3이던 8회 선두 한동희가 중월 솔로 홈런을 쳐 결승점을 만들었다.",
             "나승엽은 4타수 3안타 1득점, 레이예스는 3타수 1안타 2타점, 한동희는 4타수 1안타 1홈런 1타점을 기록했다.",
             "김원중이 7회 1이닝 무실점, 박정민이 8회 1이닝 3탈삼진 무실점으로 이어 던졌고 이이무라가 9회 세이브를 기록했다."],
         "삼성은 전병우가 4타수 2안타 1홈런 2타점, 디아즈가 2타수 1안타 1타점 2볼넷으로 분전했지만 8회 결승포를 막지 못했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": False},
    {"name": "류현진", "team": "한화", "appeared": False},
    {"name": "제레미 비슬리", "team": "롯데", "appeared": False},
    {"name": "박세웅", "team": "롯데", "appeared": False},
    {"name": "김진욱", "team": "롯데", "appeared": False},
    {"name": "김원중", "team": "롯데", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 2, "strikeouts": 0, "home_runs": 0, "pitches": 21, "season_record": "1승 5패 5세이브", "season_saves": 5, "era": "4.66", "role": "reliever", "game_decision": None},
    {"name": "박정민", "team": "롯데", "appeared": True, "innings": "1", "hits": 1, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 3, "home_runs": 0, "pitches": 19, "season_record": "7승 4패", "era": "4.38", "role": "reliever", "game_decision": None},
    {"name": "로드리게스", "team": "롯데", "appeared": False},
    {"name": "임찬규", "team": "LG", "appeared": True, "innings": "7", "hits": 5, "runs": 1, "earned_runs": 1, "walks_hbp": 0, "strikeouts": 6, "home_runs": 0, "pitches": 96, "season_record": "14승 5패", "era": "4.06", "role": "starter", "game_decision": None},
    {"name": "정해영", "team": "KIA", "appeared": False},
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 4, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 0, "strikeouts": 2, "avg": "0.288", "obp": None, "ops": None},
    {"name": "노시환", "team": "한화", "appeared": False},
    {"name": "김도영", "team": "KIA", "appeared": False},
]


def official_pitchers(gid):
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    assert doc["code"] == "100"
    rows = []
    for team in doc["arrPitcher"]:
        table = json.loads(team["table"])
        heads = [cell["Text"] for cell in table["headers"][0]["row"]]
        rows.extend(dict(zip(heads, [cell["Text"] for cell in row["row"]])) for row in table["rows"])
    return rows


def official_hitters(gid):
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    return {row["row"][2]["Text"] for team in doc["arrHitter"] for row in json.loads(team["table1"])["rows"] if len(row["row"]) >= 3}


kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 35
for g in games:
    gid = g["id"]
    board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    score = naver["scoreBoard"]["rheb"]
    assert (board["AWAY_NM"], board["HOME_NM"]) == (g["away"], g["home"])
    assert (int(score["away"]["r"]), int(score["home"]["r"])) == (g["away_score"], g["home_score"])
    official_p = {x["선수명"]: x for x in official_pitchers(gid)}
    naver_p = {x["name"]: x for side in ("away", "home") for x in naver["pitchersBoxscore"][side]}
    official_h = official_hitters(gid)
    naver_h = {x["name"]: x for side in ("away", "home") for x in naver["battersBoxscore"][side]}
    for p in pitchers:
        if p["team"] in (g["away"], g["home"]):
            assert (p["name"] in official_p) == p["appeared"] == (p["name"] in naver_p)
    for b in batters:
        if b["team"] in (g["away"], g["home"]):
            assert (b["name"] in official_h) == b["appeared"] == (b["name"] in naver_h)
for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}
# Numeric and official-role/decision checks for every appearing watched pitcher.
expected = {"임찬규": ("선발", "&nbsp;", "7", "5", "0", "6", "1", "1", "96"), "김원중": ("7.9", "&nbsp;", "1", "0", "2", "0", "0", "0", "21"), "박정민": ("8.5", "승", "1", "1", "0", "3", "0", "0", "19")}
for gid in DAUM_IDS:
    for row in official_pitchers(gid):
        if row["선수명"] in expected:
            assert tuple(row[k] for k in ("등판", "결과", "이닝", "피안타", "4사구", "삼진", "실점", "자책", "투구수")) == expected[row["선수명"]]

source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-09-19 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 35득점이다. 임찬규·김원중·박정민의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했다. 임찬규는 공식 선발·무결정, 김원중은 공식 구원·무결정, 박정민은 공식 구원·승리로 확인했으나 구원 투수의 화면 결정 배지는 세이브·홀드·블론만 허용하므로 모두 null로 보존했다. 김원중의 공식 시즌 5세이브를 보존했다. 강백호의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 나머지 관심 투수와 노시환·김도영은 해당 팀 완료 경기의 KBO 공식·네이버 전체 명단에 없어 계약상 최소 객체로 보존했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts": []}
now = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": now, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": now, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.19", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 19일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {now}")
