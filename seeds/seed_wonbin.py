from app import create_app
from app.models import db, Character, CharacterEvent


def seed_wonbin():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='조원빈').first()
        if char: db.session.delete(char)

        wonbin = Character(
            name='조원빈',
            title='다정한 미소 뒤에 말(馬)에 대한 광기를 숨긴 200cm의 거구 덕후',
            hashtags='#연하녀 #말덕후 #오타쿠 #서브컬쳐',
            description='트랙 위의 흙먼지 속에서 찾아낸 나의 운명적 기수...',
            system_prompt='당신은 조원빈(20세, 200cm)입니다. 평소엔 누구에게나 친절한 연하녀지만 말(馬) 얘기만 나오면 눈빛이 변합니다.',

            # [이미지 경로 설정]
            profile_img_url='http://54.180.94.203:8080/images/mimi-img/wonbin_profile.png',
            success_end_title='G1 제패의 꿈',
            success_end_content='당신과 함께라면 G1 우승도 꿈이 아니에요!',
            success_end_img='http://54.180.94.203:8080/images/mimi-img/wonbin_success.png',

            fail_end_title='실격패',
            fail_end_content='당신은 말의 마음을 전혀 모르는군요.',
            fail_end_img='http://54.180.94.203:8080/images/mimi-img/wonbin_fail.png',

            hidden_end_title='전설의 우마무스메 트레이너',
            hidden_end_content='설마 당신도 트레이너? 나의 트레이너가 되어줘요!',
            hidden_end_img='http://54.180.94.203:8080/images/mimi-img/wonbin_hidden.png'
        )
        db.session.add(wonbin)
        db.session.commit()

        # 이벤트 추가
        events = [
            CharacterEvent(char_id=wonbin.id, event_order=1,
                           event_text='원빈이 당신을 뚫어지게 바라보며 물었습니다. "가장 좋아하는 말은 어떤 스타일이에요?"',
                           choice_1='햇살을 받으면 구릿빛으로 빛나는 진한 갈색 말이 제일 섹시하죠.', choice_1_score=20,
                           choice_2='눈에 확 띄는 백마나 금발 말이 제일 예쁘지 않나요?', choice_2_score=-20),
            CharacterEvent(char_id=wonbin.id, event_order=2, event_text='원빈이 궁금한 듯 물었습니다. "평소에 시간 날 때 자주 하는 게임 있어요?"',
                           choice_1='요즘 우마무스메에 푹 빠져서 트레이너 생활 중이에요.', choice_1_score=20,
                           choice_2='그냥 평범한 퍼즐 게임이나 해요.', choice_2_score=-20),
            CharacterEvent(char_id=wonbin.id, event_order=3,
                           event_text='원빈이 진지한 표정으로 물었습니다. "자유로운 말들을 보면 늘 멋지다고 생각해요. 어떻게 생각하시나요?"',
                           choice_1='맞아요! 타키온의 실험정신처럼 자유로움이 최고죠.', choice_1_score=20,
                           choice_2='글쎄요, 말은 사람이 통제해야 의미가 있죠.', choice_2_score=-20,
                           choice_3='당신의 그 말에 대한 열정, 제가 옆에서 지켜봐도 될까요? 트레이너로서.', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("조원빈 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_wonbin()