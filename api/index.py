from app import create_app
from flask_cors import CORS  # 반드시 import

app = create_app()

# Vercel이 실행하는 app 객체에 CORS 설정을 직접 주입
CORS(app,
    resources={r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "https://mimi-client.vercel.app"
        ]
    }},
    supports_credentials=True
)