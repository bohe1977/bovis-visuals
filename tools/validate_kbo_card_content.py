#!/usr/bin/env python3
"""Fail closed unless a KBO report preserves the approved four-fact game-card form."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kbo_card_content import validate_game_points


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    data_path = args.root / 'kbo' / 'data.json'
    data = json.loads(data_path.read_text(encoding='utf-8'))
    games = [game for game in data.get('games', []) if game.get('status') == '경기 종료']
    if not games:
        raise SystemExit('KBO card contract: no final games')
    for game in games:
        validate_game_points(game)
    print(f'KBO card content contract: OK ({data["date"]}, {len(games)} games)')


if __name__ == '__main__':
    main()
