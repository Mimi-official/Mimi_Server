from flask import Flask, request
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
from app.models import db
from app.swagger_config import swagger_config, swagger_template


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. CORS 설정 최적화
    # - resources: 모든 경로(/*)에 대해 설정
    # - origins: 허용할 주소 (리스트 형태 권장)
    # - methods: OPTIONS를 반드시 포함해야 Preflight 에러가 안 납니다.
    CORS(app,
         resources={r"/*": {
             "origins": app.config.get('CORS_ORIGINS', ["http://localhost:5173"]),
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"]
         }},
         supports_credentials=True)

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

    # 2. [중요] 모든 OPTIONS 요청에 대해 200 OK 응답 강제 (Preflight 해결)
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            return {}, 200

    @app.route('/', methods=['GET'])
    def index():
        return {'status': 'OK', 'message': 'Mimi Server is running!'}, 200

    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'OK', 'message': 'Server is running'}, 200

    # 3. 기존의 @app.after_request는 지우거나 주석 처리하세요.
    # flask-cors 설정과 충돌하여 헤더가 중복되거나 누락될 수 있습니다.

    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '요청한 리소스를 찾을 수 없습니다.'}, 404

    return app