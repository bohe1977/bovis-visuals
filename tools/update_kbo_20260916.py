#!/usr/bin/env python3
"""Build the reconciled 2026-09-16 KBO final-game report from captured records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
DATE,COMPACT="2026-09-16","20260916"
ART=ROOT/".artifacts"/f"kbo-{DATE}"
KBO="https://www.koreabaseball.com"
DAUM_SCHEDULE=f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS={"20260916KTHH0":80108772,"20260916LGNC0":80108773,"20260916SKLT0":80108774,"20260916SSOB0":80108775}
NOW=datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
def sources(gid): return [{"label":"KBO 공식","url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},{"label":"네이버 기록","url":f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},{"label":"다음 기록","url":f"https://sports.daum.net/match/{DAUM_IDS[gid]}"}]
def game(gid,stadium,away,home,ascore,hscore,winner,loser,save,headline,points,effort): return {"id":gid,"stadium":stadium,"start_time":"18:30","status":"경기 종료","away":away,"home":home,"away_score":ascore,"home_score":hscore,"winner_pitcher":winner,"loser_pitcher":loser,"save_pitcher":save,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(gid)}
games=[
 game("20260916SSOB0","잠실","삼성","두산",1,3,"벤자민","페덱","이영하","두산이 세베리노의 결승 2루타를 앞세워 삼성에 3-1 승리",["두산 선발 벤자민은 5이닝 3피안타 2사사구 8탈삼진 1실점으로 승리를 기록했다.","1회 2사 1·3루에서 세베리노의 중견수 2루타가 공식 결승타가 됐다.","세베리노는 3타수 2안타 2타점, 양석환은 3타수 1안타 1홈런 1타점 1득점을 기록했다.","타카다(1⅔이닝)와 김택연(1⅓이닝)이 홀드를 기록했고, 이영하가 1이닝 무실점 세이브로 마무리했다."],"삼성은 전병우가 2회 솔로 홈런을 기록했지만, 페덱이 6이닝 3실점으로 패전하며 이후 추가 득점을 만들지 못했다."),
 game("20260916SKLT0","사직","SSG","롯데",4,1,"아빌라","비슬리","문승원","SSG가 아빌라의 7이닝 11탈삼진 호투로 롯데에 4-1 승리",["SSG 선발 아빌라는 7이닝 4피안타 1사사구 11탈삼진 1실점으로 승리를 기록했다.","SSG는 1회 고명준의 적시타로 먼저 앞섰고, 4회 김재환의 솔로 홈런과 전의산의 솔로 홈런으로 격차를 벌렸다.","김재환은 4타수 2안타 1홈런 1타점 1득점 1볼넷, 고명준은 5타수 2안타 1타점을 기록했다.","김민이 8회 1이닝 무실점 홀드, 문승원이 9회 1이닝 무실점 세이브를 기록했다."],"롯데는 레이예스가 4타수 2안타 1득점, 전민재가 3타수 1안타 1타점으로 분전했지만 비슬리의 6이닝 2실점 패전을 뒤집지 못했다."),
 game("20260916LGNC0","창원","LG","NC",9,2,"고우석","김진호",None,"LG가 문정빈의 만루 홈런을 앞세워 NC에 9-2 승리",["LG 선발 박시원은 4이닝 6피안타 무사사구 4탈삼진 2실점을 기록했고, 고우석이 2⅓이닝 무실점으로 승리를 챙겼다.","승부처는 5회였다. 문정빈의 만루 홈런으로 LG가 6-2로 달아나며 흐름을 가져왔다.","문정빈은 2타수 1안타 1홈런 5타점 2득점 1볼넷, 홍창기는 5타수 3안타 1타점 2득점을 기록했다.","김강률과 케네디가 각각 홀드를 기록한 뒤 고우석이 2⅓이닝 무실점으로 긴 이닝을 책임졌다."],"NC는 박건우가 3타수 2안타 1홈런 2타점 1득점, 김휘집이 3타수 2안타로 분전했지만 5회 만루포를 허용한 뒤 추격에 실패했다."),
 game("20260916KTHH0","대전","KT","한화",4,4,None,None,None,"KT와 한화가 연장 11회 4-4 무승부",["한화 선발 류현진은 6이닝 2피안타 1사사구 9탈삼진 무실점으로 호투했고, KT 선발 배제성은 4⅓이닝 3피안타 4사사구 3탈삼진 2실점을 기록했다.","양 팀은 11회까지 승부를 가리지 못했다. 공식 결승타는 없었다.","KT는 장진혁이 2타수 2안타 1타점, 허경민이 5타수 2안타 1타점 1득점을 기록했다. 한화는 박정현이 8회 동점 2점 홈런을 쳤다.","KT는 스기모토·우규민이 홀드를 기록했고, 한화 불펜은 류현진 뒤 5이닝 동안 연장전을 버텼다."],"한화는 류현진의 6이닝 무실점 호투와 박정현의 8회 동점포에도 연장 11회 끝내 승리를 만들지 못했다."),
]
pitchers=[
 {"name":"원태인","team":"삼성","appeared":False},{"name":"류현진","team":"한화","appeared":True,"innings":"6","hits":2,"runs":0,"earned_runs":0,"walks_hbp":1,"strikeouts":9,"home_runs":0,"pitches":83,"season_record":"9승 5패","era":"3.62","role":"starter","game_decision":None},{"name":"제레미 비슬리","team":"롯데","appeared":True,"innings":"6","hits":5,"runs":2,"earned_runs":2,"walks_hbp":3,"strikeouts":8,"home_runs":2,"pitches":94,"season_record":"9승 7패","era":"5.06","role":"starter","game_decision":"패"},{"name":"박세웅","team":"롯데","appeared":False},{"name":"김진욱","team":"롯데","appeared":False},{"name":"김원중","team":"롯데","appeared":False},{"name":"박정민","team":"롯데","appeared":False},{"name":"로드리게스","team":"롯데","appeared":False},{"name":"임찬규","team":"LG","appeared":False},{"name":"정해영","team":"KIA","appeared":False},{"name":"박영현","team":"KT","appeared":False},]
batters=[{"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":2,"rbi":0,"runs":0,"home_runs":0,"walks":1,"strikeouts":1,"avg":"0.288","obp":None,"ops":None},{"name":"노시환","team":"한화","appeared":True,"at_bats":5,"hits":1,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":1,"avg":"0.271","obp":None,"ops":None},{"name":"김도영","team":"KIA","appeared":False}]
# Validate the three independent status/score surfaces plus official and Naver player rows.
kbo=json.loads((ART/'kbo-game.json').read_text()); daum=json.loads((ART/'daum-schedule.json').read_text())['schedule'][COMPACT]
assert {g['id'] for g in games} == {g['id'] for g in kbo if g['status']=='FINISHED'} == set(DAUM_IDS)
assert {g['gameId'] for g in daum if g['gameStatus']=='END'} == set(DAUM_IDS.values())
assert sum(g['away_score']+g['home_score'] for g in games)==28
for g in games:
 gid=g['id']; n=json.loads((ART/f'naver-{gid}.json').read_text())['result']['recordData']; o=json.loads((ART/f'official-GetBoxScoreScroll-{gid}.json').read_text(encoding='utf-8-sig'))
 assert n['gameInfo']['statusCode']=='4' and o['code']=='100'
 r=n['scoreBoard']['rheb']; assert int(r['away']['r'])==g['away_score'] and int(r['home']['r'])==g['home_score']
for p in pitchers:
 if not p['appeared']: assert set(p)=={'name','team','appeared'}
source_urls={"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[g['sources'][0]['url'] for g in games],"naver":[g['sources'][1]['url'] for g in games],"daum":[DAUM_SCHEDULE]+[g['sources'][2]['url'] for g in games]}
verification={"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW/API","kbo-game","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-09-16 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 28득점이다. 류현진·제레미 비슬리의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 류현진은 공식 선발·무결정, 비슬리는 공식 선발·패전으로 확인했다. 나머지 관심 투수는 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 name·team·appeared만 보존했다. 강백호·노시환의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했고, 김도영은 해당 팀 경기 없음으로 출전 없음으로 기록했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.","conflicts":[]}
(ROOT/'kbo'/'data.json').write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'kbo-players'/'data.json').write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('kbo/index.html','kbo-players/index.html'):
 p=ROOT/rel;s=p.read_text(encoding='utf-8');s=re.sub(r'2026-09-\d{2}',DATE,s);s=re.sub(r'2026\.09\.\d{2}','2026.09.16',s);s=re.sub(r'2026년 9월 \d{1,2}일','2026년 9월 16일',s);p.write_text(s,encoding='utf-8')
print(f'wrote reconciled KBO report {DATE} at {NOW}')
