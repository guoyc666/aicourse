import os
import magic  # pip install python-magic-bin
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,  FileResponse
import shutil
from datetime import datetime
import mysql.connector  # 新增：导入mysql连接器
from mysql.connector import Error  # 新增：导入错误处理
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

# 新增：数据库连接工具函数
def get_db_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(
            host=config.database.HOST,
            database=config.database.NAME,
            user=config.database.USER,
            password=config.database.PASSWORD,
            port=config.database.PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库连接失败: {str(e)}"
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

# 新增：提取关键词的临时函数（实际应用中可能需要更复杂的实现）
def extract_keywords(content: str) -> str:
    """简单提取关键词示例，实际应根据文件内容提取"""
    # 这里仅作为占位，实际应根据文件类型使用合适的提取方法
    return ""

@app.post(config.api.UPLOAD_ENDPOINT, summary="上传资源文件")
async def upload_resource(
    file: UploadFile = File(...),
    title: str = Form(..., description="文件标题"),
    type: str = Form(..., description="文件类型分类"),
    uploader: int = Form(..., description="上传教师ID"),  
    description: str = Form(None, description="资源详细描述（可选）")
):
    # 检查文件类型是否符合枚举值
    allowed_types = ['pdf', 'ppt', 'video', 'text']
    if type not in allowed_types:
        type = 'else'
    
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
        
        # 构建文件信息
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
        
        # 提取关键词（实际应用中应根据文件内容提取）
        keywords = extract_keywords(description or "")
        
        # 新增：将资源信息写入数据库
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # 插入数据库的SQL语句
                insert_query = """
                INSERT INTO resource (title, type, path, keywords, uploader_id, upload_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                # 准备插入的数据
                current_time = datetime.now()
                record = (
                    title,
                    type,
                    str(file_path),  # 存储文件的完整路径
                    keywords,
                    uploader,
                    current_time
                )
                # 执行插入
                cursor.execute(insert_query, record)
                connection.commit()
                # 获取插入的记录ID
                resource_id = cursor.lastrowid
                file_info["resource_id"] = resource_id  # 添加到返回信息中
            except Error as e:
                connection.rollback()  # 出错时回滚
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"数据库操作失败: {str(e)}"
                )
            finally:
                # 关闭游标和连接
                if cursor:
                    cursor.close()
                if connection.is_connected():
                    connection.close()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "文件上传成功并已保存到数据库",
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

# 资源列表查询接口（修复datetime序列化问题）
@app.get(f"{config.api.BASE_PATH}/resource/list", summary="获取资源列表")
async def get_resource_list(
    page: int = 1,
    page_size: int = 20,
    type: str = None,
    uploader_id: int = None
):
    """获取资源列表，支持分页和筛选"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # 返回字典格式结果
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if type:
            where_conditions.append("type = %s")
            params.append(type)
        if uploader_id:
            where_conditions.append("uploader_id = %s")
            params.append(uploader_id)
        
        # 基础SQL
        base_sql = "SELECT id, title, type, uploader_id, upload_time FROM resource"
        count_sql = "SELECT COUNT(*) as total FROM resource"
        
        # 拼接条件
        if where_conditions:
            where_clause = " WHERE " + " AND ".join(where_conditions)
            base_sql += where_clause
            count_sql += where_clause
        
        # 分页处理
        offset = (page - 1) * page_size
        base_sql += " ORDER BY upload_time DESC LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        
        # 执行查询
        cursor.execute(count_sql, params[:len(params)-2] if where_conditions else [])
        total = cursor.fetchone()["total"]
        
        cursor.execute(base_sql, params)
        resources = cursor.fetchall()
        
        # 关键修复：将datetime对象转换为ISO格式字符串
        for item in resources:
            if isinstance(item["upload_time"], datetime):
                item["upload_time"] = item["upload_time"].isoformat()  # 转换为ISO格式字符串
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "资源列表查询成功",
                "data": {
                    "list": resources,
                    "pagination": {
                        "page": page,
                        "page_size": page_size,
                        "total": total,
                        "total_pages": total_pages
                    }
                }
            }
        )
        
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库查询失败: {str(e)}"
        )
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# 3. 资源下载接口
@app.get(f"{config.api.BASE_PATH}/resource/download", summary="下载指定资源")
async def download_resource(
    resource_id: int = Query(..., description="资源ID", ge=1)  # 使用查询参数
):
    """根据资源ID下载对应的文件"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 查询资源信息
        query = "SELECT title, path, type FROM resource WHERE id = %s"
        cursor.execute(query, (resource_id,))
        resource = cursor.fetchone()
        
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="资源不存在或已被删除"
            )
        
        # 验证文件是否存在
        file_path = Path(resource["path"])
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文件不存在，请联系管理员"
            )
        
        # 获取文件MIME类型
        mime_type = magic.from_file(str(file_path), mime=True)
        
        # 构建下载文件名
        download_filename = f"{resource['title']}.{resource['type']}"
        # 处理特殊字符
        download_filename = resource["path"].split('\\')[-1]    ####### 文件名
        
        return FileResponse(
            path=file_path,
            media_type=mime_type,
            filename=download_filename
        )
        
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


# ex.服务健康检查接口
@app.get(f"{config.api.BASE_PATH}/health", summary="服务健康检查")
async def health_check():
    # 新增：检查数据库连接状态
    db_status = "正常"
    try:
        connection = get_db_connection()
        if connection:
            connection.close()
    except:
        db_status = "异常"
    
    return {
        "code": 200,
        "message": "服务运行正常",
        "data": {
            "timestamp": datetime.now().isoformat(),
            "upload_dir": str(config.storage.UPLOAD_DIR),
            "database_status": db_status  # 新增：数据库状态
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