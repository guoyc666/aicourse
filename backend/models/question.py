from sqlalchemy import Column, Integer, Text, Enum, Float
from database import Base
import enum


# 题目类型枚举
class QuestionType(str, enum.Enum):
    choice = "choice"  # 选择题
    fill = "fill"  # 填空题
    code = "code"  # 编程题


# 编程语言枚举
class CodeLanguage(str, enum.Enum):
    python = "python"  # Python
    c = "c"  # C语言
    cpp = "cpp"  # C++
    java = "java"  # Java


# 题目模型
class Question(Base):
    __tablename__ = "question"

    question_id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)  # 题目内容
    type = Column(Enum(QuestionType), nullable=False)  # 题目类型
    options = Column(Text)  # 选项（JSON格式，仅选择题使用）
    answer = Column(
        Text, nullable=False
    )  # 正确答案（对于编程题可存储参考答案说明或函数签名等）
    # 编程题测试用例（JSON格式，列表，每个元素形如 {"input": "...", "output": "..."}）
    code_examples = Column(Text)
    code_language = Column(
        Enum(CodeLanguage), default=CodeLanguage.python
    )  # 编程语言类型
    knowledge_id = Column(Text, nullable=False)  # 相关知识点ID列表（JSON格式）
    difficulty = Column(Float, default=0.5)  # 难度系数（0-1）
    answer_count = Column(Integer, default=0)  # 被答题次数
    correct_count = Column(Integer, default=0)  # 被正确回答次数
