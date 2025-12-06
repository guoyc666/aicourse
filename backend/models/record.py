from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from database import Base


# 学习记录模型
class LearningRecord(Base):
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    resource_id = Column(
        String(64), ForeignKey("file_resources.file_id"), nullable=False
    )
    status = Column(Integer, nullable=False)
    total_time = Column(Integer, nullable=False)
    page_times = Column(Text)
    timestamp = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )  # 最后更新时间


# 答题记录模型
class QuestionRecord(Base):
    __tablename__ = "question_record"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # 学生ID
    submit_time = Column(DateTime(timezone=True), server_default=func.now())  # 提交时间
    duration = Column(Integer, nullable=False)  # 答题用时（秒）
    accuracy = Column(Float, nullable=False)  # 正确率
    knowledge_id = Column(Text, nullable=False)  # 涉及知识点ID列表（JSON格式）
    detail = Column(Text, nullable=False)  # 答题详情（JSON格式）
    total_questions = Column(Integer, nullable=False)  # 题目数量


class Mastery(Base):
    __tablename__ = "mastery"

    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    knowledge_id = Column(String(64), primary_key=True)
    mastery = Column(Float, nullable=False)
