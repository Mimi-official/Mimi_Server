from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.utils.auth import token_required

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/<char_name>', methods=['GET'])
@token_required
def get_chat_state(char_name):
    """채팅 상태 조회 (이어하기)
    ---
    tags:
      - 채팅 (Chat)
    summary: 채팅 상태 조회
    description: 특정 캐릭터와의 채팅 진행 상태 및 대화 기록을 조회합니다.
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
                      example: 40
                    current_step:
                      type: integer
                      example: 2
                    is_ended:
                      type: boolean
                      example: false
                chat_history:
                  type: array
                  items:
                    type: object
                    properties:
                      sender:
                        type: string
                        example: ai
                      message:
                        type: string
                        example: 오... 당신, 진짜를 아시는군요?
      401:
        description: 인증 실패
      404:
        description: 캐릭터를 찾을 수 없음
    """
    try:
        user_id = request.current_user['user_id']

        progress = ChatService.get_or_create_progress(user_id, char_name)
        chat_history = ChatService.get_chat_history(user_id, char_name, limit=50)

        return jsonify({
            'success': True,
            'data': {
                'progress': progress.to_dict(),
                'chat_history': chat_history
            }
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


@chat_bp.route('/<char_name>', methods=['POST'])
@token_required
def send_message(current_user, char_name):
    """
    메시지 전송 또는 선택지 선택
    ---
    body:
      message: "안녕" (자유 채팅 시)
      choice_index: 1 (이벤트 선택지 선택 시)
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
        return jsonify({'success': False, 'message': str(e)}), 500

@chat_bp.route('/<char_name>/choice', methods=['POST'])
@token_required
def send_choice(char_name):
    """선택지 전송
    ---
    tags:
      - 채팅 (Chat)
    summary: 선택지 선택 및 AI 응답 받기
    description: 사용자가 선택한 선택지를 전송하고 AI의 응답을 받습니다.
    security:
      - Bearer: []
    parameters:
      - in: path
        name: char_name
        type: string
        required: true
        description: 캐릭터 이름
        example: 조원빈
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - choice_index
          properties:
            choice_index:
              type: integer
              example: 1
              description: 선택지 번호 (1, 2, 3)
    responses:
      200:
        description: 선택 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                ai_response:
                  type: string
                  example: 오... 당신, 진짜를 아시는군요?
                affinity:
                  type: integer
                  example: 20
                affinity_change:
                  type: integer
                  example: 20
                current_step:
                  type: integer
                  example: 2
                is_ended:
                  type: boolean
                  example: false
                ending:
                  type: object
                  nullable: true
                  properties:
                    type:
                      type: string
                      example: success
                    title:
                      type: string
                      example: 트리플 크라운 러브
                    message:
                      type: string
                      example: 다음 경기는 우리 집에서 같이 볼까요?
      400:
        description: 잘못된 요청
      401:
        description: 인증 실패
    """
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()

        choice_index = data.get('choice_index')

        if choice_index is None:
            return jsonify({
                'success': False,
                'message': '선택지를 입력해주세요.'
            }), 400

        result = ChatService.send_choice(user_id, char_name, choice_index)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


@chat_bp.route('/<char_name>/reset', methods=['POST'])
@token_required
def reset_progress(char_name):
    """진행 상태 초기화
    ---
    tags:
      - 채팅 (Chat)
    summary: 진행 상태 초기화
    description: 특정 캐릭터와의 채팅 진행 상태와 대화 기록을 모두 삭제합니다.
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
        description: 초기화 성공
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                message:
                  type: string
                  example: 진행 상태가 초기화되었습니다.
      401:
        description: 인증 실패
      404:
        description: 진행 상태를 찾을 수 없음
    """
    try:
        user_id = request.current_user['user_id']

        result = ChatService.reset_progress(user_id, char_name)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500


@chat_bp.route('/<char_name>/event', methods=['GET'])
@token_required
def get_current_event(char_name):
    """현재 이벤트 및 선택지 조회
    ---
    tags:
      - 채팅 (Chat)
    summary: 현재 이벤트 조회
    description: 현재 진행 중인 이벤트와 선택 가능한 선택지를 조회합니다.
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
                is_ended:
                  type: boolean
                  example: false
                event:
                  type: object
                  properties:
                    event_text:
                      type: string
                      example: 원빈이 당신을 뚫어지게 바라보며 물었습니다.
                choices:
                  type: array
                  items:
                    type: object
                    properties:
                      text:
                        type: string
                        example: 햇살을 받으면 구릿빛으로 빛나는...
                      score:
                        type: integer
                        example: 20
                      index:
                        type: integer
                        example: 1
                current_step:
                  type: integer
                  example: 1
                affinity:
                  type: integer
                  example: 0
      401:
        description: 인증 실패
      404:
        description: 캐릭터 또는 이벤트를 찾을 수 없음
    """
    try:
        user_id = request.current_user['user_id']

        event_data = ChatService.get_current_event(user_id, char_name)

        return jsonify({
            'success': True,
            'data': event_data
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500