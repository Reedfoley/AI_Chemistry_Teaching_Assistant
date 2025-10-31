@echo off
REM ============================================================
REM 乡村化学教师AI教学助手 - 一键部署脚本（Windows版）
REM ============================================================

setlocal enabledelayedexpansion

REM 设置编码为UTF-8
chcp 65001 > nul

REM 颜色定义
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

echo.
echo ============================================================
echo.
echo %GREEN%乡村化学教师AI教学助手 - 一键部署向导%RESET%
echo.
echo 此脚本将帮助您快速部署项目到本地或创空间
echo.
echo ============================================================
echo.

REM 检查Python是否已安装
echo %YELLOW%[1/5]检查Python环境...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ 错误: 未检测到Python，请先安装Python 3.8+%RESET%
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo %GREEN%✓ Python已安装%RESET%
python --version

REM 检查Git是否已安装
echo.
echo %YELLOW%[2/5]检查Git环境...%RESET%
git --version >nul 2>&1
if errorlevel 1 (
    echo %RED%⚠️ 警告: 未检测到Git，创空间部署将不可用%RESET%
    echo 下载地址: https://git-scm.com/
) else (
    echo %GREEN%✓ Git已安装%RESET%
    git --version
)

REM 创建虚拟环境
echo.
echo %YELLOW%[3/5]创建Python虚拟环境...%RESET%
if exist "venv" (
    echo %GREEN%✓ 虚拟环境已存在，跳过创建%RESET%
) else (
    echo 正在创建虚拟环境，请稍候...
    python -m venv venv
    if errorlevel 1 (
        echo %RED%❌ 虚拟环境创建失败%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%✓ 虚拟环境创建成功%RESET%
)

REM 激活虚拟环境
echo.
echo %YELLOW%[4/5]激活虚拟环境并安装依赖...%RESET%
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo %RED%❌ 虚拟环境激活失败%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ 虚拟环境已激活%RESET%

REM 安装依赖
echo.
echo 正在安装Python依赖，请稍候（此过程可能需要5-10分钟）...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo %RED%❌ 依赖安装失败，请检查网络连接%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ 依赖安装成功%RESET%

REM 部署选择
echo.
echo ============================================================
echo %YELLOW%[5/5]选择部署方式%RESET%
echo ============================================================
echo.
echo 请选择您要使用的部署方式：
echo.
echo  [1] Gradio应用（在线部署到创空间）
echo  [2] HTML5前端 + FastAPI后端（本地开发）
echo  [3] 上传到创空间（需要Git配置）
echo  [4] 退出
echo.

:deploy_choice
set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo %GREEN%启动Gradio应用...%RESET%
    echo.
    python gradio_app.py
    goto end
) else if "%choice%"=="2" (
    echo.
    echo %GREEN%启动FastAPI后端...%RESET%
    echo.
    echo 后端服务启动于: http://localhost:5000
    echo.
    python -m uvicorn backend.main:app --reload --port 5000
    goto end
) else if "%choice%"=="3" (
    echo.
    echo %GREEN%准备上传到创空间...%RESET%
    echo.
    
    git --version >nul 2>&1
    if errorlevel 1 (
        echo %RED%❌ 错误: 未检测到Git，无法上传%RESET%
        echo 请先安装Git: https://git-scm.com/
        pause
        goto end
    )
    
    echo 正在执行Git操作...
    echo.
    
    REM 检查Git状态
    git status >nul 2>&1
    if errorlevel 1 (
        echo %YELLOW%初始化Git仓库...%RESET%
        git init
        git config user.name "AI Chemistry Assistant"
        git config user.email "support@modelscope.cn"
    )
    
    REM 添加所有文件
    echo %YELLOW%添加文件到暂存区...%RESET%
    git add .
    
    REM 提交更改
    echo %YELLOW%提交更改...%RESET%
    git commit -m "Update AI Chemistry Teaching Assistant - Gradio UI v3.0.0"
    
    REM 推送到远程
    echo %YELLOW%推送到创空间...%RESET%
    git push -u origin main
    
    if errorlevel 0 (
        echo.
        echo %GREEN%✓ 成功上传到创空间！%RESET%
        echo.
        echo 访问地址: https://www.modelscope.cn/studios/Datawhale/AI_Chemistry_Teaching_Assistant
    ) else (
        echo %RED%⚠️ 上传过程中出现问题，请检查Git配置%RESET%
    )
    
    pause
    goto end
) else if "%choice%"=="4" (
    echo %YELLOW%已退出部署向导%RESET%
    goto end
) else (
    echo %RED%❌ 无效的选择，请重新输入%RESET%
    goto deploy_choice
)

:end
echo.
echo ============================================================
echo %GREEN%部署流程完成！%RESET%
echo ============================================================
echo.
echo 后续步骤：
echo  - Gradio应用: 浏览器自动打开，访问 http://localhost:7860
echo  - FastAPI后端: 访问 http://localhost:5000/docs 查看API文档
echo  - 创空间部署: 访问 https://www.modelscope.cn/studios 查看应用
echo.
echo 问题排查：
echo  - 依赖安装失败: 检查网络连接，尝试更换pip源
echo  - 端口被占用: 修改脚本中的端口号
echo  - Git推送失败: 检查Git配置和远程仓库地址
echo.
echo ============================================================
echo.

REM 保持窗口打开
if "%choice%"=="1" goto end_no_pause
if "%choice%"=="2" goto end_no_pause
pause

:end_no_pause
exit /b 0
