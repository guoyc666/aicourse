from pydantic import BaseModel
from typing import List
from datetime import datetime

class LearningRecordCreate(BaseModel):
    student_id: int
    resource_id: str
    status: int
    total_time: int
    page_times: List[int]
    timestamp: datetime

class LearningRecord(LearningRecordCreate):
    id: int