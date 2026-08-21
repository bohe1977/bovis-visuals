#!/usr/bin/env python3
"""Write the reconciled 2026-08-21 KBO final-game report from saved official/API captures."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-21", "20260821"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260821&toDate=20260821"
DAUM_IDS = {"20260821HTWO0": 80101117, "20260821KTSK0": 80101118, "20260821LGHH0": 80101119, "20260821LTOB0": 80101120, "20260821SSNC0": 80101121}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


games = [
    {"id":"20260821HTWO0", "stadium":"고척", "start_time":"19:00", "status":"경기 종료", "away":"KIA", "home":"키움", "away_score":11, "home_score":1, "winner_pitcher":"양현종", "loser_pitcher":"하영민", "save_pitcher":"", "headline":"KIA가 박재현의 2회 결승타와 김호령의 6타점으로 키움에 11-1 승리", "winner_points":["KIA 선발 양현종은 5⅓이닝 2피안타 3사사구 5탈삼진 1실점으로 시즌 9승째를 거뒀다.", "2회 2사 1·3루에서 박재현의 우전 적시타가 결승타가 됐고, KIA는 7회에만 5점을 더했다.", "박재현은 6타수 4안타 3타점, 김호령은 4타수 3안타 1홈런 6타점, 김도영은 4타수 2안타 1볼넷 1득점을 기록했다.", "이태양이 1⅔이닝 무실점 홀드, 김태형이 2이닝 무실점으로 뒤를 막았다."], "opponent_effort":"키움은 하영민이 6이닝 9피안타 2사사구 6탈삼진 3실점으로 선발 몫을 했고, 데이비슨이 1타점으로 유일한 득점을 냈다.", "sources":sources("20260821HTWO0")},
    {"id":"20260821KTSK0", "stadium":"문학", "start_time":"19:00", "status":"경기 종료", "away":"KT", "home":"SSG", "away_score":3, "home_score":3, "winner_pitcher":"", "loser_pitcher":"", "save_pitcher":"", "headline":"KT와 SSG가 연장 11회까지 3-3으로 승부를 가리지 못했다", "winner_points":["KT 선발 배제성은 4⅔이닝 4피안타 2사사구 3탈삼진 2실점, SSG 선발 김건우는 6이닝 4피안타 2사사구 9탈삼진 1실점을 기록했다.", "KT 안현민이 4회 솔로포와 8회 2점포로 3타점을 냈고, SSG는 7회 박성한의 적시타로 3-1까지 앞섰다.", "안현민은 4타수 2안타 2홈런 3타점 2득점, SSG 전의산은 3타수 2안타 1타점, 에레디아는 5타수 2안타 1득점을 기록했다.", "KT 박영현은 1이닝 무피안타 무사사구 3탈삼진, SSG 조병현은 1이닝 1피안타 1사사구 무실점으로 연장전까지 버텼다."], "opponent_effort":"SSG는 11회 연장까지 10안타를 만들었고, 김민·조병현·이건욱·서진용이 4이닝 무실점으로 KT 타선을 묶어 무승부를 지켰다.", "sources":sources("20260821KTSK0")},
    {"id":"20260821LGHH0", "stadium":"대전", "start_time":"19:00", "status":"경기 종료", "away":"LG", "home":"한화", "away_score":11, "home_score":15, "winner_pitcher":"조동욱", "loser_pitcher":"배재준", "save_pitcher":"", "headline":"한화가 난타전 끝 8회 김태연의 결승타로 LG에 15-11 승리", "winner_points":["양 팀 선발은 조기 강판됐고, 한화 조동욱이 8회 ⅓이닝 무실점으로 시즌 2승째를 거뒀다.", "한화는 0-10에서 6회까지 8-10으로 추격한 뒤 8회 2사 1·3루 김태연의 중전 결승타를 포함해 4점을 뽑았다.", "문현빈은 6타수 4안타 4타점 3득점, 김태연은 5타수 2안타 1홈런 3타점, 한지윤은 6타수 3안타 2타점을 기록했다.", "이민우가 1이닝 무실점, 장유호가 ⅔이닝 무실점으로 연결한 뒤 조동욱이 결승 구간을 맡았다."], "opponent_effort":"LG는 1회 7점으로 앞서 나갔고 이주헌이 4타점, 송찬의가 2안타 1홈런 3타점, 홍창기가 3안타 1타점으로 끝까지 11점을 냈다.", "sources":sources("20260821LGHH0")},
    {"id":"20260821LTOB0", "stadium":"잠실", "start_time":"19:00", "status":"경기 종료", "away":"롯데", "home":"두산", "away_score":11, "home_score":4, "winner_pitcher":"김진욱", "loser_pitcher":"최승용", "save_pitcher":"", "headline":"롯데가 김진욱의 6이닝 1실점과 고승민의 2홈런 6타점으로 두산에 11-4 승리", "winner_points":["롯데 선발 김진욱은 6이닝 1피안타 3사사구 7탈삼진 1실점으로 시즌 6승째를 거뒀다.", "5회 2사 2루에서 레이예스의 우전 적시타가 결승타가 됐고, 롯데는 8회 고승민의 만루포로 5점을 더했다.", "고승민은 5타수 2안타 2홈런 6타점 3득점, 레이예스는 5타수 4안타 1타점 2득점, 나승엽은 6타수 2안타 1타점 2득점을 기록했다.", "이이무라가 1⅓이닝 무실점 홀드를 기록했고 김한결이 ⅔이닝 무실점으로 뒤를 받쳤다."], "opponent_effort":"두산은 정수빈이 4타수 3안타 1타점, 양의지가 3볼넷 2득점으로 출루하며 7회 2점을 만회했다.", "sources":sources("20260821LTOB0")},
    {"id":"20260821SSNC0", "stadium":"창원", "start_time":"19:00", "status":"경기 종료", "away":"삼성", "home":"NC", "away_score":2, "home_score":3, "winner_pitcher":"토다", "loser_pitcher":"원태인", "save_pitcher":"전사민", "headline":"NC가 1회 박민우의 결승타를 지켜 삼성에 3-2 승리", "winner_points":["NC 선발 토다는 5⅓이닝 5피안타 3사사구 1탈삼진 2실점으로 시즌 6승째를 거뒀다.", "NC는 1회 1사 3루에서 박민우의 2루수 땅볼로 선취했고, 3회 최정원의 2타점 적시타로 3-0을 만들었다.", "최정원은 3타수 3안타 2타점, 김주원은 4타수 2안타 2득점, 천재환은 3타수 2안타 1득점을 기록했다.", "배재환·이용준·손주환이 홀드를 나눠 기록했고, 전사민이 1이닝 무실점으로 시즌 8세이브를 올렸다."], "opponent_effort":"삼성은 원태인이 7이닝 6피안타 2사사구 2탈삼진 3실점으로 완투에 가깝게 버텼고, 디아즈가 6회 2점 홈런으로 1점 차까지 추격했다.", "sources":sources("20260821SSNC0")},
]

pitchers = [
    {"name":"원태인","team":"삼성","appeared":True,"role":"starter","game_decision":"패","innings":"7","hits":6,"runs":3,"earned_runs":3,"walks_hbp":2,"strikeouts":2,"home_runs":0,"season_record":"6승 6패","era":"4.40"},
    {"name":"류현진","team":"한화","appeared":False},
    {"name":"제레미 비슬리","team":"롯데","appeared":False},
    {"name":"박세웅","team":"롯데","appeared":False},
    {"name":"김진욱","team":"롯데","appeared":True,"role":"starter","game_decision":"승","innings":"6","hits":1,"runs":1,"earned_runs":1,"walks_hbp":3,"strikeouts":7,"home_runs":0,"season_record":"6승 5패","era":"3.37"},
    {"name":"김원중","team":"롯데","appeared":False},
    {"name":"박정민","team":"롯데","appeared":False},
    {"name":"로드리게스","team":"롯데","appeared":False},
    {"name":"임찬규","team":"LG","appeared":False},
    {"name":"정해영","team":"KIA","appeared":False},
    {"name":"박영현","team":"KT","appeared":True,"role":"reliever","game_decision":None,"innings":"1","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":3,"home_runs":0,"season_record":"6승 0패","season_saves":22,"era":"2.25"},
]

batters = [
    {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":2,"rbi":2,"runs":0,"home_runs":0,"walks":2,"strikeouts":0,"avg":"0.301","obp":None,"ops":None},
    {"name":"노시환","team":"한화","appeared":True,"at_bats":4,"hits":2,"rbi":1,"runs":1,"home_runs":0,"walks":2,"strikeouts":0,"avg":"0.276","obp":None,"ops":None},
    {"name":"김도영","team":"KIA","appeared":True,"at_bats":4,"hits":2,"rbi":0,"runs":1,"home_runs":0,"walks":1,"strikeouts":0,"avg":"0.304","obp":None,"ops":None},
]

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status":"KBO 공식 기준 · 네이버·다음 대조",
    "sources":["KBO 공식 게임센터 REVIEW","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],
    "details":"2026-08-21 KBO 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW 경로, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조해 최종 종료로 확정했다. 5경기 합계 64득점이며 취소·연기·노게임은 없다. 원태인(선발·패), 김진욱(선발·승), 박영현(구원·결정 없음)의 당일 라인·시즌 승패·ERA는 KBO REVIEW와 네이버 박스스코어로 대조했다. 박영현의 시즌 22세이브는 공식 기록 기준으로 반영했다. 나머지 관심 투수는 해당 팀 완료 경기의 네이버 전체 투수 명단과 KBO REVIEW에서 빠져 있어 등판 없음으로 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO REVIEW와 네이버 기록 API로 대조했다. 다음의 타자 볼넷은 사사구 표기 범위 차이가 있어 독립 일치값으로 주장하지 않았다.",
    "conflicts":[],
}

(ROOT / "kbo" / "data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
for relative in ("kbo/index.html","kbo-players/index.html"):
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace("2026-08-20",DATE).replace("2026.08.20","2026.08.21").replace("2026년 8월 20일","2026년 8월 21일")
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
