from app import create_app
from app.models import db, Character, CharacterEvent


def seed_seohyun():
    app = create_app()
    with app.app_context():
        char = Character.query.filter_by(name='강서현').first()
        if char: db.session.delete(char)

        seohyun = Character(
            name='강서현',
            title='모두에게 친절하지만 아무도 모르는 서늘한 반전을 가진 천사',
            hashtags='#천사 #유리멘탈 #숨겨진이중성 #애니덕후',
            description='하얀 피부에 긴 생머리, 181cm의 큰 키. 그녀는 완벽해 보이지만 어딘가 위태롭다.',
            system_prompt='당신은 강서현(21세)입니다. 겉으론 천사같지만 한정판 애니 굿즈를 놓치면 본성이 튀어나옵니다.',

            # [이미지 경로 설정]
            profile_img_url='http://54.180.94.203:8080/images/mimi-img/seohyeon_profile.png',
            success_end_title='영원한 파트너',
            success_end_content='내 본모습을 보고도 도망가지 않았군요. 당신은 특별해요.',
            success_end_img='http://54.180.94.203:8080/images/mimi-img/seohyeon_success.png',

            fail_end_title='손절',
            fail_end_content='내 수집품에 손대지 마세요. 더 이상 볼 일 없겠네요.',
            fail_end_img='http://54.180.94.203:8080/images/mimi-img/seohyeon_fail.png',

            hidden_end_title='오타쿠의 여왕',
            hidden_end_content='서코... 같이 갈래? 코스프레도 같이 하는 거야.',
            hidden_end_img='http://54.180.94.203:8080/images/mimi-img/seohyeon_hidden.png'
        )
        db.session.add(seohyun)
        db.session.commit()

        events = [
            CharacterEvent(char_id=seohyun.id, event_order=1, event_text='"저기, 제가 실수로 지갑을 두고 왔는데 500원만 빌려주실 수 있나요?"',
                           choice_1='물론이죠! 여기 있어요. (지갑을 통째로 건넨다)', choice_1_score=20,
                           choice_2='저도 현금이 없어서요. 죄송해요.', choice_2_score=-20),
            CharacterEvent(char_id=seohyun.id, event_order=2, event_text='(한정판 피규어 추첨에서 떨어진 서현이 중얼거린다) "죽여버릴 거야..."',
                           choice_1='(못 들은 척 한다) 서현 씨, 무슨 일 있어요?', choice_1_score=-20,
                           choice_2='누굴 죽여요? 제가 대신 처리해 드릴까요? (같이 화낸다)', choice_2_score=20),
            CharacterEvent(char_id=seohyun.id, event_order=3, event_text='"제 비밀... 이제 다 아셨죠? 실망하셨나요?"',
                           choice_1='아니요, 오히려 반전 매력이라 더 좋은데요?', choice_1_score=20,
                           choice_2='좀 무섭긴 하네요. 거리를 둬야겠어요.', choice_2_score=-20,
                           choice_3='실망이라니요! 저도 사실 집에 피규어 장식장만 3개예요.', choice_3_score=30)
        ]
        db.session.add_all(events)
        db.session.commit()
        print("강서현 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_seohyun()