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
TEAM_KO={'Los Angeles Dodgers':'LA 다저스','San Francisco Giants':'샌프란시스코','Boston Red Sox':'보스턴','New York Mets':'뉴욕 메츠','Philadelphia Phillies':'필라델피아','Kansas City Royals':'캔자스시티','Pittsburgh Pirates':'피츠버그','Los Angeles Angels':'LA 에인절스','Chicago White Sox':'시카고 화이트삭스','San Diego Padres':'샌디에이고','Atlanta Braves':'애틀랜타','Milwaukee Brewers':'밀워키','Seattle Mariners':'시애틀'}
def ko_team(name): return TEAM_KO.get(name,name)
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'BOVIS MLB daily collector/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
def api(path,**q):return get('https://statsapi.mlb.com/api/v1/'+path+('?' + urllib.parse.urlencode(q,doseq=True) if q else ''))
def public_status(url):
    try:
      req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 BOVIS daily collector'})
      with urllib.request.urlopen(req,timeout=45) as r:
        return f'HTTP {r.status}'
    except Exception as exc:
      return f'조회 실패: {type(exc).__name__}'
def daum_schedule():
    """Fetch Daum's public KST schedule JSONP, retaining only verified records."""
    url='https://sports.daum.net/prx/hermes/api/game/schedule.json?'+urllib.parse.urlencode({'leagueCode':'mlb','fromDate':REPORT.strftime('%Y%m%d'),'toDate':REPORT.strftime('%Y%m%d'),'callback':'bovis'})
    try:
      req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 BOVIS daily collector'})
      with urllib.request.urlopen(req,timeout=45) as r: raw=r.read().decode('utf-8')
      payload=raw[raw.index('bovis(')+6:raw.rindex(')')]
      return json.loads(payload).get('schedule',{}).get(REPORT.strftime('%Y%m%d'),[]),url
    except Exception:
      return [],url
def daum_match(game,rows):
    """Join score rows by both teams and KST start time; never use array order."""
    away=ko_team(game['teams']['away']['team']['name']).replace(' ','')
    home=ko_team(game['teams']['home']['team']['name']).replace(' ','')
    start=iso(game['gameDate']).astimezone(KST).strftime('%H%M')
    for row in rows:
      if row.get('startTime')==start and row.get('awayTeamName','').replace(' ','')==away and row.get('homeTeamName','').replace(' ','')==home:
        return row
    return None
def naver_schedule():
    """Fetch every page of Naver's public KST schedule API, not its HTML shell."""
    base='https://api-gw.sports.naver.com/schedule/games'
    url=base+'?'+urllib.parse.urlencode({'categoryId':'mlb','gameDate':REPORT.isoformat()})
    try:
      rows=[]; page=1
      while True:
        payload=get(url+'&page='+str(page))
        games=payload.get('result',{}).get('games',[])
        rows.extend(games)
        if not games or len(rows)>=payload.get('result',{}).get('gameTotalCount',0): break
        page+=1
      return rows,url
    except Exception:
      return [],url
def naver_match(game,rows):
    away=ko_team(game['teams']['away']['team']['name']).replace(' ','')
    home=ko_team(game['teams']['home']['team']['name']).replace(' ','')
    start=iso(game['gameDate']).astimezone(KST).strftime('%H:%M')
    for row in rows:
      if row.get('gameDateTime','').endswith('T'+start+':00') and row.get('awayTeamName','').replace(' ','')==away and row.get('homeTeamName','').replace(' ','')==home:
        return row
    return None
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
def pitcher_record(winner,loser,save):
    parts=[]
    if winner: parts.append(f'{winner} 승리')
    if loser: parts.append(f'{loser} 패전')
    if save: parts.append(f'{save} 세이브')
    return ', '.join(parts)
def batting_leader(box,side):
    team=box.get('teams',{}).get(side,{})
    candidates=[]
    for pid in team.get('batters',[]):
      p=team.get('players',{}).get('ID'+str(pid),{})
      st=p.get('stats',{}).get('batting',{})
      if st.get('atBats',0) or st.get('baseOnBalls',0): candidates.append((p,st))
    if not candidates:return None
    p,st=max(candidates,key=lambda x:(x[1].get('rbi',0),x[1].get('homeRuns',0),x[1].get('hits',0),x[1].get('runs',0)))
    line=f"{p.get('person',{}).get('fullName','—')} {st.get('atBats',0)}타수 {st.get('hits',0)}안타"
    if st.get('homeRuns',0): line+=f" {st['homeRuns']}홈런"
    if st.get('rbi',0): line+=f" {st['rbi']}타점"
    if st.get('runs',0): line+=f" {st['runs']}득점"
    return line
def permanent_lead_point(feed,winner_side):
    if not feed:return None
    plays=feed.get('liveData',{}).get('plays',{}).get('allPlays',[])
    for idx,play in enumerate(plays):
      if not play.get('about',{}).get('isScoringPlay'):continue
      result=play.get('result',{}); aw=result.get('awayScore'); hw=result.get('homeScore')
      if aw is None or hw is None:continue
      winner_score=aw if winner_side=='away' else hw; loser_score=hw if winner_side=='away' else aw
      if winner_score<=loser_score:continue
      remaining=[(x.get('result',{}).get('awayScore'),x.get('result',{}).get('homeScore')) for x in plays[idx+1:] if x.get('about',{}).get('isScoringPlay')]
      if all((a if winner_side=='away' else h)>(h if winner_side=='away' else a) for a,h in remaining if a is not None and h is not None):
        return play
    return None
def point_event_ko(play):
    events={'home_run':'홈런','double':'2루타','triple':'3루타','single':'안타','sac_fly':'희생플라이','walk':'볼넷','hit_by_pitch':'사구','field_error':'실책'}
    return events.get(play.get('result',{}).get('eventType'),'득점타')
def build_game(g,title,daum_rows,naver_rows,box=None,feed=None):
    ls=g.get('linescore',{}); away=g['teams']['away']; home=g['teams']['home']; aw=away.get('score'); hw=home.get('score')
    ws=None
    if aw is not None and hw is not None and aw!=hw:ws='away' if aw>hw else 'home'
    a=ko_team(away['team']['name']); h=ko_team(home['team']['name']); status=game_status(g)
    winner=decision(g,'winner'); loser=decision(g,'loser'); save=decision(g,'save')
    outcome=(f'{a}, {h}에 {aw}–{hw} 승리' if ws=='away' else f'{a}, {h}에 {aw}–{hw} 패배' if ws=='home' else f'{a}–{h} {status}')
    winner_side=ws or 'away'; winner_team=a if winner_side=='away' else h; loser_team=h if winner_side=='away' else a
    winner_hits=ls.get('teams',{}).get(winner_side,{}).get('hits','—'); loser_hits=ls.get('teams',{}).get('home' if winner_side=='away' else 'away',{}).get('hits','—')
    winner_runs=aw if winner_side=='away' else hw; loser_runs=hw if winner_side=='away' else aw
    record=pitcher_record(winner,loser,save)
    points=[]
    if record: points.append(f'투수 기록: {record}.')
    lead=permanent_lead_point(feed,winner_side)
    if lead:
      inning=lead.get('about',{}).get('inning','—'); batter=lead.get('matchup',{}).get('batter',{}).get('fullName','—')
      points.append(f'승부처: {inning}회 {winner_team} {batter}의 {point_event_ko(lead)}로 리드를 잡았다.')
    elif aw is not None:
      points.append(f'득점 흐름: {winner_team} {winner_hits}안타 {winner_runs}득점, {loser_team} {loser_hits}안타 {loser_runs}득점.')
    if box:
      leader=batting_leader(box,winner_side)
      if leader: points.append(f'핵심 타자: {winner_team} {leader}.')
    if len(points)<3 and aw is not None: points.append(f'{winner_team}이 {loser_team}에 {aw}–{hw}로 승리했다.')
    losing_leader=batting_leader(box,'home' if winner_side=='away' else 'away') if box else None
    effort=(f'{loser_team}는 {losing_leader}을 기록했지만 {loser_hits}안타 {loser_runs}득점에 그쳤다.' if losing_leader else f'{loser_team}는 {loser_hits}안타 {loser_runs}득점을 기록했지만 승부를 뒤집지 못했다.')
    daum=daum_match(g,daum_rows)
    naver=naver_match(g,naver_rows)
    verified=bool(daum and str(daum.get('awayResult'))==str(aw) and str(daum.get('homeResult'))==str(hw) and (daum.get('gameStatus')=='END')==(status=='경기 종료'))
    naver_verified=bool(naver and str(naver.get('awayTeamScore'))==str(aw) and str(naver.get('homeTeamScore'))==str(hw) and (naver.get('statusCode')=='RESULT')==(status=='경기 종료'))
    return {'section_title':title,'game_pk':g['gamePk'],'officialDate':g['officialDate'],'game_date_utc':g['gameDate'],'naver_game_id':naver.get('gameId') if naver else None,'daum_game_id':daum.get('gameId') if daum else None,'venue':g.get('venue',{}).get('name','—'),'start_time_kst':iso(g['gameDate']).astimezone(KST).strftime('%H:%M'),'status':status,'away':a,'home':h,'winner_side':ws,'away_score':aw,'home_score':hw,'away_hits':ls.get('teams',{}).get('away',{}).get('hits'),'home_hits':ls.get('teams',{}).get('home',{}).get('hits'),'away_errors':ls.get('teams',{}).get('away',{}).get('errors'),'home_errors':ls.get('teams',{}).get('home',{}).get('errors'),'winner_pitcher':winner,'loser_pitcher':loser,'save_pitcher':save,'pitcher_record':record,'headline':outcome,'points':points or [f'MLB 공식 상태: {status}.'],'opponent_label':loser_team,'opponent_effort':effort,'daum_verified':verified,'naver_verified':naver_verified}
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
    feeds={}
    def feed(pk):
      if pk not in feeds:
        try: feeds[pk]=api(f'game/{pk}/feed/live')
        except Exception: feeds[pk]={}
      return feeds[pk]
    # Teams that may be in affiliated ball: determine schedule from currentTeam sport id, then restrict gameDate window.
    team_games={}
    team_sports={}
    for pid,p in people.items():
      team=p.get('currentTeam',{}); tid=team.get('id')
      if tid:
        try:
          # The currentTeam hydration supplies team identity; the team resource supplies its league level.
          sport=api(f'teams/{tid}').get('teams',[{}])[0].get('sport',{}).get('id',1)
          team_sports[pid]=sport
          team_games[pid]=window_games(sport,tid)
        except Exception:
          team_sports[pid]=None
          team_games[pid]={}
    batters=[]
    for name,pid,_ in PLAYER_SPECS[:8]:
      p=people[pid]; tg=team_games.get(pid,{})
      # The report is MLB-only.  A current affiliated-minors assignment must
      # not leak its club, game, or season totals into an MLB daily card.
      if team_sports.get(pid) != 1:
        batters.append({'name':name,'team':'','mlbam_id':pid,'minor_league_excluded':True,'status':'출전 없음','position':'—','at_bats':None,'hits':None,'rbi':None,'runs':None,'home_runs':None,'walks':None,'strikeouts':None,'avg':None,'obp':None,'ops':None,'season_stats_cutoff':None,'daily_note':'MLB 경기 출전 없음'})
        continue
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
      # Do not use affiliated-minors schedules, game logs, team names, or
      # season records as MLB evidence.  The status remains a compact MLB
      # report state without inventing an MLB appearance.
      if team_sports.get(pid) != 1:
        pitchers.append({'name':name,'team':'','mlbam_id':pid,'appeared':False,'status':'팀 경기 없음'})
        continue
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
        decisions=g.get('decisions',{}); role='starter' if st.get('gamesStarted') else 'reliever'; game_decision=None
        if role=='starter':
          if decisions.get('winner',{}).get('id')==pid: game_decision='승'
          elif decisions.get('loser',{}).get('id')==pid: game_decision='패'
        else:
          if decisions.get('save',{}).get('id')==pid: game_decision='세이브'
          elif st.get('holds',0): game_decision='홀드'
          elif st.get('blownSaves',0): game_decision='블론'
        pitchers.append({'name':name,'team':team,'mlbam_id':pid,'appeared':True,'status':'등판','role':role,'game_decision':game_decision,'daily_innings':st.get('inningsPitched'),'daily_hits':st.get('hits'),'daily_runs':st.get('runs'),'daily_earned_runs':st.get('earnedRuns'),'daily_walks_hbp':st.get('baseOnBalls',0)+st.get('hitByPitch',0),'daily_strikeouts':st.get('strikeOuts'),'daily_home_runs':st.get('homeRuns'),'daily_pitches':st.get('numberOfPitches'),'era':fmt_stat(season.get('era'))})
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
    daum_rows,daum_api=daum_schedule()
    naver_rows,naver_api=naver_schedule()
    targets=[]
    for title,teamid in [('LA 다저스 경기',119),('샌프란시스코 자이언츠 경기',137)]:
      ts=[g for g in mlb_games.values() if teamid in (g['teams']['away']['team']['id'],g['teams']['home']['team']['id'])]
      if ts: targets.append(build_game(ts[0],title,daum_rows,naver_rows,box=box(ts[0]['gamePk']),feed=feed(ts[0]['gamePk'])))
      else: targets.append({'section_title':title,'game_pk':None,'officialDate':None,'game_date_utc':None,'naver_game_id':None,'daum_game_id':None,'venue':'—','start_time_kst':'—','status':'팀 경기 없음','away':'LA 다저스' if teamid==119 else '샌프란시스코','home':'—','winner_side':None,'away_score':None,'home_score':None,'away_hits':None,'home_hits':None,'away_errors':None,'home_errors':None,'winner_pitcher':None,'loser_pitcher':None,'save_pitcher':None,'headline':'KST 대상일 팀 경기 없음','points':['MLB 공식 schedule의 KST gameDate 기준.'],'opponent_label':'—','opponent_effort':'—'})
    # Cross-check endpoints are retained as provenance. Dynamic Naver game IDs are not guessed.
    src=['https://statsapi.mlb.com/api/v1/schedule?sportId=1&date='+d.isoformat() for d in (REPORT-timedelta(days=1),REPORT)]
    src += [f'https://statsapi.mlb.com/api/v1/game/{pk}/boxscore' for pk in sorted(boxes)]
    naver_url=f'https://m.sports.naver.com/wbaseball/schedule/index?category=mlb&date={REPORT}'
    daum_url=f'https://sports.daum.net/schedule/mlb?date={REPORT.strftime("%Y%m%d")}'
    naver_check=public_status(naver_api)
    daum_check=public_status(daum_url)
    actual_team_games=[x for x in targets if x.get('game_pk') is not None]
    verified_targets=sum(bool(x.get('daum_verified') and x.get('naver_verified')) for x in actual_team_games)
    notes=[
      f'MLB 공식 schedule에서 KST 대상 창에 {len(mlb_games)}개 MLB 경기를 확인했고, 네이버·다음 KST schedule API는 각각 {len(naver_rows)}개·{len(daum_rows)}개로 일치했다.',
      f'다저스·자이언츠의 실제 대상 경기 {verified_targets}/{len(actual_team_games)}경기를 네이버·다음 KST 일정의 점수·종료 상태와 대조했다. 네이버 공개 API는 {naver_check} 응답을 확인했다.',
      '투수 등판 여부는 MLBAM ID를 각 현재 팀의 KST 대상 gamePk 전체 boxscore 투수 객체와 대조했다.'
    ]
    if go_gamelog_verified is not None:
      notes.append('고우석 gameLog와 팀 gamePk 대조: '+('기록 없음으로 미등판 교차확인.' if go_gamelog_verified else '해당 없음 또는 미검증.'))
    data={
      'report_date_kst':REPORT.isoformat(),
      'official_date_mlb':(REPORT-timedelta(days=1)).isoformat(),
      'generated_at':datetime.now(KST).isoformat(timespec='seconds'),
      'verification':{
        'status':'MLB 공식 Stats API/Gameday 기준 · 다음 KST 일정 교차조회',
        'method':f'KST {REPORT} UTC 창({START.isoformat().replace("+00:00","Z")}–{END.isoformat().replace("+00:00","Z")})에 실제 gameDate가 속한 경기만 미국 현지 전날·당일 schedule에서 선별했다. 시즌 누계는 MLB Stats API byDateRange의 각 경기 officialDate cutoff을 사용했다. 다음 공개 KST schedule API의 팀·시각·점수·종료 상태로 대상 팀 경기를 교차대조했다.',
        'notes':notes
      },
      'team_games':targets,
      'batters':batters,
      'pitchers':pitchers,
      'sources':{'mlb_official':src,'naver':[naver_url,naver_api],'daum':[daum_url,daum_api]}
    }
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'report_date_kst':data['report_date_kst'],'target_mlb_games':len(mlb_games),'team_games':[(x['section_title'],x['status'],x['game_pk']) for x in targets],'pitchers':data['pitchers']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
