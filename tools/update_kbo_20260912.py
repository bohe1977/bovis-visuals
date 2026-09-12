#!/usr/bin/env python3
"""Build the reconciled 2026-09-12 KBO final-game report from captured source records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-12", "20260912"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260912HTKT0": 80108760, "20260912LGSS0": 80108761, "20260912LTWO0": 80108762, "20260912NCOB0": 80108763}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(gid):
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]

def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": gid, "stadium": stadium, "start_time": "17:00", "status": "경기 종료", "away": away, "home": home, "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(gid)}

games = [
    game("20260912NCOB0", "잠실", "NC", "두산", 10, 9, "구창모", "김정우", "이용준", "NC가 난타전 끝에 두산에 10-9 승리", [
        "NC 선발 구창모는 5⅓이닝 11피안타 2사사구 4탈삼진 7실점(2자책)으로 승리를 기록했다.",
        "6회 무사 1·2루에서 박민우의 우전 적시타가 공식 결승타가 됐다.",
        "김휘집은 4타수 3안타 1홈런 5타점, 권희동은 5타수 3안타 1홈런 2타점 3득점을 기록했다.",
        "이용준이 1이닝 1실점으로 시즌 세이브를 올리며 한 점 차 리드를 지켰다."],
        "두산은 조수행이 5타수 3안타 2타점, 세베리노가 5타수 2안타 3타점으로 끝까지 추격했지만 6회 이후 리드를 되찾지 못했다."),
    game("20260912LGSS0", "대구", "LG", "삼성", 4, 3, "고우석", "이승민", "손주영", "LG가 8회 송찬의의 결승 땅볼로 삼성에 4-3 역전승", [
        "LG 선발 톨허스트는 5⅓이닝 7피안타 무사사구 3탈삼진 2실점을 기록했고, 삼성 선발 후라도도 6이닝 9피안타 2실점으로 맞섰다.",
        "8회 1사 만루에서 송찬의의 3루수 땅볼이 공식 결승타가 됐다.",
        "오스틴은 5타수 3안타 2홈런 3타점 2득점으로 LG 공격을 이끌었다.",
        "LG는 고우석이 승리를 기록하고 손주영이 세이브로 1점 리드를 마무리했다."],
        "삼성은 강민호가 4타수 4안타 1홈런 2타점 2득점으로 분전했지만 8회 만루 위기를 막지 못했다."),
    game("20260912HTKT0", "수원", "KIA", "KT", 2, 6, "대니엘", "네일", None, "KT가 2회 최원준의 결승타를 앞세워 KIA에 6-2 승리", [
        "KT 선발 대니엘은 6이닝 4피안타 2사사구 9탈삼진 1실점으로 승리했다.",
        "2회 2사 3루에서 최원준의 중전 적시타가 공식 결승타가 됐다.",
        "최원준은 5타수 2안타 1타점 1득점, 류현인은 4타수 2안타 1타점 1득점을 기록했다.",
        "박영현이 1이닝 무실점으로 뒤를 받쳤고, KIA 정해영은 1⅓이닝 2실점으로 등판했다."],
        "KIA는 박정우가 5타수 2안타 1타점 1득점, 김호령이 4타수 1안타 1득점을 올렸으나 네일의 5이닝 3실점(2자책)을 만회하지 못했다."),
    game("20260912LTWO0", "고척", "롯데", "키움", 8, 0, "로드리게스", "알칸타라", None, "롯데가 로드리게스의 무실점 호투와 장단 16안타로 키움에 8-0 완승", [
        "롯데 선발 로드리게스는 5이닝 3피안타 3사사구 6탈삼진 무실점으로 승리했다.",
        "6회 1사 1·3루에서 나승엽의 중견수 희생플라이가 공식 결승타가 됐다.",
        "한동희는 5타수 2안타 1홈런 3타점, 전준우는 5타수 3안타 1홈런 1타점을 기록했다.",
        "김원중이 1이닝 무실점 홀드, 박정민이 1이닝 무실점으로 롯데 불펜을 이었다."],
        "키움은 서건창이 4타수 2안타, 김건희가 2타수 1안타로 분전했지만 4안타에 묶이며 득점하지 못했다."),
]

pitchers = [
    {"name":"원태인","team":"삼성","appeared":False}, {"name":"류현진","team":"한화","appeared":False}, {"name":"제레미 비슬리","team":"롯데","appeared":False}, {"name":"박세웅","team":"롯데","appeared":False}, {"name":"김진욱","team":"롯데","appeared":False},
    {"name":"김원중","team":"롯데","appeared":True,"innings":"1","hits":0,"runs":0,"earned_runs":0,"walks_hbp":1,"strikeouts":1,"home_runs":0,"pitches":13,"season_record":"1승 5패","season_saves":5,"era":"4.89","role":"reliever","game_decision":"홀드"},
    {"name":"박정민","team":"롯데","appeared":True,"innings":"1","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":0,"home_runs":0,"pitches":16,"season_record":"6승 3패","era":"3.78","role":"reliever","game_decision":None},
    {"name":"로드리게스","team":"롯데","appeared":True,"innings":"5","hits":3,"runs":0,"earned_runs":0,"walks_hbp":3,"strikeouts":6,"home_runs":0,"pitches":97,"season_record":"8승 11패","era":"4.20","role":"starter","game_decision":"승"},
    {"name":"임찬규","team":"LG","appeared":False},
    {"name":"정해영","team":"KIA","appeared":True,"innings":"1⅓","hits":1,"runs":2,"earned_runs":2,"walks_hbp":1,"strikeouts":3,"home_runs":0,"pitches":26,"season_record":"2승 1패","season_saves":2,"era":"6.17","role":"reliever","game_decision":None},
    {"name":"박영현","team":"KT","appeared":True,"innings":"1","hits":1,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":1,"home_runs":0,"pitches":13,"season_record":"6승 0패","season_saves":26,"era":"2.59","role":"reliever","game_decision":None},
]
batters = [
    {"name":"강백호","team":"한화","appeared":False}, {"name":"노시환","team":"한화","appeared":False}, {"name":"김도영","team":"KIA","appeared":False},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 42
for g in games:
    gid = g["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert official["code"] == "100" and board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}

source_urls = {"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[g["sources"][0]["url"] for g in games], "naver":[g["sources"][1]["url"] for g in games], "daum":[DAUM_SCHEDULE]+[g["sources"][2]["url"] for g in games]}
verification = {"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources":["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details":"2026-09-12 KST 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 42득점이다. 로드리게스·김원중·박정민·정해영·박영현의 실제 등판 라인과 시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했으며, 로드리게스의 선발·승리 및 김원중의 구원·홀드는 KBO 공식 결과와 네이버 wls를 확인했다. 실제 등판한 마무리투수 김원중·정해영·박영현의 시즌 세이브는 KBO 공식·네이버 기록으로 확인했다. 비등판 관심 투수는 해당 팀 완료 경기의 KBO 공식·네이버 전체 투수 명단 부재를 확인해 계약상 name·team·appeared만 보존했다. 한화는 해당 날짜 경기 없음, 김도영은 KIA 타자 명단 부재로 관심 타자 3명은 출전 없음으로 기록했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts":[]}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.12", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 12일", text)
    path.write_text(text,encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
