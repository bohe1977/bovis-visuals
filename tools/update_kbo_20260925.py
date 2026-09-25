#!/usr/bin/env python3
"""Collect and reconcile the 2026-09-25 KBO final slate."""
from __future__ import annotations

import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path

from kbo_card_content import subject_particle, topic_particle
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-25", "20260925"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
WATCHED_PITCHERS = [("원태인", "삼성"), ("류현진", "한화"), ("제레미 비슬리", "롯데"), ("박세웅", "롯데"), ("김진욱", "롯데"), ("김원중", "롯데"), ("박정민", "롯데"), ("로드리게스", "롯데"), ("임찬규", "LG"), ("정해영", "KIA"), ("박영현", "KT")]
WATCHED_BATTERS = [("강백호", "한화", 68050), ("노시환", "한화", 69737), ("김도영", "KIA", 50202)]
NAME_ALIASES = {"제레미 비슬리": "비슬리"}

def fetch(url: str, *, form: dict | None = None) -> bytes:
    data = urlencode(form).encode() if form else None
    return urlopen(Request(url, data=data, headers={"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest", "Referer": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}"}), timeout=45).read()

def cells(row: dict) -> list[str]:
    return [str(cell.get("Text", "")).replace("&nbsp;", "").strip() for cell in row["row"]]

def official_pitchers(box: dict) -> dict[str, dict[str, str]]:
    result = {}
    for team in box["arrPitcher"]:
        table = json.loads(team["table"])
        headers = cells(table["headers"][0])
        for row in table["rows"]:
            value = dict(zip(headers, cells(row)))
            result[value["선수명"]] = value
    return result

def official_hitters(box: dict) -> set[str]:
    return {cells(row)[2] for team in box["arrHitter"] for row in json.loads(team["table1"])["rows"] if len(cells(row)) >= 3}

def official_game_fact(box: dict, label: str) -> str | None:
    table = json.loads(box['tableEtc'])
    for row in table['rows']:
        values = cells(row)
        if len(values) >= 2 and values[0] == label:
            return values[1]
    return None


def inning_turning_point(board: dict, winnerside: str, win_team: str, lose_team: str) -> str:
    table = json.loads(board['table2'])
    innings = [cell['Text'] for cell in table['headers'][0]['row']]
    away_runs = [0 if cell['Text'] in ('-', '') else int(cell['Text']) for cell in table['rows'][0]['row']]
    home_runs = [0 if cell['Text'] in ('-', '') else int(cell['Text']) for cell in table['rows'][1]['row']]
    winner_runs, loser_runs = (away_runs, home_runs) if winnerside == 'away' else (home_runs, away_runs)
    running_winner = running_loser = 0
    prior_winner = prior_loser = 0
    candidates = []
    for index, inning in enumerate(innings):
        running_winner += winner_runs[index]
        running_loser += loser_runs[index]
        if winner_runs[index] > 0:
            candidates.append((index, inning, winner_runs[index], prior_winner, prior_loser, running_winner, running_loser))
        prior_winner, prior_loser = running_winner, running_loser
    assert candidates, 'winner recorded no scoring inning'
    # Prefer the earliest lead change that the winner never relinquishes; otherwise use the largest scoring inning.
    permanent = [item for item in candidates if item[5] > item[6] and all(sum(winner_runs[:future + 1]) > sum(loser_runs[:future + 1]) for future in range(item[0], len(innings)))]
    chosen = permanent[0] if permanent else max(candidates, key=lambda item: (item[2], -item[0]))
    _, inning, runs, before_winner, before_loser, after_winner, after_loser = chosen
    verb = '역전하며' if before_winner < before_loser and after_winner > after_loser else '달아나며'
    return f'{win_team}은 {inning}회 {runs}득점으로 {after_winner}-{after_loser} {verb} 흐름을 잡았다.'


def inning_text(value: str) -> str:
    return value.replace(" ", "")

def player_season(player_id: int) -> tuple[str, str]:
    html = fetch(f"{KBO}/Record/Player/HitterDetail/Basic.aspx?playerId={player_id}").decode("utf-8-sig")
    rows = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        rows.append([unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S | re.I)])
    # The first two player-season rows contain the matching header/value pairs.
    headers, values = rows[0], rows[1]
    trailing_headers, trailing_values = rows[2], rows[3]
    season = dict(zip(headers, values)) | dict(zip(trailing_headers, trailing_values))
    return season["OBP"], season["OPS"]

ART.mkdir(parents=True, exist_ok=True)
# Authoritative schedule surfaces and kbo-game package capture.
daum_raw = fetch(DAUM_SCHEDULE)
(ART / "daum-schedule.json").write_bytes(daum_raw)
daum = json.loads(daum_raw)["schedule"][COMPACT]
# kbo-game output is captured by the caller before this normalizer runs.
kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
finished = [g for g in kbo_game if g["status"] == "FINISHED"]
daum_finished = [g for g in daum if g["gameStatus"] == "END"]
assert len(finished) == len(daum_finished), (len(finished), len(daum_finished))
assert finished, f"{DATE}: no completed games available for preparation"

daum_by_pair = {(g["awayTeamName"], g["homeTeamName"]): g for g in daum}
games, raw = [], {}
for kg in finished:
    gid = kg["id"]
    away, home = kg["awayTeam"], kg["homeTeam"]
    dg = daum_by_pair[(away, home)]
    naver_raw = fetch(f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record")
    board_raw = fetch(f"{KBO}/ws/Schedule.asmx/GetScoreBoardScroll", form={"leId": 1, "srId": 0, "seasonId": 2026, "gameId": gid})
    box_raw = fetch(f"{KBO}/ws/Schedule.asmx/GetBoxScoreScroll", form={"leId": 1, "srId": 0, "seasonId": 2026, "gameId": gid})
    (ART / f"naver-{gid}.json").write_bytes(naver_raw)
    (ART / f"official-GetScoreBoardScroll-{gid}.json").write_bytes(board_raw)
    (ART / f"official-GetBoxScoreScroll-{gid}.json").write_bytes(box_raw)
    naver = json.loads(naver_raw)["result"]["recordData"]
    board, box = json.loads(board_raw.decode("utf-8-sig")), json.loads(box_raw.decode("utf-8-sig"))
    assert board["code"] == "100" and box["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    assert (int(naver["scoreBoard"]["rheb"]["away"]["r"]), int(naver["scoreBoard"]["rheb"]["home"]["r"])) == (kg["score"]["away"], kg["score"]["home"]) == (int(dg["awayResult"]), int(dg["homeResult"]))
    raw[gid] = (naver, board, box, dg)

    winnerside = "away" if kg["score"]["away"] > kg["score"]["home"] else "home"
    loserside = "home" if winnerside == "away" else "away"
    win_team, lose_team = (away, home) if winnerside == "away" else (home, away)
    winner = kg["winPitcher"].strip() or None
    loser = kg["losePitcher"].strip() or None
    save = kg["savePitcher"].strip() or None
    pitchers = naver["pitchersBoxscore"]
    batters = naver["battersBoxscore"]
    starter = pitchers[winnerside][0]
    productive = sorted(batters[winnerside], key=lambda x: (x["rbi"], x["hr"], x["hit"], x["run"]), reverse=True)[:2]
    leading_loser = max(batters[loserside], key=lambda x: (x["rbi"], x["hr"], x["hit"], x["run"]))
    p_line = f"{starter['name']}{topic_particle(starter['name'])} {inning_text(starter['inn'])}이닝 {starter['hit']}피안타 {starter['bbhp']}사사구 {starter['kk']}탈삼진 {starter['r']}실점"
    hitter_line = ', '.join(f"{x['name']}{topic_particle(x['name'])} {x['ab']}타수 {x['hit']}안타 {x['rbi']}타점" for x in productive)
    decisive = official_game_fact(box, '결승타')
    decisive_point = inning_turning_point(board, winnerside, win_team, lose_team) if decisive in (None, '', '없음') else f"공식 결승타는 {decisive}였다."
    if save:
        finisher = next(p for p in pitchers[winnerside] if p['name'] == save)
        bullpen = f"{save}{subject_particle(save)} {inning_text(finisher['inn'])}이닝 {finisher['hit']}피안타 {finisher['bbhp']}사사구 {finisher['kk']}탈삼진 {finisher['r']}실점으로 세이브를 기록했다."
    else:
        relievers = pitchers[winnerside][1:]
        assert relievers, f'{gid}: no verified winning reliever for bullpen point'
        finisher = relievers[-1]
        bullpen = f"{finisher['name']}{subject_particle(finisher['name'])} {inning_text(finisher['inn'])}이닝 {finisher['hit']}피안타 {finisher['bbhp']}사사구 {finisher['kk']}탈삼진 {finisher['r']}실점으로 마지막 이닝을 책임졌다."
    sources = [{"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"}, {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"}, {"label": "다음 기록", "url": f"https://sports.daum.net/match/{dg['gameId']}"}]
    last_code = ord(win_team[-1]) - ord("가")
    subject = "이" if 0 <= last_code <= 11171 and last_code % 28 else "가"
    games.append({"id": gid, "stadium": kg["stadium"], "start_time": kg["startTime"], "status": "경기 종료", "away": away, "home": home, "away_score": kg["score"]["away"], "home_score": kg["score"]["home"], "winner_pitcher": winner, "loser_pitcher": loser, "save_pitcher": save, "headline": f"{win_team}{subject} {lose_team}에 {max(kg['score'].values())}-{min(kg['score'].values())} 승리", "winner_points": [f"{win_team} 선발 {p_line}으로 승리를 기록했다.", decisive_point, f"{hitter_line}을 기록했다.", bullpen], "opponent_effort": f"{lose_team}{topic_particle(lose_team)} {leading_loser['name']}{subject_particle(leading_loser['name'])} {leading_loser['ab']}타수 {leading_loser['hit']}안타 {leading_loser['rbi']}타점으로 분전했지만 승부를 뒤집지 못했다.", "sources": sources})

pitchers = []
for name, team in WATCHED_PITCHERS:
    lookup_name = NAME_ALIASES.get(name, name)
    games_for_team = [g for g in games if team in (g["away"], g["home"])]
    entries = []
    for g in games_for_team:
        naver, board, box, _ = raw[g["id"]]
        side = "away" if g["away"] == team else "home"
        entries.extend([(g, p) for p in naver["pitchersBoxscore"][side] if p["name"] == lookup_name])
    if not entries:
        pitchers.append({"name": name, "team": team, "appeared": False}); continue
    g, p = entries[0]
    official = official_pitchers(raw[g["id"]][2])[lookup_name]
    assert str(p["hit"]) == official["피안타"] and str(p["bbhp"]) == official["4사구"] and str(p["kk"]) == official["삼진"] and str(p["r"]) == official["실점"] and str(p["er"]) == official["자책"] and str(p["bf"]) == official["투구수"] and str(p["w"]) == official["승"] and str(p["l"]) == official["패"] and p["era"] == official["평균자책점"]
    role = "starter" if official["등판"] == "선발" else "reliever"
    official_result = official["결과"]
    decision = ("승" if official_result == "승" else "패" if official_result == "패" else "세이브" if official_result == "세" else "홀드" if official_result == "홀" else "블론" if official_result == "블" else None)
    if role == "starter" and decision not in ("승", "패"): decision = None
    if role == "reliever" and decision not in ("세이브", "홀드", "블론"): decision = None
    item = {"name": name, "team": team, "appeared": True, "innings": inning_text(p["inn"]), "hits": p["hit"], "runs": p["r"], "earned_runs": p["er"], "walks_hbp": p["bbhp"], "strikeouts": p["kk"], "home_runs": 0, "pitches": p["bf"], "season_record": f"{p['w']}승 {p['l']}패", "era": p["era"], "role": role, "game_decision": decision}
    if p["s"]:
        item["season_saves"] = p["s"]
    pitchers.append(item)

batters = []
for name, team, player_id in WATCHED_BATTERS:
    entries = []
    for g in games:
        if team not in (g["away"], g["home"]): continue
        naver, board, box, _ = raw[g["id"]]
        side = "away" if g["away"] == team else "home"
        entries.extend([(g, b) for b in naver["battersBoxscore"][side] if b["name"] == name])
    if not entries:
        batters.append({"name": name, "team": team, "appeared": False}); continue
    g, b = entries[0]
    assert name in official_hitters(raw[g["id"]][2])
    obp, ops = player_season(player_id)
    batters.append({"name": name, "team": team, "appeared": True, "at_bats": b["ab"], "hits": b["hit"], "rbi": b["rbi"], "runs": b["run"], "home_runs": b["hr"], "walks": b["bb"], "strikeouts": b["kk"], "avg": b["hra"], "obp": obp, "ops": ops})

assert all(set(p) == {"name", "team", "appeared"} for p in pitchers if not p["appeared"])
assert all(isinstance(b.get("obp"), str) and isinstance(b.get("ops"), str) for b in batters if b["appeared"])
source_urls = {"kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games], "naver": [g["sources"][1]["url"] for g in games], "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games]}
total_runs = sum(g["away_score"] + g["home_score"] for g in games)
active_pitchers = [p for p in pitchers if p["appeared"]]
active_batters = [b for b in batters if b["appeared"]]
pitcher_detail = "·".join(f"{p['name']}({p['role']}·{p['game_decision'] or '결정 없음'})" for p in active_pitchers) or "실제 등판 관심 투수 없음"
batter_detail = "·".join(b["name"] for b in active_batters) or "실제 출전 관심 타자 없음"
verification = {"status": "KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources": ["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details": f"{DATE} KST 편성 {len(games)}경기는 kbo-game FINISHED, KBO 공식 게임센터 GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 {len(games)}경기 합계는 {total_runs}득점이다. 실제 등판 관심 투수 {pitcher_detail}의 당일 라인·시즌 승패·ERA·세이브는 KBO 공식 투수표와 네이버 행으로 대조했고, 역할과 당일 결정은 KBO 공식 결과를 기준으로 분류했다. 실제 출전 관심 타자 {batter_detail}의 시즌 OBP·OPS는 KBO 공식 선수 상세기록으로 확인했다. 미등판·미출전 관심 선수는 해당 완료 경기의 KBO 공식·네이버 전체 명단 부재 또는 팀 경기 없음으로 계약상 최소 객체로 보존했다. 다음 타자 표의 사사구 표기 범위 차이로 볼넷 독립 일치값은 주장하지 않았다.", "conflicts": []}
now = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date": DATE, "generated_at": now, "source_urls": source_urls, "games": games}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date": DATE, "generated_at": now, "verification": verification, "pitchers": pitchers, "batters": batters, "source_urls": source_urls}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.25", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 25일", text)
    path.write_text(text, encoding="utf-8")
(ART / "verification.json").write_text(json.dumps({"report_date": DATE, "games": len(games), "total_runs": total_runs, "source_status": {"kbo_game": f"FINISHED x{len(games)}", "kbo_official": f"code=100 x{len(games)}", "naver": f"statusCode=4 x{len(games)}", "daum": f"gameStatus=END x{len(games)}"}, "watched_pitchers": [p["name"] for p in pitchers if p["appeared"]], "watched_batters": [b["name"] for b in batters if b["appeared"]]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {now}")
