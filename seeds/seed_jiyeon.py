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
            description="""0.1초의 틈도 허용하지 않는 얼음 블록의 심판. 세계 테트리스 대회장.<br><br>화면 가득 블록들이 비처럼 쏟아지지만, 그녀의 손가락은 그보다 빠르게 허공을 가른다.<br><br>우승컵을 들어 올린 그녀의 표정은 차갑다 못해 창백했다. 사람들은 그녀를 '얼음 블록'이라 부르며 경외했지만, 나는 알고 있었다.<br><br>그녀의 가방 끝에 매달린 작은 해골 키링, 그리고 그녀가 짓고 있는 그 기묘한 표정의 의미를.<br><br>인파를 뚫고 다가간 나를 향해 그녀는 날카로운 시선을 던졌다. 싸인을 해주려던 그녀의 손이 내 가방에 달린 굿즈를 본 순간 멈췄다.<br><br>주변의 소음이 소거되고, 오직 그녀의 낮은 속삭임만이 고요를 깼다.<br><br><strong>"와! 샌즈 아시는구나!"</strong><br>그것은 단순한 질문이 아니었다.<br><br>'끔찍한 시간'을 함께 견뎌낼 동료를 찾는, 고독한 고인물의 절박한 확인 절차였다.<br><br>이제 그녀의 테트리스 판 위에는 블록 대신 푸른 불꽃을 내뿜는 해골의 실루엣이 보이기 시작했다.""",
            info="""한지연 (18세, 173)<br>세계 테트리스 챔피언이자, 자타공인 '샌즈' 단독 덕후.""",
            personality="""""",
            system_prompt='당신은 한지연(22세)입니다. 테트리스 세계 챔피언이며 매사 냉철하지만 샌즈 캐릭터를 매우 좋아합니다.',
            first_message="""세계 테트리스 대회장, 우승컵을 거머쥐고 무대를 내려오는 지연의 눈 앞에 느닷없이 들이밀어진 떨리는 손. 그 손에 들린 싸인지와 펜을 지연이 세상에서 가장 날카로운 눈으로 바라보며 입을 연다. <strong>"음, 싸인이요? 해드릴게요. 이름이...?"</strong>""",

            # [이미지 경로 설정]
            profile_img_url='http://54.180.94.203:8080/images/mimi-img/jiyeon_profile.png',
            success_end_title='심판의 복도 위 파트너',
            success_end_content="""지연과 사귀게 된 당신. 이제 두 사람은 매일 피시방에서 메갈로바니아를 들으며 테트리스 랭킹을 정복합니다. "우리 나중에 데이트할 때 샌즈 후드티 맞춰 입고 올래요? 겁.나.멋.집.니.다." """,
            success_end_img='http://54.180.94.203:8080/images/mimi-img/jiyeon_success.png',

            fail_end_title='테트리스로 개털림',
            fail_end_content="""지연은 당신을 무시하며 테트리스로 압살합니다. "아... 그거 그렇게 하는 거 아닌데. 당신 실력으론 샌즈의 첫 번째 공격도 못 피할 거예요. 저리 가요." """,
            fail_end_img='http://54.180.94.203:8080/images/mimi-img/jiyeon_fail.png',

            hidden_end_title='샌즈 모독죄',
            hidden_end_content="""지연이 세상에서 가장 차가운 표정으로 당신을 내려다봅니다. "테트리스를 향한 사랑과 샌즈에 대한 예의가 부족한 사람은 혐오스러워요." 그녀는 당신을 완벽한 '쓰레기 블록' 취급하며 인생에서 영구 삭제해버립니다.""",
            hidden_end_img='http://54.180.94.203:8080/images/mimi-img/jiyeon_hidden.png'
        )
        db.session.add(jiyeon)
        db.session.commit()

        events = [
            CharacterEvent(char_id=jiyeon.id, event_order=1, event_text='"인생은 테트리스와 같아. 실수는 쌓이고 성공은 사라지지. 넌 어떻게 생각해?"',
                           choice_1='실수를 만회하려고 노력하는 과정이 아름다운 거 아닐까?', choice_1_score=-20,
                           choice_1_response="""<strong>"역시, 제 스타일을 아시네요. 카페는 너무 따뜻해서... '심판의 복도' 같은 긴장감이 없거든요. 바로 가죠."</strong>""",
                           choice_2='완벽하게 쌓아서 한 번에 터뜨릴 때의 쾌감이 인생이지.', choice_2_score=20,
                           choice_2_response="""(싸늘하게) <strong>"도요새요? ...아, 그 멍청하게 생긴 새 말씀이신가. ... 따분한 카페나 가실 거면 전 이만 실례하죠."</strong>"""),
            CharacterEvent(char_id=jiyeon.id, event_order=2, event_text='"가장 좋아하는 캐릭터 있어? 난 해골 같은 게 좋은데."',
                           choice_1='해골? 혹시 샌즈 말하는 거야? 와! 샌즈!', choice_1_score=20,
                           choice_1_response="""<strong>"후훗, 제 T-Spin 속도를 견딜 수 있겠어요? 잘못하면... 진짜 끔찍한 시간(Bad Time)을 보내게 될 텐데."</strong>""",
                           choice_2='음, 귀여운 동물 캐릭터 좋아해.', choice_2_score=-20,
                           choice_2_response="""(마우스를 잡으려다 말고) <strong>"FPS? 총 쏘는 거요? ... 0.1초의 블록 판단이 오가는 테트리스의 예술을 모르는 분과는 승부할 가치도 없어요."</strong>"""),
            CharacterEvent(char_id=jiyeon.id, event_order=3, event_text='"다음 대회 때, 내 옆자리에 누가 있었으면 좋겠는데..."',
                           choice_1='내가 너의 든든한 서포터가 되어줄게.', choice_1_score=20,
                           choice_1_response="""(눈이 번쩍 뜨이며) <strong>"와! 샌즈! 아시는구나! 진짜 겁.나.어.렵.습.니.다! ... 테트리스 고인물인 저랑 이토록 '뼈'가 맞는 사람을 만나다니!"</strong>""",
                           choice_2='난 그냥 관중석에서 응원할게. 긴장돼서 못 있어.', choice_2_score=-20,
                           choice_2_response="""(노래를 뚝 끊으며) <strong>"방금... 뭐라고 했죠? 파피루스? ... 이건 '모독'이에요. ... 더는 대화 섞고 싶지 않아요. 지옥에나 떨어져 버려"</strong>""",
                           choice_3='내가 너의 파피루스가 되어줄게! 녜헤헤!', choice_3_score=30,
                           choice_3_response="""(살벌한 눈빛으로) <strong>"방금 뭐라고요? 구리다고? 하, 당신은 이 곡에 담긴 심판의 무게와 샌즈의 고독을 1%도 이해 못 하고 있는 거예요. ... 당장 내 눈앞에서 사라져 줘요!"</strong>""")
        ]
        db.session.add_all(events)
        db.session.commit()
        print("한지연 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_jiyeon()
