from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

import schemas.ai_assistant as schemas
import models.ai_assistant as models
from models import User as UserModel
from database import get_db
from utils.auth import get_current_user
from utils.ai_client import chat_once
from utils.stream_processer import StreamProcessor

router = APIRouter()


# 创建一个新会话
@router.post(
    "/conversations", 
    response_model=schemas.ConversationSummary
)
def create_conversation(
    conv: schemas.ConversationCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new = models.Conversation(
        title=conv.title, 
        user_id=current_user.id
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


# 删除会话并级联删除消息
@router.delete("/conversations/{conv_id}")
def delete_conversation(
    conv_id: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    conv = (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conv_id)
        .first()
    )
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to delete this conversation")
    db.delete(conv)
    db.commit()
    return {"ok": True}


# 列出所有会话
@router.get(
    "/conversations", 
    response_model=list[schemas.ConversationSummary]
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    convs = (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == current_user.id)
        .order_by(models.Conversation.created_at.desc())
        .all()
    )
    return convs


# 重命名会话
@router.put(
    "/conversations/{conv_id}", 
    response_model=schemas.ConversationSummary
)
def rename_conversation(
    conv_id: str, 
    conv_: schemas.ConversationCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    conv = (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conv_id)
        .first()
    )
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to rename this conversation")
    conv.title = conv_.title
    db.commit()
    db.refresh(conv)
    return conv


# 发送消息并获取回复
@router.post("/conversations/{conv_id}/messages")
def send_message(
    conv_id: str, 
    msg: schemas.MessageIn, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    conv = (
            db.query(models.Conversation)
            .filter(models.Conversation.id == conv_id)
            .first()
        )
    print(conv)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to access this conversation")

    processor = StreamProcessor(db, conv_id, msg.user_input)
    return StreamingResponse(
        processor.generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# 获取会话的所有消息
@router.get(
    "/conversations/{conv_id}/messages", 
    response_model=schemas.ConversationOut
)
def get_messages(
    conv_id: str, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    conv = (
        db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()
    )

    if not conv or conv.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to access this conversation")
    
    return conv


@router.post("/easychat", response_model=str)
def easy_chat(msg: str):
    # 处理简易聊天逻辑
    return chat_once(msg)
