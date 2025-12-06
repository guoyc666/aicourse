from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# 讨论区主题模型
class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_sticky = Column(Boolean, default=False)  # 是否置顶
    is_closed = Column(Boolean, default=False)  # 是否关闭

    # 关联关系
    created_user = relationship("User", foreign_keys=[created_by_id])
    replies = relationship(
        "Reply", back_populates="topic", cascade="all, delete-orphan"
    )


# 讨论区回复模型
class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    content = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    topic = relationship("Topic", back_populates="replies")
    created_user = relationship("User", foreign_keys=[created_by_id])
