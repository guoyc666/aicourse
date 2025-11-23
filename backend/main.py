from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime, timedelta
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
from models import User, Role, Permission
from auth import authenticate_user, create_access_token, get_current_user, verify_permission
from schemas import UserCreate, UserLogin, UserResponse, Token, RoleResponse, TopicResponse, ReplyResponse
from routers import auth, users, tasks, topics, ai_assistant, graph, knowledge, records, progress, mastery
from file_resources import router as file_router
from question import router as question_router

load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI辅助学习系统",
    version="1.0.0"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8080"],  # Vue开发服务器和备用端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由 
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务管理"])
app.include_router(topics.router, prefix="/api/topics", tags=["讨论区"])
app.include_router(file_router, prefix="", tags=["文件资源"])  # 注意：file_router内部已包含/api前缀
app.include_router(question_router, prefix="", tags=["题库"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["AI助手"])
app.include_router(graph.router, prefix="/api")
app.include_router(knowledge.router, prefix="/api")
app.include_router(records.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(mastery.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI辅助学习系统"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
