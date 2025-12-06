import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from dotenv import load_dotenv

from database import engine, Base
from routers import auth, users, tasks, topics, ai_assistant, graph, records, progress, mastery, question, file_resources

load_dotenv()

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=os.getenv("APP_NAME", "AI辅助学习系统"),
    version=os.getenv("APP_VERSION", "1.0.0")
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:80", 
    "http://frontend:80", "http://frontend:3000"],  # Vue开发服务器和备用端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由 
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务管理"])
app.include_router(topics.router, prefix="/api/topics", tags=["讨论区"])
app.include_router(file_resources.router, prefix="/api", tags=["文件资源"])
app.include_router(question.router, prefix="/api/question", tags=["题库"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["AI助手"])
app.include_router(graph.router, prefix="/api", tags=["知识图谱"])
app.include_router(records.router, prefix="/api", tags=["学习记录"])
app.include_router(progress.router, prefix="/api", tags=["学习进度"])
app.include_router(mastery.router, prefix="/api", tags=["知识掌握度"])

@app.get("/")
async def root():
    return {"message": "AI辅助学习系统"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
