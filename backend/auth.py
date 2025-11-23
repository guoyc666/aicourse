from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from database import get_db
from models import User, Role, Permission, UserRole, RolePermission
from schemas import TokenData
import os

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 使用pbkdf2_sha256替代bcrypt，避免版本兼容性问题
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# 确保tokenUrl与实际的login路由路径完全匹配
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/")

def verify_password(plain_password, hashed_password):
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """生成密码哈希"""
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    """验证用户身份"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    print(f"[认证日志] 收到的token前20字符: {token[:20] if token else '无'}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        if not token:
            print("[认证日志] 未提供token")
            raise credentials_exception
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("[认证日志] token解码成功")
        
        username: str = payload.get("sub")
        print(f"[认证日志] 从token中提取的用户名: {username}")
        
        if username is None:
            print("[认证日志] token中未找到用户名")
            raise credentials_exception
        
        token_data = TokenData(username=username)
        
        # 检查令牌是否过期
        exp = payload.get("exp")
        if exp:
            from datetime import datetime
            now = datetime.utcnow().timestamp()
            if exp < now:
                print("[认证日志] token已过期")
                raise credentials_exception
            else:
                print(f"[认证日志] token有效期还剩: {(exp - now)/60:.1f}分钟")
    except JWTError as e:
        print(f"[认证日志] JWT解码错误: {str(e)}")
        raise credentials_exception
    
    # 确保使用正确导入的User模型
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        print(f"[认证日志] 未找到用户: {token_data.username}")
        raise credentials_exception
    
    print(f"[认证日志] 用户验证成功: {user.username}")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_user_roles(db: Session, user_id: int) -> List[Role]:
    """获取用户角色"""
    return db.query(Role).join(UserRole).filter(UserRole.user_id == user_id).all()

def get_user_permissions(db: Session, user_id: int) -> List[Permission]:
    """获取用户权限"""
    # 使用更明确的连接方式
    return db.query(Permission).\
        join(RolePermission, Permission.id == RolePermission.permission_id).\
        join(UserRole, RolePermission.role_id == UserRole.role_id).\
        filter(UserRole.user_id == user_id).\
        all()

def has_permission(db: Session, user_id: int, permission_name: str) -> bool:
    """检查用户是否有特定权限"""
    permissions = get_user_permissions(db, user_id)
    return any(perm.name == permission_name for perm in permissions)

def verify_permission(db: Session, user_id: int, permission_name: str):
    """验证用户权限，没有权限则抛出异常"""
    if not has_permission(db, user_id, permission_name):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

def check_role(db: Session, user_id: int, role_name: str) -> bool:
    """检查用户是否有特定角色"""
    roles = get_user_roles(db, user_id)
    return any(role.name == role_name for role in roles)

def verify_role(db: Session, user_id: int, role_name: str):
    """验证用户角色，没有角色则抛出异常"""
    if not check_role(db, user_id, role_name):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {role_name} role"
        )

# 角色权限装饰器
def require_permission(permission_name: str):
    """权限检查装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            if db and current_user:
                verify_permission(db, current_user.id, permission_name)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_role(role_name: str):
    """角色检查装饰器"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            db = kwargs.get('db')
            current_user = kwargs.get('current_user')
            if db and current_user:
                verify_role(db, current_user.id, role_name)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
