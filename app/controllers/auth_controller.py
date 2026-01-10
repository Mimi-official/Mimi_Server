from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입"""
    try:
        data = request.get_json()

        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')

        if not username or not nickname or not password:
            return jsonify({
                'success': False,
                'message': '모든 필드를 입력해주세요.'
            }), 400

        user = AuthService.register(username, nickname, password)

        return jsonify({
            'success': True,
            'message': '회원가입이 완료되었습니다.',
            'data': user
        }), 201

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


@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인"""
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'success': False,
                'message': '아이디와 비밀번호를 입력해주세요.'
            }), 400

        result = AuthService.login(username, password)

        return jsonify({
            'success': True,
            'message': '로그인에 성공했습니다.',
            'data': result
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 오류가 발생했습니다.'
        }), 500