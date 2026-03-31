import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'ai_character_chat')
    DB_PORT = os.getenv('DB_PORT', '3306')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'

    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRES_IN_DAYS = 7

    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "https://mimi-client.vercel.app"]

    #STATIC
    STATIC_URL = '/static/'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    # 배포 시 파일들이 모이는 곳 (Vercel 빌드용)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')