#!/usr/bin/env python3
"""Build the reconciled 2026-09-11 KBO report from captured official, Naver and Daum records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-11", "20260911"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260911WOSS0": 80108759, "20260911KTLT0": 80108757, "20260911SKHT0": 80108876, "20260911NCHH0": 80108758}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(gid):
    return [
      {"label":"KBO 공식", "url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
      {"label":"네이버 기록", "url":f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
      {"label":"다음 기록", "url":f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]
def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id":gid,"stadium":stadium,"start_time":"18:30","status":"경기 종료","away":away,"home":home,"away_score":away_score,"home_score":home_score,"winner_pitcher":winner,"loser_pitcher":loser,"save_pitcher":save,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(gid)}

games = [
 game("20260911WOSS0","대구","키움","삼성",4,6,"페덱","전준표","김재윤","삼성이 디아즈의 2홈런 5타점에 힘입어 키움에 6-4 승리",[
  "삼성 선발 페덱은 6이닝 9피안타 3실점, 볼넷 없이 5탈삼진으로 승리를 기록했다.",
  "1회 1사 1·2루에서 최형우의 우전 적시타가 공식 결승타가 됐다.",
  "디아즈는 3타수 3안타 2홈런 5타점 2득점, 구자욱은 4타수 2안타 2득점을 기록했다.",
  "이승민·김태훈이 각각 1이닝 무실점 홀드, 김재윤이 1이닝 1실점으로 시즌 32세이브를 올렸다."],
  "키움은 박찬혁이 4타수 2안타 1홈런 2타점, 데이비슨이 4타수 2안타 1홈런으로 추격했지만 1회 리드를 뒤집지 못했다."),
 game("20260911KTLT0","사직","KT","롯데",7,1,"로건","김진욱",None,"KT가 2회 류현인의 결승 희생플라이를 시작으로 롯데에 7-1 승리",[
  "KT 선발 로건은 5⅓이닝 7피안타 1실점 3탈삼진으로 승리를 기록했다.",
  "2회 1사 2·3루에서 류현인의 좌익수 희생플라이가 공식 결승타가 됐다.",
  "힐리어드는 4타수 2안타 3타점 3득점, 안현민은 2타수 2안타 2볼넷 1득점을 기록했다.",
  "스기모토·오원석·손동현이 홀드를 이어가며 KT 불펜이 리드를 지켰다."],
  "롯데는 전민재가 4타수 3안타로 분전했고 레이예스가 3회 솔로 홈런을 쳤지만, 이후 추가 득점이 없었다."),
 game("20260911SKHT0","광주","SSG","KIA",2,5,"양현종","박시후","곽도규","KIA가 박재현의 5회 결승 홈런과 양현종의 호투로 SSG에 5-2 승리",[
  "KIA 선발 양현종은 5⅓이닝 4피안타 2실점 7탈삼진으로 승리를 기록했다.",
  "5회 2사에서 박재현의 우월 솔로 홈런이 공식 결승타가 됐다.",
  "박재현은 2타수 1안타 1홈런 1타점 2득점, 박정우는 3타수 2안타 1타점 2득점을 기록했다.",
  "전상현이 1⅔이닝 무실점 홀드, 곽도규가 2이닝 무실점 세이브로 마무리했다."],
  "SSG는 정준재가 3타수 2안타 1볼넷 1득점으로 출루했고, 선발 이준기가 3이닝 1피안타 2실점으로 버텼으나 득점 지원이 부족했다."),
 game("20260911NCHH0","대전","NC","한화",9,7,"류진욱","강재민","전사민","NC가 8회 박민우의 결승 희생플라이로 한화에 9-7 승리",[
  "NC 선발 이재학은 5이닝 6피안타 6실점 4탈삼진이었고, 류진욱이 ⅔이닝 무실점으로 승리를 기록했다.",
  "8회 무사 만루에서 박민우의 좌익수 희생플라이가 공식 결승타가 됐다.",
  "박민우는 3타수 3안타 3타점 2득점 1볼넷, 김형준은 5타수 2안타 1홈런 1타점을 기록했다.",
  "배재환이 1이닝 1실점 홀드, 전사민이 1이닝 무실점 세이브로 지켰다."],
  "한화는 심우준이 3타수 3안타 2볼넷 1타점 1득점, 허인서가 솔로 홈런 포함 2타점을 올리며 끝까지 맞섰다."),
]

pitchers = [
 {"name":"원태인","team":"삼성","appeared":False}, {"name":"류현진","team":"한화","appeared":False}, {"name":"제레미 비슬리","team":"롯데","appeared":False}, {"name":"박세웅","team":"롯데","appeared":False},
 {"name":"김진욱","team":"롯데","appeared":True,"innings":"5","hits":4,"runs":3,"earned_runs":3,"walks_hbp":4,"strikeouts":4,"home_runs":0,"pitches":102,"season_record":"6승 8패","era":"3.95","role":"starter","game_decision":"패"},
 {"name":"김원중","team":"롯데","appeared":True,"innings":"1","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":1,"home_runs":0,"pitches":14,"season_record":"1승 5패","season_saves":5,"era":"5.00","role":"reliever","game_decision":None},
 {"name":"박정민","team":"롯데","appeared":True,"innings":"1","hits":0,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":1,"home_runs":0,"pitches":6,"season_record":"6승 3패","era":"3.86","role":"reliever","game_decision":None},
 {"name":"로드리게스","team":"롯데","appeared":False}, {"name":"임찬규","team":"LG","appeared":False}, {"name":"정해영","team":"KIA","appeared":False}, {"name":"박영현","team":"KT","appeared":False},
]
batters = [
 {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":1,"rbi":1,"runs":0,"home_runs":0,"walks":0,"strikeouts":1,"avg":"0.287","obp":None,"ops":None},
 {"name":"노시환","team":"한화","appeared":True,"at_bats":4,"hits":0,"rbi":0,"runs":1,"home_runs":0,"walks":1,"strikeouts":2,"avg":"0.279","obp":None,"ops":None},
 {"name":"김도영","team":"KIA","appeared":False},
]

kbo_game=json.loads((ART/'kbo-game.json').read_text())
daum=json.loads((ART/'daum-schedule.json').read_text())["schedule"][COMPACT]
assert {g['id'] for g in games} == {g['id'] for g in kbo_game if g['status']=='FINISHED'} == set(DAUM_IDS)
assert {g['gameId'] for g in daum if g['gameStatus']=='END'} == set(DAUM_IDS.values())
assert sum(g['away_score'] + g['home_score'] for g in games) == 41
for g in games:
    gid=g['id']; official=json.loads((ART/f'official-GetBoxScoreScroll-{gid}.json').read_text(encoding='utf-8-sig')); board=json.loads((ART/f'official-GetScoreBoardScroll-{gid}.json').read_text(encoding='utf-8-sig')); naver=json.loads((ART/f'naver-{gid}.json').read_text())["result"]["recordData"]
    assert official['code']=='100' and board['code']=='100' and naver['gameInfo']['statusCode']=='4'
    rheb=naver['scoreBoard']['rheb']; assert int(rheb['away']['r'])==g['away_score'] and int(rheb['home']['r'])==g['home_score']
for p in pitchers:
    if not p['appeared']: assert set(p)=={'name','team','appeared'}
# Exact watched-player rows from the complete Naver pitcher/hitter arrays; official KBO box-score responses above are captured in the same packet.
ktlt=json.loads((ART/'naver-20260911KTLT0.json').read_text())["result"]["recordData"]
nchh=json.loads((ART/'naver-20260911NCHH0.json').read_text())["result"]["recordData"]
all_pitchers=[x for side in ('away','home') for x in ktlt['pitchersBoxscore'][side]]
by_name={x['name']:x for x in all_pitchers}
assert (by_name['김진욱']['inn'],by_name['김진욱']['wls'],by_name['김진욱']['era'])==('5','패','3.95')
assert (by_name['김원중']['inn'],by_name['김원중']['s'])==('1',5)
assert by_name['박정민']['inn']=='1'
all_batters=[x for side in ('away','home') for x in nchh['battersBoxscore'][side]]
bat_by_name={x['name']:x for x in all_batters}
assert (bat_by_name['강백호']['ab'],bat_by_name['강백호']['hit'],bat_by_name['강백호']['rbi'],bat_by_name['강백호']['hra'])==(4,1,1,'0.287')
assert (bat_by_name['노시환']['ab'],bat_by_name['노시환']['hit'],bat_by_name['노시환']['bb'],bat_by_name['노시환']['hra'])==(4,0,1,'0.279')

source_urls={"kbo_official":[f'{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}']+[g['sources'][0]['url'] for g in games],"naver":[g['sources'][1]['url'] for g in games],"daum":[DAUM_SCHEDULE]+[g['sources'][2]['url'] for g in games]}
verification={"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW/API","kbo-game","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-09-11 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 41득점이다. 김진욱·김원중·박정민의 당일 등판 라인과 시즌 성적·ERA는 KBO 공식 박스스코어와 네이버 투수 행으로 대조했고, 김진욱의 선발·패전 및 김원중·박정민의 구원·무결정은 공식 결과 행과 네이버 pitchingResult를 확인했다. 김원중의 시즌 5세이브는 공식·네이버 기록으로 확인했다. 비등판 투수는 해당 팀 완료 경기의 KBO 공식·네이버 전체 투수 명단 부재를 확인해 계약상 name·team·appeared만 보존했다. 강백호·노시환의 당일 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했고, 김도영은 KIA 타자 명단에 없어 출전 없음으로 기록했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.","conflicts":[]}
(ROOT/'kbo'/'data.json').write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+'\n')
(ROOT/'kbo-players'/'data.json').write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+'\n')
for rel in ('kbo/index.html','kbo-players/index.html'):
    p=ROOT/rel; text=p.read_text(); text=re.sub(r'2026-09-\d{2}',DATE,text); text=re.sub(r'2026\.09\.\d{2}','2026.09.11',text); text=re.sub(r'2026년 9월 \d{1,2}일','2026년 9월 11일',text); p.write_text(text)
print(f'wrote reconciled KBO report {DATE} at {NOW}')
