"""
反应现象文生图模块
"""

import operator
import logging
import time
import json
import requests
from dataclasses import dataclass
from typing import Literal
from typing_extensions import TypedDict, Annotated

from langchain_openai import ChatOpenAI
from langchain.messages import AnyMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)

def generate_reaction_image(prompt: str, api_key: str) -> str:
    """
    Args:
        prompt: 简要反应现象描述
        api_key: ModelScope API密钥（必需）
        
    Returns:
        图像URL或占位符URL（生成失败时）
    """
    try:
        class State(TypedDict):
            messages: Annotated[list[AnyMessage], operator.add]
            prompt: str
            eval_prompt: str
            image_url: str
            eval_image: str
            prompt_generation_count: int
            image_generation_count: int

        generate_prompt_model = ChatOpenAI(
            api_key="ms-fb065d50-eedf-41e5-9bc0-7700362c0c45",
            model="Qwen/Qwen3-VL-30B-A3B-Instruct",
            base_url="https://api-inference.modelscope.cn/v1",
            temperature=0.7
        )
        
        def generate_prompt_node(state: State):
            """
            调用提示词生成模型，生成增强后的提示词
            """
            
            system_prompt = """
            
            你是一位化学教育视觉设计师，专门将简略的化学反应描述转化为适合AI绘图模型（如Stable Diffusion）使用的详细视觉提示词。你的目标是：根据用户输入的化学反应（如“镁条燃烧”或“HCl + NaOH”），自动生成一段**具体、可画、安全、教学友好**的图像生成提示，重点描述**可观察的实验现象与实验场景**，而非抽象原理。

            请严格遵循以下规则：

            1. **输入理解**：
            - 用户输入通常为反应名称、化学方程式或简单描述（如“水电解”“铁钉放入硫酸铜”）。
            - 自动补全反应条件（如常温、加热、通电）和典型实验装置（如试管、烧杯、酒精灯），若未指明则采用**中学课堂最常见演示方式**。

            2. **输出要求**：
            - 输出一段**英文提示词（prompt）**，用于直接输入文生图模型。
            - 提示词必须包含以下要素：
                - **核心现象**：颜色变化、沉淀生成、气体冒出、火焰、烟雾、温度表现（如“试管壁发热”）；
                - **实验器材**：如“glass test tube”、“beaker with blue solution”、“iron nail submerged”；
                - **物质状态与外观**：如“shiny magnesium ribbon”、“reddish-brown solid deposit”、“colorless gas bubbles”；
                - **环境与视角**：如“classroom lab setting, natural lighting, close-up view, clear focus”；
                - **风格限定**：添加“, realistic photo, high detail, educational illustration, no text, no labels” 以确保图像适合教学使用。
            - **禁止包含**：抽象概念（如“oxidation”“electron transfer”）、文字标签、卡通风格、危险操作（如爆炸、浓烟）。

            3. **安全与教学适配**：
            - 所有场景必须是**中学课堂可安全演示**的实验；
            - 若反应通常不可视（如中和反应无现象），需通过**指示剂变色**等方式可视化（如“phenolphthalein turns from pink to colorless”）；
            - 不生成涉及剧毒、强腐蚀或高危操作的图像。

            4. **语言格式**：
            - 输出**纯英文**，逗号分隔关键词，结构清晰；
            - 无需控制长度，越清晰越好
            - 使用现在时、主动描述。

            5. **示例参考**（非输出内容）：

            ▶ 用户输入：“铁和硫酸铜反应”  
            你应输出：
            A shiny iron nail partially submerged in a clear glass beaker filled with bright blue copper sulfate solution, reddish-brown solid copper depositing on the nail surface, solution gradually fading to pale green, classroom lab setting, natural lighting, close-up view, realistic photo, high detail, educational illustration, no text, no labels

            ▶ 用户输入：“镁条燃烧”  
            你应输出：
            A bright white magnesium ribbon burning intensely with a dazzling white flame, producing white powdery ash (magnesium oxide), held by tongs over a ceramic dish, dark background to highlight the glare, sparks flying, safety goggles visible nearby, realistic photo, high detail, educational illustration, no text, no labels

            ▶ 用户输入：“盐酸和氢氧化钠反应”  
            你应输出:
            A clear glass beaker containing colorless hydrochloric acid, a few drops of phenolphththalein indicator turning from pink to colorless as colorless sodium hydroxide solution is added, gentle swirling motion, lab bench with safety equipment in background, soft lighting, close-up realistic photo, high detail, educational illustration, no text, no labels

            现在，请根据用户输入的化学反应，生成符合上述规范的英文文生图提示词。
            
            """
            
            response = generate_prompt_model.invoke(
                [SystemMessage(content=system_prompt)]
                + state["messages"]
            )
            
            return {
                "messages": [response],
                "prompt": response.content,
                "prompt_generation_count": state.get('prompt_generation_count', 0) + 1
            }

        eval_prompt_model = ChatOpenAI(
            api_key="ms-fb065d50-eedf-41e5-9bc0-7700362c0c45",
            model="Qwen/Qwen3-VL-30B-A3B-Instruct",
            base_url="https://api-inference.modelscope.cn/v1",
            temperature=0.7
        )

        def eval_prompt_node(state: State):
            """
            调用提示词评估模型，评估生成的提示词是否符合规范
            """
            system_prompt = """
            
            你是一位专业的化学教育内容审核员，负责检查由AI生成的化学反应绘图提示词（prompt）。你的任务是根据一系列严格的标准评估这些提示词，确保它们包含足够的信息来生成高质量、具体且适合教学使用的图像。如果提示词符合要求，则输出“ok”；若存在问题或缺失关键信息，则提供具体的改进建议。

            请遵循以下指导原则进行评估：

            1. **核心现象**：
            - 必须明确指出实验的主要观察结果（如颜色变化、沉淀形成、气体释放等）。
            - 如果缺少对主要现象的描述，请建议添加。

            2. **实验器材**：
            - 描述中应包括使用的实验器具（如试管、烧杯等），并清晰表明物质的状态（固体、液体、气体）。
            - 若未提及关键实验设备或物质状态，请提出补充建议。

            3. **环境与视角**：
            - 提示词需指定场景设置（如教室实验室）、光源类型（自然光、室内灯）以及观察角度（近距离、特写等）。
            - 如果没有提供关于拍摄角度或光照的信息，请提醒添加。

            4. **风格限定**：
            - 确认提示词末尾包含“, realistic photo, high detail, educational illustration, no text, no labels”以确保图像风格适合教学使用。
            - 如果缺少风格限定，请补充说明。

            5. **安全性与适宜性**：
            - 所有描述都必须适用于中学课堂演示，不应涉及危险操作或材料。
            - 若发现不安全或不适合教学展示的内容，请指明问题并建议替换。

            6. **语言格式**：
            - 提示词应为纯英文，结构清晰，长度适中（80-120词）。
            - 如果语言表达不够清晰或超出推荐长度，请给出编辑建议。

            7. **示例反馈**：

            ▶ 输入：“A shiny iron nail partially submerged in a clear glass beaker filled with bright blue copper sulfate solution, reddish-brown solid copper depositing on the nail surface, classroom lab setting, natural lighting.”
            
            你应输出：  
            “Please add details about the solution's color change and ensure to include 'realistic photo, high detail, educational illustration, no text, no labels' at the end of the prompt.”

            ▶ 输入：“A bright white magnesium ribbon burning intensely with a dazzling white flame, producing white powdery ash (magnesium oxide), held by tongs over a ceramic dish, dark background to highlight the glare, sparks flying, safety goggles visible nearby, realistic photo, high detail, educational illustration, no text, no labels”
            
            你应输出：  
            “ok”

            现在，请根据上述标准评估给定的化学反应绘图提示词，并按照指示输出“ok”或具体的改进建议。
            
            """
            
            
            response = eval_prompt_model.invoke(
                [SystemMessage(content=system_prompt)]
                + [state["prompt"]]
            )
            
            eval_result = response.content.strip()
            
            return {
                "messages": [response],
                "eval_prompt": eval_result,
            }

        @dataclass
        class ContextSchema(TypedDict):
            api_key: str
            
        def generate_image_node(state: State, runtime: Runtime[ContextSchema]):
            """
            调用图像生成模型，根据评估后的提示词生成图像
            """
            api_key = runtime.context["api_key"]
            prompt = state["prompt"]
            
            base_url = 'https://api-inference.modelscope.cn/'
            
            # 设置请求头
            common_headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
                            
            # 提交异步图像生成任务
            response = requests.post(
                f"{base_url}v1/images/generations",
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                data=json.dumps({
                    "model": "black-forest-labs/FLUX.1-Krea-dev",
                    "prompt": prompt
                }, ensure_ascii=False).encode('utf-8')
                )
            response.raise_for_status()
                    
            task_id = response.json()["task_id"]
                    
            # 轮询任务结果（最多轮询30次，每次间隔10秒）  
            max_attempts = 30
            for attempt in range(max_attempts):
                        
                result = requests.get(
                    f"{base_url}v1/tasks/{task_id}",
                    headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                )
                result.raise_for_status()
                data = result.json()
                    
                # 任务成功
                if data["task_status"] == "SUCCEED":
                    image_url = data["output_images"][0]
                    return {
                        "image_url": image_url,
                        "image_generation_count": state.get('image_generation_count', 0) + 1
                        }
                        
                # 任务失败
                elif data["task_status"] == "FAILED":
                    # 返回占位符URL保证前端正常渲染
                    return {
                        "image_url": "https://via.placeholder.com/512x512?text=Image+Generation+Failed",
                        "image_generation_count": state.get('image_generation_count', 0) + 1
                        }
                    
                # 任务进行中，等待后重试
                time.sleep(10)
                            
            # 超时处理
            return {
                "image_url": "https://via.placeholder.com/512x512?text=Generation+Timeout",
                "image_generation_count": state.get('image_generation_count', 0) + 1
                    }
            

        eval_image_model = ChatOpenAI(
            api_key="ms-fb065d50-eedf-41e5-9bc0-7700362c0c45",
            model="Qwen/Qwen3-VL-30B-A3B-Instruct",
            base_url="https://api-inference.modelscope.cn/v1",
            temperature=0.7
        )

        def eval_image_node(state: State):
            """
            调用图像评估模型，根据图像URL评估图像质量
            """
            prompt = state["prompt"]
            image_url = state["image_url"]
            
            system_prompt = """
            
            你是一位具备化学专业知识的多模态AI审核员，能够同时理解一张化学实验图像和一段英文文生图提示词（prompt）。你的任务是：判断该图像是否准确、完整地呈现了提示词中描述的化学反应现象、实验器材、颜色变化、物质状态等关键视觉元素。

            请严格按以下流程执行：

            1. **输入说明**：
            - 你会收到两部分内容：
                - 【提示词】：一段用于生成图像的英文描述（如 "A shiny iron nail in blue solution..."）；
                - 【图像】：由文生图模型根据该提示词生成的图片。
            - 请基于化学常识和视觉细节，评估图像与提示词的一致性。

            2. **审核标准**：
            - **现象匹配**：图像是否呈现了提示词中描述的核心现象（如“蓝色溶液变浅绿”“红色沉淀”“白色火焰”）？
            - **器材正确**：是否包含指定的实验器具（如烧杯、试管、酒精灯）？摆放是否合理？
            - **物质外观**：颜色、状态（固体/液体/气体）、形态（晶体/粉末/气泡）是否与提示一致？
            - **安全与教学适宜性**：图像是否符合中学课堂安全规范？无危险、无误导？
            - 若图像缺失关键元素、颜色错误、现象不符、或出现提示词未提及的干扰内容（如文字、卡通风格、无关人物），则视为不一致。

            3. **输出规则**：
            - **如果图像与提示词高度一致，且适合教学使用** → 仅输出：  
                `ok`
            - **如果存在不一致或缺陷** → 输出一段**简洁的英文优化建议**，格式为：  
                `Refine prompt to: [改进后的完整提示词]`  
                改进建议必须：
                - 保留原提示词合理部分；
                - 补充缺失的视觉细节（如“add reddish-brown deposit on iron nail”）；
                - 修正错误描述（如将“white precipitate”改为“blue precipitate”）；
                - 强化关键特征以提升生成准确性。

            4. **语言与边界**：
            - 输出必须为**纯英文**（因用于下游文生图模型）；
            - 不解释原因，不输出中文，不评价图像质量（如“模糊”“低分辨率”），仅关注**语义一致性**；
            - 不引入新化学知识，仅基于提示词已有意图进行修正。

            5. **示例参考**：

            ▶ 【提示词】  
            "A shiny iron nail in bright blue copper sulfate solution, reddish-brown copper forming on surface, solution turning pale green, glass beaker, classroom setting, realistic photo, no text"  
            【图像】  
            （图像显示：铁钉在蓝色溶液中，表面有红棕色固体，溶液呈浅绿色）  
            → 输出：  
            `ok`

            ▶ 【提示词】  
            "Magnesium ribbon burning with bright white flame, producing white ash, dark background"  
            【图像】  
            （图像显示：镁条在燃烧，但火焰为黄色，且无白色灰烬）  
            → 输出：  
            `Refine prompt to: Magnesium ribbon burning with intense bright white flame (not yellow), producing visible white powdery ash (magnesium oxide), dark background to enhance contrast, realistic photo, high detail, educational illustration, no text, no labels`

            ▶ 【提示词】  
            "Hydrochloric acid and sodium hydroxide reaction with phenolphthalein, color change from pink to colorless"  
            【图像】  
            （图像显示：烧杯中液体为蓝色，无颜色过渡）  
            → 输出：  
            `Refine prompt to: Clear beaker with pink solution (due to phenolphthalein in basic NaOH), gradually turning colorless as HCl is added, close-up view of swirling liquid, lab bench background, realistic photo, high detail, educational illustration, no text, no labels`

            现在，请根据提供的【提示词】和【图像】，输出“ok”或“Refine prompt to: [...]”。
            
            """
            
            response = eval_image_model.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"【提示词】: {prompt}\n【图像】: {image_url}"}
            ])
            
            eval_result = response.content.strip()
            
            output = {
                "messages": [response],
                "eval_image": eval_result,
            }
            
            if "refine prompt to:" in eval_result.lower():
                new_prompt = eval_result.split("Refine prompt to: ", 1)[-1].strip()
                output["prompt"] = new_prompt

            return output
            
        builder  = StateGraph(State, context_schema=ContextSchema)

        builder.add_node("generate_prompt_node", generate_prompt_node)
        builder.add_node("eval_prompt_node", eval_prompt_node)
        builder.add_node("generate_image_node", generate_image_node)
        builder.add_node("eval_image_node", eval_image_node)

        builder.add_edge(START, "generate_prompt_node")
        builder.add_edge("generate_prompt_node", "eval_prompt_node")

        def route_1(state: State) -> Literal["generate_prompt_node", "generate_image_node"]:
            if state["eval_prompt"] == "ok":
                return "generate_image_node"
            elif state["prompt_generation_count"] > 2:
                return "generate_image_node"
            else:
                return "generate_prompt_node"
        builder.add_conditional_edges("eval_prompt_node", route_1)

        builder.add_edge("generate_image_node", "eval_image_node")

        def route_2(state: State) -> Literal["generate_image_node", END]:
            if state["eval_image"] == "ok":
                return END
            elif state["image_generation_count"] > 2:
                return END
            else:
                return "generate_image_node"
        builder.add_conditional_edges("eval_image_node", route_2)
            
        graph = builder.compile()
        
        response = graph.invoke({"messages": [{"role": "user", "content": prompt}]}, context={"api_key": api_key})
        
        return response["image_url"]
        
    except Exception as e:
        logger.error(f"生成图像失败: {str(e)}")
        # 返回占位符URL保证前端正常渲染
        return "https://via.placeholder.com/512x512?text=Generation+Error"
