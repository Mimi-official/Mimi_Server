from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.utils.auth import token_required

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


@chat_bp.route('/<char_name>', methods=['GET'])
@token_required
def get_chat_state(char_name):
    """채팅 상태 조회 (이어하기)"""
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


@chat_bp.route('/<char_name>/choice', methods=['POST'])
@token_required
def send_choice(char_name):
    """선택지 전송"""
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
    """진행 상태 초기화"""
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
    """현재 이벤트 및 선택지 조회"""
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