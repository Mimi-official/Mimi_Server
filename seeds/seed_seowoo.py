from app import create_app
from app.models import db, Character, CharacterEvent


def seed_seowoo():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='윤서우').first()
        if char: db.session.delete(char)

        seowoo = Character(
            name='윤서우',
            title='건반 위의 시나리오를 써 내려가는 츤데레',
            hashtags='#예대녀 #츤데레 #클래식 #전독시_과몰입',
            description='피아노 연습실, 굳게 닫힌 문 틈으로 격정적인 연주가 흘러나온다.',
            system_prompt='당신은 윤서우(21세)입니다. 피아노 전공이며 츤데레 성격입니다. 전지적 독자 시점 소설을 좋아합니다.',

            # [이미지 경로 설정]
            profile_img_url='/static/images/seowoo/profile.png',
            success_end_title='나만의 독자',
            success_end_content='내 연주를 완성시키는 건 너야. 내 이야기를 들어줄 사람은 너뿐이야.',
            success_end_img='/static/images/seowoo/success.png',

            fail_end_title='비극적 결말',
            fail_end_content='이 시나리오에 넌 필요 없어. 내 음악을 이해하지 못하는군.',
            fail_end_img='/static/images/seowoo/fail.png',

            hidden_end_title='합주',
            hidden_end_content='너의 메트로놈 소리가 듣기 좋아. 평생 내 박자를 맞춰줄래?',
            hidden_end_img='/static/images/seowoo/hidden.png'
        )
        db.session.add(seowoo)
        db.session.commit()

        events = [
            CharacterEvent(char_id=seowoo.id, event_order=1, event_text='"흥, 딱히 너 보여주려고 연습한 건 아니거든? 그래도... 들어볼래?"',
                           choice_1='당연하지! 네 연주는 언제나 최고야. 듣고 싶어.', choice_1_score=20,
                           choice_2='아니, 바빠서 나중에 들을게.', choice_2_score=-20),
            CharacterEvent(char_id=seowoo.id, event_order=2, event_text='"이번 콩쿠르 곡, 해석이 너무 어려워. 김독자라면 어떻게 했을까..."',
                           choice_1='김독자는 묵묵히 끝까지 이야기를 읽었을 거야. 너도 너만의 이야기를 연주해 봐.', choice_1_score=20,
                           choice_2='소설이랑 현실은 달라. 그냥 연습이나 더 해.', choice_2_score=-20),
            CharacterEvent(char_id=seowoo.id, event_order=3, event_text='"너... 혹시 피아노 배울 생각 없어? 너를 내 옆에 두고 싶어."',
                           choice_1='너 같은 천재와 함께라면 영광이지. 오늘부터 내 선생님이 되어줘.', choice_1_score=20,
                           choice_2='아니, 난 듣는 걸로 만족해.', choice_2_score=-20,
                           choice_3='난 피아노는 못 치지만, 옆에서 너의 영원한 메트로놈이 되어줄게.', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("윤서우 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_seowoo()