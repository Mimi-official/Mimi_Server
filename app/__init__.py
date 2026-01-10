from flask import Flask, request
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
from app.models import db
from app.swagger_config import swagger_config, swagger_template


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. CORS 설정 (가장 중요)
    # supports_credentials=True: 인증 정보(쿠키/헤더) 포함 허용
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}}, supports_credentials=True)

    # 데이터베이스 초기화
    db.init_app(app)

    # Swagger 초기화
    Swagger(app, config=swagger_config, template=swagger_template)

    # 블루프린트 등록
    from app.controllers.auth_controller import auth_bp
    from app.controllers.character_controller import char_bp
    from app.controllers.chat_controller import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(char_bp)
    app.register_blueprint(chat_bp)

    # [수정됨] 루트 경로('/') 처리 추가
    # 프론트에서 실수로 기본 주소를 찔러봐도 200 OK를 주도록 설정
    @app.route('/', methods=['GET', 'OPTIONS'])
    def index():
        return {'status': 'OK', 'message': 'Mimi Server is running!'}, 200

    # [수정됨] 헬스 체크
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'OK', 'message': 'Server is running'}, 200

    # [추가됨] 모든 응답에 CORS 헤더 강제 주입 (가장 강력한 해결책)
    @app.after_request
    def after_request(response):
        # 허용할 출처 목록
        allowed_origins = app.config['CORS_ORIGINS']
        origin = request.headers.get('Origin')

        # 요청한 곳이 허용 목록에 있다면 헤더 추가
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)

        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # 404 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '요청한 리소스를 찾을 수 없습니다.'}, 404

    return app