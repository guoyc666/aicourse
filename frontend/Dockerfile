# 生产镜像：多阶段构建，第一阶段构建静态资源，第二阶段用 nginx 提供服务
FROM node:20-alpine AS builder
WORKDIR /app

# 只拷贝依赖清单以利用缓存
COPY package*.json ./
RUN npm ci --silent --no-audit --progress=false

# 拷贝源码并构建
COPY . .
RUN npm run build

# 生产镜像：使用 nginx 提供静态文件
FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# 开发镜像：可用于本地开发（可配合 volumes 挂载源码）
FROM node:18-alpine AS dev
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY package*.json ./
RUN npm install --silent --no-audit --progress=false

COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]