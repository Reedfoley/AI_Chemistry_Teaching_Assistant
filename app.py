"""	
统一启动脚本 - 启动前端和后端服务
功能：	
- 检查依赖是否已安装	
- 自动启动FastAPI后端服务（端口5000）	
- 自动启动前端HTTP服务器（端口8000）	
- 自动打开浏览器访问前端	
- 支持优雅关闭（Ctrl+C）	
 	
使用：	
    python app.py	
    	
访问地址：	
    前端：http://localhost:8000	
    后端API文档：http://localhost:5000/docs	
"""	
 	
import os	
import sys	
import subprocess	
import time	
import webbrowser	
import threading	
from pathlib import Path	
import signal	
 	
from backend.main import app
 	
 	
# 全局变量，用于存储进程	
backend_process = None	
frontend_process = None	
 	
 	
def print_banner():	
    """打印欢迎横幅"""	
    print("\n")	
    print("╔" + "=" * 58 + "╗")	
    print("║" + " " * 8 + "🧪 乡村化学教师AI教学助手（前后端统一启动）" + " " * 6 + "║")	
    print("╚" + "=" * 58 + "╝\n")	
 	
 	
def check_dependencies():	
    """检查并安装必要的依赖"""	
    required_packages = {	
        'fastapi': 'fastapi',	
        'uvicorn': 'uvicorn',	
        'python-multipart': 'python-multipart',	
    }	
    	
    print("=" * 60)	
    print("📦 检查依赖...")	
    print("=" * 60)	
    	
    missing_packages = []	
    for import_name, package_name in required_packages.items():	
        try:	
            if import_name == 'python-multipart':	
                # python-multipart 的导入名称不同	
                __import__('multipart')	
            else:	
                __import__(import_name)	
            print(f"✓ {package_name} 已安装")	
        except ImportError:	
            print(f"✗ {package_name} 未安装")	
            missing_packages.append(package_name)	
    	
    if missing_packages:	
        print(f"\n📥 安装缺失的依赖: {', '.join(missing_packages)}")	
        try:	
            subprocess.check_call(	
                [sys.executable, '-m', 'pip', 'install'] + missing_packages,	
                stdout=subprocess.DEVNULL,	
                stderr=subprocess.DEVNULL	
            )	
            print("✓ 依赖安装完成\n")	
        except subprocess.CalledProcessError:	
            print("⚠️ 依赖安装失败，请手动安装：")	
            print(f"   pip install {' '.join(missing_packages)}\n")	
            return False	
    else:	
        print("✓ 所有依赖已安装\n")	
    	
    return True	
 	
 	
def start_backend():	
    """启动FastAPI后端服务"""	
    global backend_process	
    	
    print("=" * 60)	
    print("🚀 启动FastAPI后端服务（端口5000）...")	
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
    	
    print(f"工作目录: {workspace_root}")	
    print(f"启动命令: {' '.join(cmd)}\n")	
    	
    try:	
        # 启动后端进程	
        backend_process = subprocess.Popen(	
            cmd,	
            stdout=subprocess.PIPE,	
            stderr=subprocess.PIPE,	
            cwd=workspace_root,	
            text=True,	
            bufsize=1	
        )	
        	
        print("✓ 后端服务进程已启动（PID: {}）\n".format(backend_process.pid))	
        return True	
        	
    except Exception as e:	
        print(f"❌ 后端启动失败: {e}\n")	
        return False	
 	
 	
def start_frontend():	
    """启动前端HTTP服务器"""	
    global frontend_process	
    	
    print("=" * 60)	
    print("🎨 启动前端HTTP服务器（端口8000）...")	
    print("=" * 60)	
    	
    # 确定前端目录	
    workspace_root = Path(__file__).parent	
    frontend_dir = workspace_root / 'frontend'	
    	
    # 启动命令	
    cmd = [	
        sys.executable,	
        '-m',	
        'http.server',	
        '8000',	
        '--directory', str(frontend_dir)	
    ]	
    	
    print(f"前端目录: {frontend_dir}")	
    print(f"启动命令: {' '.join(cmd)}\n")	
    	
    try:	
        # 启动前端进程	
        frontend_process = subprocess.Popen(	
            cmd,	
            stdout=subprocess.PIPE,	
            stderr=subprocess.PIPE,	
            cwd=frontend_dir,	
            text=True,	
            bufsize=1	
        )	
        	
        print("✓ 前端服务进程已启动（PID: {}）\n".format(frontend_process.pid))	
        return True	
        	
    except Exception as e:	
        print(f"❌ 前端启动失败: {e}\n")	
        return False	
 	
 	
def open_browser():	
    """在默认浏览器中打开应用"""	
    print("=" * 60)	
    print("🌐 打开浏览器...")	
    print("=" * 60)	
    	
    # 等待服务启动	
    time.sleep(3)	
    	
    try:	
        # 尝试打开前端	
        webbrowser.open('http://localhost:8000')	
        print("✓ 已在浏览器中打开前端应用\n")	
    except Exception as e:	
        print(f"⚠️ 打开浏览器失败: {e}\n")	
 	
 	
def log_service_info():	
    """输出服务信息"""	
    print("=" * 60)	
    print("📊 服务信息")	
    print("=" * 60)	
    print("\n🎨 前端服务:")	
    print("   URL: http://localhost:8000")	
    print("   入口: http://localhost:8000/index.html\n")	
    	
    print("🔌 后端API服务:")	
    print("   基础URL: http://localhost:5000")	
    print("   API文档（Swagger）: http://localhost:5000/docs")	
    print("   API文档（ReDoc）: http://localhost:5000/redoc")	
    print("   健康检查: http://localhost:5000/api/health")	
    print("   配置信息: http://localhost:5000/api/config\n")	
    	
    print("⚙️  功能接口:")	
    print("   - POST /api/reaction/explain         - 化学反应智能讲解")	
    print("   - POST /api/equation/balance         - 化学方程式自动配平")	
    print("   - POST /api/reaction/image           - 反应现象文生图")	
    print("   - POST /api/material/recognize       - 实验物质图生文识别\n")	
    	
    print("🛑 停止服务: 按 Ctrl+C 停止所有服务\n")	
    print("=" * 60 + "\n")	
 	
 	
def handle_shutdown(signum, frame):	
    """处理关闭信号"""	
    print("\n\n" + "=" * 60)	
    print("🛑 正在关闭服务...")	
    print("=" * 60)	
    	
    global backend_process, frontend_process	
    	
    # 关闭后端	
    if backend_process:	
        try:	
            backend_process.terminate()	
            backend_process.wait(timeout=5)	
            print("✓ 后端服务已关闭")	
        except subprocess.TimeoutExpired:	
            backend_process.kill()	
            print("✓ 后端服务已强制关闭")	
    	
    # 关闭前端	
    if frontend_process:	
        try:	
            frontend_process.terminate()	
            frontend_process.wait(timeout=5)	
            print("✓ 前端服务已关闭")	
        except subprocess.TimeoutExpired:	
            frontend_process.kill()	
            print("✓ 前端服务已强制关闭")	
    	
    print("=" * 60)	
    print("👋 所有服务已停止，再见！\n")	
    sys.exit(0)	
 	
 	
def main():	
    """主函数"""	
    print_banner()	
    	
    try:	
        # 检查依赖	
        if not check_dependencies():	
            print("⚠️ 依赖检查失败，程序退出\n")	
            sys.exit(1)	
        	
        # 启动后端	
        if not start_backend():	
            print("⚠️ 后端启动失败，程序退出\n")	
            sys.exit(1)	
        	
        # 启动前端	
        if not start_frontend():	
            print("⚠️ 前端启动失败，程序退出\n")	
            sys.exit(1)	
        	
        # 输出服务信息	
        log_service_info()	
        	
        # 在后台线程中打开浏览器	
        browser_thread = threading.Thread(target=open_browser, daemon=True)	
        browser_thread.start()	
        	
        # 注册信号处理器，用于优雅关闭	
        signal.signal(signal.SIGINT, handle_shutdown)	
        signal.signal(signal.SIGTERM, handle_shutdown)	
        	
        # 保持主线程运行	
        while True:	
            time.sleep(1)	
            	
            # 检查进程是否还在运行	
            if backend_process and backend_process.poll() is not None:	
                print("\n⚠️ 后端进程已退出，程序停止")	
                break	
            	
            if frontend_process and frontend_process.poll() is not None:	
                print("\n⚠️ 前端进程已退出，程序停止")	
                break	
    	
    except KeyboardInterrupt:	
        handle_shutdown(None, None)	
    except Exception as e:	
        print(f"\n❌ 发生错误: {e}\n")	
        sys.exit(1)	
 	
 	
if __name__ == '__main__':	
    main()
