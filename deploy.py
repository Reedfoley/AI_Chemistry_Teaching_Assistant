#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乡村化学教师AI教学助手 - 一键部署脚本（跨平台版）

支持平台: Windows, Linux, macOS
使用方式: python deploy.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# 颜色定义（支持Windows 10+）
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    @staticmethod
    def disable_on_windows():
        """在不支持ANSI颜色的Windows上禁用颜色"""
        if platform.system() == 'Windows':
            Colors.GREEN = Colors.YELLOW = Colors.RED = Colors.RESET = ''

Colors.disable_on_windows()

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"{Colors.GREEN}{title}{Colors.RESET}")
    print(f"{'='*60}\n")

def print_step(step_num, title):
    """打印步骤"""
    print(f"{Colors.YELLOW}[{step_num}]{title}...{Colors.RESET}")

def print_success(msg):
    """打印成功消息"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    """打印错误消息"""
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warning(msg):
    """打印警告消息"""
    print(f"{Colors.YELLOW}⚠️ {msg}{Colors.RESET}")

def run_command(cmd, shell=False, check=True):
    """运行系统命令"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python():
    """检查Python环境"""
    print_step("1/5", "检查Python环境")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python版本过低 (当前: {version.major}.{version.minor}, 需要: 3.8+)")
        return False
    
    print_success(f"Python已安装 ({version.major}.{version.minor}.{version.micro})")
    return True

def check_git():
    """检查Git环境"""
    print_step("2/5", "检查Git环境")
    
    success, _, _ = run_command(['git', '--version'], check=False)
    if not success:
        print_warning("未检测到Git，创空间部署将不可用")
        print("  下载地址: https://git-scm.com/")
        return False
    
    success, output, _ = run_command(['git', '--version'], check=False)
    if success:
        print_success(output.strip())
    return True

def setup_venv():
    """设置虚拟环境"""
    print_step("3/5", "创建Python虚拟环境")
    
    venv_path = Path('venv')
    if venv_path.exists():
        print_success("虚拟环境已存在，跳过创建")
        return True
    
    print("  正在创建虚拟环境，请稍候...")
    success, _, err = run_command([sys.executable, '-m', 'venv', 'venv'], check=False)
    
    if not success:
        print_error("虚拟环境创建失败")
        print(f"  错误信息: {err}")
        return False
    
    print_success("虚拟环境创建成功")
    return True

def install_dependencies():
    """安装依赖"""
    print_step("4/5", "激活虚拟环境并安装依赖")
    
    # 获取虚拟环境的pip路径
    if platform.system() == 'Windows':
        pip_cmd = str(Path('venv/Scripts/pip'))
    else:
        pip_cmd = str(Path('venv/bin/pip'))
    
    print("  正在安装Python依赖，请稍候（此过程可能需要5-10分钟）...")
    success, _, err = run_command([pip_cmd, 'install', '-q', '-r', 'requirements.txt'], check=False)
    
    if not success:
        print_error("依赖安装失败，请检查网络连接")
        print(f"  错误信息: {err}")
        print("  尝试更换pip源:")
        print("    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/")
        return False
    
    print_success("依赖安装成功")
    return True

def get_python_executable():
    """获取虚拟环境的Python可执行文件路径"""
    if platform.system() == 'Windows':
        return str(Path('venv/Scripts/python'))
    else:
        return str(Path('venv/bin/python'))

def run_gradio_app():
    """运行Gradio应用"""
    print("\n")
    print_success("启动Gradio应用...")
    print()
    
    python_exe = get_python_executable()
    subprocess.call([python_exe, 'gradio_app.py'])

def run_fastapi_backend():
    """运行FastAPI后端"""
    print("\n")
    print_success("启动FastAPI后端...")
    print()
    print("后端服务启动于: http://localhost:5000")
    print()
    
    python_exe = get_python_executable()
    subprocess.call([python_exe, '-m', 'uvicorn', 'backend.main:app', '--reload', '--port', '5000'])

def push_to_modelscope():
    """推送到ModelScope创空间"""
    print("\n")
    print_success("准备上传到创空间...")
    print()
    
    # 检查Git
    success, _, _ = run_command(['git', '--version'], check=False)
    if not success:
        print_error("未检测到Git，无法上传")
        print("  请先安装Git: https://git-scm.com/")
        return
    
    print("  正在执行Git操作...")
    print()
    
    # 检查Git状态
    success, _, _ = run_command(['git', 'status'], check=False)
    if not success:
        print_warning("初始化Git仓库...")
        run_command(['git', 'init'], check=False)
        run_command(['git', 'config', 'user.name', 'AI Chemistry Assistant'], check=False)
        run_command(['git', 'config', 'user.email', 'support@modelscope.cn'], check=False)
    
    # 添加文件
    print_warning("添加文件到暂存区...")
    run_command(['git', 'add', '.'], check=False)
    
    # 提交更改
    print_warning("提交更改...")
    run_command(['git', 'commit', '-m', 'Update AI Chemistry Teaching Assistant - Gradio UI v3.0.0'], check=False)
    
    # 推送到远程
    print_warning("推送到创空间...")
    success, _, _ = run_command(['git', 'push', '-u', 'origin', 'main'], check=False)
    
    if success:
        print()
        print_success("成功上传到创空间！")
        print()
        print("访问地址: https://www.modelscope.cn/studios/Datawhale/AI_Chemistry_Teaching_Assistant")
    else:
        print_warning("上传过程中出现问题，请检查Git配置")

def show_menu():
    """显示部署选择菜单"""
    print_step("5/5", "选择部署方式")
    print()
    print("请选择您要使用的部署方式：")
    print()
    print("  [1] Gradio应用（在线部署到创空间）")
    print("  [2] HTML5前端 + FastAPI后端（本地开发）")
    print("  [3] 上传到创空间（需要Git配置）")
    print("  [4] 退出")
    print()
    
    while True:
        choice = input("请输入选择 (1-4): ").strip()
        
        if choice == '1':
            run_gradio_app()
            break
        elif choice == '2':
            run_fastapi_backend()
            break
        elif choice == '3':
            push_to_modelscope()
            break
        elif choice == '4':
            print_warning("已退出部署向导")
            break
        else:
            print_error("无效的选择，请重新输入")

def show_completion():
    """显示完成信息"""
    print()
    print("="*60)
    print_success("部署流程完成！")
    print("="*60)
    print()
    print("后续步骤：")
    print("  - Gradio应用: 浏览器自动打开，访问 http://localhost:7860")
    print("  - FastAPI后端: 访问 http://localhost:5000/docs 查看API文档")
    print("  - 创空间部署: 访问 https://www.modelscope.cn/studios 查看应用")
    print()
    print("问题排查：")
    print("  - 依赖安装失败: 检查网络连接，尝试更换pip源")
    print("  - 端口被占用: 修改脚本中的端口号")
    print("  - Git推送失败: 检查Git配置和远程仓库地址")
    print()
    print("="*60)
    print()

def main():
    """主函数"""
    print_header("乡村化学教师AI教学助手 - 一键部署向导")
    print("此脚本将帮助您快速部署项目到本地或创空间")
    
    # 执行检查和设置
    if not check_python():
        print_error("Python版本检查失败，退出部署")
        sys.exit(1)
    
    git_available = check_git()
    
    if not setup_venv():
        print_error("虚拟环境设置失败，退出部署")
        sys.exit(1)
    
    if not install_dependencies():
        print_error("依赖安装失败，退出部署")
        sys.exit(1)
    
    # 显示部署选择菜单
    show_menu()
    
    # 显示完成信息
    show_completion()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("部署被用户中断")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"发生错误: {str(e)}")
        sys.exit(1)
