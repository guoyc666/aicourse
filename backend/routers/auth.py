from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User, Role
from schemas import UserCreate, UserLogin, UserResponse, Token
from utils.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, get_user_roles, ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    hashed_password = get_password_hash(user.password)
    
    # 创建用户对象 - 注意：User模型已不包含email字段
    db_user = User(
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 根据传入的角色参数分配角色，但不允许管理员角色
    allowed_roles = ["student", "teacher"]  # 允许的角色列表
    role_name = user.role if user.role and user.role.lower() in allowed_roles else "student"
    
    # 查找指定角色
    target_role = db.query(Role).filter(Role.name == role_name).first()
    if target_role:
        from models import UserRole
        user_role = UserRole(user_id=db_user.id, role_id=target_role.id)
        db.add(user_role)
        db.commit()
    
    # 获取用户角色信息
    roles = get_user_roles(db, db_user.id)
    db_user.roles = roles
    
    return db_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # 获取用户角色信息
    roles = get_user_roles(db, user.id)
    user.roles = roles
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """获取当前用户信息"""
    roles = get_user_roles(db, current_user.id)
    current_user.roles = roles
    return current_user

@router.post("/logout")
async def logout():
    """用户登出"""
    return {"message": "登出成功"}
