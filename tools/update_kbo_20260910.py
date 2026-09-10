#!/usr/bin/env python3
"""Build the reconciled 2026-09-10 KBO report from captured official/Naver/Daum records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
DATE, COMPACT='2026-09-10','20260910'
ART=ROOT/'.artifacts'/f'kbo-{DATE}'
KBO='https://www.koreabaseball.com'
DAUM_SCHEDULE=f'https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}'
DAUM_IDS={'20260910WOOB0':80108875,'20260910KTLT0':80108755,'20260910HHSK0':80108754,'20260910NCHT0':80108756}
NOW=datetime.now(ZoneInfo('Asia/Seoul')).isoformat(timespec='seconds')

def sources(gid):
    return [{'label':'KBO 공식','url':f'{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW'}, {'label':'네이버 기록','url':f'https://api-gw.sports.naver.com/schedule/games/{gid}2026/record'}, {'label':'다음 기록','url':f'https://sports.daum.net/match/{DAUM_IDS[gid]}'}]
def game(gid,stadium,away,home,ascore,hscore,win,lose,save,headline,points,effort):
    return {'id':gid,'stadium':stadium,'start_time':'18:30','status':'경기 종료','away':away,'home':home,'away_score':ascore,'home_score':hscore,'winner_pitcher':win,'loser_pitcher':lose,'save_pitcher':save,'headline':headline,'winner_points':points,'opponent_effort':effort,'sources':sources(gid)}

games=[
 game('20260910WOOB0','잠실','키움','두산',0,5,'김정우','박준현',None,'두산이 세베리노의 2회 결승 홈런과 불펜 무실점으로 키움에 5-0 승리',["두산 선발 벤자민은 4⅔이닝 4피안타 무실점 6탈삼진으로 버텼다.","2회 1사에서 세베리노의 중월 솔로 홈런이 공식 결승타가 됐다.","세베리노는 결승 홈런을 포함해 타선을 이끌었고, 두산은 5득점으로 승부를 벌렸다.","김정우가 2⅓이닝 무실점으로 승리, 불펜이 남은 이닝을 무실점으로 막았다."],"키움은 박준현이 3⅓이닝 동안 버텼고 안타 4개를 기록했지만 득점으로 연결하지 못했다."),
 game('20260910KTLT0','사직','KT','롯데',16,3,'배제성','비슬리',None,'KT가 3회 김민혁의 결승타를 시작으로 16득점, 롯데에 16-3 대승',["KT 선발 배제성은 6이닝 3피안타 무실점 8탈삼진으로 승리를 기록했다.","3회 1사 2루에서 김민혁의 우전 안타가 공식 결승타가 됐다.","힐리어드는 5회 솔로 홈런(시즌 33호)을 쳤고, KT는 19안타로 16점을 냈다.","김정운·문용익이 각각 1이닝 무실점으로 뒤를 받쳤다."],"롯데는 고승민의 1회 3루타와 이호준의 9회 3루타를 포함해 8안타 3득점을 올렸지만 초반 대량 실점을 뒤집지 못했다."),
 game('20260910HHSK0','문학','한화','SSG',3,4,'아빌라','박준영','조병현','SSG가 박성한의 3회 결승타와 조병현의 세이브로 한화에 4-3 승리',["SSG 선발 아빌라는 6이닝 3피안타 1실점 6탈삼진으로 승리를 기록했다.","3회 1사 3루에서 박성한의 2루수 땅볼이 공식 결승타가 됐다.","김태연이 7회 문승원을 상대로 시즌 13호 2점 홈런을 쳐 한화의 추격을 이끌었다.","김민·이건욱이 홀드, 조병현이 1이닝 무실점으로 시즌 20세이브를 기록했다."],"한화는 김태연의 2점포로 7회 2점 차까지 추격했고, 박준영은 5이닝 4실점 뒤에도 타선이 끝까지 승부를 이어갔다."),
 game('20260910NCHT0','광주','NC','KIA',2,1,'손주환','조상우','이용준','NC가 연장 11회 김주원의 결승타로 KIA에 2-1 승리',["NC 선발 라일리는 7이닝 2피안타 무실점 6탈삼진으로 호투했다.","연장 11회 1사 3루에서 김주원의 유격수 내야안타가 공식 결승타가 됐다.","박건우는 5회 올러를 상대로 시즌 18호 솔로 홈런을 쳐 NC의 선취점을 만들었다.","손주환이 1⅔이닝 무실점으로 승리, 이용준이 1이닝 무실점으로 시즌 1세이브를 올렸다."],"KIA는 올러가 7이닝 2피안타 1실점 5탈삼진으로 버텼고, 연장 11회 김선빈의 적시타로 동점을 만들었지만 끝내기 실점을 막지 못했다.")]

pitchers=[
 {'name':'원태인','team':'삼성','appeared':False},
 {'name':'류현진','team':'한화','appeared':False},
 {'name':'제레미 비슬리','team':'롯데','appeared':True,'innings':'4','hits':10,'runs':9,'earned_runs':9,'walks_hbp':3,'strikeouts':4,'home_runs':1,'pitches':88,'season_record':'9승 6패','era':'5.15','role':'starter','game_decision':'패'},
 {'name':'박세웅','team':'롯데','appeared':False}, {'name':'김진욱','team':'롯데','appeared':False}, {'name':'김원중','team':'롯데','appeared':False}, {'name':'박정민','team':'롯데','appeared':False}, {'name':'로드리게스','team':'롯데','appeared':False}, {'name':'임찬규','team':'LG','appeared':False}, {'name':'정해영','team':'KIA','appeared':False}, {'name':'박영현','team':'KT','appeared':False}]
batters=[
 {'name':'강백호','team':'한화','appeared':True,'at_bats':3,'hits':0,'rbi':0,'runs':0,'home_runs':0,'walks':1,'strikeouts':1,'avg':'0.287','obp':None,'ops':None},
 {'name':'노시환','team':'한화','appeared':True,'at_bats':4,'hits':1,'rbi':0,'runs':0,'home_runs':0,'walks':0,'strikeouts':1,'avg':'0.281','obp':None,'ops':None},
 {'name':'김도영','team':'KIA','appeared':False}]
# Fixture-and-source assertions: official REVIEW, Naver record API and Daum schedule agree on every completed game and score.
kbo_game=json.loads((ART/'kbo-game.json').read_text(encoding='utf-8'))
daum=json.loads((ART/'daum-schedule.json').read_text(encoding='utf-8'))['schedule'][COMPACT]
assert {x['id'] for x in games}=={x['id'] for x in kbo_game if x['status']=='FINISHED'}==set(DAUM_IDS)
assert {x['gameId'] for x in daum if x['gameStatus']=='END'}==set(DAUM_IDS.values())
assert sum(x['away_score']+x['home_score'] for x in games)==34
for g in games:
 gid=g['id']; official=json.loads((ART/f'official-GetBoxScoreScroll-{gid}.json').read_text(encoding='utf-8-sig')); board=json.loads((ART/f'official-GetScoreBoardScroll-{gid}.json').read_text(encoding='utf-8-sig')); naver=json.loads((ART/f'naver-{gid}.json').read_text(encoding='utf-8'))['result']['recordData']; rheb=naver['scoreBoard']['rheb']
 assert official['code']=='100' and board['code']=='100' and naver['gameInfo']['statusCode']=='4'
 assert int(rheb['away']['r'])==g['away_score'] and int(rheb['home']['r'])==g['home_score']
for p in pitchers:
 if not p['appeared']: assert set(p)=={'name','team','appeared'}
source_urls={'kbo_official':[f'{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}']+[g['sources'][0]['url'] for g in games],'naver':[g['sources'][1]['url'] for g in games],'daum':[DAUM_SCHEDULE]+[g['sources'][2]['url'] for g in games]}
verification={'status':'KBO 공식 기준 · kbo-game·네이버·다음 대조','sources':['KBO 공식 게임센터 REVIEW/API','kbo-game','네이버스포츠 공개 기록 API','다음스포츠 일정·박스스코어'],'details':'2026-09-10 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 34득점이다. 비슬리는 KBO 공식 선발·패 행과 네이버 투수 행에서 4이닝 10피안타 3사사구 4탈삼진 9실점·시즌 9승 6패·ERA 5.15를 대조했다. 나머지 관심 투수는 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 계약상 name·team·appeared만 보존했다. 강백호·노시환은 KBO 공식·네이버 타자 행으로 당일 라인과 시즌 타율을 대조했고, 김도영은 KIA 타자 명단에 없어 출전 없음으로 기록했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.','conflicts':[]}
(ROOT/'kbo'/'data.json').write_text(json.dumps({'date':DATE,'generated_at':NOW,'source_urls':source_urls,'games':games},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'kbo-players'/'data.json').write_text(json.dumps({'report_date':DATE,'generated_at':NOW,'verification':verification,'pitchers':pitchers,'batters':batters,'source_urls':source_urls},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('kbo/index.html','kbo-players/index.html'):
 path=ROOT/rel; text=path.read_text(encoding='utf-8'); text=re.sub(r'2026-09-\d{2}',DATE,text); text=re.sub(r'2026\.09\.\d{2}','2026.09.10',text); text=re.sub(r'2026년 9월 \d{1,2}일','2026년 9월 10일',text); path.write_text(text,encoding='utf-8')
print(f'wrote reconciled KBO report {DATE} at {NOW}')
