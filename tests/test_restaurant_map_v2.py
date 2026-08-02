import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "restaurant-guides" / "manifest.json"
VERIFY = ROOT / "scripts" / "render_all_restaurant_guides.py"


def test_manifest_declares_unique_public_guides_and_existing_files():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["version"].startswith("2.")
    assert manifest["siteBase"] == "/bovis-visuals/"
    guides = manifest["guides"]
    assert len({guide["slug"] for guide in guides}) == len(guides)
    for guide in guides:
        assert (ROOT / guide["data"]).is_file()
        assert (ROOT / guide["output"]).is_file()
        if "archiveHref" in guide:
            assert f'href="{guide["archiveHref"]}"' in (ROOT / "index.html").read_text(encoding="utf-8")


def test_manifest_outputs_and_aliases_are_current():
    result = subprocess.run(
        [sys.executable, str(VERIFY), "--check"], cwd=ROOT, text=True, capture_output=True
    )
    assert result.returncode == 0, result.stderr
    expected = len(json.loads(MANIFEST.read_text(encoding="utf-8"))["guides"])
    assert f"verified {expected} restaurant guides" in result.stdout
