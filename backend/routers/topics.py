from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Topic as TopicModel, Reply as ReplyModel, User as UserModel
from schemas import TopicBase, TopicCreate, TopicUpdate, TopicResponse, ReplyBase, ReplyCreate, ReplyResponse
from auth import get_current_user
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.routing import APIRoute

# 自定义路由类，确保重定向时保留认证头
class CustomAPIRoute(APIRoute):
    def __init__(self, path, endpoint, **kwargs):
        # 确保路径以斜杠结尾，避免重定向问题
        if path.endswith('/'):
            super().__init__(path, endpoint, **kwargs)
        else:
            super().__init__(path + '/', endpoint, **kwargs)

# 使用自定义路由类初始化router
router = APIRouter(route_class=CustomAPIRoute)

# 获取所有主题
def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TopicModel).offset(skip).limit(limit).all()

# 创建新主题
@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic: TopicCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_topic = TopicModel(
        title=topic.title,
        content=topic.content,
        created_by_id=current_user.id,
        is_sticky=topic.is_sticky if hasattr(topic, 'is_sticky') else False,
        is_closed=topic.is_closed if hasattr(topic, 'is_closed') else False
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    
    # 返回带创建者名称的响应
    topic_response = TopicResponse(
        id=db_topic.id,
        title=db_topic.title,
        content=db_topic.content,
        created_by_id=db_topic.created_by_id,
        created_at=db_topic.created_at,
        updated_at=db_topic.updated_at,
        is_sticky=db_topic.is_sticky,
        is_closed=db_topic.is_closed,
        created_by_name=current_user.username,
        replies_count=0  # 新创建的主题没有回复
    )
    
    return topic_response

# 获取主题列表（支持搜索）
@router.get("/", response_model=List[TopicResponse])
def read_topics(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(TopicModel)
    
    # 如果提供了搜索关键词，添加搜索条件
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            TopicModel.title.ilike(search_pattern) | 
            TopicModel.content.ilike(search_pattern)
        )
    
    # 应用分页
    topics = query.offset(skip).limit(limit).all()
    
    # 转换为响应模型
    topic_responses = []
    for topic in topics:
        # 获取创建者信息
        creator = db.query(UserModel).filter(UserModel.id == topic.created_by_id).first()
        # 获取回复数量
        replies_count = db.query(ReplyModel).filter(ReplyModel.topic_id == topic.id).count()
        
        topic_responses.append(
            TopicResponse(
                id=topic.id,
                title=topic.title,
                content=topic.content,
                created_by_id=topic.created_by_id,
                created_at=topic.created_at,
                updated_at=topic.updated_at,
                is_sticky=topic.is_sticky,
                is_closed=topic.is_closed,
                created_by_name=creator.username if creator else "Unknown",
                replies_count=replies_count
            )
        )
    
    return topic_responses

# 获取单个主题详情
@router.get("/{topic_id}", response_model=TopicResponse)
def read_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    db_topic = db.query(TopicModel).filter(TopicModel.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    
    # 获取创建者信息
    creator = db.query(UserModel).filter(UserModel.id == db_topic.created_by_id).first()
    # 获取回复数量
    replies_count = db.query(ReplyModel).filter(ReplyModel.topic_id == db_topic.id).count()
    
    return TopicResponse(
        id=db_topic.id,
        title=db_topic.title,
        content=db_topic.content,
        created_by_id=db_topic.created_by_id,
        created_at=db_topic.created_at,
        updated_at=db_topic.updated_at,
        is_sticky=db_topic.is_sticky,
        is_closed=db_topic.is_closed,
        created_by_name=creator.username if creator else "Unknown",
        replies_count=replies_count
    )

# 更新主题
@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    topic: TopicUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_topic = db.query(TopicModel).filter(TopicModel.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    
    # 检查权限：只有创建者或者管理员可以更新主题
    if db_topic.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限更新此主题")
    
    if topic.title is not None:
        db_topic.title = topic.title
    if topic.content is not None:
        db_topic.content = topic.content
    if hasattr(topic, 'is_sticky'):
        db_topic.is_sticky = topic.is_sticky
    if hasattr(topic, 'is_closed'):
        db_topic.is_closed = topic.is_closed
    
    db_topic.updated_at = datetime.now()
    db.commit()
    db.refresh(db_topic)
    
    # 获取创建者信息
    creator = db.query(UserModel).filter(UserModel.id == db_topic.created_by_id).first()
    # 获取回复数量
    replies_count = db.query(ReplyModel).filter(ReplyModel.topic_id == db_topic.id).count()
    
    return TopicResponse(
        id=db_topic.id,
        title=db_topic.title,
        content=db_topic.content,
        created_by_id=db_topic.created_by_id,
        created_at=db_topic.created_at,
        updated_at=db_topic.updated_at,
        is_sticky=db_topic.is_sticky,
        is_closed=db_topic.is_closed,
        created_by_name=creator.username if creator else "Unknown",
        replies_count=replies_count
    )

# 删除主题
@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_topic = db.query(TopicModel).filter(TopicModel.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    
    # 检查权限：只有创建者或者管理员可以删除主题
    if db_topic.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限删除此主题")
    
    # 删除所有相关回复
    db.query(ReplyModel).filter(ReplyModel.topic_id == topic_id).delete()
    # 删除主题
    db.delete(db_topic)
    db.commit()
    return None

# 获取主题的所有回复
@router.get("/{topic_id}/replies", response_model=List[ReplyResponse])
def read_topic_replies(
    topic_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # 检查主题是否存在
    db_topic = db.query(TopicModel).filter(TopicModel.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    
    replies = db.query(ReplyModel).filter(ReplyModel.topic_id == topic_id).offset(skip).limit(limit).all()
    reply_responses = []
    
    for reply in replies:
        # 获取回复者信息
        replier = db.query(UserModel).filter(UserModel.id == reply.created_by_id).first()
        
        reply_responses.append(
            ReplyResponse(
                id=reply.id,
                topic_id=reply.topic_id,
                content=reply.content,
                created_by_id=reply.created_by_id,
                created_at=reply.created_at,
                updated_at=reply.updated_at,
                created_by_name=replier.username if replier else "Unknown"
            )
        )
    
    return reply_responses

# 创建回复
@router.post("/{topic_id}/replies", response_model=ReplyResponse, status_code=status.HTTP_201_CREATED)
def create_reply(
    topic_id: int,
    reply: ReplyCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 检查主题是否存在
    db_topic = db.query(TopicModel).filter(TopicModel.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="主题不存在")
    
    # 检查主题是否已关闭
    if db_topic.is_closed:
        raise HTTPException(status_code=403, detail="主题已关闭，无法回复")
    
    db_reply = ReplyModel(
        topic_id=topic_id,
        content=reply.content,
        created_by_id=current_user.id
    )
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    
    # 返回带回复者名称的响应
    return ReplyResponse(
        id=db_reply.id,
        topic_id=db_reply.topic_id,
        content=db_reply.content,
        created_by_id=db_reply.created_by_id,
        created_at=db_reply.created_at,
        updated_at=db_reply.updated_at,
        created_by_name=current_user.username
    )

# 更新回复
@router.put("/replies/{reply_id}", response_model=ReplyResponse)
def update_reply(
    reply_id: int,
    reply: ReplyBase,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_reply = db.query(ReplyModel).filter(ReplyModel.id == reply_id).first()
    if db_reply is None:
        raise HTTPException(status_code=404, detail="回复不存在")
    
    # 检查权限：只有回复者或者管理员可以更新回复
    if db_reply.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限更新此回复")
    
    # 检查主题是否已关闭
    db_topic = db.query(TopicModel).filter(TopicModel.id == db_reply.topic_id).first()
    if db_topic and db_topic.is_closed:
        raise HTTPException(status_code=403, detail="主题已关闭，无法更新回复")
    
    db_reply.content = reply.content
    db_reply.updated_at = datetime.now()
    db.commit()
    db.refresh(db_reply)
    
    # 获取回复者信息
    replier = db.query(UserModel).filter(UserModel.id == db_reply.created_by_id).first()
    
    return ReplyResponse(
        id=db_reply.id,
        topic_id=db_reply.topic_id,
        content=db_reply.content,
        created_by_id=db_reply.created_by_id,
        created_at=db_reply.created_at,
        updated_at=db_reply.updated_at,
        created_by_name=replier.username if replier else "Unknown"
    )

# 删除回复
@router.delete("/replies/{reply_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db_reply = db.query(ReplyModel).filter(ReplyModel.id == reply_id).first()
    if db_reply is None:
        raise HTTPException(status_code=404, detail="回复不存在")
    
    # 检查权限：只有回复者或者管理员可以删除回复
    if db_reply.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权限删除此回复")
    
    db.delete(db_reply)
    db.commit()
    return None