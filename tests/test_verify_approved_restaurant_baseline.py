import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_approved_restaurant_baseline.py"


def test_all_generated_guides_match_approved_sadang_final_baseline():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=ROOT, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stderr
    guide_count = len(json.loads((ROOT / "data/restaurant-guides/manifest.json").read_text(encoding="utf-8"))["guides"])
    assert f"PASS: approved Sadang final baseline verified for {guide_count} generated guides" in result.stdout
