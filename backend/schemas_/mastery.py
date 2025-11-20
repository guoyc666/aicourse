from pydantic import BaseModel

class MasteryBase(BaseModel):
    student_id: int
    knowledge_id: str
    mastery: float

class MasteryCreate(MasteryBase):
    pass

class MasteryUpdate(BaseModel):
    mastery: float

class MasteryOut(MasteryBase):
    pass