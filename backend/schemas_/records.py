from pydantic import BaseModel
from typing import List
from datetime import datetime

class LearningRecordCreate(BaseModel):
    student_id: int
    resource_id: str
    status: int
    total_time: int
    page_times: List[int]

class LearningRecord(LearningRecordCreate):
    id: int
    timestamp: datetime

class StudyTimeOut(BaseModel):
    study_time: float
    knowledge_id: str

class AverageStudyTimeOut(BaseModel):
    knowledge_id: str
    average_study_time: float

class StudyTimeListOut(BaseModel):
    knowledge_id: str
    study_time: float
    student_id: int
    student_name: str