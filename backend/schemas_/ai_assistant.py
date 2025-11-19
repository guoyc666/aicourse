# Pydantic 模式定义
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    rag_docs: Optional[list[dict]] = None

    model_config = ConfigDict(from_attributes=True)


class ConversationCreate(BaseModel):
    title: str


# 不包含 messages 的会话摘要，用于列表/创建/重命名等场景
class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationOut(BaseModel):
    id: str
    title: str
    created_at: datetime
    messages: List[MessageOut] = []

    model_config = ConfigDict(from_attributes=True)


class MessageIn(BaseModel):
    user_input: str
