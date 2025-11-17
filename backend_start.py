"""
后端启动脚本 - 单独启动 FastAPI 后端服务

使用：
    python backend_start.py
"""

import os
import sys
import subprocess

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """启动后端服务"""
    print("\n" + "=" * 60)
    print("  🧪 乡村化学教师AI教学助手 - 后端启动脚本")
    print("=" * 60)
    print()
    print("  📍 后端地址: http://127.0.0.1:5000")
    print("  📍 API 文档: http://127.0.0.1:5000/docs")
    print()
    print("  按 Ctrl+C 停止服务")
    print()
    print("=" * 60 + "\n")
    
    try:
        # 启动 uvicorn
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host", "127.0.0.1",
            "--port", "5000",
            "--reload",
            "--log-level", "info"
        ]
        
        print("启动后端服务...")
        print(f"命令: {' '.join(cmd)}\n")
        
        subprocess.run(cmd, cwd=SCRIPT_DIR)
    
    except KeyboardInterrupt:
        print("\n\n后端服务已停止")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
