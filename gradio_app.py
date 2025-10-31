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

def handle_explain_reaction(reaction: str) -> str:
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
    """创建 Gradio 界面 - 设计风格与 HTML 版本一致"""
    
    # 自定义 CSS 样式
    custom_css = """
    /* 全局样式 */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #64748b;
        --success-color: #16a34a;
        --error-color: #dc2626;
        --warning-color: #ea580c;
        --border-radius: 12px;
        --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* 容器样式 */
    .gradio-container {
        max-width: 1200px;
        margin: 0 auto;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* 标题区域 */
    .gradio-container h1 {
        color: #1e293b;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #2563eb 0%, #0891b2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .gradio-container > p {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }
    
    /* API 密钥设置区域 */
    .api-key-section {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
    }
    
    .api-key-section h3 {
        color: #1e293b;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    
    .api-key-section p {
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    .api-key-section a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
    }
    
    /* 标签页样式 */
    .tabs {
        margin: 2rem 0;
    }
    
    .gradio-tabs {
        background: transparent;
    }
    
    .gradio-tabitem {
        background: transparent;
    }
    
    /* 卡片样式 */
    .tab-content {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow);
        border: 1px solid #e2e8f0;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .card-header h2 {
        margin: 0;
        color: #1e293b;
        font-size: 1.5rem;
    }
    
    /* 使用说明 */
    .instructions {
        background: #f0f9ff;
        border-left: 4px solid var(--primary-color);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .instructions h3 {
        color: #1e293b;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    
    .instructions ul {
        margin: 0;
        padding-left: 1.5rem;
        color: #475569;
    }
    
    .instructions li {
        margin-bottom: 0.25rem;
        line-height: 1.6;
    }
    
    /* 输入框样式 */
    .gradio-textbox input,
    .gradio-textbox textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .gradio-textbox input:focus,
    .gradio-textbox textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* 按钮样式 */
    .gradio-button {
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .gradio-button.primary {
        background: linear-gradient(135deg, var(--primary-color) 0%, #0891b2 100%);
        color: white;
    }
    
    .gradio-button.primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    .gradio-button.secondary {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    
    .gradio-button.secondary:hover {
        background: #e2e8f0;
    }
    
    /* 结果区域 */
    .result-area {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .result-title {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .result-title::before {
        content: "✓";
        color: var(--success-color);
        margin-right: 0.5rem;
        font-weight: bold;
    }
    
    .result-content {
        color: #475569;
        line-height: 1.8;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    
    /* 加载动画 */
    .loading {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #e2e8f0;
        border-top-color: var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: var(--primary-color);
        font-weight: 500;
    }
    
    /* 错误消息 */
    .error-message {
        background: #fef2f2;
        border: 2px solid #fecaca;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        display: none;
    }
    
    .error-message.show {
        display: block;
    }
    
    /* 成功消息 */
    .success-message {
        background: #f0fdf4;
        border: 2px solid #bbf7d0;
        color: #166534;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        display: none;
    }
    
    .success-message.show {
        display: block;
    }
    
    /* 页脚 */
    .gradio-container footer {
        text-align: center;
        color: #64748b;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #e2e8f0;
        font-size: 0.95rem;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container {
            margin: 0;
            padding: 1rem;
        }
        
        .gradio-container h1 {
            font-size: 1.8rem;
        }
        
        .tab-content {
            padding: 1.5rem;
        }
    }
    """
    
    with gr.Blocks(
        title="乡村化学教师AI教学助手",
        css=custom_css
    ) as demo:
        
        # 标题部分
        gr.Markdown("# 🧪 乡村化学教师AI教学助手")
        gr.Markdown("**智能讲解** · **方程式配平** · **反应现象可视化** · **实验物质识别**")
        
        # API密钥设置区域
        with gr.Group(elem_classes="api-key-section"):
            gr.Markdown("### ⚙️ API密钥设置")
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
                value="❌ 未设置API密钥",
                show_label=True
            )
        
        save_btn.click(
            fn=set_api_key,
            inputs=[api_key_input],
            outputs=[api_status]
        )
        
        # 主功能区域
        with gr.Tabs():
            
            # 标签1：反应讲解
            with gr.TabItem(label="📚 化学反应智能讲解", id="tab1"):
                with gr.Group(elem_classes="tab-content"):
                    gr.Markdown("""### 使用说明
                    - 输入化学反应名称或描述（如"铁与硫酸铜反应"）
                    - 点击"生成讲解"获取详细反应原理说明
                    """)
                    
                    reaction_input = gr.Textbox(
                        label="请输入化学反应",
                        placeholder="例如：铁与硫酸铜反应",
                        lines=2
                    )
                    
                    with gr.Row():
                        explain_btn = gr.Button("🚀 生成讲解", variant="primary", scale=1)
                        clear_btn = gr.Button("🗑️ 清空", scale=1)
                    
                    explain_output = gr.Textbox(
                        label="讲解结果",
                        lines=12,
                        interactive=False,
                        show_copy_button=True
                    )
                    
                    explain_btn.click(
                        fn=handle_explain_reaction,
                        inputs=[reaction_input],
                        outputs=[explain_output]
                    )
                    
                    clear_btn.click(
                        fn=lambda: ("", ""),
                        outputs=[reaction_input, explain_output]
                    )
            
            # 标签2：方程式配平
            with gr.TabItem(label="⚖️ 化学方程式自动配平", id="tab2"):
                with gr.Group(elem_classes="tab-content"):
                    gr.Markdown("""### 使用说明
                    - 输入未配平的化学方程式（如"Fe + O2 → Fe2O3"）
                    - 点击"配平方程式"获取配平结果和步骤
                    - 支持查看详细的配平过程
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
                        lines=12,
                        interactive=False,
                        show_copy_button=True
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
                with gr.Group(elem_classes="tab-content"):
                    gr.Markdown("""### 使用说明
                    - 输入反应现象描述（如"产生红棕色沉淀"）
                    - 点击"生成图像"获取对应的反应现象图片
                    - 可用于课堂直观展示实验效果
                    """)
                    
                    prompt_input = gr.Textbox(
                        label="请输入反应现象描述",
                        placeholder="例如：产生红棕色沉淀，剧烈冒泡并放热",
                        lines=3
                    )
                    
                    with gr.Row():
                        image_btn = gr.Button("🎬 生成图像", variant="primary", scale=1)
                        clear_btn = gr.Button("🗑️ 清空", scale=1)
                    
                    image_output = gr.Image(
                        label="生成的反应现象图像",
                        type="filepath"
                    )
                    
                    image_btn.click(
                        fn=handle_generate_image,
                        inputs=[prompt_input],
                        outputs=[image_output]
                    )
                    
                    clear_btn.click(
                        fn=lambda: ("", None),
                        outputs=[prompt_input, image_output]
                    )
            
            # 标签4：物质识别
            with gr.TabItem(label="🔍 实验物质图生文识别", id="tab4"):
                with gr.Group(elem_classes="tab-content"):
                    gr.Markdown("""### 使用说明
                    - 上传常见化学物质或实验器材的图片
                    - AI将自动识别物质并生成简明说明
                    - 包括可能的化学名称、性质及安全制备方法
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
                        lines=12,
                        interactive=False,
                        show_copy_button=True
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
            "---\n🎓 **乡村化学教师AI教学助手** | 专为乡村教育设计，提升教学效率，弥补实验资源不足"
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
