import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "mlb" / "2026-08-26"
PITCHER_METRICS = (
    "${metric(p.daily_innings,'이닝')}"
    "${metric(p.daily_hits,'피안타')}"
    "${metric(p.daily_runs,'실점')}"
    "${metric(p.daily_earned_runs,'자책')}"
    "${metric(p.daily_walks_hbp,'4사구')}"
    "${metric(p.daily_strikeouts,'삼진')}"
    "${metric(p.daily_home_runs,'피홈런')}"
    "${metric(p.daily_pitches,'투구수')}"
    "${metric(p.era,'시즌 ERA')}"
    "${metric(p.season_record,'시즌 성적')}"
)


def test_active_pitcher_card_has_tenth_season_record_cell_in_current_and_archive():
    data = json.loads((ARCHIVE / "data.json").read_text(encoding="utf-8"))
    skenes = next(p for p in data["pitchers"] if p["name"] == "폴 스킨스")

    assert skenes["appeared"] is True
    assert skenes["season_record"] == "9승 11패"
    for page in (ROOT / "mlb" / "index.html", ARCHIVE / "index.html"):
        content = page.read_text(encoding="utf-8")
        assert PITCHER_METRICS in content
        assert content.count("${metric(p.season_record,'시즌 성적')}") == 1
