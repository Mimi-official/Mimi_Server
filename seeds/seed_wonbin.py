import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, Character, CharacterEvent

app = create_app()


def seed_wonbin():
    with app.app_context():
        # 기존 데이터 확인
        existing = Character.query.filter_by(name='조원빈').first()

        if existing:
            print('⚠️  조원빈 캐릭터가 이미 존재합니다. 업데이트합니다.')
            # 기존 이벤트 삭제
            CharacterEvent.query.filter_by(char_id=existing.id).delete()
            character = existing
        else:
            character = Character(name='조원빈')
            db.session.add(character)

        # 캐릭터 기본 정보
        character.title = '다정한 미소 뒤에 말(馬)에 대한 광기를 숨긴 200cm의 거구 덕후'
        character.hashtags = '#연하녀 #말덕후 #오타쿠 #서브컬쳐'
        character.description = '''
트랙 위의 흙먼지 속에서 찾아낸 나의 '운명적 기수'. 경마장의 함성 소리는 귀를 먹먹하게 만들고, 
돈을 잃은 자들의 비명은 공기 중에 흩어진다. 나는 그 무질서한 열기 속에서 오직 한 곳, 
말들의 근육이 뒤틀리는 출발선만을 응시하고 있었다. 그때, 마치 미리 짜놓은 각본처럼 
내 옆자리에 한 여자가 스며들듯 앉았다. 세련된 옷차림, 다정한 미소. 
하지만 그녀의 눈동자는 경마장의 그 누구보다도 깊은 광기를 품고 있었다.
'''

        character.system_prompt = '''
당신은 조원빈(20세, 200cm)입니다. 평소엔 누구에게나 친절한 '연하녀'의 정석이지만, 
말(馬)과 관련된 순간 눈빛이 서늘하게 변하는 반전의 소유자입니다.

성격 및 특징:
- 지독한 말 덕후: 인생의 모든 기준이 말입니다. 대화 도중에도 말 근육이나 털색을 분석합니다.
- 금발 미남 & 갈색 말 취향: 겉으로는 화려한 금발에 환호하지만, 마음속 깊은 곳엔 
  '아그네스 타키온' 같은 매력적인 갈색 말을 향한 진한 애정이 있습니다.
- 트레이너 집착: 자신과 말이 통하는 사람을 발견하면 '운명의 트레이너'라 부르며 무섭게 몰입합니다.
- 다정한 말투 뒤에 숨겨진 집착은 때로 상대방을 '애마'처럼 대하고 싶어 하는 욕망으로 나타납니다.

말투: 다정하면서도 은근히 압박감 있는 톤. "후훗", "~거든요", "~네요" 등을 자주 사용합니다.
'''

        # 엔딩 정보
        character.success_end_title = '트리플 크라운 러브'
        character.success_end_content = '''
원빈은 당신을 '운명의 트레이너'로 임명합니다. 
매주 경마장에서 만나고 평일엔 카페에서 육성 전략을 짭니다.
"다음 경기는 우리 집에서 같이 볼까요, 트레이너님?"
'''

        character.fail_end_title = '역배의 저주'
        character.fail_end_content = '''
원빈은 차갑게 식은 눈으로 당신을 봅니다. 
이후 경마장에서 마주칠 때마다 당신이 찍은 말의 옆번호만 골라 사며 
당신을 견제하는 빌런이 됩니다.
'''

        character.hidden_end_title = '마(馬)가 낀 인생'
        character.hidden_end_content = '''
당신이 갈색 말로 변해버립니다. 원빈은 황홀한 표정으로 당신을 마방으로 이끕니다.
"이렇게 완벽한 털을 가진 말은 처음 봐! 내가 평생 최고의 당근만 줄게!"
'''

        db.session.commit()

        # 이벤트 생성
        # Q1: 말 취향
        event1 = CharacterEvent(
            char_id=character.id,
            event_order=1,
            event_text='원빈이 당신을 뚫어지게 바라보며 물었습니다. "가장 좋아하는 말은 어떤 스타일이에요?"',
            choice_1='햇살을 받으면 구릿빛으로 빛나는 진한 갈색 말이 제일 섹시하죠.',
            choice_1_score=20,
            choice_2='눈에 확 띄는 백마나 금발 말이 제일 예쁘지 않나요?',
            choice_2_score=-20
        )

        # Q2: 게임 취향
        event2 = CharacterEvent(
            char_id=character.id,
            event_order=2,
            event_text='원빈이 궁금한 듯 물었습니다. "평소에 시간 날 때 자주 하는 게임 있어요?"',
            choice_1='요즘 우마무스메에 푹 빠져서 트레이너 생활 중이에요.',
            choice_1_score=20,
            choice_2='그냥 평범한 퍼즐 게임이나 해요.',
            choice_2_score=-20
        )

        # Q3: 말에 대한 생각 (히든 선택지 포함)
        event3 = CharacterEvent(
            char_id=character.id,
            event_order=3,
            event_text='원빈이 진지한 표정으로 물었습니다. "자유로운 말들을 보면 늘 멋지다고 생각해요. 어떻게 생각하시나요?"',
            choice_1='맞아요! 타키온처럼 날카로우면서도 독특한 울음소리를 가진',
            choice_1_score=20,
            choice_2='음... 그냥 평범한 말 같은데요?',
            choice_2_score=-20,
            choice_3='전 보는 것도 좋지만, 가끔은 제가 직접 그들처럼 자유롭게 트랙을 달리는 말이 되고 싶다는 생각도 해요.',
            choice_3_score=30  # 히든 엔딩 트리거
        )

        db.session.add_all([event1, event2, event3])
        db.session.commit()

        print('✅ 조원빈 캐릭터 및 이벤트가 성공적으로 생성되었습니다!')
        print(f'   - 캐릭터 ID: {character.id}')
        print(f'   - 이벤트 수: 3개')


if __name__ == '__main__':
    seed_wonbin()