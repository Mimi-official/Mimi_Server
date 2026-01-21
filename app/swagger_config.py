"""
Swagger 설정
"""
import os

is_production = os.getenv('FLASK_ENV') == 'production'

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "AI 캐릭터 채팅 API",
        "description": "선택지 기반 인터랙티브 스토리 형식의 AI 캐릭터 채팅 서비스 API 문서",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@example.com"
        }
    },
    "host": "mimi-server.vercel.app" if is_production else "localhost:5000",
    "basePath": "/",
    "schemes": ["https"] if is_production else ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT 토큰을 입력하세요. 형식: 'Bearer {token}'"
        }
    }
}