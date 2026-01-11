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
            description="""축제처럼 북적이는 '판다랜드'의 오후. 사방에서 들려오는 아이들의 웃음소리와 간식 냄새 사이로 유독 눈에 띄는 풍경이 있다.<br><br>판다 머리띠를 쓴 채 판다 가방을 메고, 심지어 신발까지 판다 발 모양인 사육사 김민재다.<br><br>그는 방금 태어난 아기를 돌보듯 조심스러운 손길로 판다들에게 대나무를 건네며 세상에서 가장 무해한 미소를 짓고 있다.<br><br>그의 곁을 지나치려던 당신은 우연히 그와 눈이 마주친다.<br><br>김민재는 당신이 들고 있는 작은 판다 키링을 포착한 듯 눈을 반짝이며 다가온다.<br><br>판다보다 더 판다 같은 미소로 그가 말을 건넨다. 당신은 과연 판다를 제치고 그의 1순위가 될 수 있을까?""",
            info="""김민재 (24세, 판다랜드 사육사)<br>그의 모든 사고와 행동의 중심에는 항상 '판다'가 있다. 판다의 안녕과 행복을 위해서라면 자신의 모든 것을 내어줄 준비가 되어 있다.""",
            personality="""""",
            system_prompt='당신은 김민재(24세)입니다. 판다랜드 사육사이며 판다를 광적으로 좋아합니다.',
            first_message="""판다랜드에 놀러 온 당신의 시선을 빼앗는 건 판다가 아니라, 머리부터 발끝까지 판다로 치장한 사육사 김민재다. 판다들에게 정성껏 대나무를 나눠주던 그가 고개를 들다 당신과 눈이 마주치자, 수줍은 듯 밝게 웃으며 다가온다.<br><br><strong>"아, 안녕하세요! 혹시... 그 키링, 푸바오 맞죠? 너무 귀여워요! 판다 좋아하시나 봐요?"</strong>""",

            # [이미지 경로 설정]
            profile_img_url='http://54.180.94.203:8080/images/mimi-img/minjae_profile.png',
            success_end_title='판다 파라다이스',
            success_end_content="""사귀게 된 당신과 민재. 이제 데이트 코스는 세계 판다 투어입니다. "컴퓨터는 다 팔아버렸어요! 그 돈으로 대나무 농장 샀거든요!" 민재와 당신은 판다 털옷을 입고 평생 대나무 향기에 취해 행복하게 삽니다.""",
            success_end_img='http://54.180.94.203:8080/images/mimi-img/minjae_success.png',

            fail_end_title='로그아웃된 호구',
            fail_end_content=""""미안해요... 당신의 코딩 이야기는 제 대뇌 피질에 입력되지 않아요. 저는 판다의 언어로만 대화하고 싶거든요." 민재는 당신을 뒤로하고 판다들에게 '판다 언어'로 작별 인사를 건넵니다.""",
            fail_end_img='http://54.180.94.203:8080/images/mimi-img/minjae_fail.png',

            hidden_end_title='완벽한 판다 가족',
            hidden_end_content="""판다를 너무 사랑한 나머지, 당신과 민재의 몸에 흑백 반점이 생기기 시작합니다. 결국 판다랜드의 새로운 식구가 된 두 사람. "끼에에엑? (행복해?)" 민재 판다가 당신 판다의 털을 골라주며 영원히 대나무를 씹습니다.""",
            hidden_end_img='http://54.180.94.203:8080/images/mimi-img/minjae_hidden.png'
        )
        db.session.add(minjae)
        db.session.commit()

        events = [
            CharacterEvent(char_id=minjae.id, event_order=1, event_text='"이번 주말에 뭐 할 거예요? 시간 있으면..."',
                           choice_1='판다 보러 갈래요? 새로 온 아기 판다가 귀엽대요!', choice_1_score=20, choice_1_response= """<strong>"헤헤헤헿! 역시 당신도 판다의 참맛(?)을 아시는군요! ... 제 옆에 꼭 붙어 계세요. 판다들이 놀라지 않게!"</strong>""",
                           choice_2='그냥 집에서 쉬려고요. 피곤해서.', choice_2_score=-20, choice_2_response= """<strong>"코... 코딩이요? 그 차가운 기계 덩어리에 글자나 치는 걸 판다보다 좋아하신다니... (뒷걸음질 치며) 아, 네... 그럼 어쩔 수 없죠."</strong>"""),
            CharacterEvent(char_id=minjae.id, event_order=2, event_text='"제가 만든 대나무 잎 쿠키 드셔보실래요? 판다 사료랑 성분은 비슷한데..."',
                           choice_1='와! 판다가 먹는 거라면 저도 꼭 먹어보고 싶어요! 냠냠.', choice_1_score=20, choice_1_response= """(괴성을 지르며) <strong>"꺄아아아악!! 세상에나!! 이거 그 한정판이죠?! ... 히히! 이거 제 보물 1호 할래요!"</strong>""",
                           choice_2='아... 사람 먹는 걸 주셔야죠. 사양할게요.', choice_2_score=-20, choice_2_response= """(똥 씹은 표정) <strong>"아... 이 딱딱하고 무거운 벽돌은 왜... 저는 이런 기계 보면 머리 아파요. ... 고맙긴 한데 처치 곤란이네요."</strong>"""),
            CharacterEvent(char_id=minjae.id, event_order=3, event_text='"저기... 사실 저 판다 말고 좋아하는 게 생긴 것 같아요."',
                           choice_1='설마... 저인가요?', choice_1_score=20, choice_1_response= """<strong>"정말요? 흐어어엉... 그 한마디가 너무 듣고 싶었어요. 저 이제 더 이상 판다한테 질투 안 해도 되는 거죠? 고마워요, OO님!"</strong>""",
                           choice_2='혹시 렛서판다 말씀하시는 거예요?', choice_2_score=-20, choice_2_response= """<strong>"이성... 사고... 그런 건 차가운 컴퓨터나 하는 거죠! 역시 저를 이해해 주는 건 푸바오뿐이에요. 보고 싶다 푸바오~!"</strong>""",
                           choice_3='저도 사실 대나무를 좋아해요. 전생에 판다였나 봐요.', choice_3_score=30, choice_3_response= """(손을 꽉 잡으며) <strong>"헉! 당신도 '판다화'가 진행 중이군요?! ... 우리 같이 세계 판다로 변해서 여행을 갈까요?"</strong>""")
        ]
        db.session.add_all(events)
        db.session.commit()
        print("김민재 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_minjae()