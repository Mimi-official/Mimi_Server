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
            description="""텅 빈 학교 체육관, 날카로운 피아노 선율이 당신의 발소리에 뚝 끊긴다.<br><br>윤서우가 천천히 고개를 돌리며 당신을 꿰뚫어 보듯 쳐다본다.<br><br>"너는 뭐야? 내 연습 방해하지 말고 나가줄래? 예술을 모르는 사람의 발소리는 내 시나리오를 망치는 소음일 뿐이니까." """,
            info="""윤서우 (24세, 165cm)<br>현재 예대 입시생이다. 클래식에 대한 압도적 자부심이 있으며, 자신의 연주를 진정으로 '읽어주는' 사람에게 지독한 소유욕을 느낀다.""",
            personality="""""",
            system_prompt='당신은 윤서우(21세)입니다. 피아노 전공이며 츤데레 성격입니다. 전지적 독자 시점 소설을 좋아합니다.',
            first_message="""텅 빈 체육관 안, 차가운 공기를 가르고 울려 퍼지던 피아노 선율이 당신의 발소리가 닿는 순간 칼날처럼 날카롭게 끊긴다. 피아노 앞에 앉아 있던 서우는 건반에서 손을 떼지도 않은 채, 고개만 천천히 돌려 당신을 응시한다. 조명조차 비껴간 그녀의 서늘한 눈동자에는 침입자를 향한 노골적인 오만함과 불쾌함이 서려 있다. 그녀는 마치 당신이라는 존재가 자신의 정교한 악보 위에 떨어진 한 방울의 먹물이라도 되는 양, 한참 동안 당신을 훑어내린 뒤 낮게 읊조린다.<br><br><strong>"연습실 문을 열었으면 대가를 지불해야지. 내 연주를 끝까지 '읽어낼' 자신도 없으면서 들어온 거야?"</strong>""",

            # [이미지 경로 설정]
            profile_img_url='http://54.180.94.203:8080/images/mimi-img/seowoo_profile.png',
            success_end_title='불멸의 듀엣',
            success_end_content="""서우는 이제 당신 없이는 피아노 앞에 앉지 않습니다. 당신은 그녀의 음악을 이해해준 유일한 파트너입니다. "너... 정말 보기 드문 참된 교양인이야. 아니, 이제 '내 사람'이라 부를게. 너, 오늘부터 내 옆에서 평생 피아노 배워. 네가 내 음악을 읽어준 것처럼 나도 네 인생을 끝까지 읽어줄 테니까." """,
            success_end_img='http://54.180.94.203:8080/images/mimi-img/seowoo_success.png',

            fail_end_title='영원한 불협화음',
            fail_end_content="""서우의 눈동자에서 일말의 기대조차 사라집니다. 당신의 말은 그녀에게 그저 읽히지 않는 깨진 문장일 뿐입니다. 반응:"저질스럽고 교양 없는... 너랑 예술을 논하려 한 내가 바보지. 이 세계선에서 너 같은 소음은 필요 없어. 내 인생에서 당장 나가줘. 다신 내 음악을 들으러 오지 마." """,
            fail_end_img='http://54.180.94.203:8080/images/mimi-img/seowoo_fail.png',

            hidden_end_title='서우가 갑자기 진지한 표정으로 피아노 의자 위에 올라가 당신을 내려다보며 선언합니다.',
            hidden_end_content="""결정했어. 넌 이제부터 사람이 아니라 내 '메트로놈'이야. 네 심장 박동은 이제 내 연주 템포에만 맞춰서 뛰어야 해! 자, 어서 입으로 박자 넣어. 틱- 택- 틱- 택-! 안 하면 이 세계선은 멸망이야!" """,
            hidden_end_img='http://54.180.94.203:8080/images/mimi-img/seowoo_hidden.png'
        )
        db.session.add(seowoo)
        db.session.commit()

        events = [
            CharacterEvent(char_id=seowoo.id, event_order=1, event_text='"흥, 딱히 너 보여주려고 연습한 건 아니거든? 그래도... 들어볼래?"',
                           choice_1='당연하지! 네 연주는 언제나 최고야. 듣고 싶어.', choice_1_score=20, choice_1_response = """(눈동자가 크게 흔들리며 당신의 소매를 꽉 잡는다) <strong>"너... 그걸 읽어냈구나. 단순히 지루해할 줄 알았는데. 좋아. 너라면 내 '이야기'를 끝까지 지켜볼 자격이 있어. 내 음악을... 외면하지 마."</strong>""",
                           choice_2='아니, 바빠서 나중에 들을게.', choice_2_score=-20, choice_2_response = """(동공이 차갑게 식으며 고개를 돌린다) <strong>"저질스럽고 교양 없는...! 감히 내 시나리오를 지루하다고 하다니. 너 같은 독자는 필요 없어. 영원히 내 시야에서 사라져 줘."</strong>"""),
            CharacterEvent(char_id=seowoo.id, event_order=2, event_text='"이번 콩쿠르 곡, 해석이 너무 어려워. 김독자라면 어떻게 했을까..."',
                           choice_1='김독자는 묵묵히 끝까지 이야기를 읽었을 거야. 너도 너만의 이야기를 연주해 봐.', choice_1_score=20, choice_1_response = """(얼굴이 붉어지며 고개를 숙인다) <strong>"뭐... 뭐야, 그 오글거리는 대사는... (작게 중얼거리며) 그래도, 그렇게 말하니까 기분은 나쁘지 않네. 절대로... 내 허락 없이 먼저 눈 돌리지 마. 알았어?"</strong>""",
                           choice_2='소설이랑 현실은 달라. 그냥 연습이나 더 해.', choice_2_score=-20, choice_2_response = """(입술을 깨물며 낮게 읊조린다) <strong>"미스터치...? 네가 뭘 안다고 내 선율을 비난해? 너는 내 음악을 '읽는' 게 아니라 '평가'하려 드는구나. 너 같은 관객은 이제 질색이야."</strong>"""),
            CharacterEvent(char_id=seowoo.id, event_order=3, event_text='"너... 혹시 피아노 배울 생각 없어? 너를 내 옆에 두고 싶어."',
                           choice_1='너 같은 천재와 함께라면 영광이지. 오늘부터 내 선생님이 되어줘.', choice_1_score=20, choice_1_response = """(당신을 빤히 쳐다보다 손가락을 깍지 끼며) <strong>"후훗, 좋아. 너를 가장 완벽한 연주자로 길들여 줄게. 이제 넌 나 없이는 음악을 논할 수 없게 될 거야. 이 이야기의 끝은... 우리가 정하는 거야."</strong>""",
                           choice_2='아니, 난 듣는 걸로 만족해.', choice_2_score=-20, choice_2_response = """(허탈한 듯 짧게 실소하며) <strong>"그래, 역시 넌 그저 스쳐 지나가는 이방인이었구나. 내 시나리오에 너를 억지로 끼워 넣으려 했던 내가 바보지. 이제 그만 가봐. 다신 오지 말고."</strong>""",
                           choice_3='난 피아노는 못 치지만, 옆에서 너의 영원한 메트로놈이 되어줄게.', choice_3_score=30, choice_3_response = """(당신을 놀란 눈으로 보며) <strong>"내가 왜 그 생각을 못 했을까..? 좋았어, 넌 이제부터 영원히 나의 메트로놈이야. 나의 옆에서 영원히 박자를 맞추도록 해."</strong>""")
        ]
        db.session.add_all(events)
        db.session.commit()
        print("윤서우 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_seowoo()