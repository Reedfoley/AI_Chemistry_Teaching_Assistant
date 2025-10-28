"""
Gradio 应用 - 乡村化学教师AI教学助手

这是一个完整的 Gradio 应用，适配 ModelScope 创空间部署

功能：
- 化学反应智能讲解
- 化学方程式自动配平
- 反应现象文生图展示
- 实验物质图生文识别

使用：
    python gradio_app.py
"""

import os
import sys
import logging
import base64
from pathlib import Path

# 自动安装依赖
def ensure_dependencies():
    """确保必要的依赖已安装"""
    try:
        import gradio
    except ImportError:
        print("正在安装 gradio...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio", "-q"])
    
    # 尝试导入后端服务
    try:
        from backend.services import ChemistryService
        return True
    except ImportError:
        print("警告：后端服务不可用，将运行演示模式")
        return False

# 检查依赖
HAS_BACKEND = ensure_dependencies()

import gradio as gr

if HAS_BACKEND:
    from backend.services import ChemistryService
else:
    ChemistryService = None

# ===================== 日志配置 =====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===================== 全局变量 =====================

global_api_key = None


# ===================== API 密钥管理 =====================

def set_api_key(api_key: str) -> str:
    """设置API密钥"""
    global global_api_key
    if not api_key or not api_key.strip():
        return "❌ API密钥不能为空"
    global_api_key = api_key.strip()
    logger.info("API密钥已保存")
    return "✅ API密钥已保存"


# ===================== 功能处理器 =====================

def handle_explain_reaction(reaction: str, level: str) -> str:
    """处理化学反应讲解"""
    global global_api_key
    
    if not global_api_key:
        return "❌ 请先设置API密钥"
    
    if not reaction or not reaction.strip():
        return "❌ 请输入化学反应描述"
    
    if not ChemistryService:
        return "❌ 后端服务不可用"
    
    try:
        logger.info(f"处理反应讲解: {reaction}")
        result = ChemistryService.explain_reaction(
            reaction=reaction,
            level=level,
            api_key=global_api_key
        )
        return result
    except Exception as e:
        logger.error(f"反应讲解失败: {str(e)}")
        return f"❌ 讲解失败: {str(e)}"


def handle_balance_equation(equation: str) -> str:
    """处理方程式配平"""
    global global_api_key
    
    if not global_api_key:
        return "❌ 请先设置API密钥"
    
    if not equation or not equation.strip():
        return "❌ 请输入化学方程式"
    
    if not ChemistryService:
        return "❌ 后端服务不可用"
    
    try:
        logger.info(f"处理方程式配平: {equation}")
        result = ChemistryService.balance_equation(
            equation=equation,
            api_key=global_api_key
        )
        return str(result)
    except Exception as e:
        logger.error(f"方程式配平失败: {str(e)}")
        return f"❌ 配平失败: {str(e)}"


def handle_generate_image(prompt: str) -> str:
    """处理图像生成"""
    global global_api_key
    
    if not global_api_key:
        return "❌ 请先设置API密钥"
    
    if not prompt or not prompt.strip():
        return "❌ 请输入反应现象描述"
    
    if not ChemistryService:
        return "❌ 后端服务不可用"
    
    try:
        logger.info(f"处理图像生成: {prompt}")
        result = ChemistryService.generate_reaction_image(
            prompt=prompt,
            api_key=global_api_key
        )
        return result
    except Exception as e:
        logger.error(f"图像生成失败: {str(e)}")
        return f"❌ 生成失败: {str(e)}"


def handle_recognize_material(image) -> str:
    """处理物质识别"""
    global global_api_key
    
    if not global_api_key:
        return "❌ 请先设置API密钥"
    
    if image is None:
        return "❌ 请上传图片"
    
    if not ChemistryService:
        return "❌ 后端服务不可用"
    
    try:
        logger.info("处理物质识别")
        
        # Gradio Image 组件返回的是本地文件路径
        # 需要转换为 base64 格式供后端使用
        image_path = image if isinstance(image, str) else str(image)
        
        # 检查文件是否存在
        if not Path(image_path).exists():
            return f"❌ 图片文件不存在: {image_path}"
        
        # 读取文件并转换为 base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 确定图片类型
        image_ext = Path(image_path).suffix.lower()
        mime_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
        }
        mime_type = mime_type_map.get(image_ext, 'image/jpeg')
        
        # 构造 data URL
        image_url = f"data:{mime_type};base64,{image_data}"
        
        result = ChemistryService.recognize_material(
            image_url=image_url,
            api_key=global_api_key
        )
        return str(result)
    except Exception as e:
        logger.error(f"物质识别失败: {str(e)}")
        return f"❌ 识别失败: {str(e)}"


# ===================== UI 创建 =====================

def create_interface():
    """创建 Gradio 界面"""
    
    with gr.Blocks(title="乡村化学教师AI教学助手") as demo:
        
        # 标题
        gr.Markdown(
            """# 🧪 乡村化学教师AI教学助手
            
            智能讲解 · 方程式配平 · 反应现象可视化 · 实验物质识别
            """
        )
        
        # API密钥设置
        gr.Markdown("#### ⚙️ API密钥设置")
        gr.Markdown("请前往 [ModelScope控制台](https://www.modelscope.cn/my/myaccesstoken) 获取您的访问令牌")
            
        with gr.Row():
            api_key_input = gr.Textbox(
                label="API密钥",
                placeholder="请输入您的 ModelScope API KEY",
                type="password",
                scale=4
            )
            save_btn = gr.Button("💾 保存", scale=1, variant="primary")
        
        api_status = gr.Textbox(
            label="状态",
            interactive=False,
            value="❌ 未设置API密钥"
        )
        
        save_btn.click(
            fn=set_api_key,
            inputs=[api_key_input],
            outputs=[api_status]
        )
        
        # 功能标签
        with gr.Tabs():
            
            # 标签1：反应讲解
            with gr.TabItem(label="📚 化学反应智能讲解", id="tab1"):
                gr.Markdown("""### 使用说明
                1. 输入化学反应名称或描述（如"铁与硫酸铜反应"）
                2. 选择适用的教学阶段（初中/高中）
                3. 点击"生成讲解"获取详细反应原理说明
                """)
                
                with gr.Row():
                    reaction_input = gr.Textbox(
                        label="请输入化学反应",
                        placeholder="例如：铁与硫酸铜反应",
                        scale=3
                    )
                    level_select = gr.Dropdown(
                        choices=[("初中", "junior"), ("高中", "senior")],
                        value="junior",
                        label="教学阶段",
                        scale=1
                    )
                
                with gr.Row():
                    explain_btn = gr.Button("🚀 生成讲解", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ 清空", scale=1)
                
                explain_output = gr.Textbox(
                    label="讲解结果",
                    lines=10,
                    interactive=False
                )
                
                explain_btn.click(
                    fn=handle_explain_reaction,
                    inputs=[reaction_input, level_select],
                    outputs=[explain_output]
                )
                
                clear_btn.click(
                    fn=lambda: ("", "junior", ""),
                    outputs=[reaction_input, level_select, explain_output]
                )
            
            # 标签2：方程式配平
            with gr.TabItem(label="⚖️ 化学方程式自动配平", id="tab2"):
                gr.Markdown("""### 使用说明
                1. 输入未配平的化学方程式（如"Fe + O2 → Fe2O3"）
                2. 点击"配平方程式"获取配平结果和步骤
                3. 支持查看详细的配平过程
                """)
                
                equation_input = gr.Textbox(
                    label="请输入未配平的化学方程式",
                    placeholder="例如：Fe + O2 → Fe2O3",
                    lines=2
                )
                
                with gr.Row():
                    balance_btn = gr.Button("⚙️ 配平方程式", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ 清空", scale=1)
                
                balance_output = gr.Textbox(
                    label="配平结果",
                    lines=10,
                    interactive=False
                )
                
                balance_btn.click(
                    fn=handle_balance_equation,
                    inputs=[equation_input],
                    outputs=[balance_output]
                )
                
                clear_btn.click(
                    fn=lambda: ("", ""),
                    outputs=[equation_input, balance_output]
                )
            
            # 标签3：图像生成
            with gr.TabItem(label="🎨 反应现象文生图展示", id="tab3"):
                gr.Markdown("""### 使用说明
                1. 输入反应现象描述（如"产生红棕色沉淀"）
                2. 点击"生成图像"获取对应的反应现象图片
                3. 可用于课堂直观展示实验效果
                """)
                
                prompt_input = gr.Textbox(
                    label="请输入反应现象描述",
                    placeholder="例如：产生红棕色沉淀，剧烈冒泡并放热",
                    lines=3
                )
                
                with gr.Row():
                    image_btn = gr.Button("🎬 生成图像", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ 清空", scale=1)
                
                image_output = gr.Textbox(
                    label="生成的反应现象图像 URL",
                    interactive=False
                )
                
                image_btn.click(
                    fn=handle_generate_image,
                    inputs=[prompt_input],
                    outputs=[image_output]
                )
                
                clear_btn.click(
                    fn=lambda: ("", ""),
                    outputs=[prompt_input, image_output]
                )
            
            # 标签4：物质识别
            with gr.TabItem(label="🔍 实验物质图生文识别", id="tab4"):
                gr.Markdown("""### 使用说明
                1. 上传常见化学物质或实验器材的图片
                2. AI将自动识别物质并生成简明说明
                3. 包括可能的化学名称、性质及安全制备方法
                """)
                
                image_input = gr.Image(
                    label="请上传化学物质或实验器材图片",
                    type="filepath"
                )
                
                with gr.Row():
                    recognize_btn = gr.Button("🔬 识别物质", variant="primary", scale=1)
                    clear_btn = gr.Button("🗑️ 清空", scale=1)
                
                material_output = gr.Textbox(
                    label="识别结果",
                    lines=10,
                    interactive=False
                )
                
                recognize_btn.click(
                    fn=handle_recognize_material,
                    inputs=[image_input],
                    outputs=[material_output]
                )
                
                clear_btn.click(
                    fn=lambda: (None, ""),
                    outputs=[image_input, material_output]
                )
        
        # 页脚
        gr.Markdown(
            """---
            乡村化学教师AI教学助手 © 2024 | 专为乡村教育设计，提升教学效率，弥补实验资源不足
            """
        )
    
    return demo


if __name__ == "__main__":
    # 创建并启动应用
    app = create_interface()
    
    # 获取端口配置
    port = int(os.environ.get('GRADIO_PORT', os.environ.get('PORT', '7860')))
    
    logger.info(f"启动 Gradio 应用，端口: {port}")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        show_error=True,
        debug=True
    )
