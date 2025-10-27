import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 使用条件导入，解决直接运行时的相对导入问题
try:
    # 当作为模块导入时（正常情况）
    from .routes import router
    from .models import BaseResponse
except ImportError:
    # 当直接运行时
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend.routes import router
    from backend.models import BaseResponse

# ===================== 日志配置 =====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===================== 应用初始化 =====================

def create_app() -> FastAPI:
    """创建并配置FastAPI应用"""
    
    app = FastAPI(
        title="乡村化学教师AI教学助手",
        description="智能讲解 · 方程式配平 · 反应现象可视化 · 实验物质识别",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS 配置必须在最前面
    # 允许所有源进行跨域请求（开发环境）
    # 生产环境应限制具体的域名
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:5000",
            "http://localhost:5173",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8000",
            "*",  # 开发环境允许所有源
        ],
        allow_credentials=False,  # 当 allow_origins 包含 "*" 时，必须设置为 False
        allow_methods=["*"],  # 允许所有 HTTP 方法
        allow_headers=["*"],  # 允许所有请求头
        expose_headers=["*"],  # 暴露所有响应头
        max_age=600,  # OPTIONS 请求缓存时间（秒）
    )
    
    # 包含路由
    app.include_router(router)
    
    # 全局异常处理
    setup_exception_handlers(app)
    
    # 应用启动事件
    @app.on_event("startup")
    async def startup_event():
        logger.info("应用启动 - 乡村化学教师AI教学助手 v2.0.0")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("应用关闭")
    
    return app


# ===================== 异常处理 =====================

def setup_exception_handlers(app: FastAPI) -> None:
    """设置全局异常处理器"""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc: HTTPException):
        """处理HTTP异常"""
        return JSONResponse(
            status_code=exc.status_code,
            content=BaseResponse(
                success=False,
                error=exc.detail
            ).dict()
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc: ValueError):
        """处理值错误"""
        return JSONResponse(
            status_code=400,
            content=BaseResponse(
                success=False,
                error=f"请求参数错误: {str(exc)}"
            ).dict()
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        """处理未捕获的异常"""
        logger.error(f"未处理的异常: {type(exc).__name__}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                success=False,
                error="内部服务器错误"
            ).dict()
        )


# ===================== 应用实例 =====================

app = create_app()


# ===================== 本地运行 =====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        reload=True
    )
