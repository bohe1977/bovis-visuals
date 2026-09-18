#!/usr/bin/env python3
"""Build the reconciled 2026-09-18 KBO final-game report from captured records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-18", "20260918"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260918LGKT0": 80108778, "20260918NCLT0": 80108779, "20260918SSHH0": 80108780, "20260918WOOB0": 80108781}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(gid):
    return [
        {"label":"KBO 공식","url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label":"네이버 기록","url":f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label":"다음 기록","url":f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]

def game(gid, stadium, away, home, ascore, hscore, winner, loser, save, headline, points, effort):
    return {"id":gid,"stadium":stadium,"start_time":"18:30","status":"경기 종료","away":away,"home":home,"away_score":ascore,"home_score":hscore,"winner_pitcher":winner,"loser_pitcher":loser,"save_pitcher":save,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(gid)}

games = [
    game("20260918LGKT0", "수원", "LG", "KT", 12, 1, "톨허스트", "로건", None,
         "LG가 5회와 8회 대량 득점으로 KT에 12-1 승리", [
             "LG 선발 톨허스트는 6이닝 5피안타 1사사구 7탈삼진 1실점으로 승리를 기록했다.",
             "LG는 5회 3점을 보태 6-0으로 달아났고, 8회 5득점으로 승부를 굳혔다.",
             "오지환은 5타수 4안타 2홈런 4타점 2득점, 송찬의는 3타수 2안타 2타점 2득점을 기록했다.",
             "이우찬·이정용·양우진이 각각 1이닝씩 무실점으로 이어 던졌다."],
         "KT는 김현수가 3타수 2안타 1홈런 1타점으로 유일한 득점을 만들었고 안현민도 4타수 2안타로 분전했지만, 5회 이후 LG 타선을 막지 못했다."),
    game("20260918NCLT0", "사직", "NC", "롯데", 6, 9, "로드리게스", "이재학", None,
         "롯데가 4·5회 연속 빅이닝으로 NC에 9-6 승리", [
             "롯데 선발 로드리게스는 7⅔이닝 6피안타 무사사구 9탈삼진 5실점으로 승리를 기록했다.",
             "롯데는 4회 3점과 5회 2점을 더해 7-1로 격차를 벌렸고, NC의 8회 3득점 추격을 견뎠다.",
             "한동희는 4타수 3안타 1홈런 1타점 1득점, 전민재는 3타수 2안타 3타점 1득점 2볼넷을 기록했다.",
             "김원중이 8회 ⅓이닝 무실점 홀드를 기록했고, 이이무라가 9회 1실점으로 경기를 마쳤다."],
         "NC는 윤준혁이 1타수 1안타 1홈런 2타점 1득점, 박민우가 4타수 2안타 1홈런 1타점 2득점으로 8회 추격을 이끌었지만 초반 열세를 뒤집지 못했다."),
    game("20260918SSHH0", "대전", "삼성", "한화", 10, 4, "후라도", "박준영", None,
         "삼성이 5회 5득점 빅이닝을 앞세워 한화에 10-4 승리", [
             "삼성 선발 후라도는 7이닝 6피안타 무사사구 7탈삼진 3실점(1자책)으로 승리를 기록했다.",
             "3회 선취점 뒤 5회 5득점을 더해 6-0으로 달아난 장면이 승부처였다.",
             "구자욱은 3타수 3안타 5타점 1득점 1볼넷, 최형우는 3타수 1안타 1홈런 2타점 1득점을 기록했다.",
             "장찬희와 임기영이 남은 2이닝을 합쳐 3피안타 1실점으로 막았다."],
         "한화는 강백호가 4타수 2안타 1타점 1득점, 한지윤이 4타수 2안타 1득점으로 분전했고 7회 3점을 냈지만 5회 대량 실점을 만회하지 못했다."),
    game("20260918WOOB0", "잠실", "키움", "두산", 6, 6, None, None, None,
         "키움과 두산이 연장 11회 6-6 무승부", [
             "키움 선발 알칸타라는 6⅔이닝 7피안타 2사사구 5탈삼진 6실점을 기록했고, 두산 선발 잭로그는 4⅔이닝 5피안타 1사사구 1탈삼진 3실점(2자책)을 기록했다.",
             "두산이 7회 3득점으로 6-3을 만들었지만, 키움이 8회 3득점으로 동점을 만들며 승부가 연장으로 이어졌다.",
             "키움 박찬혁은 6타수 3안타 2홈런 5타점 2득점, 두산 안재석은 5타수 3안타 2타점 2득점을 기록했다.",
             "키움은 이강준·유토·김선기·조영건이 8회부터 4이닝 무실점, 두산은 이영하·이용찬·김정우가 9회부터 3이닝 무실점으로 버텼다."],
         "두산은 세베리노가 4타수 2안타 1홈런 1타점 1득점으로 분전했고 7회 역전에 성공했지만, 8회 동점을 허용한 뒤 연장 11회까지 결승점을 만들지 못했다."),
]

pitchers = [
    {"name":"원태인","team":"삼성","appeared":False},
    {"name":"류현진","team":"한화","appeared":False},
    {"name":"제레미 비슬리","team":"롯데","appeared":False},
    {"name":"박세웅","team":"롯데","appeared":False},
    {"name":"김진욱","team":"롯데","appeared":False},
    {"name":"김원중","team":"롯데","appeared":True,"innings":"⅓","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":0,"home_runs":0,"pitches":3,"season_record":"1승 5패 5세이브","season_saves":5,"era":"4.75","role":"reliever","game_decision":"홀드"},
    {"name":"박정민","team":"롯데","appeared":False},
    {"name":"로드리게스","team":"롯데","appeared":True,"innings":"7⅔","hits":6,"runs":5,"earned_runs":5,"walks_hbp":0,"strikeouts":9,"home_runs":2,"pitches":101,"season_record":"9승 11패","era":"4.28","role":"starter","game_decision":"승"},
    {"name":"임찬규","team":"LG","appeared":False},
    {"name":"정해영","team":"KIA","appeared":False},
    {"name":"박영현","team":"KT","appeared":False},
]
batters = [
    {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":2,"rbi":1,"runs":1,"home_runs":0,"walks":0,"strikeouts":0,"avg":"0.290","obp":None,"ops":None},
    {"name":"노시환","team":"한화","appeared":False},
    {"name":"김도영","team":"KIA","appeared":False},
]

def official_pitchers(gid):
    doc=json.loads((ART/f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig")); assert doc["code"]=="100"
    rows=[]
    for team in doc["arrPitcher"]:
        tab=json.loads(team["table"]); heads=[c["Text"] for c in tab["headers"][0]["row"]]
        rows.extend(dict(zip(heads,[c["Text"] for c in row["row"]])) for row in tab["rows"])
    return rows

def official_hitters(gid):
    doc=json.loads((ART/f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig")); assert doc["code"]=="100"
    return {row["row"][2]["Text"] for team in doc["arrHitter"] for row in json.loads(team["table1"])["rows"] if len(row["row"])>=3}

kbo_game=json.loads((ART/"kbo-game.json").read_text(encoding="utf-8"))
daum=json.loads((ART/"daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games}=={g["id"] for g in kbo_game if g["status"]=="FINISHED"}==set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"]=="END"}==set(DAUM_IDS.values())
assert sum(g["away_score"]+g["home_score"] for g in games)==54
for g in games:
    gid=g["id"]
    board=json.loads((ART/f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver=json.loads((ART/f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"]=="100" and naver["gameInfo"]["statusCode"]=="4"
    r=naver["scoreBoard"]["rheb"]
    assert (board["AWAY_NM"],board["HOME_NM"])==(g["away"],g["home"])
    assert (int(r["away"]["r"]),int(r["home"]["r"]))==(g["away_score"],g["home_score"])
    official_p={x["선수명"]:x for x in official_pitchers(gid)}
    naver_p={x["name"]:x for side in ("away","home") for x in naver["pitchersBoxscore"][side]}
    official_h=official_hitters(gid)
    naver_h={x["name"]:x for side in ("away","home") for x in naver["battersBoxscore"][side]}
    for p in pitchers:
        if p["team"] in (g["away"],g["home"]):
            if p["appeared"]:
                assert p["name"] in official_p and p["name"] in naver_p
            else: assert p["name"] not in official_p and p["name"] not in naver_p
    for b in batters:
        if b["team"] in (g["away"],g["home"]):
            if b["appeared"]: assert b["name"] in official_h and b["name"] in naver_h
            else: assert b["name"] not in official_h and b["name"] not in naver_h
for p in pitchers:
    if not p["appeared"]: assert set(p)=={"name","team","appeared"}
source_urls={"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[g["sources"][0]["url"] for g in games],"naver":[g["sources"][1]["url"] for g in games],"daum":[DAUM_SCHEDULE]+[g["sources"][2]["url"] for g in games]}
verification={"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW/API","kbo-game","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-09-18 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 54득점이다. 로드리게스와 김원중의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했다. 로드리게스는 공식 선발·승리, 김원중은 공식 구원·홀드로 확인했고 김원중의 공식 시즌 5세이브를 보존했다. 강백호의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 나머지 관심 투수와 노시환은 해당 팀 완료 경기의 KBO 공식·네이버 전체 명단에 없어 계약상 최소 객체로 보존했으며, 김도영은 KIA 경기 없음으로 출전 없음이다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.","conflicts":[]}
(ROOT/"kbo"/"data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"kbo-players"/"data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for rel in ("kbo/index.html","kbo-players/index.html"):
    path=ROOT/rel; text=path.read_text(encoding="utf-8")
    text=re.sub(r"2026-09-\d{2}",DATE,text); text=re.sub(r"2026\.09\.\d{2}","2026.09.18",text); text=re.sub(r"2026년 9월 \d{1,2}일","2026년 9월 18일",text)
    path.write_text(text,encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
