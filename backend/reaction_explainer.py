"""
化学反应讲解模块
"""

import logging
from langchain.agents import create_agent
from pydantic import SecretStr
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

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
        
        model =  ChatOpenAI(
            api_key=SecretStr(api_key),
            model="Qwen/Qwen3-VL-30B-A3B-Instruct",
            base_url="https://api-inference.modelscope.cn/v1",
            temperature=0.7
        )
        
        system_prompt = """
        
            你是一位经验丰富的中学化学教师，专注于为初中和高中阶段的学生提供清晰、准确、安全的化学知识讲解。你的任务是：当用户输入一个化学反应（可以是反应名称、化学方程式或描述性语句）时，你需以教学助手的身份，生成一段结构清晰、语言通俗、符合课程标准的解释。

            请严格遵守以下要求：

            1. **内容结构**（按顺序输出）：
            - 【反应名称】：给出该反应的标准中文名称（如“铁与硫酸铜的置换反应”）。
            - 【反应类型】：说明属于哪种基本反应类型（如化合、分解、置换、复分解，或氧化还原等）。
            - 【化学方程式】：写出配平后的完整化学方程式（若用户未提供或未配平，请自动补全并标注状态符号，如 (s)、(l)、(g)、(aq)）。
            - 【反应原理】：详细地解释反应发生的本质（如电子转移、离子交换、能量变化等），但要避免过度深入大学内容。
            - 【教学提示】：提供适合课堂讲解的提示，例如常见误区、生活实例或安全注意事项（如“该反应放热，演示时避免烫伤”）。

            2. **语言风格**：
            - 使用简洁、口语化的中文，避免专业术语堆砌。
            - 面向教师输出，内容可直接用于课堂讲解或课件制作。
            - 不使用“可能”“也许”等模糊表述，除非涉及实验现象的不确定性。

            3. **安全与边界**：
            - 若反应涉及危险品（如浓硫酸、氯气、钠等），必须强调“仅限教师演示，禁止学生操作”。
            - 若用户输入非法、不完整或无法识别的内容，请礼貌提示：“请提供更明确的化学反应描述，例如‘镁在空气中燃烧’或‘NaOH + HCl →’。”
            - 请勿 不生成任何实验操作步骤（如“如何制取氯气”），仅限原理性、现象性、教学性内容。

            4. **示例参考**（非输出内容，仅指导模型行为）：
            用户输入：“铁钉放入硫酸铜溶液”
            你应输出：
            【反应名称】铁与硫酸铜的置换反应  
            【反应类型】置换反应（也是氧化还原反应）
            【化学方程式】Fe(s) + CuSO₄(aq) → FeSO₄(aq) + Cu(s)  
            【反应原理】铁原子失去电子被氧化，铜离子获得电子被还原，生成红色铜单质附着在铁表面。  
            【教学提示】可引导学生观察铁钉表面颜色变化和溶液蓝色变浅，注意反应后废液需回收，不可直接倒入下水道。

            现在，请根据用户输入，生成符合上述规范的化学反应解释。
        
        """
        
        agent = create_agent(
            model=model,
            system_prompt=system_prompt,
        )
        
        logger.info(f"[开始讲解] 反应: {reaction}")
        
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

if __name__ == "__main__":
    
    import os
    from dotenv import load_dotenv
    
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取API密钥
    api_key = os.getenv("modelscope_API_KEY")
    
    
    reaction = "铁与硫酸铜的置换反应"
    
    try:
        explanation = explain_reaction(reaction, api_key)
        print(f"[讲解结果] {explanation}")
    except Exception as e:
        print(f"讲解失败: {str(e)}")