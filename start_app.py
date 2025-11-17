"""
乡村化学教师AI教学助手 - Python 启动脚本

功能：
- 启动 FastAPI 后端服务（端口 5000）
- 启动前端 HTTP 服务器（端口 8000）
- 自动打开浏览器访问应用

使用：
    python start_app.py
"""

import os
import sys
import time
import logging
import subprocess
import webbrowser
from pathlib import Path
from threading import Thread

# ===================== 日志配置 =====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===================== 配置 =====================

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = SCRIPT_DIR / "backend"
FRONTEND_DIR = SCRIPT_DIR / "frontend"

# 服务配置
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 5000
FRONTEND_HOST = "127.0.0.1"
FRONTEND_PORT = 8000

# 应用 URL
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"


# ===================== 工具函数 =====================

def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 7):
        logger.error("❌ Python 版本过低，需要 Python 3.7 或更高版本")
        sys.exit(1)
    logger.info(f"✓ Python 版本: {sys.version.split()[0]}")


def check_dependencies():
    """检查必要的依赖"""
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            logger.info(f"✓ {name} 已安装")
        except ImportError:
            logger.warning(f"⚠ {name} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        logger.info(f"正在安装缺失的依赖: {', '.join(missing_packages)}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing_packages,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            logger.info("✓ 依赖安装完成")
        except subprocess.CalledProcessError:
            logger.error("❌ 依赖安装失败")
            sys.exit(1)


def start_backend():
    """启动 FastAPI 后端"""
    logger.info(f"启动后端服务 ({BACKEND_URL})...")
    
    try:
        # 使用 uvicorn 启动 FastAPI 应用
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host", BACKEND_HOST,
            "--port", str(BACKEND_PORT),
            "--log-level", "info"
        ]
        
        process = subprocess.Popen(
            cmd,
            cwd=str(SCRIPT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        logger.info(f"✓ 后端服务已启动 (PID: {process.pid})")
        
        # 在后台线程中读取输出
        def read_output():
            try:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(f"[Backend] {line.rstrip()}")
            except:
                pass
        
        output_thread = Thread(target=read_output, daemon=True)
        output_thread.start()
        
        return process
    
    except Exception as e:
        logger.error(f"❌ 后端启动失败: {str(e)}")
        return None


def start_frontend():
    """启动前端 HTTP 服务器"""
    logger.info(f"启动前端服务 ({FRONTEND_URL})...")
    
    try:
        # 使用 Python 内置的 http.server 启动前端
        cmd = [
            sys.executable,
            "-m",
            "http.server",
            str(FRONTEND_PORT),
            "--directory", str(FRONTEND_DIR)
        ]
        
        process = subprocess.Popen(
            cmd,
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        logger.info(f"✓ 前端服务已启动 (PID: {process.pid})")
        
        # 在后台线程中读取输出
        def read_output():
            try:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(f"[Frontend] {line.rstrip()}")
            except:
                pass
        
        output_thread = Thread(target=read_output, daemon=True)
        output_thread.start()
        
        return process
    
    except Exception as e:
        logger.error(f"❌ 前端启动失败: {str(e)}")
        return None


def wait_for_service(url, timeout=60, service_name="Service", endpoint=""):
    """等待服务启动"""
    import urllib.request
    import urllib.error
    
    start_time = time.time()
    attempt = 0
    check_url = url + endpoint
    
    while time.time() - start_time < timeout:
        attempt += 1
        try:
            response = urllib.request.urlopen(check_url, timeout=2)
            logger.info(f"✓ {service_name} 已就绪 (尝试 {attempt} 次)")
            return True
        except urllib.error.HTTPError as e:
            # 404 或其他 HTTP 错误表示服务在运行
            if e.code in [404, 405]:
                logger.info(f"✓ {service_name} 已就绪 (HTTP {e.code})")
                return True
            elapsed = time.time() - start_time
            if attempt % 10 == 0:
                logger.debug(f"等待 {service_name}... ({elapsed:.1f}s)")
            time.sleep(0.5)
        except (urllib.error.URLError, Exception) as e:
            elapsed = time.time() - start_time
            if attempt % 10 == 0:
                logger.debug(f"等待 {service_name}... ({elapsed:.1f}s)")
            time.sleep(0.5)
    
    logger.warning(f"⚠ {service_name} 启动超时 (等待 {timeout}s)")
    return False


def open_browser():
    """打开浏览器访问应用"""
    logger.info(f"打开浏览器访问应用...")
    time.sleep(2)  # 等待服务完全启动
    
    try:
        webbrowser.open(FRONTEND_URL)
        logger.info(f"✓ 浏览器已打开: {FRONTEND_URL}")
    except Exception as e:
        logger.warning(f"⚠ 无法自动打开浏览器: {str(e)}")
        logger.info(f"请手动访问: {FRONTEND_URL}")


def print_startup_info():
    """打印启动信息"""
    print("\n" + "=" * 60)
    print("  🧪 乡村化学教师AI教学助手 - Python 启动脚本")
    print("=" * 60)
    print()
    print(f"  📍 前端地址: {FRONTEND_URL}")
    print(f"  📍 后端地址: {BACKEND_URL}")
    print()
    print("  按 Ctrl+C 停止应用")
    print()
    print("=" * 60 + "\n")


def main():
    """主函数"""
    try:
        # 检查环境
        check_python_version()
        check_dependencies()
        
        # 打印启动信息
        print_startup_info()
        
        # 启动服务
        backend_process = start_backend()
        frontend_process = start_frontend()
        
        if not backend_process or not frontend_process:
            logger.error("❌ 服务启动失败")
            sys.exit(1)
        
        # 等待服务启动
        logger.info("等待服务启动...")
        
        backend_ready = wait_for_service(BACKEND_URL, timeout=60, service_name="后端服务", endpoint="/docs")
        frontend_ready = wait_for_service(FRONTEND_URL, timeout=30, service_name="前端服务", endpoint="/index.html")
        
        if not backend_ready:
            logger.warning(f"⚠ 后端服务可能未完全启动，但继续尝试...")
        
        if not frontend_ready:
            logger.warning(f"⚠ 前端服务可能未完全启动，但继续尝试...")
        
        # 打开浏览器
        open_browser()
        
        # 等待进程
        logger.info("应用运行中...")
        
        while True:
            if backend_process.poll() is not None:
                logger.error("❌ 后端服务已停止")
                break
            if frontend_process.poll() is not None:
                logger.error("❌ 前端服务已停止")
                break
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\n正在关闭应用...")
        
        # 关闭进程
        if backend_process:
            backend_process.terminate()
            logger.info("✓ 后端服务已关闭")
        
        if frontend_process:
            frontend_process.terminate()
            logger.info("✓ 前端服务已关闭")
        
        logger.info("应用已停止")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
