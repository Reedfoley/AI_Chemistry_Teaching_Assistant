"""
统一启动脚本 - 启动优化后的后端服务

功能：
- 检查依赖是否已安装
- 自动启动FastAPI后端服务
- 提供开发环境热重载支持

使用：
    python backend_start.py
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path


def check_dependencies():
    """检查并安装必要的依赖"""
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
    }
    
    print("=" * 60)
    print("📦 检查依赖...")
    print("=" * 60)
    
    missing_packages = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n安装缺失的依赖: {', '.join(missing_packages)}")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install'] + missing_packages
        )
        print("✓ 依赖安装完成\n")
    
    return True


def start_backend():
    """启动FastAPI后端服务"""
    print("=" * 60)
    print("🚀 启动FastAPI后端服务...")
    print("=" * 60)
    
    # 确定工作目录
    workspace_root = Path(__file__).parent
    os.chdir(workspace_root)
    
    # 启动命令
    cmd = [
        sys.executable,
        '-m',
        'uvicorn',
        'backend.main:app',
        '--reload',
        '--host', '0.0.0.0',
        '--port', '5000'
    ]
    
    print(f"\n工作目录: {workspace_root}")
    print(f"启动命令: {' '.join(cmd)}\n")
    
    print("=" * 60)
    print("📊 服务信息:")
    print("=" * 60)
    print("API文档: http://localhost:5000/docs")
    print("ReDoc: http://localhost:5000/redoc")
    print("健康检查: http://localhost:5000/api/health")
    print("\n按 Ctrl+C 停止服务")
    print("=" * 60 + "\n")
    
    try:
        # 等待一秒后尝试打开浏览器
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open('http://localhost:5000/docs')
                print("\n✓ 已在浏览器中打开API文档\n")
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # 启动服务
        subprocess.run(cmd, check=False)
        
    except KeyboardInterrupt:
        print("\n\n🛑 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "乡村化学教师AI教学助手后端启动脚本" + " " * 10 + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    try:
        # 检查依赖
        check_dependencies()
        
        # 启动服务
        start_backend()
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
