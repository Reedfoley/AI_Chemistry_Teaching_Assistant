"""
前端启动脚本 - 单独启动前端 HTTP 服务器

使用：
    python frontend_start.py
"""

import os
import sys
import subprocess
import webbrowser
import time

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(SCRIPT_DIR, "frontend")

def main():
    """启动前端服务"""
    print("\n" + "=" * 60)
    print("  🧪 乡村化学教师AI教学助手 - 前端启动脚本")
    print("=" * 60)
    print()
    print("  📍 前端地址: http://127.0.0.1:8000")
    print()
    print("  按 Ctrl+C 停止服务")
    print()
    print("=" * 60 + "\n")
    
    try:
        # 启动 HTTP 服务器
        cmd = [
            sys.executable,
            "-m",
            "http.server",
            "8000",
            "--directory", FRONTEND_DIR
        ]
        
        print("启动前端服务...")
        print(f"命令: {' '.join(cmd)}\n")
        
        # 延迟打开浏览器
        time.sleep(1)
        try:
            webbrowser.open("http://127.0.0.1:8000")
            print("✓ 浏览器已打开\n")
        except:
            print("⚠ 无法自动打开浏览器，请手动访问: http://127.0.0.1:8000\n")
        
        subprocess.run(cmd, cwd=FRONTEND_DIR)
    
    except KeyboardInterrupt:
        print("\n\n前端服务已停止")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
