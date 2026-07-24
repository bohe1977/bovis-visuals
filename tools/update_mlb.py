#!/usr/bin/env python3
"""Build BOVIS MLB daily data from MLB Stats API using a KST game-start window."""
from __future__ import annotations
import json, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'mlb'/'data.json'
KST=ZoneInfo('Asia/Seoul')
UTC=timezone.utc
REPORT=datetime.now(KST).date()
START=datetime.combine(REPORT-timedelta(days=1),datetime.min.time(),tzinfo=UTC)+timedelta(hours=15)
END=START+timedelta(days=1)-timedelta(seconds=1)
PLAYER_SPECS=[
 ('오타니 쇼헤이',660271,'batter'),('이정후',808982,'batter'),('바비 위트 주니어',677951,'batter'),('마이크 트라웃',545361,'batter'),
 ('무라카미 무네타카',808959,'batter'),('송성문',823550,'batter'),('김하성',673490,'batter'),('김혜성',808975,'batter'),
 ('오타니 쇼헤이',660271,'pitcher'),('폴 스킨스',694973,'pitcher'),('고우석',808970,'pitcher')]
TEAM_KO={'Los Angeles Dodgers':'LA 다저스','San Francisco Giants':'샌프란시스코','Philadelphia Phillies':'필라델피아','Kansas City Royals':'캔자스시티','Pittsburgh Pirates':'피츠버그','Los Angeles Angels':'LA 에인절스','Chicago White Sox':'시카고 화이트삭스','San Diego Padres':'샌디에이고','Atlanta Braves':'애틀랜타','Gwinnett Stripers':'Gwinnett Stripers','Oklahoma City Comets':'Oklahoma City Comets','St. Paul Saints':'세인트폴 세인츠'}
def ko_team(name): return TEAM_KO.get(name,name)
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'BOVIS MLB daily collector/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
def api(path,**q):return get('https://statsapi.mlb.com/api/v1/'+path+('?' + urllib.parse.urlencode(q,doseq=True) if q else ''))
def iso(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def games_for_date(date,sport=1,team=None):
    q={'sportId':sport,'date':date.isoformat(),'hydrate':'linescore,decisions'}
    if team:q['teamId']=team
    return [g for d in api('schedule',**q).get('dates',[]) for g in d.get('games',[])]
def window_games(sport=1,team=None):
    gs=[]
    for date in (REPORT-timedelta(days=1),REPORT):
        gs+=games_for_date(date,sport,team)
    return {g['gamePk']:g for g in gs if START<=iso(g['gameDate'])<=END}
def fmt_stat(v,default='—'):
    return v if v not in (None,'') else default
def batter_season(pid,end):
    try:
      splits=api(f'people/{pid}/stats',stats='byDateRange',group='hitting',season=REPORT.year,startDate=f'{REPORT.year}-03-01',endDate=end).get('stats',[{}])[0].get('splits',[])
      return splits[0].get('stat',{}) if splits else {}
    except Exception:return {}
def pitcher_season(pid,end):
    try:
      splits=api(f'people/{pid}/stats',stats='byDateRange',group='pitching',season=REPORT.year,startDate=f'{REPORT.year}-03-01',endDate=end).get('stats',[{}])[0].get('splits',[])
      return splits[0].get('stat',{}) if splits else {}
    except Exception:return {}
def participant(box,pid,group):
    # Boxscore `players` includes roster shells; participation is established only by the role array.
    role='batters' if group=='batting' else 'pitchers'
    key='ID'+str(pid)
    for side in ('away','home'):
      team=box.get('teams',{}).get(side,{})
      if pid in team.get(role,[]):
        p=team.get('players',{}).get(key)
        if p and group in p.get('stats',{}): return p,side
    return None,None
def game_status(g):
    state=g['status'].get('abstractGameState','')
    detailed=g['status'].get('detailedState','')
    if state=='Final':return '경기 종료'
    if state in ('Preview','Pre-Game'):return '경기 예정'
    if 'Postponed' in detailed or 'Cancelled' in detailed:return '연기'
    return detailed or state or '상태 미확인'
def decision(g,k):return g.get('decisions',{}).get(k,{}).get('fullName')
def build_game(g,title):
    ls=g.get('linescore',{}); away=g['teams']['away']; home=g['teams']['home']; aw=away.get('score'); hw=home.get('score')
    ws=None
    if aw is not None and hw is not None and aw!=hw:ws='away' if aw>hw else 'home'
    a=ko_team(away['team']['name']); h=ko_team(home['team']['name']); status=game_status(g)
    winner=decision(g,'winner'); loser=decision(g,'loser'); save=decision(g,'save')
    outcome=(f'{a}, {h}에 {aw}–{hw} 승리' if ws=='away' else f'{a}, {h}에 {aw}–{hw} 패배' if ws=='home' else f'{a}–{h} {status}')
    points=[]
    if aw is not None: points.append(f'{a} {ls.get("teams",{}).get("away",{}).get("hits","—")}안타 {aw}득점, {h} {ls.get("teams",{}).get("home",{}).get("hits","—")}안타 {hw}득점.')
    if winner: points.append(f'공식 결정: {winner} 승리, {loser} 패전'+(f', {save} 세이브.' if save else '.'))
    return {'section_title':title,'game_pk':g['gamePk'],'officialDate':g['officialDate'],'game_date_utc':g['gameDate'],'naver_game_id':None,'daum_game_id':None,'venue':g.get('venue',{}).get('name','—'),'start_time_kst':iso(g['gameDate']).astimezone(KST).strftime('%H:%M'),'status':status,'away':a,'home':h,'winner_side':ws,'away_score':aw,'home_score':hw,'away_hits':ls.get('teams',{}).get('away',{}).get('hits'),'home_hits':ls.get('teams',{}).get('home',{}).get('hits'),'away_errors':ls.get('teams',{}).get('away',{}).get('errors'),'home_errors':ls.get('teams',{}).get('home',{}).get('errors'),'winner_pitcher':winner,'loser_pitcher':loser,'save_pitcher':save,'headline':outcome,'points':points or [f'MLB 공식 상태: {status}.'],'opponent_label':h if a=='LA 다저스' or a=='샌프란시스코' else a,'opponent_effort':'MLB 공식 Stats API/Gameday 기준.'}
def main():
    # `currentTeam` is only present when explicitly hydrated; do not infer it from a roster name.
    people={}
    for pid in sorted({x[1] for x in PLAYER_SPECS}):
      people[pid]=api(f'people/{pid}',hydrate='currentTeam').get('people',[{}])[0]
    mlb_games=window_games()
    boxes={}
    def box(pk):
      if pk not in boxes:boxes[pk]=api(f'game/{pk}/boxscore')
      return boxes[pk]
    # Teams that may be in affiliated ball: determine schedule from currentTeam sport id, then restrict gameDate window.
    team_games={}
    for pid,p in people.items():
      team=p.get('currentTeam',{}); tid=team.get('id')
      if tid:
        try:
          # The currentTeam hydration supplies team identity; the team resource supplies its league level.
          sport=api(f'teams/{tid}').get('teams',[{}])[0].get('sport',{}).get('id',1)
          team_games[pid]=window_games(sport,tid)
        except Exception: team_games[pid]={}
    batters=[]
    for name,pid,_ in PLAYER_SPECS[:8]:
      p=people[pid]; tg=team_games.get(pid,{})
      appearances=[]
      for pk,g in tg.items():
        pp,_side=participant(box(pk),pid,'batting')
        if pp:appearances.append((g,pp))
      team=ko_team(p.get('currentTeam',{}).get('name','—'))
      cutoff=max((g['officialDate'] for g in tg.values()),default=(REPORT-timedelta(days=1)).isoformat())
      season=batter_season(pid,cutoff)
      if appearances:
        g,pp=appearances[-1]; st=pp['stats']['batting']; pos=pp.get('position',{}).get('abbreviation','—')
        note=f'{pos} · {st.get("hits",0)}-{st.get("atBats",0)}'
        extras=[]
        for key,label in [('homeRuns','HR'),('triples','3B'),('doubles','2B'),('baseOnBalls','BB'),('strikeOuts','K')]:
          if st.get(key,0):extras.append(f'{st[key]} {label}')
        if extras:note+=' | '+', '.join(extras)
        status='출전'
      else:
        st={};pos='—'; status='비출전' if tg else '팀 경기 없음'; note='MLB 공식 boxscore: 타격 기록 없음' if tg else 'KST 대상일 현재 팀 경기 없음'
      batters.append({'name':name,'team':team,'mlbam_id':pid,'status':status,'position':pos,'at_bats':st.get('atBats'),'hits':st.get('hits'),'rbi':st.get('rbi'),'runs':st.get('runs'),'home_runs':st.get('homeRuns'),'walks':st.get('baseOnBalls'),'strikeouts':st.get('strikeOuts'),'avg':fmt_stat(season.get('avg')),'obp':fmt_stat(season.get('obp')),'ops':fmt_stat(season.get('ops')),'season_stats_cutoff':cutoff,'daily_note':note})
    pitchers=[]
    go_gamelog_verified=None
    for name,pid,_ in PLAYER_SPECS[8:]:
      p=people[pid];tg=team_games.get(pid,{})
      apps=[]
      for pk,g in tg.items():
        pp,_side=participant(box(pk),pid,'pitching')
        if pp:apps.append((g,pp))
      team=ko_team(p.get('currentTeam',{}).get('name','—'))
      if not tg:
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':False,'status':'팀 경기 없음'});continue
      # Any cancellation/pre-game means no unqualified non-appearance inference.
      states={game_status(g) for g in tg.values()}
      if any(x=='연기' for x in states):
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':False,'status':'연기'});continue
      if apps:
        g,pp=apps[-1];st=pp['stats']['pitching'];cutoff=g['officialDate'];season=pitcher_season(pid,cutoff)
        decisions=g.get('decisions',{}); outcome=''
        if decisions.get('winner',{}).get('id')==pid:outcome='승리'
        elif decisions.get('loser',{}).get('id')==pid:outcome='패전'
        elif decisions.get('save',{}).get('id')==pid:outcome='세이브'
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':True,'status':'등판'+(f' · {outcome}' if outcome else ''),'daily_innings':st.get('inningsPitched'),'daily_hits':st.get('hits'),'daily_runs':st.get('runs'),'daily_earned_runs':st.get('earnedRuns'),'daily_walks_hbp':st.get('baseOnBalls'),'daily_strikeouts':st.get('strikeOuts'),'daily_home_runs':st.get('homeRuns'),'daily_pitches':st.get('numberOfPitches'),'era':fmt_stat(season.get('era'))})
      elif all(game_status(g)=='경기 종료' for g in tg.values()):
        if pid==808970:
          # A separate official game log is required before calling Go's absence verified.
          try:
            gl=api(f'people/{pid}/stats',stats='gameLog',group='pitching',season=REPORT.year).get('stats',[{}])[0].get('splits',[])
            logged={x.get('game',{}).get('gamePk') for x in gl}
            go_gamelog_verified=not bool(logged.intersection(tg))
          except Exception:
            go_gamelog_verified=False
          if not go_gamelog_verified:
            pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':False,'status':'상태 미검증'})
            continue
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':False,'status':'등판 없음'})
      else:
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':False,'status':'경기 진행/예정'})
    targets=[]
    for title,teamid in [('LA 다저스 경기',119),('샌프란시스코 자이언츠 경기',137)]:
      ts=[g for g in mlb_games.values() if teamid in (g['teams']['away']['team']['id'],g['teams']['home']['team']['id'])]
      if ts: targets.append(build_game(ts[0],title))
      else: targets.append({'section_title':title,'game_pk':None,'officialDate':None,'game_date_utc':None,'naver_game_id':None,'daum_game_id':None,'venue':'—','start_time_kst':'—','status':'팀 경기 없음','away':'LA 다저스' if teamid==119 else '샌프란시스코','home':'—','winner_side':None,'away_score':None,'home_score':None,'away_hits':None,'home_hits':None,'away_errors':None,'home_errors':None,'winner_pitcher':None,'loser_pitcher':None,'save_pitcher':None,'headline':'KST 대상일 팀 경기 없음','points':['MLB 공식 schedule의 KST gameDate 기준.'],'opponent_label':'—','opponent_effort':'—'})
    # Cross-check endpoints are retained as provenance. Their dynamic IDs are not guessed.
    src=['https://statsapi.mlb.com/api/v1/schedule?sportId=1&date='+d.isoformat() for d in (REPORT-timedelta(days=1),REPORT)]
    src += [f'https://statsapi.mlb.com/api/v1/game/{pk}/boxscore' for pk in sorted(boxes)]
    data={'report_date_kst':REPORT.isoformat(),'official_date_mlb':(REPORT-timedelta(days=1)).isoformat(),'generated_at':datetime.now(KST).isoformat(timespec='seconds'),'verification':{'status':'MLB 공식 Stats API/Gameday 기준 · 네이버·다음 KST 일정 교차조회','method':f'KST {REPORT} UTC 창({START.isoformat().replace("+00:00","Z")}–{END.isoformat().replace("+00:00","Z")})에 실제 gameDate가 속한 경기만 미국 현지 전날·당일 schedule에서 선별했다. 시즌 누계는 MLB Stats API byDateRange의 각 경기 officialDate cutoff을 사용했다. 네이버·다음 KST 일정 URL을 교차조회했으며 동적 페이지의 경기 ID는 추정하지 않았다.','notes':[f'MLB 공식 schedule에서 KST 대상 창에 {len(mlb_games)}개 MLB 경기를 확인했다.', '투수 등판 여부는 MLBAM ID를 각 현재 팀의 KST 대상 gamePk 전체 boxscore 투수 객체와 대조했다.']+([f'고우석 gameLog와 팀 gamePk 대조: {"기록 없음으로 미등판 교차확인" if go_gamelog_verified else "해당 없음 또는 미검증"}.'] if go_gamelog_verified is not None else [])},'team_games':targets,'batters':batters,'pitchers':pitchers,'sources':{'mlb_official':src,'naver':[f'https://m.sports.naver.com/wbaseball/schedule/index?category=mlb&date={REPORT}'],'daum':[f'https://sports.daum.net/schedule/mlb?date={REPORT.strftime("%Y%m%d")}']}}
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report_date_kst':data['report_date_kst'],'target_mlb_games':len(mlb_games),'team_games':[(x['section_title'],x['status'],x['game_pk']) for x in targets],'pitchers':data['pitchers']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
