from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# 任务模型
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    created_user = relationship("User", foreign_keys=[created_by_id])
    assigned_tasks = relationship(
        "AssignedTask", back_populates="task", cascade="all, delete-orphan"
    )
    submissions = relationship(
        "TaskSubmission", back_populates="task", cascade="all, delete-orphan"
    )


# 任务分配模型
class AssignedTask(Base):
    __tablename__ = "assigned_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_completed = Column(Boolean, default=False)

    # 关联关系
    task = relationship("Task", back_populates="assigned_tasks")
    student = relationship("User")


# 任务提交模型
class TaskSubmission(Base):
    __tablename__ = "task_submissions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    grade = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    task = relationship("Task", back_populates="submissions")
    student = relationship("User")
