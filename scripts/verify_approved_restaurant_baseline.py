#!/usr/bin/env python3
"""Fail closed when a generated restaurant guide drifts from its approved final baseline."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = json.loads((ROOT / "standards" / "approved-sadang-final-baseline.json").read_text(encoding="utf-8"))
TEMPLATE = ROOT / "templates" / "restaurant-map-v1.html"
MANIFEST = ROOT / "data" / "restaurant-guides" / "manifest.json"


def check_text(label: str, text: str, required: list[str], forbidden: list[str]) -> list[str]:
    problems = [f"{label}: missing required baseline marker: {marker}" for marker in required if marker not in text]
    problems += [f"{label}: contains forbidden intermediate marker: {marker}" for marker in forbidden if marker in text]
    return problems


def output_paths() -> list[Path]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [ROOT / item["output"] for item in manifest["guides"]]


def main() -> int:
    problems = check_text(
        "template",
        TEMPLATE.read_text(encoding="utf-8"),
        BASELINE["templateRequired"],
        BASELINE["templateForbidden"],
    )
    for path in output_paths():
        if not path.exists():
            problems.append(f"rendered guide missing: {path.relative_to(ROOT)}")
            continue
        problems += check_text(
            str(path.relative_to(ROOT)),
            path.read_text(encoding="utf-8"),
            BASELINE["renderedRequired"],
            BASELINE["templateForbidden"],
        )
    if problems:
        print("FAIL: approved Sadang final baseline drift detected", file=sys.stderr)
        print("\n".join(f"- {problem}" for problem in problems), file=sys.stderr)
        return 1
    print(f"PASS: approved Sadang final baseline verified for {len(output_paths())} generated guides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
