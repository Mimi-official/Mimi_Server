import os
from openai import OpenAI
from flask import current_app


class OpenRouterService:
    def __init__(self):
        self.client = None
        # 사용하고 싶은 모델 ID (OpenRouter 사이트에서 확인 가능)
        self.model_id = "google/gemma-3-12b-it:free"

    def initialize(self):
        """OpenRouter API 초기화"""
        api_key = current_app.config.get('OPENROUTER_API_KEY')
        if not api_key:
            api_key = os.environ.get("OPENROUTER_API_KEY")

        # OpenRouter 전용 설정
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            # 선택 사항: OpenRouter 랭킹에 표시될 앱 정보 (없어도 무방)
            default_headers={
                "HTTP-Referer": "http://localhost:5000",  # 앱의 URL
                "X-Title": "My Character Chat App",  # 앱의 이름
            }
        )

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        """AI 응답 생성"""
        if not self.client:
            self.initialize()

        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})

            messages.append({"role": "user", "content": prompt})

            # OpenAI 인터페이스와 동일하게 호출
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=300,
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"🔥 OpenRouter Error: {e}")
            return "잠시 통신 연결이 불안정해요. 다시 한번 말씀해 주시겠어요?"

    def build_character_prompt(self, character, user_text: str, affinity: int, chat_history: list) -> str:
        """캐릭터 응답 프롬프트 생성 (기존 로직 유지)"""
        history_text = '\n'.join([
            f"{'사용자' if log['sender'] == 'user' else character.name}: {log['message']}"
            for log in chat_history[-10:]
        ])

        prompt = f"""
        당신은 "{character.name}"입니다. 아래의 규칙을 지켜 역할극에 참여하세요.

        [캐릭터 정보]
        - 이름: {character.name}
        - 설정: {character.description}
        - 성격/말투: {character.system_prompt}
        - 현재 호감도: {affinity}/100

        [최근 대화 기록]
        {history_text}

        [사용자 입력]
        "{user_text}"

        [규칙]
        1. 캐릭터의 말투를 완벽하게 유지하며 한국어로만 대답하세요.
        2. 150자 이내로 짧고 강렬하게 응답하세요.
        3. 생각/지문은 평문으로, 실제 대사만 <strong> 태그로 감싸세요.
        4. 줄바꿈은 <br> 태그를 사용하세요.
        5. 이모티콘과 한자는 사용하지 마세요.
        6. 인간처럼 자연스럽게 대화하세요.
        """
        return prompt

    def build_ending_prompt(self, character, ending_content: str, affinity: int) -> str:
        """엔딩 프롬프트"""
        prompt = f"""
        당신은 "{character.name}"입니다. 마지막 장면을 연기하세요.

        [엔딩 시나리오]
        {ending_content}

        [최종 호감도: {affinity}]

        - 200자 이내로 작성
        - 대사만 <strong> 태그로 강조
        - 줄바꿈은 <br> 사용
        """
        return prompt


# 서비스 교체
gemini_service = OpenRouterService()