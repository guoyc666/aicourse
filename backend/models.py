from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    user_roles = relationship("UserRole", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    user_roles = relationship("UserRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    resource = Column(String(50))  # 资源类型：user, role, permission
    
    # 关联关系
    role_permissions = relationship("RolePermission", back_populates="permission")

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    
    # 关联关系
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")

# 任务模型
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    created_user = relationship("User", foreign_keys=[created_by_id])
    assigned_tasks = relationship("AssignedTask", back_populates="task", cascade="all, delete-orphan")
    submissions = relationship("TaskSubmission", back_populates="task", cascade="all, delete-orphan")

# 任务分配模型
class AssignedTask(Base):
    __tablename__ = "assigned_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_completed = Column(Boolean, default=False)
    
    # 关联关系
    task = relationship("Task", back_populates="assigned_tasks")
    student = relationship("User")

# 任务提交模型
class TaskSubmission(Base):
    __tablename__ = "task_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    grade = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    task = relationship("Task", back_populates="submissions")
    student = relationship("User")

# 讨论区主题模型
class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_sticky = Column(Boolean, default=False)  # 是否置顶
    is_closed = Column(Boolean, default=False)  # 是否关闭
    
    # 关联关系
    created_user = relationship("User", foreign_keys=[created_by_id])
    replies = relationship("Reply", back_populates="topic", cascade="all, delete-orphan")

# 讨论区回复模型
class Reply(Base):
    __tablename__ = "replies"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    content = Column(Text, nullable=False)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联关系
    topic = relationship("Topic", back_populates="replies")
    created_user = relationship("User", foreign_keys=[created_by_id])

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
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    uploader = relationship("User")

# 导入enum支持题目类型枚举
from sqlalchemy import Enum
import enum

# 题目类型枚举
class QuestionType(str, enum.Enum):
    choice = "choice"  # 选择题
    fill = "fill"      # 填空题
    code = "code"      # 编程题

# 编程语言枚举
class CodeLanguage(str, enum.Enum):
    python = "python"      # Python
    c = "c"               # C语言
    cpp = "cpp"           # C++
    java = "java"         # Java

# 题目模型
class Question(Base):
    __tablename__ = "question"
    
    question_id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # 题目内容
    type = Column(Enum(QuestionType), nullable=False)  # 题目类型
    options = Column(Text)  # 选项（JSON格式，仅选择题使用）
    answer = Column(Text, nullable=False)  # 正确答案（对于编程题可存储参考答案说明或函数签名等）
    # 编程题测试用例（JSON格式，列表，每个元素形如 {"input": "...", "output": "..."}）
    code_examples = Column(Text)  
    code_language = Column(Enum(CodeLanguage), default=CodeLanguage.python)  # 编程语言类型
    knowledge_id = Column(Text, nullable=False)  # 相关知识点ID列表（JSON格式）
    difficulty = Column(Float, default=0.5)  # 难度系数（0-1）
    answer_count = Column(Integer, default=0)  # 被答题次数
    correct_count = Column(Integer, default=0)  # 被正确回答次数

# 学习记录模型
class LearningRecord(Base):
    __tablename__ = "learning_record"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # 学生ID（关联users表id）
    knowledge_id = Column(String(100), nullable=False)  # 知识点节点ID
    progress = Column(Float, default=0.0)  # 掌握度（0~1）
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())  # 最后更新时间

# 答题记录模型
class QuestionRecord(Base):
    __tablename__ = "question_record"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # 学生ID
    submit_time = Column(DateTime(timezone=True), server_default=func.now())  # 提交时间
    duration = Column(Integer, nullable=False)  # 答题用时（秒）
    accuracy = Column(Float, nullable=False)  # 正确率
    knowledge_id = Column(Text, nullable=False)  # 涉及知识点ID列表（JSON格式）
    detail = Column(Text, nullable=False)  # 答题详情（JSON格式）
    total_questions = Column(Integer, nullable=False)  # 题目数量
