from fastapi import APIRouter
from crud.knowledge import (
    create_knowledge_point,
    get_knowledge_point,
    list_knowledge_points,
    delete_knowledge_point,
)
from schemas_.knowledge import KnowledgePoint

router = APIRouter()

@router.post("/knowledge_point")
def add_knowledge_point(kp: KnowledgePoint):
    obj = create_knowledge_point(kp.id, kp.name, kp.category)
    return {"success": True, "id": obj.id}

@router.get("/knowledge_point/{id}")
def get_kp(id: str):
    obj = get_knowledge_point(id)
    if obj:
        return {
            "id": obj.id,
            "name": obj.name,
            "category": obj.category,
        }
    return {"error": "Not found"}

@router.get("/knowledge_points")
def list_kps():
    points = list_knowledge_points()
    return [
        {"id": p.id, "name": p.name, "category": p.category}
        for p in points
    ]

@router.delete("/knowledge_point/{id}")
def delete_kp(id: str):
    delete_knowledge_point(id)
    return {"success": True}