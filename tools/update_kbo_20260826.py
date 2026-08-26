#!/usr/bin/env python3
"""Write the reconciled 2026-08-26 KBO final-game report from captured records."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-26", "20260826"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260826&toDate=20260826"
DAUM_IDS = {"20260826HHSK0":80101137,"20260826LTHT0":80101138,"20260826NCLG0":80101139,"20260826OBKT0":80101140,"20260826SSWO0":80101141}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(game_id):
    return [{"label":"KBO 공식","url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},{"label":"네이버 기록","url":f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},{"label":"다음 기록","url":f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"}]

def game(game_id, stadium, away, home, a, h, winner, loser, headline, points, effort):
    return {"id":game_id,"stadium":stadium,"start_time":"18:30","status":"경기 종료","away":away,"home":home,"away_score":a,"home_score":h,"winner_pitcher":winner,"loser_pitcher":loser,"save_pitcher":None,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(game_id)}

games = [
 game("20260826NCLG0","잠실","NC","LG",0,8,"임찬규","구창모","LG가 임찬규의 6이닝 무실점과 오스틴의 2홈런으로 NC에 8-0 승리",["LG 선발 임찬규는 6이닝 2피안타 3사사구 4탈삼진 무실점으로 시즌 12승째를 거뒀다.","1회 2사 오스틴의 좌월 솔로포가 결승타가 됐다.","오스틴은 4타수 2안타 2홈런 4타점 2득점, 송찬의는 4타수 3안타 1홈런 1타점을 기록했다.","우강훈·김영우·이정용이 각 1이닝 무실점으로 완봉을 마무리했다."],"NC는 구창모가 5이닝 5실점했지만 신영우가 1이닝 무실점 2탈삼진으로 뒤를 버텼다."),
 game("20260826HHSK0","문학","한화","SSG",1,6,"최민준","류현진","SSG가 1회 박성한의 결승 2루타를 앞세워 한화에 6-1 승리",["SSG 선발 최민준은 5⅓이닝 2피안타 4사사구 무실점으로 승리투수가 됐다.","1회 무사 2루에서 박성한의 우익수 2루타가 결승타가 됐고, SSG는 6회 5득점으로 달아났다.","박성한은 4타수 2안타 1타점 1득점, 에레디아와 최지훈은 각각 2타점을 기록했다.","김민이 ⅔이닝 무실점 홀드를 기록했고 이건욱·노경은이 8~9회를 무실점으로 지켰다."],"한화는 류현진이 5이닝 3피안타 7탈삼진 1실점(비자책)으로 버텼고, 채은성이 7회 솔로포를 쳤다."),
 game("20260826LTHT0","광주","롯데","KIA",11,16,"김태형","로드리게스","KIA가 김도영의 결승 2루타와 카스트로의 2홈런으로 롯데에 16-11 승리",["KIA 선발 황동하는 2⅔이닝 3실점, 김태형은 2⅓이닝 2실점으로 구원승을 거뒀다.","3회 1사 1루 김도영의 좌중간 2루타가 결승타가 됐다.","카스트로는 5타수 3안타 2홈런 7타점, 김도영은 4타수 2안타 1홈런 4타점 3득점을 기록했다.","정해영은 8회 ⅓이닝을 삼진 1개로 무실점 처리했고 곽도규가 9회를 무실점으로 막았다."],"롯데는 레이예스가 4타수 4안타 1홈런 4타점 2득점, 한동희가 4타수 3안타 1타점으로 11득점 추격을 이끌었다."),
 game("20260826OBKT0","수원","두산","KT",4,5,"김정운","이영하","KT가 9회 김현수의 끝내기 안타로 두산에 5-4 승리",["KT 선발 대니엘은 6이닝 4피안타 4사사구 7탈삼진 2실점을 기록했고 김정운이 1이닝 무실점으로 승리투수가 됐다.","4-3으로 뒤진 9회 1사 만루에서 김현수의 우전 안타가 끝내기 결승타가 됐다.","김현수는 5타수 2안타 2타점, 장성우는 3타수 1안타 1홈런 1타점 1득점을 기록했다.","김정운이 9회 1이닝 무실점 1탈삼진으로 끝내기 승리의 기반을 만들었다."],"두산은 잭로그가 6이닝 1자책점 7탈삼진으로 버텼고 조수행·박찬호가 나란히 2안타 1타점을 기록했다."),
 game("20260826SSWO0","고척","삼성","키움",12,2,"최원태","박준현","삼성이 최형우의 1회 만루 결승포와 김영웅의 만루포로 키움에 12-2 승리",["삼성 선발 최원태는 6이닝 5피안타 2사사구 6탈삼진 2실점으로 승리했다.","1회 무사 만루에서 최형우의 중월 만루 홈런이 결승타가 됐다.","최형우는 5타수 2안타 1홈런 4타점, 김영웅은 4타수 1안타 1홈런 4타점, 김성윤은 2안타 2타점을 기록했다.","양창섭·사토시·배찬승이 7~9회를 무실점으로 막았고 배찬승은 1탈삼진을 보탰다."],"키움은 김건희가 4타수 1안타 2타점, 서건창과 히우라가 각각 2안타로 분전했다."),
]

pitchers = [
 {"name":"원태인","team":"삼성","appeared":False},
 {"name":"류현진","team":"한화","appeared":True,"role":"starter","game_decision":"패","innings":"5","hits":3,"runs":1,"earned_runs":0,"walks_hbp":0,"strikeouts":7,"home_runs":0,"pitches":86,"season_record":"8승 5패","era":"3.85"},
 {"name":"제레미 비슬리","team":"롯데","appeared":False},{"name":"박세웅","team":"롯데","appeared":False},{"name":"김진욱","team":"롯데","appeared":False},{"name":"김원중","team":"롯데","appeared":False},{"name":"박정민","team":"롯데","appeared":False},
 {"name":"로드리게스","team":"롯데","appeared":True,"role":"starter","game_decision":"패","innings":"3⅔","hits":6,"runs":8,"earned_runs":8,"walks_hbp":5,"strikeouts":7,"home_runs":2,"pitches":84,"season_record":"7승 9패","era":"4.23"},
 {"name":"임찬규","team":"LG","appeared":True,"role":"starter","game_decision":"승","innings":"6","hits":2,"runs":0,"earned_runs":0,"walks_hbp":3,"strikeouts":4,"home_runs":0,"pitches":105,"season_record":"12승 4패","era":"3.95"},
 {"name":"정해영","team":"KIA","appeared":True,"role":"reliever","game_decision":None,"innings":"⅓","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":1,"home_runs":0,"pitches":3,"season_record":"2승 1패","season_saves":2,"era":"6.00"},
 {"name":"박영현","team":"KT","appeared":False},
]
batters = [
 {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":0,"avg":"0.291","obp":None,"ops":None},
 {"name":"노시환","team":"한화","appeared":True,"at_bats":3,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":1,"strikeouts":2,"avg":"0.279","obp":None,"ops":None},
 {"name":"김도영","team":"KIA","appeared":True,"at_bats":4,"hits":2,"rbi":4,"runs":3,"home_runs":1,"walks":1,"strikeouts":1,"avg":"0.305","obp":None,"ops":None},
]
source_urls={"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[x["sources"][0]["url"] for x in games],"naver":[x["sources"][1]["url"] for x in games],"daum":[DAUM_SCHEDULE]+[x["sources"][2]["url"] for x in games]}
verification={"status":"KBO 공식 기준 · 네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-08-26 편성 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW 박스스코어, 네이버 공개 기록 API statusCode=4, 다음 일정 API gameStatus=END·스코어를 대조해 모두 최종 종료로 확정했다. 5경기 합계 65득점이며 취소·연기·노게임은 없다. 류현진·로드리게스·임찬규는 KBO 공식 선발 행과 네이버 기록에서 당일 라인·시즌 승패·ERA를 대조했고 각각 패·패·승으로 기록했다. 정해영은 KBO 공식 구원 행 및 네이버 기록에서 ⅓이닝 무실점·결정 기록 없음·시즌 2세이브를 대조했다. 나머지 관심 투수는 해당 팀 완료 경기의 KBO·네이버 전체 투수 명단에 없어 등판 없음으로 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO REVIEW와 네이버 API로 대조했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.","conflicts":[]}
assert len(games)==5 and all(g["status"]=="경기 종료" for g in games)
assert sum(g["away_score"]+g["home_score"] for g in games)==65
for p in pitchers:
 if not p["appeared"]: assert set(p)=={"name","team","appeared"}
 else: assert p["role"] in {"starter","reliever"} and p["game_decision"] in ({"승","패",None} if p["role"]=="starter" else {"세이브","홀드","블론",None})
(ROOT/"kbo"/"data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT/"kbo-players"/"data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for relative in ("kbo/index.html","kbo-players/index.html"):
 p=ROOT/relative;t=p.read_text(encoding="utf-8");t=t.replace("2026-08-25",DATE).replace("2026.08.25","2026.08.26").replace("2026년 8월 25일","2026년 8월 26일");p.write_text(t,encoding="utf-8")
print(f"wrote reconciled KBO data for {DATE} at {NOW}")
