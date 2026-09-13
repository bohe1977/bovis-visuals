#!/usr/bin/env python3
"""Build the reconciled 2026-09-13 KBO final-game report from captured source records."""
from __future__ import annotations
import json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-13", "20260913"
ART = ROOT / ".artifacts" / f"kbo-{DATE}"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = f"https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate={COMPACT}&toDate={COMPACT}"
DAUM_IDS = {"20260913HHHT0": 80108764, "20260913LGSS0": 80108765, "20260913LTKT0": 80108766, "20260913NCOB0": 80108767}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")

def sources(gid):
    return [
        {"label":"KBO 공식", "url":f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={gid}&section=REVIEW"},
        {"label":"네이버 기록", "url":f"https://api-gw.sports.naver.com/schedule/games/{gid}2026/record"},
        {"label":"다음 기록", "url":f"https://sports.daum.net/match/{DAUM_IDS[gid]}"},
    ]

def game(gid, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id":gid,"stadium":stadium,"start_time":"17:00","status":"경기 종료","away":away,"home":home,"away_score":away_score,"home_score":home_score,"winner_pitcher":winner,"loser_pitcher":loser,"save_pitcher":save,"headline":headline,"winner_points":points,"opponent_effort":effort,"sources":sources(gid)}

games = [
    game("20260913NCOB0", "잠실", "NC", "두산", 2, 9, "최민석", "토다", None, "두산이 김민석·세베리노의 홈런포를 앞세워 NC에 9-2 승리", [
        "두산 선발 최민석은 5이닝 8피안타 2실점 4탈삼진으로 승리를 기록했다.",
        "2회 1사 만루에서 안재석의 우익수 희생플라이가 공식 결승타가 됐다.",
        "김민석은 1타수 1안타 1홈런 2타점 3볼넷, 양의지는 3타수 2안타 1홈런 1타점을 기록했다.",
        "박치국·타카다가 각각 1이닝 무실점으로 리드를 지켰다."],
        "NC는 김휘집·박건우·천재환이 나란히 2안타를 기록했지만, 선발 토다가 2⅔이닝 7실점으로 흔들린 초반 격차를 좁히지 못했다."),
    game("20260913LGSS0", "대구", "LG", "삼성", 13, 5, "임찬규", "최원태", None, "LG가 홈런 3방을 포함한 17안타로 삼성에 13-5 승리", [
        "LG 선발 임찬규는 7이닝 7피안타 4실점 6탈삼진으로 시즌 14승째를 올렸다.",
        "4회 1사 만루에서 신민재의 중전 적시타가 공식 결승타가 됐다.",
        "오지환은 3타수 2안타 2홈런 3타점, 오스틴은 5타수 2안타 1홈런 3타점으로 공격을 이끌었다.",
        "김진수는 1이닝 무실점, 김강률은 1이닝 1실점으로 뒤를 이었다."],
        "삼성은 박승규가 5타수 2안타 2홈런 3타점으로 분전했지만 선발 최원태가 3⅓이닝 4실점으로 패전을 기록했다."),
    game("20260913HHHT0", "광주", "한화", "KIA", 2, 9, "시라카와", "화이트", None, "KIA가 카스트로의 결승 홈런과 김도영의 3안타로 한화에 9-2 승리", [
        "KIA 선발 시라카와는 5이닝 4피안타 2실점 8탈삼진으로 승리를 기록했다.",
        "4회 무사에서 카스트로의 우중월 솔로 홈런이 공식 결승타가 됐다.",
        "김도영은 4타수 3안타 3타점 1득점 1볼넷, 박재현은 5타수 3안타 2타점을 기록했다.",
        "곽도규와 전상현이 각각 1이닝 무실점 홀드로 승리를 뒷받침했다."],
        "한화는 강백호가 4회 2점 홈런 포함 4타수 1안타 2타점, 노시환이 4타수 2안타로 맞섰지만 화이트의 5이닝 4실점을 만회하지 못했다."),
    game("20260913LTKT0", "수원", "롯데", "KT", 2, 5, "소형준", "나균안", "박영현", "KT가 안현민의 결승타와 소형준의 호투로 롯데에 5-2 승리", [
        "KT 선발 소형준은 6이닝 7피안타 2실점 7탈삼진으로 승리를 기록했다.",
        "1회 1사 2루에서 안현민의 좌전 적시타가 공식 결승타가 됐다.",
        "안현민은 4타수 2안타 2타점, 힐리어드는 5회 2점 홈런으로 4타수 1안타 2타점을 기록했다.",
        "스기모토가 1⅓이닝 무실점 홀드, 박영현이 1이닝 무실점 세이브로 마무리했다."],
        "롯데는 레이예스가 5타수 3안타 1타점, 고승민과 나승엽이 각각 2안타로 분전했지만 나균안의 5이닝 5실점 패전을 뒤집지 못했다."),
]

pitchers = [
    {"name":"원태인","team":"삼성","appeared":False}, {"name":"류현진","team":"한화","appeared":False}, {"name":"제레미 비슬리","team":"롯데","appeared":False}, {"name":"박세웅","team":"롯데","appeared":False}, {"name":"김진욱","team":"롯데","appeared":False}, {"name":"김원중","team":"롯데","appeared":False}, {"name":"박정민","team":"롯데","appeared":False}, {"name":"로드리게스","team":"롯데","appeared":False},
    {"name":"임찬규","team":"LG","appeared":True,"innings":"7","hits":7,"runs":4,"earned_runs":4,"walks_hbp":0,"strikeouts":6,"home_runs":2,"pitches":97,"season_record":"14승 5패","era":"4.19","role":"starter","game_decision":"승"},
    {"name":"정해영","team":"KIA","appeared":False},
    {"name":"박영현","team":"KT","appeared":True,"innings":"1","hits":1,"runs":0,"earned_runs":0,"walks_hbp":0,"strikeouts":1,"home_runs":0,"pitches":10,"season_record":"6승 0패","season_saves":27,"era":"2.54","role":"reliever","game_decision":"세이브"},
]
batters = [
    {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":1,"rbi":2,"runs":1,"home_runs":1,"walks":0,"strikeouts":2,"avg":"0.287","obp":None,"ops":None},
    {"name":"노시환","team":"한화","appeared":True,"at_bats":4,"hits":2,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":1,"avg":"0.281","obp":None,"ops":None},
    {"name":"김도영","team":"KIA","appeared":True,"at_bats":4,"hits":3,"rbi":3,"runs":1,"home_runs":0,"walks":1,"strikeouts":1,"avg":"0.310","obp":None,"ops":None},
]

kbo_game = json.loads((ART / "kbo-game.json").read_text(encoding="utf-8"))
daum = json.loads((ART / "daum-schedule.json").read_text(encoding="utf-8"))["schedule"][COMPACT]
assert {g["id"] for g in games} == {g["id"] for g in kbo_game if g["status"] == "FINISHED"} == set(DAUM_IDS)
assert {g["gameId"] for g in daum if g["gameStatus"] == "END"} == set(DAUM_IDS.values())
assert sum(g["away_score"] + g["home_score"] for g in games) == 47

def official_rows(game_id, category):
    document = json.loads((ART / f"official-GetBoxScoreScroll-{game_id}.json").read_text(encoding="utf-8-sig"))
    assert document["code"] == "100"
    result = []
    for team in document[category]:
        table = json.loads(team["table"])
        headers = [cell["Text"] for cell in table["headers"][0]["row"]]
        result.extend(dict(zip(headers, [cell["Text"] for cell in row["row"]])) for row in table["rows"])
    return result

watched_pitchers = {p["name"] for p in pitchers}
for g in games:
    gid = g["id"]
    board = json.loads((ART / f"official-GetScoreBoardScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert board["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
    assert board["AWAY_NM"] == g["away"] and board["HOME_NM"] == g["home"]
    all_official = official_rows(gid, "arrPitcher")
    all_naver = [x for side in ("away", "home") for x in naver["pitchersBoxscore"][side]]
    for p in pitchers:
        if p["team"] in (g["away"], g["home"]) and not p["appeared"]:
            assert p["name"] not in {x["선수명"] for x in all_official}
            assert p["name"] not in {x["name"] for x in all_naver}
for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}
lg_official = {x["선수명"]:x for x in official_rows("20260913LGSS0", "arrPitcher")}
kt_official = {x["선수명"]:x for x in official_rows("20260913LTKT0", "arrPitcher")}
assert (lg_official["임찬규"]["등판"], lg_official["임찬규"]["결과"], lg_official["임찬규"]["이닝"], lg_official["임찬규"]["평균자책점"]) == ("선발", "승", "7", "4.19")
assert (kt_official["박영현"]["결과"], kt_official["박영현"]["세"], kt_official["박영현"]["이닝"], kt_official["박영현"]["평균자책점"]) == ("세", "27", "1", "2.54")
hh_naver = json.loads((ART / "naver-20260913HHHT0.json").read_text(encoding="utf-8"))["result"]["recordData"]
hitters = {x["name"]:x for side in ("away", "home") for x in hh_naver["battersBoxscore"][side]}
assert (hitters["강백호"]["ab"], hitters["강백호"]["hit"], hitters["강백호"]["rbi"], hitters["강백호"]["hr"], hitters["강백호"]["hra"]) == (4,1,2,1,"0.287")
assert (hitters["노시환"]["ab"], hitters["노시환"]["hit"], hitters["노시환"]["kk"], hitters["노시환"]["hra"]) == (4,2,1,"0.281")
assert (hitters["김도영"]["ab"], hitters["김도영"]["hit"], hitters["김도영"]["rbi"], hitters["김도영"]["bb"], hitters["김도영"]["hra"]) == (4,3,3,1,"0.310")

source_urls = {"kbo_official":[f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"]+[g["sources"][0]["url"] for g in games], "naver":[g["sources"][1]["url"] for g in games], "daum":[DAUM_SCHEDULE]+[g["sources"][2]["url"] for g in games]}
verification = {"status":"KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources":["KBO 공식 게임센터 REVIEW/API", "kbo-game", "네이버스포츠 공개 기록 API", "다음스포츠 일정·박스스코어"], "details":"2026-09-13 KST 편성 4경기는 kbo-game FINISHED, KBO 공식 게임센터 REVIEW GetScoreBoardScroll·GetBoxScoreScroll(code=100), 네이버 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 종료 상태와 스코어를 대조했다. 종료 4경기 합계는 47득점이다. 임찬규와 박영현의 실제 등판 라인·시즌 성적·ERA는 KBO 공식 투수표와 네이버 투수 행으로 대조했고, 임찬규의 선발·승리 및 박영현의 구원·세이브는 KBO 공식 결과와 네이버 wls를 확인했다. 박영현의 시즌 27세이브는 공식·네이버 기록으로 확인했다. 나머지 관심 투수는 해당 팀 완료 경기의 KBO 공식·네이버 전체 투수 명단에 없어 계약상 name·team·appeared만 보존했다. 강백호·노시환·김도영의 당일 타격 라인과 시즌 타율은 KBO 공식·네이버 기록으로 대조했다. 다음 타자 표는 사사구를 통합 표기할 수 있어 볼넷 독립 일치값으로 주장하지 않았다.", "conflicts":[]}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
for rel in ("kbo/index.html", "kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"2026-09-\d{2}", DATE, text)
    text = re.sub(r"2026\.09\.\d{2}", "2026.09.13", text)
    text = re.sub(r"2026년 9월 \d{1,2}일", "2026년 9월 13일", text)
    path.write_text(text, encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
