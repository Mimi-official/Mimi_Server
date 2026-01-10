from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.utils.auth import token_required

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/<char_name>', methods=['GET'])
@token_required
def get_chat_state(current_user, char_name):
    """채팅 상태 조회 (이어하기)
    ---
    tags:
      - 채팅 (Chat)
    summary: 채팅 상태 및 로그 조회
    description: 특정 캐릭터와의 채팅 진행 상태, 호감도, 대화 기록을 조회합니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: "캐릭터 이름 (예: 조원빈)"
    responses:
      200:
        description: 조회 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                progress:
                  type: object
                  properties:
                    affinity:
                      type: integer
                    current_step:
                      type: integer
                    is_ended:
                      type: boolean
                    turn_count:
                      type: integer
                chat_history:
                  type: array
                  items:
                    type: object
                    properties:
                      sender:
                        type: string
                      message:
                        type: string
      404:
        description: 캐릭터를 찾을 수 없음
    """
    try:
        user_id = current_user['user_id']

        progress = ChatService.get_or_create_progress(user_id, char_name)
        chat_history = ChatService.get_chat_history(user_id, char_name, limit=50)

        return jsonify({
            'success': True,
            'data': {
                'progress': progress.to_dict(),
                'chat_history': chat_history
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@chat_bp.route('/<char_name>/event', methods=['GET'])
@token_required
def get_current_event(current_user, char_name):
    """현재 이벤트 조회
    ---
    tags:
      - 채팅 (Chat)
    summary: 진행 중인 이벤트 및 선택지 조회
    description: 현재 단계의 이벤트 내용과 선택지를 가져옵니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: "캐릭터 이름"
    responses:
      200:
        description: 성공
      404:
        description: 이벤트 없음
    """
    try:
        user_id = current_user['user_id']
        result = ChatService.get_current_event(user_id, char_name)
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@chat_bp.route('/<char_name>', methods=['POST'])
@token_required
def send_message(current_user, char_name):
    """메시지 전송 또는 선택지 선택
    ---
    tags:
      - 채팅 (Chat)
    summary: 대화하기 또는 선택지 고르기
    description: |
        - **자유 채팅**: `message` 필드에 내용을 담아 보냅니다.
        - **선택지 선택**: `choice_index` (1, 2, 3)를 담아 보냅니다.
        둘 중 하나는 반드시 포함되어야 합니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: "캐릭터 이름"
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              description: "사용자 입력 메시지 (자유 채팅용)"
              example: "안녕, 오늘 기분 어때?"
            choice_index:
              type: integer
              description: "선택지 번호 (이벤트용, 1~3)"
              example: 1
    responses:
      200:
        description: 응답 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                type:
                  type: string
                  description: "chat 또는 choice_result"
                response:
                  type: string
                  description: AI 응답 또는 리액션
                affinity:
                  type: integer
                trigger_event:
                  type: boolean
                  description: "(채팅시) 이벤트 발생 여부"
      400:
        description: 입력 오류 (메시지와 선택지 둘 다 없음)
    """
    try:
        user_id = current_user['user_id']
        data = request.get_json()

        user_message = data.get('message')
        choice_index = data.get('choice_index')

        # 1. 선택지 응답인 경우
        if choice_index is not None:
            result = ChatService.handle_choice(user_id, char_name, choice_index)

        # 2. 자유 채팅인 경우
        elif user_message:
            result = ChatService.chat_with_character(user_id, char_name, user_message)

        else:
            return jsonify({'success': False, 'message': '메시지나 선택지를 입력해주세요.'}), 400

        return jsonify({'success': True, 'data': result}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@chat_bp.route('/<char_name>/reset', methods=['POST'])
@token_required
def reset_chat(current_user, char_name):
    """대화 초기화
    ---
    tags:
      - 채팅 (Chat)
    summary: 진행 상황 초기화
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        required: true
        type: string
    responses:
      200:
        description: 초기화 성공
    """
    try:
        user_id = current_user['user_id']
        result = ChatService.reset_progress(user_id, char_name)
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500