from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

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
    
    model_config = ConfigDict(from_attributes=True)