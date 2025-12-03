from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_active_user, check_role
from models import User
from database import get_db
from schemas_.mastery import MasteryListOut, MasteryOut, AverageMasteryOut
from crud.mastery import (
    get_average_mastery,
    list_average_mastery,
    get_mastery,
    list_mastery,
    get_mastery_list,
    list_mastery_list
)

router = APIRouter()

@router.get("/mastery/list", response_model=list[MasteryListOut])
def get_mastery_list_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    # 仅供教师或管理员查看所有学生的掌握度列表
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    mastery_list = get_mastery_list(db, knowledge_id)
    if not mastery_list:
        raise HTTPException(status_code=404, detail="Mastery list not found")
    return mastery_list

@router.get("/mastery/list/all", response_model=list[MasteryListOut])
def list_mastery_list_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 仅供教师或管理员查看所有学生的掌握度列表
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    mastery_list = list_mastery_list(db)
    if not mastery_list:
        raise HTTPException(status_code=404, detail="Mastery list not found")
    return mastery_list

@router.get("/mastery/average", response_model=AverageMasteryOut)
def get_average_mastery_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    avg_mastery = get_average_mastery(db, knowledge_id)
    if not avg_mastery:
        raise HTTPException(status_code=404, detail="Average mastery not found")
    return avg_mastery

@router.get("/mastery/average/all", response_model=list[AverageMasteryOut])
def list_average_mastery_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    avg_mastery_list = list_average_mastery(db)
    if not avg_mastery_list:
        raise HTTPException(status_code=404, detail="Average mastery list not found")
    return avg_mastery_list

@router.get("/mastery", response_model=MasteryOut)
def get_mastery_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    # 仅供学生查看自己的掌握度
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized, only students can view their own mastery")
    mastery = get_mastery(db, current_user.id, knowledge_id)
    if not mastery:
        raise HTTPException(status_code=404, detail="Mastery not found")
    return mastery

@router.get("/mastery/all", response_model=list[MasteryOut])
def list_mastery_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 仅供学生查看自己的掌握度列表
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized")
    mastery_list = list_mastery(db, current_user.id)
    if not mastery_list:
        raise HTTPException(status_code=404, detail="Mastery list not found")
    return mastery_list