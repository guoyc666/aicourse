from fastapi import APIRouter, Depends, HTTPException
from neo4j import get_graph
from utils.auth import get_current_active_user,verify_permission, check_role
from models import User
from database import get_db
from sqlalchemy.orm import Session
from schemas.progress import ProgressOut, ProgressListOut, AverageProgressOut
from crud.progress import (
    get_progress,
    list_progress,
    get_progress_list,
    list_progress_list,
    get_average_progress,
    list_average_progress
)

router = APIRouter()

@router.get("/progress", response_model=ProgressOut)
def get_progress_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    # 仅供学生查看自己的进度
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized")
    progress = get_progress(db, current_user.id, knowledge_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress

@router.get("/progress/all", response_model=list[ProgressOut])
def list_progress_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 仅供学生查看自己的进度
    if not check_role(db, current_user.id, "student"):
        raise HTTPException(status_code=403, detail="Not authorized")
    progress_list = list_progress(db, current_user.id)
    if not progress_list:
        raise HTTPException(status_code=404, detail="Progress list not found")
    return progress_list

@router.get("/progress/average", response_model=AverageProgressOut)
def get_average_progress_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    avg_progress = get_average_progress(db, knowledge_id)
    if not avg_progress:
        raise HTTPException(status_code=404, detail="Average progress not found")
    return avg_progress

@router.get("/progress/average/all", response_model=list[AverageProgressOut])
def list_average_progress_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    avg_progress_list = list_average_progress(db)
    if not avg_progress_list:
        raise HTTPException(status_code=404, detail="Average progress list not found")
    return avg_progress_list

@router.get("/progress/list", response_model=list[ProgressListOut])
def get_progress_list_by_knowledge(
    knowledge_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not knowledge_id:
        raise HTTPException(status_code=400, detail="knowledge_id is required")
    # 仅供教师或管理员查看所有学生的进度列表
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    progress_list = get_progress_list(db, knowledge_id)
    if not progress_list:
        raise HTTPException(status_code=404, detail="Progress list not found")
    return progress_list

@router.get("/progress/list/all", response_model=list[ProgressListOut])
def list_progress_list_all(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 仅供教师或管理员查看所有学生的进度列表
    if not check_role(db, current_user.id, "teacher") and not check_role(db, current_user.id, "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    progress_list = list_progress_list(db)
    if not progress_list:
        raise HTTPException(status_code=404, detail="Progress list not found")
    return progress_list