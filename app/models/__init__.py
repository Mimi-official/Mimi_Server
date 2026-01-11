from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .character import Character
from .user_progress import UserProgress
from .chat_log import ChatLog
from .character_event import CharacterEvent
from .token_blocklist import TokenBlocklist  # [추가]

# [수정] __all__ 리스트에도 추가
__all__ = ['db', 'User', 'Character', 'UserProgress', 'ChatLog', 'CharacterEvent', 'TokenBlocklist']