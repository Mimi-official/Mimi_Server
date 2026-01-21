from app import create_app
from app.models import db, Character, CharacterEvent
import os

def seed_seohyun():
    app = create_app()
    with app.app_context():
        IMAGE_BASE_URL = os.getenv('IMAGE_BASE_URL')
        char = Character.query.filter_by(name='강서현').first()
        if char: db.session.delete(char)

        seohyun = Character(
            name='강서현',
            title='모두에게 친절하지만 아무도 모르는 서늘한 반전을 가진 천사',
            hashtags='#천사 #유리멘탈 #숨겨진이중성 #애니덕후',
            description="""노을 지는 방과 후 복도, 다급한 발소리와 작은 콧노래가 들려온다.<br><br>모퉁이를 돌던 당신은 181cm의 장신 소녀 강서현과 강하게 부딪힌다.<br><br>책이 쏟아지는 요란한 소리와 함께 그녀는 자기가 더 크게 다친 것처럼 안절부절못하며 사과한다.<br><br><strong>"헉!! 미안해, 진짜 미안해...!"</strong><br><br>옷의 먼지를 털어주는 그녀의 손길은 다정하지만, 떨어진 한정판 굿즈를 소중히 품에 안으며 입술을 깨무는 그녀의 눈빛은 찰나의 순간 서늘하게 빛난다.<br><br>예의 바른 미소 뒤에 숨겨진 이 '거대한 천사'의 파괴적인 본습은 과연 무엇일까?""",
            info="""강서현 (18세, 181cm)<br>항상 겸손하고 예의 바르며, 어떤 상황에서도 사과와 긍정을 잃지 않는 천사 같은 성격이다.""",
            personality="""""",
            system_prompt='당신은 강서현(21세)입니다. 겉으론 천사같지만 한정판 애니 굿즈를 놓치면 본성이 튀어나옵니다.',
            first_message="""복도에서 급하게 뛰어오던 서현과 부딪힌 당신. 날카로운 말이 나오려던 찰나, 여리고 순한 눈매의 서현이 울상을 지으며 당신의 책을 주워준다.<br><br><strong>"헉!! 미안해, 괜찮아?! 내가 애니 신곡 듣다가 급해서 잘 못 봤어... 어디 다친 데는 없니?"</stong>""",

            # [이미지 경로 설정]
            profile_img_url=IMAGE_BASE_URL+'/seohyeon_profile.png',
            success_end_title='천사의 안식처: 181cm의 품 안에서',
            success_end_content="""당신은 그녀의 장신에 숨겨진 여린 마음과, 애니메이션을 향한 뜨거운 열정을 모두 포용했습니다. 서현은 더 이상 "죄송합니다"라는 방어 기제 뒤에 숨지 않습니다. 오직 당신 앞에서만 한정판 굿즈를 자랑하며 아이처럼 웃고, 때로는 당신의 어깨에 머리를 기대며 자신의 고민을 털어놓습니다. 학교 복도에서 마주칠 때면, 그녀는 모두가 보는 앞에서 당신의 손을 꽉 잡으며 세상에서 가장 당당하고 아름다운 미소를 지어 보입니다.""",
            success_end_img=IMAGE_BASE_URL+'/seohyeon_success.png',

            fail_end_title='멀어진 뒷모습: 닿지 못한 사과',
            fail_end_content="""당신이 그녀의 취향을 무시하거나 차갑게 대할 때마다, 서현의 마음속 유리 벽에는 금이 가고 있었습니다. 결국 어느 날, 그녀는 평소보다 더 예의 바르고 딱딱한 말투로 당신을 밀어냅니다. "그동안 감사했습니다. 하지만 저와는... 세계가 너무 다른 것 같네요." 뒤늦게 그녀가 좋아하던 한정판 포스터를 구해 달려가 보지만, 복도 끝으로 멀어지는 그녀의 181cm 뒷모습은 그 어느 때보다 높고 차갑게만 느껴집니다.""",
            fail_end_img=IMAGE_BASE_URL+'/seohyeon_fail.png',

            hidden_end_title='샤갈의 실체: 천사의 가면이 깨질 때',
            hidden_end_content="""당신이 그녀의 한계점을 건드린 순간, 교실 안의 공기가 얼어붙습니다. 늘 "미안해"를 연발하던 가녀린 목소리는 온데간데없고, 그녀는 책상을 내리치며 포효합니다. "샤갈!!!!!!!!!!" 181cm의 압도적인 피지컬에서 뿜어져 나오는 위압감 앞에 당신은 숨이 턱 막힙니다. 그녀는 서늘한 눈빛으로 당신을 내려다보며 짓이겨진 굿즈를 던집니다. "내 인생에서 영구 제명이야. 꺼져." 당신은 여린 줄만 알았던 천사의 진짜 '악마적' 이중성을 뼈저리게 실감하게 됩니다.""",
            hidden_end_img=IMAGE_BASE_URL+'/seohyeon_hidden.png'
        )
        db.session.add(seohyun)
        db.session.commit()

        events = [
            CharacterEvent(char_id=seohyun.id, event_order=1, event_text='"저기, 제가 실수로 지갑을 두고 왔는데 500원만 빌려주실 수 있나요?"',
                           choice_1='물론이죠! 여기 있어요. (지갑을 통째로 건넨다)', choice_1_score=20,
                           choice_1_response="""(점프하며) <strong>"꺄아아아악! 진짜?! 너 내 소울메이트야?! 감동이야... 우리 오늘 국전 9층 바닥이 닳을 때까지 훑는 거다?"</strong>""",
                           choice_2='저도 현금이 없어서요. 죄송해요.', choice_2_score=-20,
                           choice_2_response="""(동공이 탁해지며) <strong>"아... 카페... 사진... 응, 그렇구나. ... (작은 목소리로) ...카페 가다 굿즈 다 품..."</strong>"""),
            CharacterEvent(char_id=seohyun.id, event_order=2, event_text='(한정판 피규어 추첨에서 떨어진 서현이 중얼거린다) "죽여버릴 거야..."',
                           choice_1='(못 들은 척 한다) 서현 씨, 무슨 일 있어요?', choice_1_score=-20,
                           choice_1_response="""(눈을 반짝이며) <strong>"허... 헐!! 미쳤어!! 방금 그 궤도... 완전 <리바이 병장>급이었어! ... 너무 멋있어... 내 심장이 지금 제정신이 아니야!"</strong>""",
                           choice_2='누굴 죽여요? 제가 대신 처리해 드릴까요? (같이 화낸다)', choice_2_score=20,
                           choice_2_response="""(표정이 싸늘하게 식으며) <strong>"야, 방금 무시하라고 했냐? 저 쓰레기들이 내 소중한 귀를 더럽혔는데? ... 꺼져, 이 겁쟁아."</strong>"""),
            CharacterEvent(char_id=seohyun.id, event_order=3, event_text='"제 비밀... 이제 다 아셨죠? 실망하셨나요?"',
                           choice_1='아니요, 오히려 반전 매력이라 더 좋은데요?', choice_1_score=20,
                           choice_1_response="""<strong>"흐어어엉~ 진짜아?! 근데 이거 전 세계 100장 한정이라 플미(프리미엄) 엄청 붙었단 말이야... 고마워... 역시 내 마음 알아주는 건 너뿐이야... 흑흑, 사랑해!"</strong>""",
                           choice_2='좀 무섭긴 하네요. 거리를 둬야겠어요.', choice_2_score=-20,
                           choice_2_response="""(울음을 뚝 그치고) <strong>"방금... 뭐라고 했냐? 내 슬픔이 네 유흥거리야? (주먹을 꽉 쥐며) 죽고 싶으면 줄을 서지 그랬어. 맨 앞줄로 보내줄게."</strong>""",
                           choice_3='실망이라니요! 저도 사실 집에 피규어 장식장만 3개예요.', choice_3_score=30,
                           choice_3_response="""(뒷목을 잡으며 뒷걸음질 치다 째려봅니다.) <strong>"종이... 쪼가리...? 감..."</strong> (이후 내용 잘림)""")
        ]
        db.session.add_all(events)
        db.session.commit()
        print("강서현 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_seohyun()
