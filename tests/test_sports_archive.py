import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("archive_daily_sports", ROOT / "tools" / "archive_daily_sports.py")
archive_daily_sports = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(archive_daily_sports)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_kbo_archive_is_date_scoped_and_uses_its_own_player_data(tmp_path):
    write(tmp_path / "kbo" / "data.json", json.dumps({"date": "2026-08-02"}))
    write(tmp_path / "kbo" / "index.html", "fetch('./data.json'); fetch('../kbo-players/data.json')")
    write(tmp_path / "kbo-players" / "data.json", json.dumps({"report_date": "2026-08-02"}))
    write(tmp_path / "kbo-players" / "index.html", '<a href="../kbo/">통합</a> fetch(\'./data.json\')')

    archive_daily_sports.archive_kbo(tmp_path)

    archived = tmp_path / "kbo" / "2026-08-02"
    assert json.loads((archived / "data.json").read_text(encoding="utf-8"))["date"] == "2026-08-02"
    assert (archived / "kbo-players" / "data.json").exists()
    page = (archived / "index.html").read_text(encoding="utf-8")
    assert "./kbo-players/data.json" in page
    assert "../kbo-players/data.json" not in page
    player_page = (tmp_path / "kbo-players" / "2026-08-02" / "index.html").read_text(encoding="utf-8")
    assert '../../kbo/2026-08-02/' in player_page


def test_archive_refuses_to_overwrite_a_date_snapshot_with_different_bytes(tmp_path):
    write(tmp_path / "mlb" / "data.json", json.dumps({"report_date_kst": "2026-08-02"}))
    write(tmp_path / "mlb" / "index.html", "fetch('./data.json')")
    archive_daily_sports.archive_mlb(tmp_path)
    write(tmp_path / "mlb" / "data.json", json.dumps({"report_date_kst": "2026-08-02", "changed": True}))

    with pytest.raises(SystemExit, match="immutable archive conflict"):
        archive_daily_sports.archive_mlb(tmp_path)
