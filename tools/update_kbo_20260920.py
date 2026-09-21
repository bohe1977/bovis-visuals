#!/usr/bin/env python3
"""Build the reconciled 2026-09-20 KBO final-game report from captured official/API records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-20", "20260920"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260920HHLG0": 80108786, "20260920HTNC0": 80108787, "20260920OBKT0": 80108788, "20260920SSLT0": 80108789, "20260920WOSK0": 80108790}


def sources(gid: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]


def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "14:00", "status": "경기 종료", "away": away, "home": home, "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}


games = [
    game("20260920HHLG0", "잠실", "한화", "LG", 3, 4, "카라스코", "황준서", "손주영",
         "LG가 5회 재역전 뒤 한화에 4-3 승리", [
             "LG 선발 카라스코는 5이닝 3피안타 3사사구 5탈삼진 3실점으로 시즌 6승째를 기록했다.",
             "LG는 5회 2득점으로 3-4로 재역전해 승부를 갈랐다.",
             "이재원은 4타수 1안타 1홈런 2타점 1득점, 박해민은 4타수 2안타 1득점을 기록했다.",
             "김강률(1이닝)·케네디(2이닝)가 홀드를 기록했고, 손주영은 9회 1이닝 1피안타 무실점으로 시즌 30세이브를 올렸다."],
         "한화는 5회 3득점으로 역전했고 최인호·한지윤이 각각 1타점을 냈지만, 이후 4이닝 동안 1안타에 그쳐 재역전하지 못했다."),
    game("20260920HTNC0", "창원", "KIA", "NC", 8, 6, "조상우", "이용준", "이의리",
         "KIA가 8회 6득점으로 NC에 8-6 역전승", [
             "KIA 선발 시라카와는 5이닝 무피안타 5사사구 4탈삼진 무실점을 기록했고, 조상우가 7회 승리를 기록했다.",
             "2-4로 뒤진 8회 KIA가 6득점으로 전세를 뒤집은 장면이 승부처였다.",
             "박정우는 5타수 1안타 3타점 1득점, 카스트로는 5타수 2안타 2타점 1득점, 한준수는 4타수 2안타 1타점 2득점을 기록했다.",
             "정해영은 8회 1이닝 무피안타 무실점으로 연결했고, 이의리는 9회 1이닝 무피안타 2사사구 2탈삼진 무실점으로 시즌 6세이브를 기록했다."],
         "NC는 박건우가 3타수 2안타 1홈런 3타점, 이우성이 1타수 1안타 2타점으로 6·7회 추격을 이끌었지만 8회 6실점으로 리드를 지키지 못했다."),
    game("20260920OBKT0", "수원", "두산", "KT", 8, 9, "고영표", "박신지", "김정운",
         "KT가 두산의 8회 추격을 뿌리치고 9-8 승리", [
             "KT 선발 고영표는 7이닝 3피안타 무사사구 4탈삼진 1실점으로 시즌 13승째를 기록했다.",
             "KT는 2회 4득점, 3회 2득점으로 초반 흐름을 가져갔고 8회 두산의 7득점 추격을 1점 차로 막았다.",
             "장준원은 4타수 2안타 2홈런 5타점 2득점, 한승택은 4타수 3안타 1홈런 1타점 3득점을 기록했다.",
             "김정운은 8회 2사부터 1⅓이닝 1피안타 무실점 4탈삼진으로 시즌 첫 세이브를 기록했다."],
         "두산은 8회 7득점으로 8-9까지 따라붙었고 세베리노가 4타수 1안타 1홈런 3타점, 김민석이 5타수 2안타 1타점으로 분전했지만 동점에는 실패했다."),
    game("20260920SSLT0", "사직", "삼성", "롯데", 6, 13, "이진하", "원태인", None,
         "롯데가 4회 10득점 빅이닝으로 삼성에 13-6 승리", [
             "롯데는 선발 김태균 뒤 이진하가 2이닝 2피안타 무사사구 2탈삼진 1실점으로 시즌 2승째를 기록했다.",
             "롯데가 1-3으로 뒤진 4회 10득점 빅이닝을 만들며 단숨에 경기를 뒤집었다.",
             "황성빈은 6타수 2안타 3타점, 장두성은 4타수 3안타 2타점, 고승민은 4타수 2안타 2타점 2득점을 기록했다.",
             "현도훈은 2⅓이닝 1피안타 무실점 2탈삼진으로 중간을 막았고, 구승민도 9회 무실점으로 마쳤다."],
         "삼성은 디아즈가 3타수 2안타 1홈런 3타점, 김도환이 4타수 2안타 1홈런 2타점으로 분전했지만 4회 대량 실점을 만회하지 못했다."),
    game("20260920WOSK0", "문학", "키움", "SSG", 5, 10, "김건우", "하영민", None,
         "SSG가 3회 역전 뒤 키움에 10-5 승리", [
             "SSG 선발 김건우는 5이닝 8피안타 2사사구 5탈삼진 4실점으로 시즌 9승째를 기록했다.",
             "0-2로 뒤진 3회 SSG가 3득점으로 역전했고, 5·6회에 각각 3득점을 보태 격차를 벌렸다.",
             "최지훈은 4타수 3안타 1홈런 5타점 2득점, 김재환은 5타수 2안타 1홈런 2타점 1득점을 기록했다.",
             "문승원이 6회 1이닝 무피안타 무실점 홀드를 기록했고, 이건욱·타케다가 7·8회를 무실점으로 이었다."],
         "키움은 데이비슨이 4타수 2안타 1홈런 1타점 1득점, 김동헌이 3타수 1안타 1홈런 1타점으로 분전했지만 3회 역전 뒤 추가 실점을 막지 못했다."),
]

pitchers = [
    {"name": "원태인", "team": "삼성", "appeared": True, "innings": "3⅓", "hits": 11, "runs": 9, "earned_runs": 9, "walks_hbp": 2, "strikeouts": 2, "home_runs": 0, "pitches": 82, "season_record": "7승 8패", "era": "4.66", "role": "starter", "game_decision": "패"},
    {"name": "류현진", "team": "한화", "appeared": False}, {"name": "제레미 비슬리", "team": "롯데", "appeared": False}, {"name": "박세웅", "team": "롯데", "appeared": False}, {"name": "김진욱", "team": "롯데", "appeared": False}, {"name": "김원중", "team": "롯데", "appeared": False}, {"name": "박정민", "team": "롯데", "appeared": False}, {"name": "로드리게스", "team": "롯데", "appeared": False}, {"name": "임찬규", "team": "LG", "appeared": False},
    {"name": "정해영", "team": "KIA", "appeared": True, "innings": "1", "hits": 0, "runs": 0, "earned_runs": 0, "walks_hbp": 0, "strikeouts": 0, "home_runs": 0, "pitches": 10, "season_record": "2승 1패 2세이브", "season_saves": 2, "era": "6.23", "role": "reliever", "game_decision": None},
    {"name": "박영현", "team": "KT", "appeared": False},
]
batters = [
    {"name": "강백호", "team": "한화", "appeared": True, "at_bats": 3, "hits": 0, "rbi": 0, "runs": 0, "home_runs": 0, "walks": 1, "strikeouts": 1, "avg": "0.286", "obp": "0.355", "ops": "0.900"},
    {"name": "노시환", "team": "한화", "appeared": False}, {"name": "김도영", "team": "KIA", "appeared": False},
]


def official_pitchers(gid: str) -> dict[str, dict[str, str]]:
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig")); assert doc["code"] == "100"
    result = {}
    for team in doc["arrPitcher"]:
        table = json.loads(team["table"]); heads = [c["Text"] for c in table["headers"][0]["row"]]
        for row in table["rows"]: result[dict(zip(heads, [c["Text"] for c in row["row"]]))["선수명"]] = dict(zip(heads, [c["Text"] for c in row["row"]]))
    return result


def official_hitter_names(gid: str) -> set[str]:
    doc = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    return {row["row"][2]["Text"] for team in doc["arrHitter"] for row in json.loads(team["table1"])["rows"] if len(row["row"]) >= 3}

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8")); daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 72
for game_row in games:
    gid = game_row["id"]; board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig")); naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    score = naver["scoreBoard"]["rheb"]
    assert (board["AWAY_NM"], board["HOME_NM"]) == (game_row["away"], game_row["home"])
    assert (int(score["away"]["r"]), int(score["home"]["r"])) == (game_row["away_score"], game_row["home_score"])
    op, oh = official_pitchers(gid), official_hitter_names(gid)
    np = {x["name"]: x for side in ("away", "home") for x in naver["pitchersBoxscore"][side]}; nh = {x["name"]: x for side in ("away", "home") for x in naver["battersBoxscore"][side]}
    for p in pitchers:
        if p["team"] in (game_row["away"], game_row["home"]): assert (p["name"] in op) == p["appeared"] == (p["name"] in np)
    for b in batters:
        if b["team"] in (game_row["away"], game_row["home"]): assert (b["name"] in oh) == b["appeared"] == (b["name"] in nh)
for p in pitchers:
    if not p["appeared"]: assert set(p) == {"name", "team", "appeared"}
# Actual watched-player numeric/role/decision rows: KBO official baseline and Naver cross-check.
won = official_pitchers("20260920SSLT0")["원태인"]; won_n = json.loads((ART / "naver-20260920SSLT0.json").read_text())["result"]["recordData"]["pitchersBoxscore"]["away"][0]
assert tuple(won[k] for k in ("등판", "결과", "이닝", "피안타", "4사구", "삼진", "실점", "자책", "투구수", "승", "패", "평균자책점")) == ("선발", "패", "3 1/3", "11", "2", "2", "9", "9", "82", "7", "8", "4.66")
assert (won_n["inn"], won_n["hit"], won_n["bbhp"], won_n["kk"], won_n["r"], won_n["er"], won_n["bf"], won_n["w"], won_n["l"], won_n["era"], won_n["wls"]) == ("3 ⅓", 11, 2, 2, 9, 9, 82, 7, 8, "4.66", "패")
jae = official_pitchers("20260920HTNC0")["정해영"]; jae_n = next(x for x in json.loads((ART / "naver-20260920HTNC0.json").read_text())["result"]["recordData"]["pitchersBoxscore"]["away"] if x["name"] == "정해영")
assert tuple(jae[k] for k in ("등판", "결과", "이닝", "피안타", "4사구", "삼진", "실점", "자책", "투구수", "승", "패", "세", "평균자책점")) == ("8.7", "&nbsp;", "1", "0", "0", "0", "0", "0", "10", "2", "1", "2", "6.23")
assert (jae_n["inn"], jae_n["hit"], jae_n["bbhp"], jae_n["kk"], jae_n["r"], jae_n["er"], jae_n["bf"], jae_n["w"], jae_n["l"], jae_n["s"], jae_n["era"], jae_n["wls"]) == ("1", 0, 0, 0, 0, 0, 10, 2, 1, 2, "6.23", "")
kang_n = next(x for x in json.loads((ART / "naver-20260920HHLG0.json").read_text())["result"]["recordData"]["battersBoxscore"]["away"] if x["name"] == "강백호")
assert (kang_n["ab"], kang_n["hit"], kang_n["rbi"], kang_n["run"], kang_n["hr"], kang_n["bb"], kang_n["kk"], kang_n["hra"]) == (3, 0, 0, 0, 0, 1, 1, "0.286")

source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": "2026-09-20 KST 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 5경기 합계는 72득점이다. 원태인의 선발·패전 및 3⅓이닝 11피안타 2사사구 2탈삼진 9실점·시즌 7승 8패·ERA 4.66, 정해영의 구원 1이닝 무피안타 무실점·시즌 2승 1패 2세이브·ERA 6.23을 KBO 공식 투수표와 네이버 행으로 대조했다. 정해영은 공식 결과가 없어 game_decision을 null로 보존했다. 강백호의 3타수 무안타 1볼넷 1삼진·타율 0.286도 대조했다. 나머지 관심 투수와 노시환·김도영은 해당 팀 완료 경기의 KBO 공식·네이버 전체 명단에 없어 계약상 최소 객체로 보존했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts": []}
now = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": now, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": now, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel; text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text); text = re.sub(r"2026\.09\.\d{2}", "2026.09.20", text); text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 20일", text)
    path.write_text(text, encoding="utf-8")
(ART / "verification.json").write_text(json.dumps({"report_date": DATE, "games": len(games), "total_runs": 72, "source_status": {"kbo_game": "FINISHED x5", "kbo_official": "code=100 x5", "naver": "statusCode=4 x5", "daum": "gameStatus=END x5"}, "watched_pitchers": [p["name"] for p in pitchers if p["appeared"]], "watched_batters": [b["name"] for b in batters if b["appeared"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {now}")
