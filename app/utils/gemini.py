import google.generativeai as genai
from flask import current_app


class GeminiService:
    def __init__(self):
        self.model = None

    def initialize(self):
        """Gemini API 초기화"""
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt: str) -> str:
        """AI 응답 생성"""
        if not self.model:
            self.initialize()

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f'AI 응답 생성 실패: {str(e)}')

    def build_character_prompt(self, character, user_choice: str, affinity: int, chat_history: list) -> str:
        """캐릭터 응답 프롬프트 생성"""
        history_text = '\n'.join([
            f"{'사용자' if log['sender'] == 'user' else character.name}: {log['message']}"
            for log in chat_history[-5:]  # 최근 5개만
        ])

        prompt = f"""
당신은 "{character.name}"라는 캐릭터입니다.

[캐릭터 기본 정보]
- 이름: {character.name}
- 타이틀: {character.title}
- 해시태그: {character.hashtags}

[캐릭터 성격 및 설정]
{character.system_prompt}

[현재 상황]
{character.description}

[대화 기록]
{history_text}

[사용자의 선택]
사용자가 "{user_choice}"를 선택했습니다.

[현재 호감도: {affinity}]

위 정보를 바탕으로 캐릭터 {character.name}의 성격과 특징을 완벽하게 반영하여 자연스럽고 몰입감 있는 반응을 생성해주세요.
- 캐릭터의 말투, 성격, 특징을 정확히 표현하세요
- 선택지에 대한 적절한 반응을 보여주세요
- 현재 호감도와 상황을 고려하세요
- 150자 이내로 간결하게 작성하세요
- 마크다운 없이 순수 텍스트만 출력하세요
"""
        return prompt

    def build_ending_prompt(self, character, ending_content: str, affinity: int) -> str:
        """엔딩 응답 프롬프트 생성"""
        prompt = f"""
당신은 "{character.name}"라는 캐릭터입니다.

[엔딩 내용]
{ending_content}

[최종 호감도: {affinity}]

위 엔딩 내용을 바탕으로 {character.name}의 성격을 반영한 마무리 대사를 작성해주세요.
- 캐릭터의 특징과 말투를 유지하세요
- 엔딩의 감정을 생생하게 표현하세요
- 200자 이내로 작성하세요
- 마크다운 없이 순수 텍스트만 출력하세요
"""
        return prompt


gemini_service = GeminiService()