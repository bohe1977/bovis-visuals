"""KBO game-card content contract: four verified facts and Korean particles."""
from __future__ import annotations

FORBIDDEN_GENERIC = {
    '승리의 발판을 놓았다',
    '공격을 이끌었다',
    '불펜이 리드를 지켰다',
    '최종 스코어를 지켰다',
}


def subject_particle(value: str) -> str:
    """Return 이/가 for Korean names; vowel-ending foreign names use 가."""
    for char in reversed(value.strip()):
        if '가' <= char <= '힣':
            return '이' if (ord(char) - ord('가')) % 28 else '가'
        if char.isalpha():
            return '가'
    return '이'


def topic_particle(value: str) -> str:
    """Return 은/는 for Korean names; vowel-ending foreign names use 는."""
    for char in reversed(value.strip()):
        if '가' <= char <= '힣':
            return '은' if (ord(char) - ord('가')) % 28 else '는'
        if char.isalpha():
            return '는'
    return '은'


def validate_game_points(game: dict) -> None:
    points = game.get('winner_points')
    if not isinstance(points, list) or len(points) < 4:
        raise ValueError(f"{game.get('id')}: need starter, decisive play, hitter, bullpen (four GAME POINTS)")
    joined = ' '.join(points)
    if '결승타는 없음' in joined or '결승타 없음' in joined:
        raise ValueError(f"{game.get('id')}: missing source-backed decisive-play point")
    if not any(token in joined for token in ('결승타', '결승 홈런', '끝내기', '승부처', '역전', '흐름을 잡았다')):
        raise ValueError(f"{game.get('id')}: missing source-backed decisive-play point")
    if not any('타수' in point and '안타' in point for point in points):
        raise ValueError(f"{game.get('id')}: missing source-backed hitter point")
    if any(token in joined for token in FORBIDDEN_GENERIC):
        raise ValueError(f"{game.get('id')}: generic filler is not an approved GAME POINT")
    save = game.get('save_pitcher')
    if save:
        expected = subject_particle(save)
        incorrect = '이' if expected == '가' else '가'
        if f'{save}{incorrect} 마무리' in joined:
            raise ValueError(f"{game.get('id')}: invalid subject particle after {save}")
