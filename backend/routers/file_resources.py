import os
import magic  # pip install python-magic-bin
import uuid
import urllib.parse
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from database import get_db
from models import FileResource, User
from auth import get_current_user
from schemas import FileResourceResponse
from config import config  # 导入配置对象

# 创建路由对象
router = APIRouter()

# 1.资源上传接口
def get_unique_filename(original_filename: str) -> str:
    """生成唯一文件名"""
    if config.storage.PRESERVE_ORIGINAL_FILENAME and original_filename:
        # 保留原始文件名，添加UUID前缀避免冲突
        file_extension = Path(original_filename).suffix.lower()
        filename_without_ext = Path(original_filename).stem
        return f"{filename_without_ext}_{uuid.uuid4().hex[:8]}{file_extension}"
    else:
        # 完全使用UUID生成文件名
        file_extension = Path(original_filename).suffix.lower() if original_filename else ""
        return f"{uuid.uuid4().hex}{file_extension}"

def verify_file_type(file_path: str) -> bool:
    """验证文件MIME类型是否在允许列表中"""
    if not config.file_limits.ALLOWED_MIME_TYPES:
        return True  # 允许所有类型
    
    file_mime = magic.from_file(file_path, mime=True)
    return file_mime in config.file_limits.ALLOWED_MIME_TYPES

def verify_file_extension(filename: str) -> bool:
    """验证文件扩展名是否在允许列表中"""
    if not config.file_limits.ALLOWED_EXTENSIONS:
        return True  # 允许所有扩展名
    
    file_extension = Path(filename).suffix.lower()
    return file_extension in config.file_limits.ALLOWED_EXTENSIONS

def _analyze_file_task(
    filename: str,
    filepath: str,
    fileid: str,
    file_type: str,
    download_url: str
):
    """后台任务：解析文件并存入向量数据库"""
    from utils.parse_file import analyse_file  # 延迟导入，避免循环依赖
    file_type = Path(filepath).suffix.lower().lstrip(".")
    analyse_file(
        filename=filename,
        filepath=filepath,
        fileid=fileid,
        file_type=file_type,
        download_url=download_url,
    )

@router.post("/resource/upload", summary="上传资源文件")
async def upload_resource(
    file: UploadFile = File(...),
    title: str = Form(..., description="文件标题"),
    type: str = Form(..., description="文件类型分类"),
    description: Optional[str] = Form(None, description="资源详细描述（可选）"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # 1. 验证文件扩展名
    if not verify_file_extension(file.filename):
        allowed_exts = ", ".join(config.file_limits.ALLOWED_EXTENSIONS)
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"不支持的文件扩展名，允许的扩展名：{allowed_exts}"
        )
    
    # 2. 检查文件大小
    try:
        file_content = await file.read()  # 一次性读取文件内容
        file_size = len(file_content)
        
        if file_size > config.file_limits.MAX_SIZE_BYTES:
            max_size_mb = config.file_limits.MAX_SIZE_BYTES / 1024 / 1024
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件过大，最大允许 {max_size_mb:.2f} MB"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"读取文件内容失败: {str(e)}"
        )
    
    # 3. 准备存储路径
    upload_dir = config.storage.UPLOAD_DIR
    upload_dir.mkdir(parents=True, exist_ok=True)  # 确保目录存在
    
    # 4. 生成文件名并保存文件
    unique_filename = get_unique_filename(file.filename)
    file_path = upload_dir / unique_filename
    
    try:
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # 5. 验证文件真实类型
        if not verify_file_type(str(file_path)):
            os.remove(file_path)  # 删除不符合要求的文件
            allowed_types = ", ".join(config.file_limits.ALLOWED_MIME_TYPES)
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"不支持的文件类型，允许的类型：{allowed_types}"
            )
        
        # 生成文件信息
        file_id = uuid.uuid4().hex
        file_mime = magic.from_file(str(file_path), mime=True)
        download_url = f"{config.api.DOWNLOAD_URL_PREFIX}/{file_path.relative_to(config.storage.UPLOAD_DIR)}"
        
        # 保存到数据库
        db_file = FileResource(
            file_id=file_id,
            original_name=file.filename,
            unique_filename=unique_filename,
            title=title,
            type=type,
            uploader_id=current_user.id,
            description=description,
            size=file_size,
            mime_type=file_mime,
            storage_path=str(file_path),
            relative_path=str(file_path.relative_to(config.storage.UPLOAD_DIR)),
            download_url=download_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        
        # 构建返回数据
        file_info = {
            "file_id": file_id,
            "original_name": file.filename,
            "unique_filename": unique_filename,
            "title": title,
            "type": type,
            "uploader": current_user.username,
            "description": description,
            "size": file_size,
            "mime_type": file_mime,
            "upload_time": datetime.now().isoformat(),
            "storage_path": str(file_path),
            "relative_path": str(file_path.relative_to(config.storage.UPLOAD_DIR)),
            "download_url": download_url
        }
        

        background_tasks.add_task(
            _analyze_file_task,
            filename=title,
            filepath=str(file_path),
            fileid=file_id,
            file_type=type,
            download_url=download_url,
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "文件上传成功",
                "data": file_info
            }
        )
        
    except Exception as e:
        # 发生错误时清理文件
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 500,
                "message": f"文件上传失败: {str(e)}",
                "data": None
            }
        )

# 2.获取文件列表（支持搜索和分页）
@router.get(f"/resources", summary="获取文件资源列表")
async def get_resources(
    skip: int = 0,
    limit: int = 10,
    title: Optional[str] = None,
    file_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 构建查询
    query = db.query(FileResource)
    
    # 搜索条件
    if title:
        query = query.filter(FileResource.title.ilike(f"%{title}%"))
    if file_type:
        query = query.filter(FileResource.type == file_type)
    
    # 获取总数
    total = query.count()
    
    # 分页
    resources = query.offset(skip).limit(limit).all()
    
    # 格式化响应，确保包含created_at字段
    result = []
    for resource in resources:
        result.append({
            "file_id": resource.file_id,
            "title": resource.title,
            "description": resource.description,
            "type": resource.type,
            "size": resource.size,
            "mime_type": resource.mime_type,
            "download_url": resource.download_url,
            "created_at": resource.created_at.isoformat() if resource.created_at else None,
            "uploader_id": resource.uploader_id,
            "original_name": resource.original_name
        })
    
    # 返回带总数的响应
    return {
        "data": result,
        "total": total,
        "skip": skip,
        "limit": limit
    }

# 3.删除文件
@router.delete("/resources/{file_id}", summary="删除文件资源")
async def delete_resource(
    file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_file = db.query(FileResource).filter(FileResource.file_id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 检查权限：只有上传者可以删除文件
    if db_file.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此文件"
        )
    
    # 删除文件
    if os.path.exists(db_file.storage_path):
        os.remove(db_file.storage_path)
    
    # 从数据库删除
    db.delete(db_file)
    db.commit()
    
    return {"message": "文件删除成功"}

# 5.文件下载端点（位于编辑端点之后）
@router.get("/resources/{filename:path}", summary="下载文件资源")
async def download_file(
    filename: str,
    # 完全移除用户认证，任何人都可以访问文件
    db: Session = Depends(get_db)
):
    # 构建文件路径
    file_path = config.storage.UPLOAD_DIR / filename
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 检查文件是否在数据库中存在
    db_file = db.query(FileResource).filter(FileResource.relative_path == filename).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件记录不存在"
        )
    
    # 验证访问权限（可以根据需求调整）
    # 例如：可以限制只有上传者才能下载，或者允许所有登录用户下载
    # 这里暂时允许所有登录用户下载
    
    # 读取文件内容
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        # 确保原始文件名和MIME类型存在
        original_name = getattr(db_file, 'original_name', filename)
        mime_type = getattr(db_file, 'mime_type', 'application/octet-stream')
        
        # 对于PPT和其他可能需要下载的文件类型，设置为attachment
        is_office_file = filename.lower().endswith(('.pptx', '.ppt', '.docx', '.doc', '.xls', '.xlsx', '.zip', '.rar'))
        if is_office_file:
            # 使用UTF-8编码的文件名格式
            content_disposition = f"attachment; filename*=UTF-8''{urllib.parse.quote(original_name)}"
        else:
            content_disposition = f"inline; filename*=UTF-8''{urllib.parse.quote(original_name)}"
        
        # 返回文件内容作为响应
        return Response(
            content=file_content,
            media_type=mime_type,
            headers={
                "Content-Disposition": content_disposition,
                "Content-Length": str(len(file_content)),
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件读取失败: {str(e)}"
        )

# 4.编辑资源信息
@router.put("/resources/{file_id}", summary="编辑资源信息")
async def update_resource(
    file_id: str,
    request_data: dict,  # 使用字典接收JSON数据
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 查找文件
    db_file = db.query(FileResource).filter(FileResource.file_id == file_id).first()
    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    # 检查权限：只有上传者可以编辑文件
    if db_file.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限编辑此文件"
        )
    
    # 更新文件信息
    db_file.title = request_data.get('title', db_file.title)
    db_file.description = request_data.get('description', db_file.description)
    db_file.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_file)
    
    # 返回更新后的信息
    return {
        "message": "资源信息更新成功",
        "data": {
            "file_id": db_file.file_id,
            "title": db_file.title,
            "description": db_file.description,
            "type": db_file.type,
            "size": db_file.size,
            "mime_type": db_file.mime_type,
            "download_url": db_file.download_url,
            "created_at": db_file.created_at.isoformat() if db_file.created_at else None,
            "updated_at": db_file.updated_at.isoformat() if db_file.updated_at else None
        }
    }