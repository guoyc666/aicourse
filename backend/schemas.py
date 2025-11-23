from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 用户相关
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "student"  # 默认学生角色

class UserLogin(BaseModel):
    username: str
    password: str

# 角色权限相关（需要在UserResponse之前定义）
class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    resource: Optional[str]
    
    class Config:
        from_attributes = True

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: List[PermissionResponse] = []
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    roles: List[RoleResponse] = []
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

# 认证相关
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

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
    
    class Config:
        from_attributes = True

class TaskSubmissionBase(BaseModel):
    content: Optional[str] = None
    file_path: Optional[str] = None

class TaskSubmissionCreate(TaskSubmissionBase):
    pass

# 文件资源相关
class FileResourceBase(BaseModel):
    name: str
    file_path: str
    file_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None

class FileResourceCreate(FileResourceBase):
    pass

class FileResourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class FileResourceResponse(FileResourceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskSubmissionResponse(TaskSubmissionBase):
    id: int
    task_id: int
    student_id: int
    submitted_at: datetime
    score: Optional[int] = None
    feedback: Optional[str] = None
    graded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AssignedTaskResponse(BaseModel):
    id: int
    task_id: int
    student_id: int
    created_at: datetime
    is_completed: bool
    task: TaskResponse
    submission: Optional[TaskSubmissionResponse] = None
    
    class Config:
        from_attributes = True

# 讨论区相关模型
class TopicBase(BaseModel):
    title: str
    content: str
    is_sticky: Optional[bool] = False
    is_closed: Optional[bool] = False

class TopicCreate(TopicBase):
    pass

class TopicUpdate(TopicBase):
    title: Optional[str] = None
    content: Optional[str] = None

class TopicResponse(TopicBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    replies_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ReplyBase(BaseModel):
    content: str

class ReplyCreate(ReplyBase):
    pass

class ReplyResponse(ReplyBase):
    id: int
    topic_id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    
    class Config:
        from_attributes = True
