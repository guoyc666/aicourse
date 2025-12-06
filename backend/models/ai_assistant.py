# 数据模型：会话与消息
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid


class Conversation(Base):
    __tablename__ = "conversations"
    # 使用 UUID 字符串作为主键，长度 36（如 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'）
    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # 关联的消息
    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    # 与 Conversation.id 保持同样的 UUID 字符串类型
    conversation_id = Column(String(36), ForeignKey("conversations.id"), index=True)
    role = Column(String(32))  # system/user/assistant
    content = Column(Text)
    rag_docs = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
