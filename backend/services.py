"""
业务逻辑服务层 - 核心化学教学功能实现
"""

import logging
import json
from math import log
import time
import requests
from typing import Dict, List, Any, Optional

from langchain import agents
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

logger = logging.getLogger(__name__)

def create_agent_llm(model: str, api_key: str) -> ChatOpenAI:
    """
    创建一个Agent LLM
    
    Args:
        model: 模型名称
        api_key: API密钥
        
    Returns:
        ChatOpenAI实例
    """
    return ChatOpenAI(
        api_key=SecretStr(api_key),
        model=model,
        base_url="https://api-inference.modelscope.cn/v1",
        temperature=0.7
    )


class ChemistryService:
    """化学教学助手服务"""
    
    @staticmethod
    def _log_api_usage(operation: str, api_key: str) -> None:
        """
        记录API使用情况
        
        Args:
            operation: 操作描述
            api_key: API密钥
        """
        logger.info(f"使用ModelScope API: {operation}")

    @staticmethod
    def explain_reaction(reaction: str, level: str, api_key: str) -> str:
        """
        化学反应智能讲解
        
        Args:
            reaction: 反应描述
            level: 教学等级 ("junior" 初中 / "senior" 高中)
            api_key: ModelScope API密钥（必需）
            
        Returns:
            讲解文本
        """
        try:
            # 记录API使用
            ChemistryService._log_api_usage(f"讲解反应 - {reaction}", api_key)
            logger.info(f"[开始讲解] 反应: {reaction}，教学阶段: {level}")
            
            # TODO: 实现真实的AI讲解逻辑，可集成：
            # - ModelScope API 调用
            # - 本地知识库查询
            # - 大语言模型调用（OpenAI/Qwen等）
            
            level_name = "初中" if level == "junior" else "高中"
            
            model = create_agent_llm(model="Qwen/Qwen3-VL-30B-A3B-Instruct", api_key=api_key)
            
            agent = create_agent(
                model = model,
                system_prompt = (
                    f"你是一个专业的{level_name}化学讲解助手。"
                    f"请详细讲解以下化学反应的性质、条件和应用意义。"
                ),
            )
            
            # 构建提示词
            prompt = f"请详细讲解以下化学反应的性质、条件和应用意义：{reaction}"
            
            logger.info(f"[调用大模型] 开始处理，请等待...")
            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
            )
            logger.info(f"[大模型回复] 讲解完成")
            
            return response["messages"][-1].content
            
            
        except Exception as e:
            logger.error(f"讲解反应失败: {str(e)}")
            raise

    @staticmethod
    def balance_equation(equation: str, api_key: str) -> Dict[str, Any]:
        """
        化学方程式自动配平
        
        Args:
            equation: 未配平的方程式
            api_key: ModelScope API密钥（必需）
            
        Returns:
            配平结果 {"balanced_equation": "...", "steps": [...]}
        """
        try:
            # 记录API使用
            ChemistryService._log_api_usage(f"配平方程式 - {equation}", api_key)
            
            # TODO: 实现真实的方程式配平逻辑，可使用：
            # - 矩阵求解算法
            # - 第三方化学库（rdkit等）
            # - ModelScope方程式配平模型
            
            model = create_agent_llm(model="Qwen/Qwen3-VL-30B-A3B-Instruct", api_key=api_key)
            
            agent = create_agent(
                model = model,
                system_prompt = (
                    "你是一个专业的化学家。"
                    "请将给定的方程式进行配平，并返回一个字典，"
                    "包含已配平的方程式和步骤。"
                ),
            )
            
            prompt = f"请将给定的方程式进行配平，并返回一个字典，包含已配平的方程式和步骤：{equation}"
            
            logger.info(f"[调用大模型] 配平方程式开始处理，请等待...")
            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
            )
            logger.info(f"[大模型回复] 配平方程式完成")
            
            # 提取大模型返回的文本内容
            return response["messages"][-1].content

        except Exception as e:
            logger.error(f"配平方程式失败: {str(e)}")
            raise

    @staticmethod
    def generate_reaction_image(prompt: str, api_key: str) -> str:
        """
        反应现象文生图 - 调用ModelScope FLUX.1-Krea-dev模型
        
        流程：用户提示词 → Qwen大模型优化提示词 → FLUX模型生成图像
        
        Args:
            prompt: 简要反应现象描述
            api_key: ModelScope API密钥（必需）
            
        Returns:
            图像URL或占位符URL（生成失败时）
        """
        try:
            # 记录API使用
            ChemistryService._log_api_usage(f"生成图像 - {prompt}", api_key)
            
            # 1. 通过Qwen大模型优化用户输入，生成详细、生动的图像生成提示词
            logger.info(f"[Qwen提示词优化] 开始处理用户输入...")
            model = create_agent_llm(model="Qwen/Qwen3-VL-30B-A3B-Instruct", api_key=api_key)
            
            agent = create_agent(
                model=model,
                system_prompt=(
                    "你是一个专业的化学教育和图像描述专家。"
                    "根据用户给出的化学反应现象描述，优化算清并扩展成一个详细、生动、富有视觉感的英文提示词。"
                    "生成的提示词应包括：颜色、物质形态、反应特征、化学下降、环境光线、实验室布置等细节。勿包沿中文。"
                ),
            )
            
            user_prompt = f"请根据以下化学反应现象描述，优化生成一个详细的英文提示词用于图像生成：\n{prompt}"
            
            logger.info(f"[调用Qwen] 优化提示词，请等待...")
            response = agent.invoke(
                {"messages": [{"role": "user", "content": user_prompt}]},
            )
            logger.info(f"[Qwen回复] 提示词优化完成")
            
            detailed_prompt = response["messages"][-1].content
            logger.info(f"[优化后的提示词] {detailed_prompt}")
            
            # 2. 使用优化提示词调用FLUX模型生成图像
            logger.info(f"[提交图像任务] 开始提交到FLUX.1-Krea-dev模型...")
            
            base_url = 'https://api-inference.modelscope.cn/'
            
            # 设置请求头
            common_headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            # 1. 提交异步图像生成任务
            logger.info(f"[提交任务] 开始提交图像生成任务...")
            response = requests.post(
                f"{base_url}v1/images/generations",
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                data=json.dumps({
                    "model": "black-forest-labs/FLUX.1-Krea-dev",
                    "prompt": detailed_prompt
                }, ensure_ascii=False).encode('utf-8')
            )
            response.raise_for_status()
            
            task_id = response.json()["task_id"]
            logger.info(f"[任务ID] {task_id}")
            
            # 2. 轮询任务结果（最多轮询30次，每次间隔10秒）
            max_attempts = 30
            for attempt in range(max_attempts):
                logger.info(f"[轮询中] 第 {attempt + 1}/{max_attempts} 次检查...")
                
                result = requests.get(
                    f"{base_url}v1/tasks/{task_id}",
                    headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                )
                result.raise_for_status()
                data = result.json()
                
                # 任务成功
                if data["task_status"] == "SUCCEED":
                    image_url = data["output_images"][0]
                    logger.info(f"[生成完成] 图像URL: {image_url}")
                    return image_url
                
                # 任务失败
                elif data["task_status"] == "FAILED":
                    logger.error(f"[生成失败] 图像生成任务失败")
                    # 返回占位符URL保证前端正常渲染
                    return "https://via.placeholder.com/512x512?text=Image+Generation+Failed"
                
                # 任务进行中，等待后重试
                time.sleep(10)
            
            # 超时处理
            logger.error(f"[超时] 图像生成任务轮询超时")
            return "https://via.placeholder.com/512x512?text=Generation+Timeout"
            
        except Exception as e:
            logger.error(f"生成图像失败: {str(e)}")
            # 返回占位符URL保证前端正常渲染
            return "https://via.placeholder.com/512x512?text=Generation+Error"

    @staticmethod
    def recognize_material(image_url: str, api_key: str) -> Dict[str, Any]:
        """
        实验物质图生文识别
        
        Args:
            image_url: 图片URL地址
            api_key: ModelScope API密钥（必需）
            
        Returns:
            物质识别结果
        """
        try:
            # 记录API使用
            ChemistryService._log_api_usage("识别实验物质", api_key)
            
            logger.info(f"[识别实验物质] 开始处理图片...")
            logger.info(f"[识别实验物质] 图片URL: {image_url}")
            
            model = create_agent_llm(model="Qwen/Qwen3-VL-30B-A3B-Instruct", api_key=api_key)
            
            agent = create_agent(
                model=model,
                system_prompt=(
                    "你是一个专业的化学教育和图像描述专家。"
                    "根据用户给定的图片，识别并返回一个实验物质名称、别名、物理性质、化学性质、准备方法、安全操作指南等信息。"
                    "请返回一个JSON格式的字符串，包含以上信息。"
                ),
            )
            
            user_prompt = f"请根据图片识别并返回一个实验物质名称、别名、物理性质、化学性质、准备方法、安全操作指南等信息"
            
            logger.info(f"[识别实验物质] 开始调用大模型...")
            result = agent.invoke(
                {"messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image", "url": image_url},
                    ]}]},
            )
            
            logger.info(f"[识别实验物质] 大模型调用完成")
            return result["messages"][-1].content
            
        except Exception as e:
            logger.error(f"识别物质失败: {str(e)}")
            raise
