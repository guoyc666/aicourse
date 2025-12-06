from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from models import User, Task, AssignedTask, TaskSubmission
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    TaskSubmissionCreate, TaskSubmissionResponse,
    AssignedTaskResponse
)
from utils.auth import get_current_active_user, verify_permission, verify_role

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新任务（教师权限）"""
    # 检查是否为教师或管理员角色
    is_teacher_or_admin = False
    for role in current_user.user_roles:
        if role.role.name in ["teacher", "admin"]:
            is_teacher_or_admin = True
            break
    
    if not is_teacher_or_admin:
        raise HTTPException(status_code=403, detail="需要教师或管理员权限")
    
    # 创建任务
    db_task = Task(
        title=task.title,
        description=task.description,
        created_by_id=current_user.id,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # 分配任务给指定学生
    for student_id in task.student_ids:
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail=f"学生ID {student_id} 不存在")
        
        # 检查学生角色
        is_student = False
        for role in student.user_roles:
            if role.role.name == "student":
                is_student = True
                break
        
        if not is_student:
            raise HTTPException(status_code=400, detail=f"用户ID {student_id} 不是学生")
        
        assigned_task = AssignedTask(
            task_id=db_task.id,
            student_id=student_id
        )
        db.add(assigned_task)
    
    db.commit()
    
    # 统计已分配数量
    assigned_count = db.query(AssignedTask).filter(AssignedTask.task_id == db_task.id).count()
    db_task.assigned_count = assigned_count
    db_task.completed_count = 0
    
    return db_task

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取任务列表
    - 教师：获取自己创建的所有任务
    - 学生：获取分配给自己的所有任务
    """
    # 检查用户角色
    is_teacher_or_admin = False
    for role in current_user.user_roles:
        if role.role.name in ["teacher", "admin"]:
            is_teacher_or_admin = True
            break
    
    if is_teacher_or_admin:
        if role.role.name == "admin":
            # 管理员查看所有任务
            tasks = db.query(Task).offset(skip).limit(limit).all()
        else:
            # 教师查看自己创建的任务
            tasks = db.query(Task).filter(Task.created_by_id == current_user.id).offset(skip).limit(limit).all()
    else:
        # 学生查看分配给自己的任务
        assigned_task_ids = db.query(AssignedTask.task_id).filter(AssignedTask.student_id == current_user.id).all()
        task_ids = [at[0] for at in assigned_task_ids]
        tasks = db.query(Task).filter(Task.id.in_(task_ids)).offset(skip).limit(limit).all()
    
    # 为每个任务添加统计信息
    for task in tasks:
        assigned_count = db.query(AssignedTask).filter(AssignedTask.task_id == task.id).count()
        completed_count = db.query(AssignedTask).filter(
            AssignedTask.task_id == task.id, 
            AssignedTask.is_completed == True
        ).count()
        task.assigned_count = assigned_count
        task.completed_count = completed_count
    
    return tasks

@router.get("/assigned/", response_model=List[AssignedTaskResponse])
async def get_assigned_tasks(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取分配给当前用户的任务（学生功能）"""
    # 学生只能查看自己的任务
    assigned_tasks = db.query(AssignedTask).filter(AssignedTask.student_id == current_user.id).all()
    
    # 为每个任务分配关联的任务详情和提交信息
    for at in assigned_tasks:
        # 获取任务详情
        task = db.query(Task).filter(Task.id == at.task_id).first()
        assigned_count = db.query(AssignedTask).filter(AssignedTask.task_id == task.id).count()
        completed_count = db.query(AssignedTask).filter(
            AssignedTask.task_id == task.id, 
            AssignedTask.is_completed == True
        ).count()
        task.assigned_count = assigned_count
        task.completed_count = completed_count
        at.task = task
        
        # 获取提交信息
        submission = db.query(TaskSubmission).filter(
            TaskSubmission.task_id == at.task_id, 
            TaskSubmission.student_id == current_user.id
        ).first()
        at.submission = submission
    
    return assigned_tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取任务详情"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 检查权限
    is_teacher_or_admin = False
    is_admin = False
    for role in current_user.user_roles:
        if role.role.name == "admin":
            is_admin = True
            is_teacher_or_admin = True
            break
        elif role.role.name == "teacher":
            is_teacher_or_admin = True
            break
    
    # 管理员可以查看所有任务
    # 教师只能查看自己创建的任务
    # 学生只能查看分配给自己的任务
    if is_admin:
        # 管理员可以访问所有任务
        pass
    elif is_teacher_or_admin:
        if task.created_by_id != current_user.id:
            raise HTTPException(status_code=403, detail="无权访问此任务")
    else:
        assigned_task = db.query(AssignedTask).filter(
            AssignedTask.task_id == task_id, 
            AssignedTask.student_id == current_user.id
        ).first()
        if not assigned_task:
            raise HTTPException(status_code=403, detail="此任务未分配给你")
    
    # 添加统计信息
    assigned_count = db.query(AssignedTask).filter(AssignedTask.task_id == task.id).count()
    completed_count = db.query(AssignedTask).filter(
        AssignedTask.task_id == task.id, 
        AssignedTask.is_completed == True
    ).count()
    task.assigned_count = assigned_count
    task.completed_count = completed_count
    
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新任务（教师权限）"""
    # 检查是否为教师或管理员角色
    is_teacher_or_admin = False
    is_admin = False
    for role in current_user.user_roles:
        if role.role.name == "admin":
            is_admin = True
            is_teacher_or_admin = True
            break
        elif role.role.name == "teacher":
            is_teacher_or_admin = True
            break
    
    if not is_teacher_or_admin:
        raise HTTPException(status_code=403, detail="需要教师或管理员权限")
    
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 只有创建者或管理员可以更新任务
    if not is_admin and db_task.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能更新自己创建的任务")
    
    # 更新任务字段
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.due_date is not None:
        db_task.due_date = task_update.due_date
    db_task.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_task)
    
    # 添加统计信息
    assigned_count = db.query(AssignedTask).filter(AssignedTask.task_id == db_task.id).count()
    completed_count = db.query(AssignedTask).filter(
        AssignedTask.task_id == db_task.id, 
        AssignedTask.is_completed == True
    ).count()
    db_task.assigned_count = assigned_count
    db_task.completed_count = completed_count
    
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除任务（教师权限）"""
    # 检查是否为教师或管理员角色
    is_teacher_or_admin = False
    is_admin = False
    for role in current_user.user_roles:
        if role.role.name == "admin":
            is_admin = True
            is_teacher_or_admin = True
            break
        elif role.role.name == "teacher":
            is_teacher_or_admin = True
            break
    
    if not is_teacher_or_admin:
        raise HTTPException(status_code=403, detail="需要教师或管理员权限")
    
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 只有创建者或管理员可以删除任务
    if not is_admin and db_task.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能删除自己创建的任务")
    
    db.delete(db_task)
    db.commit()
    
    return {"message": "任务删除成功"}

@router.post("/assigned/{assigned_task_id}/complete/")
async def complete_assigned_task(
    assigned_task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """确认任务完成（学生功能）"""
    # 检查用户是否为学生角色
    is_student = False
    for role in current_user.user_roles:
        if role.role.name == "student":
            is_student = True
            break
    
    if not is_student:
        raise HTTPException(status_code=403, detail="只有学生可以确认任务完成")
    
    # 获取分配任务
    assigned_task = db.query(AssignedTask).filter(
        AssignedTask.id == assigned_task_id,
        AssignedTask.student_id == current_user.id
    ).first()
    
    if not assigned_task:
        raise HTTPException(status_code=404, detail="分配任务不存在或不属于你")
    
    # 检查任务是否已完成
    if assigned_task.is_completed:
        raise HTTPException(status_code=400, detail="任务已完成，无需重复确认")
    
    # 标记任务为已完成
    assigned_task.is_completed = True
    assigned_task.completed_at = datetime.now()
    
    db.commit()
    db.refresh(assigned_task)
    
    # 更新任务的完成数量统计
    task = db.query(Task).filter(Task.id == assigned_task.task_id).first()
    if task:
        completed_count = db.query(AssignedTask).filter(
            AssignedTask.task_id == task.id,
            AssignedTask.is_completed == True
        ).count()
        task.completed_count = completed_count
        db.commit()
    
    return {"message": "任务确认完成成功"}