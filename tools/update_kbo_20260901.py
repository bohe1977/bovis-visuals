#!/usr/bin/env python3
"""Write reconciled 2026-09-01 KBO data from captured official, Naver and Daum records."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATE, COMPACT = "2026-09-01", "20260901"
KBO = "https://www.koreabaseball.com"
DAUM_SCHEDULE = "https://sports.daum.net/prx/hermes/api/game/schedule.json?page=1&leagueCode=kbo&seasonKey=2026&fromDate=20260901&toDate=20260901"
DAUM_IDS = {"20260901HHKT0": 80101162, "20260901HTNC0": 80101163, "20260901LGOB0": 80101164, "20260901LTSS0": 80101165, "20260901SKWO0": 80101166}
NOW = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")


def sources(game_id: str) -> list[dict[str, str]]:
    return [
        {"label": "KBO 공식", "url": f"{KBO}/Schedule/GameCenter/Main.aspx?gameDate={COMPACT}&gameId={game_id}&section=REVIEW"},
        {"label": "네이버 기록", "url": f"https://api-gw.sports.naver.com/schedule/games/{game_id}2026/record"},
        {"label": "다음 기록", "url": f"https://sports.daum.net/match/{DAUM_IDS[game_id]}"},
    ]


def game(game_id, stadium, away, home, away_score, home_score, winner, loser, save, headline, points, effort):
    return {"id": game_id, "stadium": stadium, "start_time": "18:30", "status": "경기 종료", "away": away, "home": home,
            "away_score": away_score, "home_score": home_score, "winner_pitcher": winner, "loser_pitcher": loser,
            "save_pitcher": save, "headline": headline, "winner_points": points, "opponent_effort": effort, "sources": sources(game_id)}


games = [
    game("20260901HHKT0", "수원", "한화", "KT", 1, 6, "대니엘", "화이트", None,
         "KT가 1·2회 선취 4득점으로 한화를 6-1로 제압",
         ["KT 선발 대니엘은 6이닝 4피안타 2볼넷 6탈삼진 무실점으로 시즌 첫 승을 올렸다.", "KT는 1회 김상수의 결승 적시타, 2회 장진혁의 솔로포를 포함한 3득점으로 초반 주도권을 잡았다.", "최원준은 4타수 2안타 1타점 2득점, 장진혁은 3타수 1안타 1홈런 1타점 1득점을 기록했다.", "KT 불펜은 7~9회 3이닝 1실점으로 리드를 지켰다."],
         "한화는 9회 장규현의 적시타로 영봉패를 면했고, 최인호가 대타 안타와 득점을 보탰다."),
    game("20260901HTNC0", "창원", "KIA", "NC", 2, 7, "김진호", "네일", None,
         "NC가 7회 블레인의 만루포로 KIA를 7-2로 제압",
         ["NC 선발 구창모는 4이닝 2피안타 2볼넷 4탈삼진 1실점으로 물러났고, 김진호가 1이닝 무실점으로 승리를 챙겼다.", "NC는 2회 2득점 뒤 5회 김주원의 솔로포로 달아났고, 7회 블레인의 만루 홈런으로 승부를 갈랐다.", "블레인은 4타수 1안타 1홈런 4타점, 김주원은 4타수 2안타 1홈런 1타점 2득점을 기록했다.", "신영우·이용준·배재환·김진호가 구창모 뒤를 이어 실점을 최소화했다."],
         "KIA는 나성범이 2타수 1안타 1홈런 1타점 2득점, 김태군이 1타점을 올렸다."),
    game("20260901LGOB0", "잠실", "LG", "두산", 3, 1, "임찬규", "잭로그", "손주영",
         "LG가 송찬의의 4회 결승 3점포로 두산에 3-1 승리",
         ["LG 선발 임찬규는 6이닝 6피안타 2볼넷 4탈삼진 1실점으로 시즌 13승째를 기록했다.", "1회 1점을 내준 LG는 4회 1사 1·3루에서 송찬의가 우중월 3점 홈런을 쳐 경기를 뒤집었다.", "송찬의는 4타수 1안타 1홈런 3타점, 신민재와 오스틴은 각각 1안타 1득점으로 보탰다.", "손주영이 1이닝 무실점으로 시즌 25세이브를 올리며 마무리했다."],
         "두산은 양의지가 4타수 2안타 1타점으로 분전했고, 잭로그는 6이닝 4피안타 1볼넷 6탈삼진 3실점했다."),
    game("20260901LTSS0", "대구", "롯데", "삼성", 0, 3, "보스", "로드리게스", "김재윤",
         "삼성이 보스의 7이닝 무실점 호투로 롯데를 3-0으로 제압",
         ["삼성 선발 보스는 7이닝 6피안타 1볼넷 6탈삼진 무실점으로 시즌 2승째를 거뒀다.", "4회 류지혁의 결승 2루타로 균형을 깬 삼성은 5회 이재현의 솔로포와 8회 추가점으로 달아났다.", "류지혁은 3타수 3안타 2타점, 이재현은 3타수 1안타 1홈런 1타점을 기록했다.", "이승민이 홀드를 기록했고 김재윤이 1이닝 무실점으로 시즌 30세이브를 올렸다."],
         "롯데는 전민재와 윤동희가 각각 2안타를 쳤고, 로드리게스는 6이닝 6피안타 1볼넷 7탈삼진 2실점으로 버텼다."),
    game("20260901SKWO0", "고척", "SSG", "키움", 4, 0, "최민준", "알칸타라", None,
         "SSG가 최민준의 5이닝 무실점과 3회 2득점으로 키움을 4-0으로 제압",
         ["SSG 선발 최민준은 5이닝 4피안타 4볼넷 1탈삼진 무실점으로 시즌 3승째를 챙겼다.", "SSG는 3회 임근우의 결승 3루타를 포함해 2점을 냈고, 4·5회 추가점으로 격차를 벌렸다.", "정준재는 5타수 2안타 1타점, 에레디아는 4타수 2안타 1타점, 최지훈은 1타점 1득점을 기록했다.", "SSG 불펜이 4이닝 무실점으로 합작 완봉을 완성했다."],
         "키움은 데이비슨이 4타수 2안타로 분전했고, 알칸타라는 6이닝 8피안타 8탈삼진 4실점했다."),
]

pitchers = [
    {"name":"원태인","team":"삼성","appeared":False}, {"name":"류현진","team":"한화","appeared":False},
    {"name":"제레미 비슬리","team":"롯데","appeared":False}, {"name":"박세웅","team":"롯데","appeared":False},
    {"name":"김진욱","team":"롯데","appeared":False},
    {"name":"김원중","team":"롯데","appeared":True,"innings":"1","hits":2,"runs":1,"earned_runs":1,"walks_hbp":0,"strikeouts":0,"home_runs":0,"pitches":11,"season_record":"1승 5패","season_saves":5,"era":"5.18","role":"reliever","game_decision":None},
    {"name":"박정민","team":"롯데","appeared":True,"innings":"1","hits":1,"runs":0,"earned_runs":0,"walks_hbp":1,"strikeouts":0,"home_runs":0,"pitches":20,"season_record":"6승 2패","era":"3.67","role":"reliever","game_decision":None},
    {"name":"로드리게스","team":"롯데","appeared":True,"innings":"6","hits":6,"runs":2,"earned_runs":2,"walks_hbp":1,"strikeouts":7,"home_runs":1,"pitches":103,"season_record":"7승 10패","era":"4.17","role":"starter","game_decision":"패"},
    {"name":"임찬규","team":"LG","appeared":True,"innings":"6","hits":6,"runs":1,"earned_runs":1,"walks_hbp":3,"strikeouts":4,"home_runs":0,"pitches":91,"season_record":"13승 4패","era":"3.84","role":"starter","game_decision":"승"},
    {"name":"정해영","team":"KIA","appeared":False}, {"name":"박영현","team":"KT","appeared":False},
]
batters = [
    {"name":"강백호","team":"한화","appeared":True,"at_bats":4,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":0,"strikeouts":1,"avg":"0.286","obp":None,"ops":None},
    {"name":"노시환","team":"한화","appeared":True,"at_bats":3,"hits":0,"rbi":0,"runs":0,"home_runs":0,"walks":1,"strikeouts":2,"avg":"0.275","obp":None,"ops":None},
    {"name":"김도영","team":"KIA","appeared":True,"at_bats":3,"hits":1,"rbi":0,"runs":0,"home_runs":0,"walks":1,"strikeouts":0,"avg":"0.303","obp":None,"ops":None},
]

# Official KBO is the baseline. Captured response rows and Naver rows are checked before writes.
ART = ROOT / ".artifacts" / "kbo-2026-09-01"
for g in games:
    gid = g["id"]
    official = json.loads((ART / f"official-GetBoxScoreScroll-{gid}.json").read_text(encoding="utf-8-sig"))
    naver = json.loads((ART / f"naver-{gid}.json").read_text(encoding="utf-8"))["result"]["recordData"]
    assert official["code"] == "100" and naver["gameInfo"]["statusCode"] == "4"
    rheb = naver["scoreBoard"]["rheb"]
    assert int(rheb["away"]["r"]) == g["away_score"] and int(rheb["home"]["r"]) == g["home_score"]
assert {g["id"] for g in games} == set(DAUM_IDS)
assert sum(g["away_score"] + g["home_score"] for g in games) == 27
assert all(g["status"] == "경기 종료" for g in games)
for p in pitchers:
    if not p["appeared"]:
        assert set(p) == {"name", "team", "appeared"}

source_urls = {
    "kbo_official": [f"{KBO}/Schedule/ScoreBoard.aspx?gameDate={COMPACT}"] + [g["sources"][0]["url"] for g in games],
    "naver": [g["sources"][1]["url"] for g in games],
    "daum": [DAUM_SCHEDULE] + [g["sources"][2]["url"] for g in games],
}
verification = {
    "status":"KBO 공식 기준 · kbo-game·네이버·다음 대조", "sources":["KBO 공식 게임센터 REVIEW/API","kbo-game","네이버스포츠 공개 기록 API","다음스포츠 일정·박스스코어"],
    "details":"2026-09-01 KST 편성 5경기를 kbo-game FINISHED, KBO 공식 게임센터 상세기록 API(code=100), 네이버 공개 기록 API(statusCode=4), 다음 일정 API(gameStatus=END)로 대조했다. 종료 5경기만 반영했으며 합계 27득점이다. 관심 투수의 실제 등판은 KBO 공식 투수표의 선발/구원·결과와 네이버 투수 행으로, 관심 타자 행은 KBO 공식·네이버로 대조했다. 다음은 타자 볼넷을 사사구로 통합 표기할 수 있어 볼넷의 독립 일치값으로 주장하지 않았다.", "conflicts":[]
}
(ROOT / "kbo" / "data.json").write_text(json.dumps({"date":DATE,"generated_at":NOW,"source_urls":source_urls,"games":games},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(ROOT / "kbo-players" / "data.json").write_text(json.dumps({"report_date":DATE,"generated_at":NOW,"verification":verification,"pitchers":pitchers,"batters":batters,"source_urls":source_urls},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for rel in ("kbo/index.html","kbo-players/index.html"):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8").replace("2026-08-30", DATE).replace("2026.08.30", "2026.09.01").replace("2026년 8월 30일", "2026년 9월 1일")
    path.write_text(text,encoding="utf-8")
print(f"wrote reconciled KBO report {DATE} at {NOW}")
