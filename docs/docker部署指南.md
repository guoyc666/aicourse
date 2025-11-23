# Docker 部署指南

## 1. 环境准备

- 已安装 [Docker](https://docs.docker.com/get-docker/) 和 [Docker Compose](https://docs.docker.com/compose/install/)。

验证安装：

```powershell
docker --version
docker compose version
```

## 2. 构建与启动服务

```powershell
# 构建所有服务（首次或有更新时执行）
docker compose build

# 启动所有服务（前台运行，显示日志）
docker compose up

# 后台运行（推荐生产环境）
docker compose up -d
```

在项目根目录（即有 `docker-compose.yml` 的目录）打开终端，执行：

```powershell
# 构建所有服务（首次或有更新时执行）
docker compose build

# 启动所有服务（前台运行，显示日志）
docker compose up

# 后台运行（推荐生产环境）
docker compose up -d
```

## 3. 关闭服务

```powershell
# 停止所有服务（保留容器数据）
docker compose down

# 停止并删除所有容器、网络、卷
docker compose down -v
```

## 4. 常用命令

- 查看服务状态：
  ```powershell
  docker compose ps
  ```
- 查看日志：
  ```powershell
  docker compose logs
  docker compose logs backend
  docker compose logs frontend
  ```
- 进入容器内部：
  ```powershell
  docker exec -it ai_backend /bin/bash
  docker exec -it ai_frontend sh
  ```

## 5. 数据持久化

- 数据库、Neo4j、上传文件等都已通过 `volumes` 映射到本地 `data/` 目录，容器重启数据不丢失。

## 6. 端口说明

- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- MySQL 管理端口：3306
- Neo4j 管理端口：7474，Bolt 协议端口：7687

## 7. 其他说明

- 如需重建镜像（比如修改了 Dockerfile），请重新执行 `docker compose build`。
- 如需单独启动某个服务，例如只启动后端：
  ```powershell
  docker compose up backend
  ```
