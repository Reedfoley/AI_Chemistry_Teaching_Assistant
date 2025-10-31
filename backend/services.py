"""
业务逻辑服务层 - 核心化学教学功能调用
"""

import logging


from .reaction_explainer import explain_reaction
from .equation_balancer import balance_equation
from .reaction_image_generator import generate_reaction_image
from .material_recognizer import recognize_material

logger = logging.getLogger(__name__)


class ChemistryService:
    """化学教学助手服务 - 调用各功能模块"""
    
    @staticmethod
    def explain_reaction(reaction: str, api_key: str) -> str:
        """
        化学反应智能讲解
        
        Args:
            reaction: 反应描述
            api_key: ModelScope API密钥（必需）
            
        Returns:
            讲解文本
        """
        try:
            logger.info(f"[调用讲解反应模块] 反应: {reaction}")
            return explain_reaction(reaction, api_key)
        except Exception as e:
            logger.error(f"讲解反应失败: {str(e)}")
            raise

    @staticmethod
    def balance_equation(equation: str, api_key: str) -> str:
        """
        化学方程式自动配平
        
        Args:
            equation: 未配平的方程式
            api_key: ModelScope API密钥（必需）
            
        Returns:
            配平结果
        """
        try:
            logger.info(f"[调用配平方程式模块] 方程式: {equation}")
            return balance_equation(equation, api_key)
        except Exception as e:
            logger.error(f"配平方程式失败: {str(e)}")
            raise

    @staticmethod
    def generate_reaction_image(prompt: str, api_key: str) -> str:
        """
        反应现象文生图
        
        Args:
            prompt: 反应现象描述
            api_key: ModelScope API密钥（必需）
            
        Returns:
            生成的图像URL
        """
        try:
            logger.info(f"[调用图像生成模块] 提示词: {prompt}")
            return generate_reaction_image(prompt, api_key)
        except Exception as e:
            logger.error(f"生成图像失败: {str(e)}")
            raise

    @staticmethod
    def recognize_material(image_url: str, api_key: str) -> str:
        """
        实验物质图生文识别
        
        Args:
            image_url: 图片URL地址
            api_key: ModelScope API密钥（必需）
            
        Returns:
            物质识别结果
        """
        try:
            logger.info(f"[调用物质识别模块] 图片URL: {image_url}")
            return recognize_material(image_url, api_key)
        except Exception as e:
            logger.error(f"识别物质失败: {str(e)}")
            raise
