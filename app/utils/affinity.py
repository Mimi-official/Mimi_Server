def determine_ending(affinity: int, has_hidden: bool = False) -> str:
    """
    호감도에 따른 엔딩 결정

    Args:
        affinity: 현재 호감도
        has_hidden: 히든 선택지 선택 여부

    Returns:
        'success', 'fail', 'hidden' 중 하나
    """
    if has_hidden:
        return 'hidden'

    if affinity >= 90:
        return 'success'
    elif affinity <= 20:
        return 'fail'

    return None


def should_trigger_ending(affinity: int, current_step: int, total_steps: int = 3) -> bool:
    """
    엔딩을 트리거할지 결정

    Args:
        affinity: 현재 호감도
        current_step: 현재 단계
        total_steps: 전체 단계 수

    Returns:
        엔딩 트리거 여부
    """
    # 모든 이벤트를 완료했거나
    if current_step > total_steps:
        return True

    # 호감도가 극단적인 경우
    if affinity >= 90 or affinity <= 20:
        return True

    return False