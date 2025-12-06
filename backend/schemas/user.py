from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from schemas.role import RoleResponse


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


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    roles: List[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
