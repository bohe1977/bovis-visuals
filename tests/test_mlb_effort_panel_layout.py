from pathlib import Path


PAGE = (Path(__file__).resolve().parents[1] / "mlb" / "index.html").read_text(
    encoding="utf-8"
)


def test_desktop_losing_team_effort_panels_share_one_height():
    """The two desktop game cards must not leave unequal losing-team panels."""
    assert "syncEffortPanelHeights" in PAGE
    assert "window.matchMedia('(min-width: 801px)').matches" in PAGE
    assert "panel.style.height = `${height}px`" in PAGE
