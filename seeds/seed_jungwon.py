from app import create_app
from app.models import db, Character, CharacterEvent


def seed_jungwon():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='민정원').first()
        if char: db.session.delete(char)

        jungwon = Character(
            name='민정원',
            title='마인크래프트의 광기 어린 약탈자',
            hashtags='#마크 #분조장 #TNT광공 #내여자한정스윗',
            description='PC방 구석에서 들리는 샷건 소리. 모니터 속엔 TNT로 초토화된 마을이 보인다.',
            system_prompt='당신은 민정원(19세)입니다. 마인크래프트 약탈 서버 랭커이며 다혈질이지만 내 사람에겐 따뜻합니다.',

            # [이미지 경로 설정]
            profile_img_url='/static/images/jungwon/profile.png',
            success_end_title='서버의 지배자들',
            success_end_content='너와 함께라면 전 서버를 약탈할 수 있어. 우린 최강이야.',
            success_end_img='/static/images/jungwon/success.png',

            fail_end_title='밴(BAN) 처리',
            fail_end_content='내 앞길을 막지 마. 너도 약탈 대상일 뿐이야.',
            fail_end_img='/static/images/jungwon/fail.png',

            hidden_end_title='평화로운 건축가',
            hidden_end_content='약탈은 이제 지겨워... 우리만의 평화로운 집을 짓자.',
            hidden_end_img='/static/images/jungwon/hidden.png'
        )
        db.session.add(jungwon)
        db.session.commit()

        events = [
            CharacterEvent(char_id=jungwon.id, event_order=1, event_text='"아 진짜! 저 잼민이 녀석이 내 집 테러했어! 어떡하지?"',
                           choice_1='참아, 똑같은 사람 되면 안 되지. 신고만 해.', choice_1_score=-20,
                           choice_2='좌표 불러. TNT 들고 바로 갈게.', choice_2_score=20),
            CharacterEvent(char_id=jungwon.id, event_order=2, event_text='"넌 게임할 때 어떤 스타일이야? 농사? 건축?"',
                           choice_1='난 무조건 약탈이지. 뺏는 게 제일 재밌어.', choice_1_score=20,
                           choice_2='난 평화롭게 농사짓고 힐링하는 게 좋아.', choice_2_score=-20),
            CharacterEvent(char_id=jungwon.id, event_order=3, event_text='"이제 다 부수고 나니 허무하네... 넌 나랑 계속 같이 할 거야?"',
                           choice_1='당연하지. 우린 최고의 듀오잖아.', choice_1_score=20,
                           choice_2='너무 과격해서 같이 못 하겠어.', choice_2_score=-20,
                           choice_3='이젠 칼 내려놓고, 우리 둘만의 오붓한 신혼집을 지어보는 건 어때?', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("민정원 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_jungwon()