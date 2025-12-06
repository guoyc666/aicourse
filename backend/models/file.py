from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# 文件资源模型
class FileResource(Base):
    __tablename__ = "file_resources"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(255), unique=True, nullable=False, index=True)
    original_name = Column(String(255), nullable=False)
    unique_filename = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text, nullable=True)
    size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    storage_path = Column(String(500), nullable=False)
    relative_path = Column(String(500), nullable=False)
    download_url = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # 关联关系
    uploader = relationship("User")
