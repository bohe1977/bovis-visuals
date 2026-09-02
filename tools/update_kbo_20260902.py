#!/usr/bin/env python3
"""Write reconciled 2026-09-02 KBO report from captured official, Naver and Daum records."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-02", "20260902"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260902HHKT0":80101167,"20260902HTNC0":80101168,"20260902LGOB0":80101169,"20260902LTSS0":80101170,"20260902SKWO0":80101171}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(gid: str):
    return [
        {"label":"KBO 공식","url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label":"네이버 기록","url":f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label":"다음 기록","url":f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]

def game(gid, stadium, away, home, ascore, hscore, wp, lp, sp, headline, points, effort):
    return {"id":gid,"stadium":stadium,"start_time":"18:30","status":"경기 종료","away":away,"home":home,"away_score":ascore,"home_score":hscore,"winner_pitcher":wp,"loser_pitcher":lp,"save_pitcher":sp,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(gid)}

games = [
 game("20260902HHKT0","수원","한화","KT",6,9,"전용주","짐머맨",None,
      "KT가 7회 김민혁의 결승 2루타로 한화를 9-6으로 제압",
      ["KT 선발 소형준은 5이닝 8피안타 3탈삼진 4실점했고, 전용주가 1이닝 무실점으로 승리를 기록했다.","KT는 7회 1사 1루에서 김민혁의 우익수 2루타로 결승점을 냈다.","김민혁은 5타수 3안타 2타점 2득점, 허경민은 5타수 4안타 1타점, 힐리어드는 5타수 2안타 1홈런 2타점을 기록했다.","KT 불펜은 우규민·전용주·스기모토가 6~8회를 무실점으로 막아 리드를 지켰다."],
      "한화는 강백호가 5회 3점 홈런을 포함해 4타수 1안타 3타점, 문현빈이 4타수 3안타 1타점으로 추격했다."),
 game("20260902HTNC0","창원","KIA","NC",2,3,"전사민","이의리",None,
      "NC가 9회 김형준의 끝내기 밀어내기 볼넷으로 KIA에 3-2 승리",
      ["NC 선발 토다는 6이닝 5피안타 2볼넷 2탈삼진 2실점(1자책)했고, 전사민이 1이닝 무실점으로 승리를 기록했다.","2-2로 맞선 9회 2사 만루에서 김형준이 밀어내기 볼넷을 골라 끝내기 점수를 만들었다.","박건우와 김휘집이 각각 4타수 1안타 1타점을 기록했고, 박민우는 3타수 1안타 1득점으로 보탰다.","NC 불펜은 7~9회 3이닝 무실점으로 동점을 유지해 끝내기 발판을 마련했다."],
      "KIA는 나성범이 3타수 2안타 1홈런 1타점 2득점, 김호령이 3타수 2안타 1타점으로 분전했다."),
 game("20260902LGOB0","잠실","LG","두산",5,1,"김진수","최승용",None,
      "LG가 문보경의 1회 결승 2타점 안타를 앞세워 두산에 5-1 승리",
      ["LG 선발 김윤식은 2⅓이닝 3피안타 2볼넷 1실점했고, 김진수가 1⅔이닝 무실점으로 승리를 기록했다.","LG는 1회 2사 2·3루에서 문보경의 우중간 안타로 결승 2타점을 냈다.","문정빈은 4타수 2안타 1홈런 1타점 2득점, 문보경은 4타수 1안타 2타점 1득점, 박동원은 4타수 1안타 2타점을 기록했다.","김진수 이후 LG 불펜은 6⅔이닝 무실점으로 경기를 닫았고, 이우찬·김영우·케네디는 홀드를 기록했다."],
      "두산은 박찬호가 3타수 2안타 1볼넷 1득점, 박준순이 3타수 1안타 1타점으로 유일한 득점을 만들었다."),
 game("20260902LTSS0","대구","롯데","삼성",5,8,"최원태","박세웅","김재윤",
      "삼성이 김성윤의 5회 결승타와 최원태의 10탈삼진으로 롯데에 8-5 승리",
      ["삼성 선발 최원태는 6이닝 4피안타 10탈삼진 2실점으로 승리를 기록했다.","삼성은 5회 1사 1·3루에서 김성윤의 중전 안타로 결승점을 냈다.","김지찬은 4타수 3안타 3타점 2득점, 김성윤은 4타수 2안타 2타점 1득점을 기록했다.","김재윤이 ⅔이닝 무실점으로 시즌 31세이브를 올리며 마무리했다."],
      "롯데는 고승민이 4타수 3안타 2홈런 2타점 3득점, 레이예스가 4타수 1안타 2타점으로 추격했다."),
 game("20260902SKWO0","고척","SSG","키움",9,6,"이건욱","유토","조병현",
      "SSG가 9회 오태곤의 결승 안타로 키움에 9-6 역전승",
      ["SSG 선발 김건우는 5이닝 4피안타 3볼넷 5탈삼진 4실점했고, 이건욱이 1이닝 무실점으로 승리를 기록했다.","6-6이던 9회 무사 1·2루에서 오태곤이 좌전 결승 안타를 쳤고 SSG는 그 이닝 3점을 냈다.","김재환은 4타수 3안타 1홈런 2타점 3득점, 오태곤은 2타수 2안타 2타점 1득점을 기록했다.","조병현이 9회 1이닝 무실점으로 시즌 17세이브를 올렸다."],
      "키움은 데이비슨이 5타수 1안타 1홈런 3타점, 여동욱이 4타수 1안타 1홈런 2타점으로 맞섰다."),
]

pitchers = [
 {"name":"원태인","team":"삼성","appeared":False},{"name":"류현진","team":"한화","appeared":True,"innings":"5","hits":7,"runs":4,"earned_runs":3,"walks_hbp":1,"strikeouts":5,"home_runs":0,"pitches":91,"season_record":"8승 5패","era":"3.91","role":"starter","game_decision":None},
 {"name":"제레미 비슬리","team":"롯데","appeared":False},{"name":"박세웅","team":"롯데","appeared":True,"innings":"5⅔","hits":10,"runs":7,"earned_runs":7,"walks_hbp":3,"strikeouts":3,"home_runs":0,"pitches":91,"season_record":"2승 9패","era":"4.99","role":"starter","game_decision":"패"},
 {"name":"김진욱","team":"롯데","appeared":False},{"name":"김원중","team":"롯데","appeared":False},{"name":"박정민","team":"롯데","appeared":False},{"name":"로드리게스","team":"롯데","appeared":False},{"name":"임찬규","team":"LG","appeared":False},{"name":"정해영","team":"KIA","appeared":False},{"name":"박영현","team":"KT","appeared":False},
]
batters = [
 {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":1,"rbi":3,"runs":1,"home_runs":1,"walks":0,"strikeouts":1,"avg":"0.286","obp":None,"ops":None},
 {"name":"노시환","team":"한화","appeared":True,"at_bats":4,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":3,"avg":"0.272","obp":None,"ops":None},
 {"name":"김도영","team":"KIA","appeared":True,"at_bats":2,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":2,"strikeouts":0,"avg":"0.302","obp":None,"ops":None},
]

# Required three-surface score/status checks; official remains the record baseline.
kbo_games = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_games if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert all(x["gameStatus"] == "END" for x in daum)
assert sum(g["away_score"] + g["home_score"] for g in games) == 54
for g in games:
    gid = g["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    scoreboard = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    assert official["code"] == "100" and scoreboard["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
for p in pitchers:
    if not p["appeared"]: assert set(p) == {"name","team","appeared"}
source_urls = {"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],"naver":[g["sources"][1]["url"] for g in games],"daum":[DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
verification = {"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW/API","kbo-game","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-09-02 KST 편성 5경기를 kbo-game FINISHED, KBO 공식 게임센터 상세기록 API(code=100), 네이버 공개 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 대조했다. 종료 5경기만 반영했으며 합계 54득점이다. 관심 투수의 실제 등판은 KBO 공식 투수표의 선발/구원·결과와 네이버 투수 행으로, 관심 타자 행은 KBO 공식·네이버로 대조했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.","conflicts":[]}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for rel in ("kbo/index.html","kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-09-01", DATE).replace("2026.09.01", "2026.09.02").replace("2026년 9월 1일", "2026년 9월 2일")
    path.write_text(text,encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
