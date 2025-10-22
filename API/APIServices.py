import os
import magic  # pip install python-magic-bin
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
from datetime import datetime
from configurations import config  # 导入配置对象

# 初始化FastAPI应用
app = FastAPI(
    title="文件资源上传服务",
    description="基于FastAPI的文件上传接口，支持配置化管理",
    version="v1.0-resourceUpload"
)

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应指定具体前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.post(config.api.UPLOAD_ENDPOINT, summary="上传资源文件")
async def upload_resource(
    file: UploadFile = File(...),
    title: str = Form(..., description="文件标题"),
    type: str = Form(..., description="文件类型分类"),
    uploader: str = Form(..., description="上传者名称或ID"),
    description: str = Form(None, description="资源详细描述（可选）")
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
        
        # 构建文件信息（包含新增的上传者和描述信息）
        file_info = {
            "file_id": uuid.uuid4().hex,
            "original_name": file.filename,
            "unique_filename": unique_filename,
            "title": title,
            "type": type,
            "uploader": uploader,  
            "description": description,  
            "size": file_size,
            "mime_type": magic.from_file(str(file_path), mime=True),
            "upload_time": datetime.now().isoformat(),
            "storage_path": str(file_path),
            "relative_path": str(file_path.relative_to(config.storage.UPLOAD_DIR)),
            "download_url": f"{config.api.DOWNLOAD_URL_PREFIX}/{file_path.relative_to(config.storage.UPLOAD_DIR)}"
        }
        
        # TODO: 调用文件分析函数，由其他开发者实现
        # analyze_file(
        #     filename=file_info["unique_filename"],
        #     file_path=file_info["storage_path"],
        #     original_name=file_info["original_name"],
        #     file_id=file_info["file_id"],
        #     title=file_info["title"],
        #     file_type=file_info["type"],
        #     uploader=file_info["uploader"],  # 传递上传者信息
        #     description=file_info["description"],  # 传递描述信息
        #     size=file_info["size"],
        #     mime_type=file_info["mime_type"]
        # )
        
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

# 2.服务健康检查接口
@app.get(f"{config.api.BASE_PATH}/health", summary="服务健康检查")
async def health_check():
    return {
        "code": 200,
        "message": "服务运行正常",
        "data": {
            "timestamp": datetime.now().isoformat(),
            "upload_dir": str(config.storage.UPLOAD_DIR)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "APIServices:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发环境启用自动重载
    )