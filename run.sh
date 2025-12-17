#!/bin/bash

set -e  # 遇到错误立即退出

echo "🚀 开始启动服务..."

# 1. 启动 MySQL（假设使用 systemctl 管理）
echo "🔧 正在启动 MySQL..."
sudo systemctl start mysql || { echo "❌ MySQL 启动失败"; exit 1; }

# 2. 启动 Neo4j（假设 Neo4j 以 systemd 服务运行，服务名为 neo4j）
echo "🔧 正在启动 Neo4j..."
sudo ../neo4j-community-2025.10.1/bin/neo4j start || { echo "❌ Neo4j 启动失败"; exit 1; }

# 可选：等待 Neo4j 就绪（Neo4j 启动较慢）
echo "⏳ 等待 Neo4j 启动中（约10秒）..."
sleep 10

# 3. 进入 backend 目录并运行 Python 后端
echo "📂 切换到 backend 目录..."
cd "$(dirname "$0")/backend" || { echo "❌ 无法进入 backend 目录"; exit 1; }

echo "🐍 激活 Conda 环境 aicourse43 并运行 main.py..."
# 初始化 conda（如果尚未初始化）
eval "$(conda shell.bash hook)"
conda activate aicourse43 || { echo "❌ 无法激活 Conda 环境 aicourse43"; exit 1; }

# 假设 main 是一个 Python 脚本（如 main.py），如果不是请修改
python main.py &  # 后台运行，避免阻塞后续步骤
BACKEND_PID=$!

# 等待后端启动（可根据实际情况调整）
echo "⏳ 等待后端服务启动（5秒）..."
sleep 5

# 4. 进入 front 目录并启动前端开发服务器
echo "📂 切换到 front 目录..."
cd "$(dirname "$0")/front" || { echo "❌ 无法进入 front 目录"; exit 1; }

echo "🌐 启动前端开发服务器 (npm run dev)..."
npm run dev

# 注意：npm run dev 通常是前台阻塞进程，脚本会在此处停止
# 如果希望同时监控后端，可以考虑用 trap 清理后台进程

# 当用户终止前端时，也终止后端
trap 'kill $BACKEND_PID 2>/dev/null' EXIT