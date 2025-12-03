FROM python:3.10-slim

WORKDIR /app

# 设置无缓冲输出，便于日志
ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1
# 安装系统依赖（libmagic、图像依赖和编译工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev default-libmysqlclient-dev libssl-dev libffi-dev \
    libmagic-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装依赖（使用项目 backend 目录下的 requirements.txt）
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# 复制 backend 目录下的所有代码到容器工作目录
COPY . /app

# 暴露默认 FastAPI 端口
EXPOSE 8000

# 使用 uvicorn 作为容器启动命令（生产环境建议使用 gunicorn + uvicorn workers）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]