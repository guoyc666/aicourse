FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# 使用非交互模式
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-pip \
    python3-dev \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 升级pip并安装 vllm 及其依赖（视显卡和环境可能需要额外的依赖）
RUN python3 -m pip install --no-cache-dir -U pip setuptools wheel
RUN python3 -m pip install --no-cache-dir vllm[transformers,torch]==0.12.0

# 创建模型挂载点
VOLUME ["/models", "/lora_adapter"]

# 暴露 vllm 端口
EXPOSE 8888

# 运行默认命令，实际命令可在 docker-compose.yml 中覆盖
CMD ["vllm", "--help"]
