from pydantic import BaseModel
from typing import Optional

# 认证相关
from schemas.user import UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None
