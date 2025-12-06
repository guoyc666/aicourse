from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


# 任务相关
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    student_ids: List[int]  # 要分配任务的学生ID列表


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    assigned_count: Optional[int] = 0  # 已分配的学生数量
    completed_count: Optional[int] = 0  # 已完成的学生数量

    model_config = ConfigDict(from_attributes=True)


class TaskSubmissionBase(BaseModel):
    content: Optional[str] = None
    file_path: Optional[str] = None


class TaskSubmissionCreate(TaskSubmissionBase):
    pass


class TaskSubmissionResponse(TaskSubmissionBase):
    id: int
    task_id: int
    student_id: int
    submitted_at: datetime
    score: Optional[int] = None
    feedback: Optional[str] = None
    graded_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AssignedTaskResponse(BaseModel):
    id: int
    task_id: int
    student_id: int
    created_at: datetime
    is_completed: bool
    task: TaskResponse
    submission: Optional[TaskSubmissionResponse] = None

    model_config = ConfigDict(from_attributes=True)
