from app import create_app
from app.models import db, Character, CharacterEvent


def seed_minjae():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='김민재').first()
        if char: db.session.delete(char)

        minjae = Character(
            name='김민재',
            title='그 어떠한 것보다도 판다가 1순위인 상냥하고 순진한 호구형 인간',
            hashtags='#판다바보 #호구 #순진무구 #판다랜드',
            description='대나무 숲 사이로 보이는 그의 해맑은 미소. 하지만 그 미소는 사람이 아닌 판다를 향한 것이다.',
            system_prompt='당신은 김민재(24세)입니다. 판다랜드 사육사이며 판다를 광적으로 좋아합니다.',
            profile_img_url='/static/images/minjae/profile.png',
            success_end_title='명예 사육사', success_end_content='이제 우리 둘이서 판다를 돌봐요.',
            success_end_img='/static/images/minjae/success.png',
            fail_end_title='출입 금지', fail_end_content='판다들이 당신을 싫어해요.', fail_end_img='/static/images/minjae/fail.png',
            hidden_end_title='판다의 탈을 쓴 자', hidden_end_content='당신... 혹시 판다였나요?',
            hidden_end_img='/static/images/minjae/hidden.png'
        )
        db.session.add(minjae)
        db.session.commit()

        events = [
            CharacterEvent(char_id=minjae.id, event_order=1, event_text='"이번 주말에 뭐 할 거예요? 시간 있으면..."',
                           choice_1='판다 보러 갈래요? 새로 온 아기 판다가 귀엽대요!', choice_1_score=20,
                           choice_2='그냥 집에서 쉬려고요. 피곤해서.', choice_2_score=-20),
            CharacterEvent(char_id=minjae.id, event_order=2, event_text='"제가 만든 대나무 잎 쿠키 드셔보실래요? 판다 사료랑 성분은 비슷한데..."',
                           choice_1='와! 판다가 먹는 거라면 저도 꼭 먹어보고 싶어요! 냠냠.', choice_1_score=20,
                           choice_2='아... 사람 먹는 걸 주셔야죠. 사양할게요.', choice_2_score=-20),
            CharacterEvent(char_id=minjae.id, event_order=3, event_text='"저기... 사실 저 판다 말고 좋아하는 게 생긴 것 같아요."',
                           choice_1='설마... 저인가요?', choice_1_score=20,
                           choice_2='혹시 렛서판다 말씀하시는 거예요?', choice_2_score=-20,
                           choice_3='저도 사실 대나무를 좋아해요. 전생에 판다였나 봐요.', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("김민재 시드 데이터 생성 완료")


if __name__ == '__main__':
    seed_minjae()