"""
数据模型层 - 请求/响应数据定义
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any, Literal


# ===================== 请求模型 =====================

class ReactionExplainRequest(BaseModel):
    """化学反应讲解请求"""
    reaction: str = Field(..., min_length=1, description="反应描述")
    api_key: str = Field(..., min_length=1, description="ModelScope API密钥（必需）")

    class Config:
        example = {
            "reaction": "铁与硫酸铜反应"
        }


class EquationBalanceRequest(BaseModel):
    """方程式配平请求"""
    equation: str = Field(..., min_length=1, description="化学方程式")
    api_key: str = Field(..., min_length=1, description="ModelScope API密钥（必需）")

    class Config:
        example = {
            "equation": "Fe + O2 → Fe2O3"
        }


class ReactionImageRequest(BaseModel):
    """反应现象文生图请求"""
    prompt: str = Field(..., min_length=1, description="图像生成提示词")
    api_key: str = Field(..., min_length=1, description="ModelScope API密钥（必需）")

    class Config:
        example = {
            "prompt": "产生红棕色沉淀，剧烈冒泡并放热"
        }


class MaterialRecognizeRequest(BaseModel):
    """物质识别请求"""
    image_url: str = Field(..., min_length=1, description="图片URL地址")
    api_key: str = Field(..., min_length=1, description="ModelScope API密钥（必需）")

    class Config:
        example = {
            "image_url": "https://example.com/image.jpg"
        }


# ===================== 响应模型 =====================

class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = Field(..., description="操作是否成功")
    data: Optional[Any] = Field(default=None, description="响应数据")
    error: Optional[str] = Field(default=None, description="错误信息")

    class Config:
        example = {
            "success": True,
            "data": "示例数据",
            "error": None
        }
