from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .character import Character
from .user_progress import UserProgress
from .chat_log import ChatLog
from .character_event import CharacterEvent

__all__ = ['db', 'User', 'Character', 'UserProgress', 'ChatLog', 'CharacterEvent']