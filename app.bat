@echo off
REM 乡村化学教师AI教学助手 - Windows启动脚本
REM 功能: 一键启动前端和后端服务
REM 使用: 双击此文件或在命令行运行 app.bat

setlocal enabledelayedexpansion

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 设置标题
title 乡村化学教师AI教学助手 - 前后端统一启动

REM 清屏
cls

REM 打印欢迎信息
echo.
echo ============================================================
echo     ^!乡村化学教师AI教学助手^! - 前后端统一启动
echo ============================================================
echo.
echo 正在启动应用...
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: Python未安装或未添加到系统路径
    echo.
    echo 请先安装Python，然后将其添加到系统环境变量
    echo.
    pause
    exit /b 1
)

REM 运行Python启动脚本
echo 启动Python应用...
python app.py

REM 如果脚本异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo ❌ 应用启动失败！
    echo.
    pause
    exit /b 1
)

pause
