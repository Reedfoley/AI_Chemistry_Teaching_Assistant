"""
API路由层 - HTTP端点定义
"""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, Response

from .models import (
    ReactionExplainRequest,
    EquationBalanceRequest,
    ReactionImageRequest,
    MaterialRecognizeRequest,
    BaseResponse,
)
from .services import ChemistryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chemistry Teaching"])


# ===================== 健康检查 =====================

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "service": "Chemistry AI Teaching Assistant",
        "version": "1.0.0"
    }


@router.get("/config")
async def get_config():
    """获取API配置信息"""
    return {
        "service_name": "乡村化学教师AI教学助手",
        "version": "1.0.0",
        "features": [
            "化学反应智能讲解",
            "方程式自动配平",
            "反应现象可视化",
            "实验物质识别"
        ],
        "endpoints": {
            "explain_reaction": "/api/reaction/explain",
            "balance_equation": "/api/equation/balance",
            "generate_image": "/api/reaction/image",
            "recognize_material": "/api/material/recognize"
        }
    }


# ===================== 化学功能API =====================

@router.post("/reaction/explain")
async def explain_reaction(request: ReactionExplainRequest) -> Response:
    """
    化学反应智能讲解接口
    
    提供针对不同学龄的化学反应讲解
    
    Example:
        {
            "reaction": "铁与硫酸铜反应",
            "level": "junior"
        }
    """
    try:
        explanation = ChemistryService.explain_reaction(
            reaction=request.reaction,
            level=request.level,
            api_key=request.api_key
        )
        # 返回哯持但不超时的响应
        response = JSONResponse(
            status_code=200,
            content=BaseResponse(success=True, data=explanation).dict(),
            headers={
                'Connection': 'keep-alive',
                'Keep-Alive': 'timeout=300, max=1000',
                'Cache-Control': 'no-cache'
            }
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"讲解反应失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理请求失败")


@router.post("/equation/balance")
async def balance_equation(request: EquationBalanceRequest) -> Response:
    """
    化学方程式自动配平接口
    
    自动配平化学方程式并返回配平步骤
    
    Example:
        {
            "equation": "Fe + O2 → Fe2O3"
        }
    """
    try:
        result = ChemistryService.balance_equation(
            equation=request.equation,
            api_key=request.api_key
        )
        # 返回哯持但不超时的响应
        response = JSONResponse(
            status_code=200,
            content=BaseResponse(success=True, data=result).dict(),
            headers={
                'Connection': 'keep-alive',
                'Keep-Alive': 'timeout=300, max=1000',
                'Cache-Control': 'no-cache'
            }
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"配平方程式失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理请求失败")


@router.post("/reaction/image")
async def generate_reaction_image(request: ReactionImageRequest) -> Response:
    """
    反应现象文生图接口
    
    根据反应现象描述生成对应的图像
    
    Example:
        {
            "prompt": "产生红棕色沉淇，剧烈冒泡并放热"
        }
    """
    try:
        image_url = ChemistryService.generate_reaction_image(
            prompt=request.prompt,
            api_key=request.api_key
        )
        # 返回哯持但不超时的响应
        response = JSONResponse(
            status_code=200,
            content=BaseResponse(success=True, data=image_url).dict(),
            headers={
                'Connection': 'keep-alive',
                'Keep-Alive': 'timeout=300, max=1000',
                'Cache-Control': 'no-cache'
            }
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"生成图像失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理请求失败")


@router.post("/material/recognize")
async def recognize_material(request: MaterialRecognizeRequest) -> Response:
    """
    实验物质图生文识别接口
    
    根据图片URL识别化学实验物质
    
    Example:
        {
            "image_url": "https://example.com/image.jpg"
        }
    """
    try:
        result = ChemistryService.recognize_material(
            image_url=request.image_url,
            api_key=request.api_key
        )
        # 返回沓持但不超时的响应
        response = JSONResponse(
            status_code=200,
            content=BaseResponse(success=True, data=result).dict(),
            headers={
                'Connection': 'keep-alive',
                'Keep-Alive': 'timeout=300, max=1000',
                'Cache-Control': 'no-cache'
            }
        )
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"识别物质失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理请求失败")
