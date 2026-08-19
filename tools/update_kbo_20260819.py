#!/usr/bin/env python3
"""Write the reconciled 2026-08-19 KBO final-game report."""
from __future__ import annotations
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-08-19", "20260819"
NOW = datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260819&toDate=20260819"
DAUM_IDS = {"20260819HTHH0":80101107,"20260819KTLG0":80101108,"20260819OBNC0":80101109,"20260819SKSS0":80101110,"20260819WOLT0":80101111}

def sources(game_id: str) -> list[dict[str,str]]:
    return [
        {"label":"KBO 공식","url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label":"네이버 기록","url":f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label":"다음 기록","url":f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]

games = [
 {"id":"20260819KTLG0","stadium":"잠실","start_time":"19:00","status":"경기 종료","away":"KT","home":"LG","away_score":0,"home_score":1,"winner_pitcher":"톨허스트","loser_pitcher":"대니엘","save_pitcher":"손주영","headline":"LG가 1회 송찬의의 결승타와 톨허스트의 7이닝 무실점으로 KT에 1-0 승리","winner_points":["LG 선발 톨허스트는 7이닝 2피안타 1사사구 5탈삼진 무실점으로 시즌 11승째를 거뒀다.","1회 2사 1·2루에서 송찬의가 중전 적시타를 쳐 이날의 유일한 득점이자 결승점을 만들었다.","송찬의는 4타수 2안타 1타점, 오지환은 4타수 2안타로 공격을 이끌었다.","우강훈이 홀드, 손주영이 1이닝 무실점으로 시즌 24세이브를 기록했다."],"opponent_effort":"KT는 선발 대니엘이 5이닝 7피안타 3탈삼진 1실점으로 버텼고, 불펜이 남은 3이닝을 무실점으로 막았다.","sources":sources("20260819KTLG0")},
 {"id":"20260819SKSS0","stadium":"대구","start_time":"19:00","status":"경기 종료","away":"SSG","home":"삼성","away_score":4,"home_score":18,"winner_pitcher":"보스","loser_pitcher":"타케다","save_pitcher":"","headline":"삼성이 디아즈의 1회 결승 2루타를 앞세워 SSG에 18-4 대승","winner_points":["삼성 선발 보스는 5이닝 5피안타 1사사구 12탈삼진 2실점으로 시즌 첫 승을 기록했다.","1회 1사 만루에서 디아즈가 우익수 쪽 2루타를 쳐 결승타를 만들었고, 삼성은 4·5회에 4홈런을 더했다.","디아즈는 5타수 3안타 1홈런 5타점, 구자욱은 5타수 3안타 1홈런 3타점을 기록했다.","삼성 불펜은 김재윤을 포함한 4명이 4이닝 2실점으로 리드를 지켰다."],"opponent_effort":"SSG는 최정이 3타수 2안타 1타점, 하재훈이 4타수 2안타 1타점으로 분전했다.","sources":sources("20260819SKSS0")},
 {"id":"20260819WOLT0","stadium":"사직","start_time":"19:00","status":"경기 종료","away":"키움","home":"롯데","away_score":4,"home_score":5,"winner_pitcher":"박정민","loser_pitcher":"원종현","save_pitcher":"","headline":"롯데가 9회 손성빈의 끝내기 홈런으로 키움에 5-4 승리","winner_points":["롯데 선발 로드리게스는 6이닝 3피안타 6사사구 4탈삼진 2실점으로 경기 초반을 지켰다.","4-4로 맞선 9회 손성빈이 원종현을 상대로 끝내기 솔로 홈런을 쳤다.","손성빈은 4타수 2안타 1홈런 1타점, 레이예스는 4타수 3안타 1득점을 기록했다.","박정민은 1⅓이닝 무피안타 무실점으로 공식 승리투수가 됐다."],"opponent_effort":"키움은 서건창이 4타수 2안타 2타점, 추재현이 5타수 2안타 1득점을 기록하며 끝까지 맞섰다.","sources":sources("20260819WOLT0")},
 {"id":"20260819OBNC0","stadium":"창원","start_time":"19:00","status":"경기 종료","away":"두산","home":"NC","away_score":8,"home_score":2,"winner_pitcher":"최민석","loser_pitcher":"테일러","save_pitcher":"","headline":"두산이 1회 김민석의 결승 밀어내기 볼넷부터 주도해 NC에 8-2 승리","winner_points":["두산 선발 최민석은 5이닝 6피안타 3사사구 4탈삼진 2실점으로 시즌 11승째를 챙겼다.","1회 1사 만루에서 김민석이 밀어내기 볼넷을 얻어 결승점을 냈고, 3회 안재석의 3점포로 격차를 벌렸다.","안재석은 5타수 3안타 1홈런 3타점 2득점, 김민석은 4타수 2안타 1타점 2득점을 올렸다.","김정우·타카다·박치국·김택연이 4이닝을 합쳐 무실점으로 막았다."],"opponent_effort":"NC는 김휘집이 4타수 2안타 1타점, 블레인이 4회 솔로 홈런으로 2득점에 힘을 보탰다.","sources":sources("20260819OBNC0")},
 {"id":"20260819HTHH0","stadium":"대전","start_time":"19:00","status":"경기 종료","away":"KIA","home":"한화","away_score":6,"home_score":3,"winner_pitcher":"성영탁","loser_pitcher":"박상원","save_pitcher":"이의리","headline":"KIA가 9회 박재현의 결승타와 김도영의 3점포로 한화에 6-3 승리","winner_points":["KIA 선발 시라카와는 6⅓이닝 2피안타 2사사구 3탈삼진 1실점으로 호투했다.","3-3이던 9회 무사 1·2루에서 박재현이 중전 결승타를 쳤고, 이어 김도영이 3점 홈런을 더했다.","김도영은 4타수 2안타 1홈런 3타점 1득점, 박재현은 5타수 2안타 2타점 1득점을 기록했다.","성영탁이 1⅓이닝 무실점으로 승리, 이의리가 1이닝 무실점으로 시즌 4세이브를 올렸다."],"opponent_effort":"한화는 노시환이 3타수 1안타 1홈런 2타점 1득점으로 7회 동점포를 쳤고, 화이트가 7이닝 2실점으로 버텼다.","sources":sources("20260819HTHH0")},
]

pitchers = [
 {"name":"원태인","team":"삼성","appeared":False}, {"name":"류현진","team":"한화","appeared":False},
 {"name":"제레미 비슬리","team":"롯데","appeared":False}, {"name":"박세웅","team":"롯데","appeared":False},
 {"name":"김진욱","team":"롯데","appeared":False}, {"name":"김원중","team":"롯데","appeared":False},
 {"name":"박정민","team":"롯데","appeared":True,"role":"reliever","game_decision":None,"innings":"1⅓","hits":0,"runs":0,"earned_runs":0,"walks_hbp":1,"strikeouts":0,"home_runs":0,"pitches":17,"season_record":"6승 2패","era":"3.96"},
 {"name":"로드리게스","team":"롯데","appeared":True,"role":"starter","game_decision":None,"innings":"6","hits":3,"runs":2,"earned_runs":2,"walks_hbp":6,"strikeouts":4,"home_runs":0,"pitches":98,"season_record":"7승 8패","era":"3.77"},
 {"name":"임찬규","team":"LG","appeared":False}, {"name":"정해영","team":"KIA","appeared":False}, {"name":"박영현","team":"KT","appeared":False},
]
batters = [
 {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":0,"avg":"0.303","obp":None,"ops":None},
 {"name":"노시환","team":"한화","appeared":True,"at_bats":3,"hits":1,"rbi":2,"runs":1,"home_runs":1,"walks":0,"strikeouts":0,"avg":"0.272","obp":None,"ops":None},
 {"name":"김도영","team":"KIA","appeared":True,"at_bats":4,"hits":2,"rbi":3,"runs":1,"home_runs":1,"walks":1,"strikeouts":0,"avg":"0.298","obp":None,"ops":None},
]
source_urls = {"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[g['sources'][0]['url'] for g in games],"naver":[g['sources'][1]['url'] for g in games],"daum":[DAUM_SCHEDULE]+[g['sources'][2]['url'] for g in games]}
verification = {"status":"KBO 공식 기준 · 네이버·다음 대조","sources":["KBO 공식 게임센터 REVIEW·상세기록","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],"details":"2026-08-19 KBO 5경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW 상세기록, 네이버 공개 기록 API statusCode=4·박스스코어, 다음 일정 API gameStatus=END·스코어를 대조해 최종 종료로 확정했다. 롯데 관심 투수 로드리게스(선발·결정 없음)와 박정민(구원·공식 승리)은 KBO 공식 박스스코어와 네이버 기록에서 당일 라인·시즌 승패·ERA를 대조했다. 구원 박정민의 공식 승리는 화면 계약상 세이브·홀드·블론만 배지로 쓰므로 game_decision에는 기록하지 않았다. 나머지 관심 투수는 해당 팀 완료 경기의 KBO·네이버 전체 투수 명단에 없어 등판 없음으로 확인했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버에서 대조했다. 다음의 타자 볼넷은 사사구 표기 범위 차이가 있어 독립 일치값으로 주장하지 않았다.","conflicts":[]}
(ROOT/'kbo'/'data.json').write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'kbo-players'/'data.json').write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for relative in ('kbo/index.html','kbo-players/index.html'):
    path=ROOT/relative; text=path.read_text(encoding='utf-8')
    for old,new in [('2026-08-18',DATE),('2026.08.18','2026.08.19'),('2026년 8월 18일','2026년 8월 19일'),('Generated 2026-08-19 06:20 KST','Generated 2026-08-20 06:20 KST'),('2026-08-18 06:20 KST','2026-08-19 06:20 KST')]: text=text.replace(old,new)
    path.write_text(text,encoding='utf-8')
print(f'wrote reconciled KBO data for {DATE} at {NOW}')
