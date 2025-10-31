#!/bin/bash

# ============================================================
# 乡村化学教师AI教学助手 - 一键部署脚本（Linux/Mac版）
# ============================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 清屏
clear

echo ""
echo "============================================================"
echo ""
echo -e "${GREEN}乡村化学教师AI教学助手 - 一键部署向导${NC}"
echo ""
echo "此脚本将帮助您快速部署项目到本地或创空间"
echo ""
echo "============================================================"
echo ""

# 检查Python是否已安装
echo -e "${YELLOW}[1/5]检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未检测到Python，请先安装Python 3.8+${NC}"
    echo "安装命令："
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo "  macOS: brew install python3"
    exit 1
fi
echo -e "${GREEN}✓ Python已安装${NC}"
python3 --version

# 检查Git是否已安装
echo ""
echo -e "${YELLOW}[2/5]检查Git环境...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}⚠️ 警告: 未检测到Git，创空间部署将不可用${NC}"
    echo "安装命令："
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  macOS: brew install git"
else
    echo -e "${GREEN}✓ Git已安装${NC}"
    git --version
fi

# 创建虚拟环境
echo ""
echo -e "${YELLOW}[3/5]创建Python虚拟环境...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ 虚拟环境已存在，跳过创建${NC}"
else
    echo "正在创建虚拟环境，请稍候..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 虚拟环境创建失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo ""
echo -e "${YELLOW}[4/5]激活虚拟环境并安装依赖...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 虚拟环境激活失败${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"

# 安装依赖
echo ""
echo "正在安装Python依赖，请稍候（此过程可能需要5-10分钟）..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 依赖安装失败，请检查网络连接${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 依赖安装成功${NC}"

# 部署选择
echo ""
echo "============================================================"
echo -e "${YELLOW}[5/5]选择部署方式${NC}"
echo "============================================================"
echo ""
echo "请选择您要使用的部署方式："
echo ""
echo "  [1] Gradio应用（在线部署到创空间）"
echo "  [2] HTML5前端 + FastAPI后端（本地开发）"
echo "  [3] 上传到创空间（需要Git配置）"
echo "  [4] 退出"
echo ""

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}启动Gradio应用...${NC}"
        echo ""
        python3 gradio_app.py
        ;;
    2)
        echo ""
        echo -e "${GREEN}启动FastAPI后端...${NC}"
        echo ""
        echo "后端服务启动于: http://localhost:5000"
        echo ""
        python3 -m uvicorn backend.main:app --reload --port 5000
        ;;
    3)
        echo ""
        echo -e "${GREEN}准备上传到创空间...${NC}"
        echo ""
        
        if ! command -v git &> /dev/null; then
            echo -e "${RED}❌ 错误: 未检测到Git，无法上传${NC}"
            echo "请先安装Git"
            exit 1
        fi
        
        echo "正在执行Git操作..."
        echo ""
        
        # 检查Git状态
        if ! git status &> /dev/null; then
            echo -e "${YELLOW}初始化Git仓库...${NC}"
            git init
            git config user.name "AI Chemistry Assistant"
            git config user.email "support@modelscope.cn"
        fi
        
        # 添加所有文件
        echo -e "${YELLOW}添加文件到暂存区...${NC}"
        git add .
        
        # 提交更改
        echo -e "${YELLOW}提交更改...${NC}"
        git commit -m "Update AI Chemistry Teaching Assistant - Gradio UI v3.0.0"
        
        # 推送到远程
        echo -e "${YELLOW}推送到创空间...${NC}"
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}✓ 成功上传到创空间！${NC}"
            echo ""
            echo "访问地址: https://www.modelscope.cn/studios/Datawhale/AI_Chemistry_Teaching_Assistant"
        else
            echo -e "${RED}⚠️ 上传过程中出现问题，请检查Git配置${NC}"
        fi
        ;;
    4)
        echo -e "${YELLOW}已退出部署向导${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ 无效的选择${NC}"
        exit 1
        ;;
esac

echo ""
echo "============================================================"
echo -e "${GREEN}部署流程完成！${NC}"
echo "============================================================"
echo ""
echo "后续步骤："
echo "  - Gradio应用: 浏览器自动打开，访问 http://localhost:7860"
echo "  - FastAPI后端: 访问 http://localhost:5000/docs 查看API文档"
echo "  - 创空间部署: 访问 https://www.modelscope.cn/studios 查看应用"
echo ""
echo "问题排查："
echo "  - 依赖安装失败: 检查网络连接，尝试更换pip源"
echo "  - 端口被占用: 修改脚本中的端口号"
echo "  - Git推送失败: 检查Git配置和远程仓库地址"
echo ""
echo "============================================================"
echo ""
