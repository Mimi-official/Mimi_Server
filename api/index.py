from app import create_app
from app.models import db

app = create_app()

if __name__ == '__main__':
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:5173", "https://너의-프론트엔드-도메인.vercel.app"]}},
         supports_credentials=True
    )
    app.run(debug=True, host='0.0.0.0', port=5000)