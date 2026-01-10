from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from app.config import Config
from app.models import db
from app.swagger_config import swagger_config, swagger_template


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # CORS 설정
    CORS(app, origins=app.config['CORS_ORIGINS'])

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

    # 헬스 체크
    @app.route('/health')
    def health():
        return {'status': 'OK', 'message': 'Server is running'}, 200

    # 404 핸들러
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '요청한 리소스를 찾을 수 없습니다.'}, 404

    # 500 핸들러
    @app.errorhandler(500)
    def internal_error(error):
        return {'success': False, 'message': '서버 내부 오류가 발생했습니다.'}, 500

    return app