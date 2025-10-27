#!/bin/bash

# 乡村化学教师AI教学助手 - macOS/Linux启动脚本
# 功能: 一键启动前端和后端服务
# 使用: bash app.sh 或 ./app.sh（需先执行 chmod +x app.sh）

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 清屏
clear

# 打印欢迎信息
echo ""
echo "============================================================"
echo -e "${BLUE}    🧪 乡村化学教师AI教学助手 - 前后端统一启动${NC}"
echo "============================================================"
echo ""

# 检查Python是否已安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: Python3未安装${NC}"
    echo ""
    echo "请先安装Python3："
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo ""
    read -p "按 Enter 键退出..."
    exit 1
fi

# 运行Python启动脚本
echo -e "${YELLOW}启动应用...${NC}"
echo ""

python3 app.py

# 如果脚本异常退出，显示错误信息
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 应用启动失败！${NC}"
    echo ""
    read -p "按 Enter 键退出..."
    exit 1
fi
