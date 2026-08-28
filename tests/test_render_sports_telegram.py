import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "tools" / "render_sports_telegram.py"


def run_renderer(kind: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RENDERER), "--kind", kind, "--root", str(ROOT), "--allow-stale"],
        text=True,
        capture_output=True,
        check=False,
    )


def test_kbo_renderer_outputs_current_verified_date_link_and_watchlist_lines():
    result = run_renderer("kbo")
    games = json.loads((ROOT / "kbo" / "data.json").read_text(encoding="utf-8"))
    players = json.loads((ROOT / "kbo-players" / "data.json").read_text(encoding="utf-8"))
    report_date = games["date"]

    assert players["report_date"] == report_date
    final_games = [game for game in games["games"] if game.get("status") == "경기 종료"]
    if not final_games:
        # Delivery suppresses a wholly cancelled slate rather than fabricating a score briefing.
        assert result.returncode != 0
        assert result.stderr == "KBO has no final games\n"
        return

    assert result.returncode == 0, result.stderr
    assert f"## ⚾ KBO 전날 경기, {report_date}" in result.stdout
    for game in final_games:
        assert f"{game['away']} {game['away_score']} : {game['home_score']} {game['home']}" in result.stdout
    for pitcher in players["pitchers"]:
        assert f"- {pitcher['name']}({pitcher['team']})" in result.stdout
    assert f"https://bohe1977.github.io/bovis-visuals/kbo/{report_date}/" in result.stdout


def test_kbo_renderer_refuses_missing_dated_archive(tmp_path: Path):
    (tmp_path / "kbo").mkdir()
    (tmp_path / "kbo-players").mkdir()
    (tmp_path / "kbo" / "data.json").write_text(json.dumps({"date": "2026-08-16", "games": []}), encoding="utf-8")
    (tmp_path / "kbo-players" / "data.json").write_text(json.dumps({"report_date": "2026-08-16", "pitchers": [], "batters": []}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(RENDERER), "--kind", "kbo", "--root", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "dated archive missing" in result.stderr


def test_mlb_renderer_outputs_current_dated_team_report_and_archive_link():
    result = run_renderer("mlb")
    data = json.loads((ROOT / "mlb" / "data.json").read_text(encoding="utf-8"))
    report_date = data["report_date_kst"]
    dodgers = next(game for game in data["team_games"] if game["section_title"] == "LA 다저스 경기")

    assert result.returncode == 0, result.stderr
    assert f"## ⚾ MLB 오늘 경기 브리핑, {report_date} KST" in result.stdout
    assert "**LA 다저스 경기**" in result.stdout
    assert f"투수 기록: {dodgers['pitcher_record']}" in result.stdout
    assert f"https://bohe1977.github.io/bovis-visuals/mlb/{report_date}/" in result.stdout


def test_mlb_renderer_refuses_nonfinal_report_even_when_archive_exists(tmp_path: Path):
    report_date = "2026-08-19"
    report_dir = tmp_path / "mlb" / report_date
    report_dir.mkdir(parents=True)
    (report_dir / "index.html").write_text("ok", encoding="utf-8")
    (report_dir / "data.json").write_text("{}", encoding="utf-8")
    (tmp_path / "mlb" / "data.json").write_text(
        json.dumps({"report_date_kst": report_date, "team_games": [{"game_pk": 1, "section_title": "LA 다저스 경기", "status": "경기 진행 중"}]}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(RENDERER), "--kind", "mlb", "--root", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "not final" in result.stderr


def test_mlb_renderer_refuses_stale_report_for_expected_delivery_date(tmp_path: Path):
    report_date = "2026-08-19"
    report_dir = tmp_path / "mlb" / report_date
    report_dir.mkdir(parents=True)
    (report_dir / "index.html").write_text("ok", encoding="utf-8")
    (report_dir / "data.json").write_text("{}", encoding="utf-8")
    (tmp_path / "mlb" / "data.json").write_text(
        json.dumps({"report_date_kst": report_date, "team_games": [{"game_pk": 1, "section_title": "LA 다저스 경기", "status": "경기 종료"}]}),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(RENDERER), "--kind", "mlb", "--root", str(tmp_path), "--expected-date", "2026-08-20"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode != 0
    assert "date mismatch" in result.stderr
