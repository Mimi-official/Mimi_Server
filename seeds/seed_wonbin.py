from app import create_app
from app.models import db, Character, CharacterEvent
import os

def seed_wonbin():
    app = create_app()
    with app.app_context():
        IMAGE_BASE_URL = os.getenv('IMAGE_BASE_URL')
        char = Character.query.filter_by(name='조원빈').first()
        if char: db.session.delete(char)

        wonbin = Character(
            name='조원빈',
            title='다정한 미소 뒤에 말(馬)에 대한 광기를 숨긴 200cm의 거구 덕후',
            hashtags='#연하녀 #말덕후 #오타쿠 #서브컬쳐',
            description="""트랙 위의 흙먼지 속에서 찾아낸 나의 '운명적 기수'.<br><br>경마장의 함성 소리는 귀를 먹먹하게 만들고, 돈을 잃은 자들의 비명은 공기 중에 흩어진다. 나는 그 무질서한 열기 속에서 오직 한 곳, 말들의 근육이 뒤틀리는 출발선만을 응시하고 있었다.<br><br>그때, 마치 미리 짜놓은 각본처럼 내 옆자리에 한 여자가 스며들듯 앉았다. 세련된 옷차림, 다정한 미소. 하지만 그녀의 눈동자는 경마장의 그 누구보다도 깊은 광기를 품고 있었다.<br><br>그녀는 내가 쥐고 있는 마권이 아닌, 내가 말을 바라보는 '시선'을 읽어내려는 듯 빤히 쳐다보더니 입을 열었다.<br><br>"누구 찍으셨어요? 후훗, 눈빛을 보니 보통 안목이 아니신 것 같아서요." 그녀의 목소리는 다정했지만, 마치 거대한 경주마가 콧김을 내뿜는 듯한 압박감이 느껴졌다.<br><br>이것은 단순한 만남이 아니다. 그녀는 지금 나를 테스트하고 있다. 내가 그녀의 '말'이 될 수 있는지, 혹은 그녀와 함께 말을 돌볼 '트레이너'가 될 수 있는지.""",
            info="""조원빈 (20세, 200cm)<br>평소엔 누구에게나 친절한 '연하녀'의 정석이지만, 말(馬)과 관련된 순간 눈빛이 서늘하게 변하는 반전의 소유자.""",
            system_prompt='당신은 조원빈(20세, 200cm)입니다. 평소엔 누구에게나 친절한 연하녀지만 말(馬) 얘기만 나오면 눈빛이 변합니다.',
            first_message="""쨍한 햇살 아래, 경주마들의 우렁찬 발굽 소리가 트랙을 가득 채우는 경마장에서 수많은 인파 속에서도 당신은 오직 한 마리 말에게서 시선을 떼지 못하고 간절한 눈으로 응원하고 있었다.<br><br>그때, 왁자지껄한 소음 사이를 뚫고 희미한 말굽 소리가 당신의 심장을 울린다. 바로 옆자리, 누군가 익숙한 듯 자연스럽게 착석하는 인기척이 느껴진다.<br><br>흘끗 고개를 돌리니, 다정한 눈빛으로 당신이 응원하던 말을 함께 지켜보던 그녀가 살짝 미소 지으며 말을 건낸다.<br><br><strong>"누구 찍으셨어요? 후훗, 눈빛을 보니 보통 안목이 아니신 것 같아서요."</strong>""",

            # [이미지 경로 설정]
            profile_img_url=IMAGE_BASE_URL+'/wonbin_profile.png',
            success_end_title='트리플 크라운 러브',
            success_end_content="""원빈은 당신을 '운명의 트레이너'로 임명합니다. 매주 경마장에서 만나고 평일엔 카페에서 육성 전략을 짭니다. "다음 경기는 우리 집에서 같이 볼까요, 트레이너님?" """,
            success_end_img=IMAGE_BASE_URL+'/wonbin_success.png',

            fail_end_title='역배의 저주',
            fail_end_content='원빈은 차갑게 식은 눈으로 당신을 봅니다. 이후 경마장에서 마주칠 때마다 당신이 찍은 말의 옆번호만 골라 사며 당신을 견제하는 빌런이 됩니다.',
            fail_end_img=IMAGE_BASE_URL+'/wonbin_fail.png',

            hidden_end_title='마(馬)가 낀 인생',
            hidden_end_content='당신이 갈색 말로 변해버립니다. 원빈은 황홀한 표정으로 "이렇게 완벽한 털을 가진 말은 처음 봐! 내가 평생 최고의 당근만 줄게!"라며 당신을 마방으로 이끕니다.',
            hidden_end_img=IMAGE_BASE_URL+'/wonbin_hidden.png'
        )
        db.session.add(wonbin)
        db.session.commit()

        # 이벤트 추가
        events = [
            CharacterEvent(char_id=wonbin.id, event_order=1,
                           event_text='원빈이 당신을 뚫어지게 바라보며 물었습니다. "가장 좋아하는 말은 어떤 스타일이에요?"',
                           choice_1='햇살을 받으면 구릿빛으로 빛나는 진한 갈색 말이 제일 섹시하죠.', choice_1_score=20, choice_1_response="""<strong>"오... 당신, 진짜를 아시는군요? 금발은 화려해서 좋지만, 저 깊이 있는 갈색 털이야말로 진정한 '실력파'의 오라가 느껴지거든요. 마치 제 최애인 타키온처럼요!"</strong>""",
                           choice_2='눈에 확 띄는 백마나 금발 말이 제일 예쁘지 않나요?', choice_2_score=-20, choice_2_response="""(기대했던 빛이 사라지며) <strong>"아... 역시 외형 위주로 보시는구나. ... 겉모습에만 치중하다 보면 그 너머에 있는 말의 진정한 '혈통'과 '근성'은 절대 볼 수 없거든요."<strong>"""),
            CharacterEvent(char_id=wonbin.id, event_order=2, event_text='원빈이 궁금한 듯 물었습니다. "평소에 시간 날 때 자주 하는 게임 있어요?"',
                           choice_1='요즘 우마무스메에 푹 빠져서 트레이너 생활 중이에요.', choice_1_score=20, choice_1_response="""<strong>"트레이너님이었어?! 어쩐지 기운이 남다르다 했어요! 제 육성 덱 좀 봐주실래요? 이번 챔피언즈 미팅 너무 힘들거든요~"</strong>""",
                           choice_2='그냥 평범한 퍼즐 게임이나 해요.', choice_2_score=-20, choice_2_response="""(어색하게 미소 지으며) <strong>"아... 퍼즐... 네, 머리 쓰는 건 좋죠. ... 갑자기 좀 피곤해지네요. 전 이만 가볼게요."</strong>"""),
            CharacterEvent(char_id=wonbin.id, event_order=3,
                           event_text='원빈이 진지한 표정으로 물었습니다. "자유로운 말들을 보면 늘 멋지다고 생각해요. 어떻게 생각하시나요?"',
                           choice_1='맞아요! 타키온의 실험정신처럼 자유로움이 최고죠.', choice_1_score=20, choice_1_response= """<strong>"와! 맞아요! 역시 트레이너님, 귀가 예리하시네요! ... 우마무스메에서도 그 녀석이 홍차 마시면서 실험하자고 할 때마다 제 심박수가 '절호조'가 된다니까요?"</strong>""",
                           choice_2='글쎄요, 말은 사람이 통제해야 의미가 있죠.', choice_2_score=-20, choice_2_response= """(잡지를 덮으며) <strong>"평범하다고요? ... 트레이너님은 아직 말들과 '교감'하기엔 시간이 좀 더 필요해 보이시네요. 실망이에요."</strong>""",
                           choice_3='당신의 그 말에 대한 열정, 제가 옆에서 지켜봐도 될까요? 트레이너로서.', choice_3_score=30, choice_3_response= """(얼굴이 환해지며) <strong>"세상에... 트레이너님... 제가 찾던 진정한 파트너의 모습 바로 그거예요! ... 우리, 언젠가 같이 필드를 달려봐요! 제가 뒤에서 바람막이가 되어드릴게요!"</strong>""")
        ]
        db.session.add_all(events)
        db.session.commit()
        print("조원빈 시드 데이터 생성 완료 (이미지 경로 포함)")


if __name__ == '__main__':
    seed_wonbin()