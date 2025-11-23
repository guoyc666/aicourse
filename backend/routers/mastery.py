from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas_.mastery import MasteryCreate, MasteryUpdate, MasteryOut
from crud.mastery import (
    get_average_mastery, get_average_mastery_list, get_mastery, get_mastery_list, create_mastery, update_mastery
)

router = APIRouter()

@router.get("/mastery/average")
def read_average_mastery_list(db: Session = Depends(get_db)):
    avg_mastery_list = get_average_mastery_list(db)
    return avg_mastery_list

@router.get("/mastery/average/{knowledge_id}")
def read_average_mastery(knowledge_id: str, db: Session = Depends(get_db)):
    avg_mastery = get_average_mastery(db, knowledge_id)
    return {
        "knowledge_id": knowledge_id,
        "mastery": avg_mastery
    }

@router.get("/mastery/{student_id}", response_model=list[MasteryOut])
def read_mastery_list(student_id: str, db: Session = Depends(get_db)):
    return get_mastery_list(db, student_id)

@router.get("/mastery/{student_id}/{knowledge_id}", response_model=MasteryOut)
def read_mastery(student_id: str, knowledge_id: str, db: Session = Depends(get_db)):
    mastery = get_mastery(db, student_id, knowledge_id)
    if not mastery:
        raise HTTPException(status_code=404, detail="Mastery not found")
    return mastery

@router.post("/mastery", response_model=MasteryOut)
def create_mastery_api(data: MasteryCreate, db: Session = Depends(get_db)):
    return create_mastery(db, data.model_dump())

@router.put("/mastery/{student_id}/{knowledge_id}", response_model=MasteryOut)
def update_mastery_api(student_id: str, knowledge_id: str, data: MasteryUpdate, db: Session = Depends(get_db)):
    mastery = update_mastery(db, student_id, knowledge_id, data.mastery)
    if not mastery:
        raise HTTPException(status_code=404, detail="Mastery not found")
    return mastery