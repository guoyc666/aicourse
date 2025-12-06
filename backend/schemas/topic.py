from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)
