from app import create_app
from app.models import db, Character, CharacterEvent


def seed_jiyeon():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='한지연').first()
        if char: db.session.delete(char)

        jiyeon = Character(
            name='한지연',
            title='0.1초의 오차도 허용하지 않는 테트리스 세계 챔피언',
            hashtags='#테트리스 #고인물 #와샌즈 #냉미녀',
            description='그녀의 눈동자는 마치 떨어지는 테트리스 블록을 계산하듯 차갑고 예리하게 빛난다.',
            system_prompt='당신은 한지연(22세)입니다. 테트리스 세계 챔피언이며 매사 냉철하지만 샌즈 캐릭터를 매우 좋아합니다.',
            profile_img_url='/static/images/jiyeon/profile.png',
            success_end_title='퍼펙트 클리어', success_end_content='당신은 나에게 딱 맞는 마지막 조각이었어.',
            success_end_img='/static/images/jiyeon/success.png',
            fail_end_title='게임 오버', fail_end_content='당신과는 호흡이 맞지 않아.', fail_end_img='/static/images/jiyeon/fail.png',
            hidden_end_title='몰살 루트의 동반자', hidden_end_content='끔찍한 시간을 보내고 싶어? 나랑 같이.',
            hidden_end_img='/static/images/jiyeon/hidden.png'
        )
        db.session.add(jiyeon)
        db.session.commit()

        events = [
            CharacterEvent(char_id=jiyeon.id, event_order=1, event_text='"인생은 테트리스와 같아. 실수는 쌓이고 성공은 사라지지. 넌 어떻게 생각해?"',
                           choice_1='실수를 만회하려고 노력하는 과정이 아름다운 거 아닐까?', choice_1_score=-20,
                           choice_2='완벽하게 쌓아서 한 번에 터뜨릴 때의 쾌감이 인생이지.', choice_2_score=20),
            CharacterEvent(char_id=jiyeon.id, event_order=2, event_text='"가장 좋아하는 캐릭터 있어? 난 해골 같은 게 좋은데."',
                           choice_1='해골? 혹시 샌즈 말하는 거야? 와! 샌즈!', choice_1_score=20,
                           choice_2='음, 귀여운 동물 캐릭터 좋아해.', choice_2_score=-20),
            CharacterEvent(char_id=jiyeon.id, event_order=3, event_text='"다음 대회 때, 내 옆자리에 누가 있었으면 좋겠는데..."',
                           choice_1='내가 너의 든든한 서포터가 되어줄게.', choice_1_score=20,
                           choice_2='난 그냥 관중석에서 응원할게. 긴장돼서 못 있어.', choice_2_score=-20,
                           choice_3='내가 너의 파피루스가 되어줄게! 녜헤헤!', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("한지연 시드 데이터 생성 완료")


if __name__ == '__main__':
    seed_jiyeon()