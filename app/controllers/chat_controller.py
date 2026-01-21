from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.utils.auth import token_required
from urllib import parse
import traceback

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/start', methods=['POST'])
@token_required
def start_chat(current_user):
    """채팅방 시작 (초기화)
    ---
    tags:
      - 채팅 (Chat)
    summary: 캐릭터 선택 및 대화 시작
    description: |
      특정 캐릭터를 선택하여 대화를 시작합니다.
      - 기존 대화 내역이 있다면 모두 **삭제**됩니다.
      - 호감도와 진행 단계가 **초기화**됩니다.
      - 캐릭터의 성격에 맞는 **첫 인사말(AI 생성)**을 반환합니다.
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - character_id
          properties:
            character_id:
              type: integer
              example: 1
              description: 선택한 캐릭터의 ID
    responses:
      200:
        description: 시작 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                character_id:
                  type: integer
                  example: 1
                character_name:
                  type: string
                  example: "이준호"
                greeting:
                  type: string
                  example: "왔어? 기다리고 있었는데... 앉아."
                  description: AI가 생성한 첫 인사말
                profile_img:
                  type: string
                  example: "https://example.com/images/junho.jpg"
                affinity:
                  type: integer
                  example: 0
                current_step:
                  type: integer
                  example: 1
      400:
        description: 요청 데이터 오류 (character_id 누락)
      404:
        description: 캐릭터를 찾을 수 없음
      500:
        description: 서버 내부 에러
    """
    try:
        data = request.get_json()
        char_id = data.get('character_id')

        if not char_id:
            return jsonify({'success': False, 'message': 'character_id가 필요합니다.'}), 400

        user_id = current_user['user_id']

        # 서비스 호출
        result = ChatService.start_chat(user_id, char_id)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 404
    except Exception as e:
        print(f"🔥 채팅 시작 에러: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': '채팅방 생성 중 오류가 발생했습니다.'}), 500


@chat_bp.route('/list', methods=['GET'])
@token_required
def get_chat_list(current_user):
    """대화 목록 조회
    ---
    tags:
      - 채팅 (Chat)
    summary: 사용자의 대화 목록 조회
    description: 진행 중인 모든 캐릭터와의 대화 목록을 최근 순으로 조회합니다.
    security:
      - Bearer: []
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
              type: array
              items:
                type: object
                properties:
                  char_id:
                    type: integer
                    example: 1
                  char_name:
                    type: string
                    example: 조원빈
                  profile_img_url:
                    type: string
                    example: null
                  affinity:
                    type: integer
                    example: 40
                  is_ended:
                    type: boolean
                    example: false
                  last_message:
                    type: string
                    example: 오... 당신, 진짜를 아시는군요?
                  last_sender:
                    type: string
                    example: ai
                  last_chat_time:
                    type: string
                    example: "2026-01-11T10:30:00"
                  updated_at:
                    type: string
                    example: "2026-01-11T10:30:00"
      401:
        description: 인증 실패
    """
    try:
        user_id = current_user['user_id']
        chat_list = ChatService.get_user_chat_list(user_id)

        return jsonify({
            'success': True,
            'data': chat_list
        }), 200

    except Exception as e:
        print("\n\n🔥 대화 목록 조회 에러 🔥")
        traceback.print_exc()
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


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
        example: 조원빈
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
                    char_name:
                      type: string
                      example: 조원빈
                    affinity:
                      type: integer
                      example: 40
                    current_step:
                      type: integer
                      example: 2
                    turn_count:
                      type: integer
                      example: 0
                    is_ended:
                      type: boolean
                      example: false
                    is_chatting:
                      type: boolean
                      example: true
                chat_history:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      sender:
                        type: string
                        example: user
                      message:
                        type: string
                        example: 햇살을 받으면 구릿빛으로...
                      created_at:
                        type: string
                        example: "2026-01-11T10:20:00"
      404:
        description: 캐릭터를 찾을 수 없음
    """
    try:
        user_id = current_user['user_id']
        decoded_char_name = parse.unquote(char_name)

        progress = ChatService.get_or_create_progress(user_id, decoded_char_name)
        chat_history = ChatService.get_chat_history(user_id, decoded_char_name, limit=50)

        return jsonify({
            'success': True,
            'data': {
                'progress': progress.to_dict(),
                'chat_history': chat_history
            }
        }), 200

    except Exception as e:
        print("\n\n🔥 채팅 상태 조회 에러 🔥")
        traceback.print_exc()
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@chat_bp.route('/<char_name>/event', methods=['GET'])
@token_required
def get_current_event(current_user, char_name):
    """현재 이벤트 조회
    ---
    tags:
      - 채팅 (Chat)
    summary: 진행 중인 이벤트 및 선택지 조회
    description: 현재 단계의 이벤트 내용과 선택 가능한 선택지를 가져옵니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: 캐릭터 이름
        example: 조원빈
    responses:
      200:
        description: 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                is_ended:
                  type: boolean
                  example: false
                event:
                  type: object
                  properties:
                    id:
                      type: integer
                    event_order:
                      type: integer
                    event_text:
                      type: string
                    choices:
                      type: array
                      items:
                        type: object
                        properties:
                          text:
                            type: string
                          score:
                            type: integer
                          index:
                            type: integer
                current_step:
                  type: integer
                affinity:
                  type: integer
      404:
        description: 이벤트 없음
    """
    try:
        user_id = current_user['user_id']
        result = ChatService.get_current_event(user_id, char_name)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except Exception as e:
        print("\n\n🔥 이벤트 조회 에러 🔥")
        traceback.print_exc()
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


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
      - **선택지 선택**: `choice_index` (1, 2, 3)를 담아 보냅니다. 둘 중 하나는 반드시 포함되어야 합니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: 캐릭터 이름
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              example: "안녕, 반가워!"
            choice_index:
              type: integer
              example: 1
    responses:
      200:
        description: 처리 성공
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
                  example: chat
                  description: "chat(대화) 또는 choice(선택)"
                response:
                  type: string
                  example: "AI 응답 메시지"
                trigger_event:
                  type: boolean
                  example: false
                  description: "이벤트 발생 여부"
                affinity:
                  type: integer
    """
    try:
        user_id = current_user['user_id']
        data = request.get_json()

        message = data.get('message')
        choice_index = data.get('choice_index')

        if message:
            # 1. 자유 채팅
            result = ChatService.chat_with_character(user_id, char_name, message)
            return jsonify({
                'success': True,
                'data': result
            }), 200

        elif choice_index:
            # 2. 선택지 선택
            result = ChatService.handle_choice(user_id, char_name, int(choice_index))
            return jsonify({
                'success': True,
                'data': result
            }), 200

        else:
            return jsonify({
                'success': False,
                'message': 'message 또는 choice_index가 필요합니다.'
            }), 400

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        print("\n\n🔥 메시지 전송 에러 🔥")
        traceback.print_exc()
        print("🔥 ----------------------------- 🔥\n\n")

        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500