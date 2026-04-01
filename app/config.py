import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # Database (Vercel Neon PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('FLASK_ENV') == 'development'

    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRES_IN_DAYS = 7

    # Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

    # CORS
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "https://mimi-client.vercel.app", "https://mirim-mimi.vercel.app"]

    #STATIC
    STATIC_URL = '/static/'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

    # 배포 시 파일들이 모이는 곳 (Vercel 빌드용)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')