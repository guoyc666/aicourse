from pathlib import Path
from datetime import datetime
from typing import List, Dict, Union

# 项目根目录（自动计算，无需修改）
PROJECT_ROOT = Path(__file__).parent.resolve()

# ------------------------------
# 数据库配置
# ------------------------------
class DatabaseConfig:
    HOST = "localhost"
    PORT = 3306
    NAME = "zygc"
    USER = "root"
    PASSWORD = "password"

# ------------------------------
# 存储配置
# ------------------------------
class StorageConfig:
    # 文件保存根目录（支持绝对路径和相对路径）
    UPLOAD_DIR: Path = PROJECT_ROOT / "uploads"
    
    # 是否按日期创建子目录（如: uploads/2023/10/12/）
    USE_DATE_SUBDIR: bool = True
    
    # 日期目录格式（参考Python strftime格式）
    DATE_DIR_FORMAT: str = "%Y/%m/%d"
    
    # 临时文件目录（用于分片上传等场景）
    TEMP_DIR: Path = PROJECT_ROOT / "temp_uploads"
    
    # 是否保留原始文件名（false则使用UUID生成唯一文件名）
    PRESERVE_ORIGINAL_FILENAME: bool = False
    
    @classmethod
    def get_full_upload_path(cls) -> Path:
        """获取完整的上传目录路径"""
        return cls.UPLOAD_DIR / cls.get_current_date_dir()


# ------------------------------
# 文件限制配置
# ------------------------------
class FileLimitConfig:
    # 最大文件大小（单位：字节，100MB）
    MAX_SIZE_BYTES: int = 100 * 1024 * 1024
    
    # 允许的文件MIME类型（空列表表示允许所有类型）
    ALLOWED_MIME_TYPES: List[str] = [
        # # 图片
        # "image/jpeg",
        # "image/png",
        # "image/gif",
        # # 文档
        # "application/pdf",
        # # Word
        # "application/msword",
        # "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        # # Excel
        # "application/vnd.ms-excel",
        # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    
    # 允许的文件扩展名（带点前缀）
    ALLOWED_EXTENSIONS: List[str] = [
        # ".jpg", ".jpeg", ".png", ".gif",
        # ".pdf",
        # ".doc", ".docx",
        # ".xls", ".xlsx"
    ]


# ------------------------------
# API相关配置
# ------------------------------
class ApiConfig:
    # 基础路径
    BASE_PATH: str = "/api"
    
    # 上传接口完整路径
    UPLOAD_ENDPOINT: str = f"{BASE_PATH}/resource/upload"
    
    # 下载文件的URL前缀
    DOWNLOAD_URL_PREFIX: str = f"{BASE_PATH}/resources"
    
    # 获取资源时分页默认配置
    DEFAULT_PAGE: int = 1
    DEFAULT_PAGE_SIZE: int = 20


# ------------------------------
# 日志配置
# ------------------------------
class LogConfig:
    # 日志保存路径
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    
    # 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    LOG_LEVEL: str = "INFO"
    
    # 是否记录上传文件的详细信息
    LOG_FILE_DETAILS: bool = True
    
    # 日志文件名称格式
    LOG_FILE_NAME_FORMAT: str = "upload_service_{}.log"


# ------------------------------
# 合并所有配置为一个对象，方便使用
# ------------------------------
class Config:
    storage = StorageConfig
    file_limits = FileLimitConfig
    api = ApiConfig
    log = LogConfig
    database = DatabaseConfig


# 实例化配置对象，供其他模块导入使用
config = Config()

# 确保所有目录存在
for dir_path in [
    config.storage.UPLOAD_DIR,
    config.storage.TEMP_DIR,
    config.log.LOG_DIR,
]:
    dir_path.mkdir(parents=True, exist_ok=True)
