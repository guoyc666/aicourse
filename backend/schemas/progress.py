from pydantic import BaseModel

class ProgressOut(BaseModel):
    knowledge_id: str
    progress: float

class ProgressListOut(BaseModel):
    knowledge_id: str
    student_id: int
    student_name: str
    progress: float

class AverageProgressOut(BaseModel):
    knowledge_id: str
    average_progress: float