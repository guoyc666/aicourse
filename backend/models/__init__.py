from .user import (
    User,
    Role,
    Permission,
    UserRole,
    RolePermission,
)
from .topic import Topic, Reply
from .task import Task, AssignedTask, TaskSubmission
from .record import LearningRecord, QuestionRecord, Mastery
from .question import Question, QuestionType, CodeLanguage
from .file import FileResource
from .ai_assistant import Conversation, Message

from database import Base

__all__ = [
    "Base",
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "Topic",
    "Reply",
    "Task",
    "AssignedTask",
    "TaskSubmission",
    "LearningRecord",
    "QuestionRecord",
    "Mastery",
    "Question",
    "QuestionType",
    "CodeLanguage",
    "FileResource",
    "Conversation",
    "Message",
]
