from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# 角色权限相关（需要在UserResponse之前定义）
class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    resource: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: List[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: List[int] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None
