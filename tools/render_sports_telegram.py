#!/usr/bin/env python3
"""Render validated KBO or MLB JSON into a Telegram-ready Markdown report."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PUBLIC_ROOT = "https://bohe1977.github.io/bovis-visuals"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"invalid JSON object: {path}")
    return data


def require_archive(root: Path, kind: str, report_date: str) -> None:
    archive = root / kind / report_date
    if not (archive / "index.html").is_file() or not (archive / "data.json").is_file():
        fail(f"dated archive missing: {archive}")


def kbo_report(root: Path) -> str:
    games_data = read_json(root / "kbo" / "data.json")
    players_data = read_json(root / "kbo-players" / "data.json")
    report_date = games_data.get("date")
    if not isinstance(report_date, str) or players_data.get("report_date") != report_date:
        fail("KBO report date mismatch")
    require_archive(root, "kbo", report_date)
    archive_players = root / "kbo" / report_date / "players.json"
    nested_players = root / "kbo" / report_date / "kbo-players" / "data.json"
    if not archive_players.is_file() and not nested_players.is_file():
        fail(f"dated archive missing player payload: {report_date}")

    games = [game for game in games_data.get("games", []) if game.get("status") == "경기 종료"]
    if not games:
        fail("KBO has no final games")
    lines = [f"## ⚾ KBO 전날 경기, {report_date}", "", "**전체 결과**"]
    for game in games:
        lines.append(
            f"- {game['away']} {game['away_score']} : {game['home_score']} {game['home']}, {game['headline']}"
        )
    lines.extend(["", "**관심 투수**"])
    for pitcher in players_data.get("pitchers", []):
        name, team = pitcher.get("name"), pitcher.get("team")
        if pitcher.get("appeared"):
            decision = pitcher.get("game_decision") or "등판"
            saves = pitcher.get("season_saves")
            season = pitcher.get("season_record", "")
            season_text = f"시즌 {season}" + (f" {saves}세이브" if saves is not None else "")
            lines.append(
                f"- {name}({team}), {decision}, {pitcher.get('innings')}이닝, {pitcher.get('hits')}피안타, {pitcher.get('runs')}실점, {season_text}"
            )
        else:
            lines.append(f"- {name}({team}), 등판 없음")
    lines.extend(["", "**관심 타자**"])
    for batter in players_data.get("batters", []):
        if batter.get("appeared"):
            lines.append(
                f"- {batter['name']}({batter['team']}), {batter.get('at_bats')}타수 {batter.get('hits')}안타, {batter.get('rbi')}타점, {batter.get('runs')}득점"
            )
        else:
            lines.append(f"- {batter['name']}({batter['team']}), 출전 없음")
    lines.extend(["", f"[BOVIS KBO 통합 리포트]({PUBLIC_ROOT}/kbo/{report_date}/)"])
    return "\n".join(lines)


def require_mlb_final(data: dict) -> None:
    active = [game for game in data.get("team_games", []) if game.get("game_pk") is not None]
    nonfinal = [game for game in active if game.get("status") != "경기 종료"]
    if nonfinal:
        labels = ", ".join(f"{game.get('section_title', '경기')} ({game.get('status')})" for game in nonfinal)
        fail(f"MLB report not final: {labels}")


def mlb_report(root: Path, *, expected_date: str | None = None) -> str:
    data = read_json(root / "mlb" / "data.json")
    require_mlb_final(data)
    report_date = data.get("report_date_kst")
    if not isinstance(report_date, str):
        fail("MLB report date missing")
    if expected_date is not None and report_date != expected_date:
        fail(f"MLB report date mismatch: expected {expected_date}, found {report_date}")
    require_archive(root, "mlb", report_date)
    lines = [f"## ⚾ MLB 오늘 경기 브리핑, {report_date} KST", ""]
    for game in data.get("team_games", []):
        lines.extend([
            f"**{game.get('section_title')}**",
            f"- {game.get('away')} {game.get('away_score')} : {game.get('home_score')} {game.get('home')}, {game.get('headline')}",
            f"- 투수 기록: {game.get('pitcher_record')}",
        ])
        for point in game.get("game_points", [])[:3]:
            lines.append(f"- {point}")
        if game.get("opponent_effort"):
            lines.append(f"- {game.get('opponent_label')}의 분전: {game['opponent_effort']}")
        lines.append("")
    lines.append(f"[BOVIS MLB 통합 리포트]({PUBLIC_ROOT}/mlb/{report_date}/)")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("kbo", "mlb"), required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--expected-date", help="required MLB report date (YYYY-MM-DD)")
    parser.add_argument("--allow-stale", action="store_true", help="permit historical MLB rendering for tests/manual inspection")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.kind == "kbo":
        print(kbo_report(root))
        return
    expected_date = None if args.allow_stale else (args.expected_date or datetime.now(ZoneInfo("Asia/Seoul")).date().isoformat())
    print(mlb_report(root, expected_date=expected_date))


if __name__ == "__main__":
    main()
