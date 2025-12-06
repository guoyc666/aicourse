from pydantic import BaseModel

class MasteryOut(BaseModel):
    mastery: float
    knowledge_id: str

class MasteryListOut(BaseModel):
    knowledge_id: str
    student_id: int
    student_name: str
    mastery: float

class AverageMasteryOut(BaseModel):
    knowledge_id: str
    average_mastery: float
    