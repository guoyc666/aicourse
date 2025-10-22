@echo off
setlocal enabledelayedexpansion

:: 设置变量
set "PYTHON_EXE=python"
set "REQUIREMENTS_FILE=requirements.txt"
set "MAIN_SCRIPT=resourceUploadAPI.py"
set "PORT=8000"

:: 检查Python是否安装
echo 检查Python环境...
%PYTHON_EXE% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python。请先安装Python并添加到环境变量。
    pause
    exit /b 1
)

:: 创建或更新requirements.txt
echo 创建依赖文件...
(
    echo fastapi>=0.68.0
    echo uvicorn>=0.15.0
    echo python-multipart>=0.0.5
    echo python-magic-bin>=0.4.14
    echo python-dotenv>=0.19.0
) > %REQUIREMENTS_FILE%

:: 检查并安装所需依赖
echo 检查并安装依赖库...
%PYTHON_EXE% -m pip install --upgrade pip >nul 2>&1
%PYTHON_EXE% -m pip install -r %REQUIREMENTS_FILE%

if %errorlevel% neq 0 (
    echo 错误：依赖库安装失败
    pause
    exit /b 1
)

:: 检查主脚本是否存在
if not exist %MAIN_SCRIPT% (
    echo 错误：未找到主脚本文件 %MAIN_SCRIPT%
    pause
    exit /b 1
)

:: 启动API服务
echo 启动API服务...
echo 服务将运行在 http://localhost:%PORT%
echo 按 Ctrl+C 停止服务
%PYTHON_EXE% -m uvicorn %MAIN_SCRIPT%:app --host 0.0.0.0 --port %PORT% --reload

endlocal
