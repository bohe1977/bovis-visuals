import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / 'tools' / 'kbo_card_content.py'
    spec = importlib.util.spec_from_file_location('kbo_card_content', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_korean_subject_particle_uses_final_consonant():
    content = load_module()
    assert content.subject_particle('이영하') == '가'
    assert content.subject_particle('김재윤') == '이'
    assert content.subject_particle('비슬리') == '가'


def test_game_points_follow_four_fact_standard_without_generic_filler():
    content = load_module()
    game = {
        'winner_points': [
            '두산 선발 벤자민은 6이닝 4피안타 3사사구 10탈삼진 1실점으로 승리를 기록했다.',
            '공식 결승타는 김민석(3회 무사 1, 3루서 우전 안타)이었다.',
            '박찬호는 5타수 2안타 2타점, 양석환은 3타수 1안타 1타점을 기록했다.',
            '이영하가 1이닝 무실점으로 세이브를 기록했다.',
        ],
        'save_pitcher': '이영하',
    }
    content.validate_game_points(game)


def test_contract_rejects_missing_official_winning_hit_as_prose():
    content = load_module()
    game = {
        'id': 'bad',
        'save_pitcher': None,
        'winner_points': ['선발 기록', '공식 결승타는 없음이었다.', '3타수 1안타', '마지막 이닝 기록'],
    }
    try:
        content.validate_game_points(game)
    except ValueError as exc:
        assert 'missing source-backed decisive-play point' in str(exc)
    else:
        raise AssertionError('missing winning-hit value must not pass as a decisive fact')


def test_current_kbo_report_meets_four_fact_and_particle_standard():
    content = load_module()
    for path in (ROOT / 'kbo' / 'data.json', ROOT / 'kbo' / '2026-09-22' / 'data.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        for game in data['games']:
            content.validate_game_points(game)
