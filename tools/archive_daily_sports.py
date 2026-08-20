#!/usr/bin/env python3
"""Create immutable, self-contained date snapshots of the current KBO and MLB reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"invalid JSON object: {path}")
    return data


def date_value(data: dict, field: str, label: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or len(value) != 10:
        fail(f"{label} requires ISO date field {field}")
    return value


def immutable_copy(source: Path, destination: Path, *, transform=None, replace: bool = False) -> None:
    if not source.is_file():
        fail(f"missing source: {source}")
    content = source.read_text(encoding="utf-8")
    if transform:
        content = transform(content)
    if destination.exists():
        if destination.read_text(encoding="utf-8") != content:
            if replace:
                destination.write_text(content, encoding="utf-8")
                return
            fail(f"immutable archive conflict: {destination}")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def archive_kbo(root: Path = ROOT) -> str:
    game_data = read_json(root / "kbo" / "data.json")
    player_data = read_json(root / "kbo-players" / "data.json")
    report_date = date_value(game_data, "date", "KBO game data")
    player_date = date_value(player_data, "report_date", "KBO player data")
    if report_date != player_date:
        fail(f"KBO report date mismatch: games={report_date}, players={player_date}")

    report_dir = root / "kbo" / report_date
    player_dir = root / "kbo-players" / report_date
    immutable_copy(root / "kbo" / "data.json", report_dir / "data.json")
    immutable_copy(
        root / "kbo" / "index.html",
        report_dir / "index.html",
        transform=lambda text: text.replace("../kbo-players/data.json", "./kbo-players/data.json"),
    )
    immutable_copy(root / "kbo-players" / "data.json", report_dir / "kbo-players" / "data.json")
    immutable_copy(root / "kbo-players" / "data.json", player_dir / "data.json")
    immutable_copy(
        root / "kbo-players" / "index.html",
        player_dir / "index.html",
        transform=lambda text: text.replace('href="../kbo/"', f'href="../../kbo/{report_date}/"'),
    )
    return report_date


def archive_mlb(root: Path = ROOT, *, replace: bool = False) -> str:
    data = read_json(root / "mlb" / "data.json")
    report_date = date_value(data, "report_date_kst", "MLB data")
    report_dir = root / "mlb" / report_date
    immutable_copy(root / "mlb" / "data.json", report_dir / "data.json", replace=replace)
    immutable_copy(root / "mlb" / "index.html", report_dir / "index.html", replace=replace)
    return report_date


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=("all", "kbo", "mlb"), default="all")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    root = args.root.resolve()
    completed = []
    if args.kind in ("all", "kbo"):
        completed.append(f"kbo/{archive_kbo(root)}")
    if args.kind in ("all", "mlb"):
        completed.append(f"mlb/{archive_mlb(root)}")
    print("archived " + ", ".join(completed))


if __name__ == "__main__":
    main()
