from pydantic import BaseModel

class KnowledgePoint(BaseModel):
    id: str
    name: str
    category: str