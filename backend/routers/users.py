from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Role, Permission, UserRole, RolePermission
from schemas import (
    UserResponse, UserUpdate, RoleResponse, RoleCreate, RoleUpdate,
    PermissionResponse
)
from auth import (
    get_current_active_user, verify_permission, verify_role,
    get_password_hash, get_user_roles
)

router = APIRouter()

@router.get("/students/", response_model=List[dict])
async def get_all_students(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取所有学生列表，返回{id, name}
    需要有user:read权限
    """
    #verify_permission(db, current_user.id, "user:read")
    # 查询学生角色id
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        raise HTTPException(status_code=404, detail="学生角色不存在")
    # 查询所有拥有学生角色的用户
    student_ids = db.query(UserRole.user_id).filter(UserRole.role_id == student_role.id).subquery()
    students = db.query(User).filter(User.id.in_(student_ids)).all()
    return [{"id": stu.id, "name": stu.full_name} for stu in students]

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    keyword: str = None,
    role_id: int = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 检查权限
    verify_permission(db, current_user.id, "user:read")
    
    # 基础查询
    query = db.query(User)
    
    # 添加搜索条件
    if keyword:
        query = query.filter(User.username.ilike(f"%{keyword}%"))
    
    # 添加角色筛选条件
    if role_id:
        query = query.join(UserRole).filter(UserRole.role_id == role_id)
    
    # 执行查询并分页
    users = query.offset(skip).limit(limit).all()
    
    # 获取每个用户的角色信息
    for user in users:
        user.roles = get_user_roles(db, user.id)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取特定用户信息"""
    # 只能查看自己的信息，除非有管理员权限
    if current_user.id != user_id:
        verify_permission(db, current_user.id, "user:read")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user.roles = get_user_roles(db, user.id)
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    # 只能更新自己的信息，除非有管理员权限
    if current_user.id != user_id:
        verify_permission(db, current_user.id, "user:update")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新字段
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(user)
    
    user.roles = get_user_roles(db, user.id)
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除用户（需要管理员权限）"""
    verify_permission(db, current_user.id, "user:delete")
    
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(user)
    db.commit()
    return {"message": "用户删除成功"}

# 角色管理
@router.get("/roles/", response_model=List[RoleResponse])
async def get_roles(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取角色列表（需要管理员权限）"""
    verify_permission(db, current_user.id, "role:read")
    
    roles = db.query(Role).all()
    for role in roles:
        permissions = db.query(Permission).join(RolePermission).filter(
            RolePermission.role_id == role.id
        ).all()
        role.permissions = permissions
    return roles

@router.post("/roles/", response_model=RoleResponse)
async def create_role(
    role: RoleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建角色（需要管理员权限）"""
    verify_permission(db, current_user.id, "role:create")
    
    # 检查角色名是否已存在
    if db.query(Role).filter(Role.name == role.name).first():
        raise HTTPException(status_code=400, detail="角色名已存在")
    
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    # 分配权限
    for permission_id in role.permission_ids:
        role_permission = RolePermission(role_id=db_role.id, permission_id=permission_id)
        db.add(role_permission)
    
    db.commit()
    
    # 获取权限信息
    permissions = db.query(Permission).join(RolePermission).filter(
        RolePermission.role_id == db_role.id
    ).all()
    db_role.permissions = permissions
    
    return db_role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新角色（需要管理员权限）"""
    verify_permission(db, current_user.id, "role:update")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    if role_update.name is not None:
        # 检查角色名是否已存在
        existing_role = db.query(Role).filter(
            Role.name == role_update.name,
            Role.id != role_id
        ).first()
        if existing_role:
            raise HTTPException(status_code=400, detail="角色名已存在")
        role.name = role_update.name
    
    if role_update.description is not None:
        role.description = role_update.description
    
    # 更新权限
    if role_update.permission_ids is not None:
        # 删除现有权限
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        # 添加新权限
        for permission_id in role_update.permission_ids:
            role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
            db.add(role_permission)
    
    db.commit()
    db.refresh(role)
    
    # 获取权限信息
    permissions = db.query(Permission).join(RolePermission).filter(
        RolePermission.role_id == role.id
    ).all()
    role.permissions = permissions
    
    return role

@router.delete("/roles/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除角色（需要管理员权限）"""
    verify_permission(db, current_user.id, "role:delete")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查是否有用户使用此角色
    user_count = db.query(UserRole).filter(UserRole.role_id == role_id).count()
    if user_count > 0:
        raise HTTPException(status_code=400, detail="该角色正在被用户使用，无法删除")
    
    db.delete(role)
    db.commit()
    return {"message": "角色删除成功"}

# 权限管理
@router.get("/permissions/", response_model=List[PermissionResponse])
async def get_permissions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取权限列表（需要管理员权限）"""
    verify_permission(db, current_user.id, "permission:read")
    
    return db.query(Permission).all()

# 用户角色分配
@router.post("/{user_id}/roles/{role_id}")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """为用户分配角色（需要管理员权限）"""
    verify_permission(db, current_user.id, "user:assign_role")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查是否已经分配
    existing = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户已拥有该角色")
    
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    
    return {"message": "角色分配成功"}

@router.delete("/{user_id}/roles/{role_id}")
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """移除用户角色（需要管理员权限）"""
    verify_permission(db, current_user.id, "user:remove_role")
    
    user_role = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="用户角色关系不存在")
    
    db.delete(user_role)
    db.commit()
    
    return {"message": "角色移除成功"}
