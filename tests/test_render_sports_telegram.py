import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "tools" / "render_sports_telegram.py"


def run_renderer(kind: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RENDERER), "--kind", kind, "--root", str(ROOT)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_kbo_renderer_outputs_verified_date_link_and_watchlist_line():
    result = run_renderer("kbo")

    assert result.returncode == 0, result.stderr
    assert "## ⚾ KBO 전날 경기, 2026-08-16" in result.stdout
    assert "SSG 6 : 0 LG" in result.stdout
    assert "박영현(KT), 세이브, 1 ⅓이닝, 0피안타, 0실점, 시즌 6승 0패 22세이브" in result.stdout
    assert "https://bohe1977.github.io/bovis-visuals/kbo/2026-08-16/" in result.stdout


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


def test_mlb_renderer_outputs_dated_team_report_and_archive_link():
    result = run_renderer("mlb")

    assert result.returncode == 0, result.stderr
    assert "## ⚾ MLB 오늘 경기 브리핑, 2026-08-16 KST" in result.stdout
    assert "**LA 다저스 경기**" in result.stdout
    assert "투수 기록: Jacob Misiorowski 승리, Justin Wrobleski 패전, Aaron Ashby 세이브" in result.stdout
    assert "https://bohe1977.github.io/bovis-visuals/mlb/2026-08-16/" in result.stdout
