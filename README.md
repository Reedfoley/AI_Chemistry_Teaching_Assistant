# 🧪 乡村化学教师AI教学助手

## 📋 项目概述

**乡村化学教师AI教学助手** 是一个专为乡村中学化学教学设计的智能教学平台。通过集成先进的AI大模型（阿里通义千问、FLUX图像生成等），为资源受限的乡村学校提供：

- **智能讲解**：自动生成清晰、通俗的化学反应原理说明
- **方程式配平**：一键自动配平化学方程式，附带详细步骤
- **反应现象可视化**：根据反应描述生成逼真的实验现象图像
- **物质识别**：上传图片自动识别化学物质和实验器材

该项目旨在**弥补乡村学校实验资源不足**，帮助教师提升教学效率，让学生获得更好的化学学习体验。

---

## ✨ 核心功能说明

### 1️⃣ 化学反应智能讲解
**功能描述**：输入任意化学反应，系统自动生成结构化的讲解内容。

**输出内容包括**：
- 反应名称与类型（化合、分解、置换、复分解等）
- 配平后的完整化学方程式
- 反应原理与电子转移过程
- 教学提示与安全注意事项

**应用场景**：
- 教师快速备课，生成课堂讲解稿
- 学生自主学习，理解反应原理
- 制作教学课件的内容素材

**示例**：
```
输入：铁与硫酸铜反应
输出：
【反应名称】铁与硫酸铜的置换反应
【反应类型】置换反应（氧化还原反应）
【化学方程式】Fe(s) + CuSO₄(aq) → FeSO₄(aq) + Cu(s)
【反应原理】铁原子失去电子被氧化，铜离子获得电子被还原...
【教学提示】可引导学生观察铁钉表面颜色变化...
```

---

### 2️⃣ 化学方程式自动配平
**功能描述**：输入未配平的化学方程式，系统自动完成配平并解释步骤。

**输出内容包括**：
- 原始输入的规范化展示
- 问题诊断（如原子不守恒、物质缺失）
- 配平后的完整方程式
- 详细的配平步骤说明
- 教学提示与反应条件说明

**应用场景**：
- 学生作业检查与自学
- 教师快速验证方程式
- 理解配平方法与原理

**示例**：
```
输入：Fe + O2 = Fe2O3
输出：
【配平结果】4Fe + 3O₂ → 2Fe₂O₃
【配平步骤】
1. Fe₂O₃中有2个Fe和3个O，O₂含2个氧...
2. 取氧原子最小公倍数6...
```

---

### 3️⃣ 反应现象文生图展示
**功能描述**：根据反应现象描述，使用AI图像生成技术生成逼真的实验现象图像。

**工作流程**：
1. 用户输入反应现象描述（如"产生红棕色沉淀"）
2. 系统生成详细的英文图像提示词
3. 评估提示词的完整性和准确性
4. 调用FLUX图像生成模型生成图像
5. 评估生成图像与提示词的一致性
6. 返回最终图像或优化后的版本

**应用场景**：
- 课堂直观展示实验效果（特别是危险实验）
- 制作教学课件和教材
- 学生理解反应现象

**特点**：
- 支持多轮优化，确保图像质量
- 自动处理提示词优化
- 返回教学友好的图像

---

### 4️⃣ 实验物质图生文识别
**功能描述**：上传化学物质或实验器材的图片，系统自动识别并提供详细说明。

**输出内容包括**：
- 物质/器材的标准名称
- 典型视觉特征描述
- 主要用途与应用
- 安全提示与注意事项
- 教学建议与演示方法

**应用场景**：
- 学生识别实验器材
- 教师快速查询物质信息
- 安全教育与实验指导

**示例**：
```
输入：蓝色晶体图片
输出：
【识别结果】五水合硫酸铜（CuSO₄·5H₂O）
【典型特征】亮蓝色透明晶体，常呈块状或粉末状
【主要用途】检验水的存在，配制波尔多液
【安全提示】有一定毒性，避免误食或长时间皮肤接触
【教学建议】可加热演示其失去结晶水变为白色...
```

---

## 🏗️ 项目架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     用户界面层 (Frontend)                      │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐
│  │  讲解反应    │  配平方程式  │  文生图展示  │  物质识别    │
│  └──────────────┴──────────────┴──────────────┴──────────────┘
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                   API 路由层 (FastAPI)                        │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐
│  │ /reaction/   │ /equation/   │ /reaction/   │ /material/   │
│  │  explain     │   balance    │    image     │  recognize   │
│  └──────────────┴──────────────┴──────────────┴──────────────┘
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   业务逻辑层 (Services)                       │
│              ChemistryService 统一调度中心
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   功能模块层 (Modules)                        │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐
│  │ Reaction     │ Equation     │ Image        │ Material     │
│  │ Explainer    │ Balancer     │ Generator    │ Recognizer   │
│  └──────────────┴──────────────┴──────────────┴──────────────┘
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   AI 模型层 (LLM & Vision)                    │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐
│  │ Qwen3 Chat   │ Qwen3 Chat   │ FLUX Image   │ Qwen3 Vision │
│  │ (讲解)       │ (配平)       │ (生成)       │ (识别)       │
│  └──────────────┴──────────────┴──────────────┴──────────────┘
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 项目文件结构

```
chemistry-ai-teacher/
│
├── README.md                          # 项目说明文档（本文件）
├── requirements.txt                   # Python 依赖列表
├── .env                              # 环境变量配置（API密钥等）
│
├── app.py                            # Gradio 应用入口（可选UI）
├── start_app.py                      # 完整应用启动脚本
├── backend_start.py                  # 后端单独启动脚本
├── frontend_start.py                 # 前端单独启动脚本
│
├── backend/                          # 后端服务目录
│   ├── __init__.py
│   ├── main.py                       # FastAPI 应用主文件
│   ├── routes.py                     # API 路由定义
│   ├── models.py                     # 数据模型（Pydantic）
│   ├── services.py                   # 业务逻辑服务层
│   │
│   ├── reaction_explainer.py         # 化学反应讲解模块
│   ├── equation_balancer.py          # 方程式配平模块
│   ├── reaction_image_generator.py   # 反应现象文生图模块
│   └── material_recognizer.py        # 物质识别模块
│
└── frontend/                         # 前端应用目录
    ├── index.html                    # 主页面
    └── assets/
        ├── css/                      # 样式文件
        │   ├── variables.css         # CSS 变量定义
        │   ├── base.css              # 基础样式
        │   ├── layout.css            # 布局样式
        │   ├── components.css        # 组件样式
        │   ├── animations.css        # 动画效果
        │   └── responsive.css        # 响应式设计
        └── js/                       # JavaScript 文件
            ├── config.js             # 配置管理
            ├── api.js                # API 调用封装
            ├── ui.js                 # UI 交互逻辑
            └── app.js                # 应用主逻辑
```

---

## 🔄 数据流设计

### 1. 化学反应讲解流程

```
用户输入反应描述
    ↓
[Frontend] 验证输入 → 显示加载动画
    ↓
[API] POST /api/reaction/explain
    ↓
[Service] ChemistryService.explain_reaction()
    ↓
[Module] reaction_explainer.explain_reaction()
    ↓
[LLM] Qwen3 Chat Model
    ├─ System Prompt: 化学教师角色设定
    ├─ User Input: 反应描述
    └─ Output: 结构化讲解内容
    ↓
[Backend] 返回讲解文本
    ↓
[Frontend] 显示结果 → 隐藏加载动画
    ↓
用户查看讲解内容
```

### 2. 方程式配平流程

```
用户输入未配平方程式
    ↓
[Frontend] 验证输入 → 显示加载动画
    ↓
[API] POST /api/equation/balance
    ↓
[Service] ChemistryService.balance_equation()
    ↓
[Module] equation_balancer.balance_equation()
    ↓
[LLM] Qwen3 Chat Model
    ├─ System Prompt: 配平规则与教学指导
    ├─ User Input: 未配平方程式
    └─ Output: 配平结果 + 步骤说明
    ↓
[Backend] 返回配平结果
    ↓
[Frontend] 显示结果
    ↓
用户查看配平过程
```

### 3. 反应现象文生图流程

```
用户输入反应现象描述
    ↓
[Frontend] 验证输入 → 显示加载动画
    ↓
[API] POST /api/reaction/image
    ↓
[Service] ChemistryService.generate_reaction_image()
    ↓
[Module] reaction_image_generator.generate_reaction_image()
    ↓
[LLM] Qwen3 Chat Model (提示词生成)
    ├─ 输入: 反应现象描述
    └─ 输出: 英文图像提示词
    ↓
[LLM] Qwen3 Chat Model (提示词评估)
    ├─ 评估提示词完整性
    └─ 若不完整则返回优化建议
    ↓
[Image Model] FLUX.1-Krea-dev (图像生成)
    ├─ 异步提交任务
    ├─ 轮询任务状态（最多30次，每次10秒）
    └─ 获取生成的图像URL
    ↓
[LLM] Qwen3 Vision Model (图像评估)
    ├─ 对比图像与提示词
    └─ 若不一致则返回优化建议
    ↓
[Backend] 返回最终图像URL
    ↓
[Frontend] 显示图像
    ↓
用户查看反应现象图像
```

### 4. 物质识别流程

```
用户上传物质图片
    ↓
[Frontend] 验证图片 → 转换为 Base64 → 显示加载动画
    ↓
[API] POST /api/material/recognize
    ├─ 请求体: { image_url: "data:image/...;base64,..." }
    ↓
[Service] ChemistryService.recognize_material()
    ↓
[Module] material_recognizer.recognize_material()
    ↓
[LLM] Qwen3 Vision Model
    ├─ System Prompt: 物质识别与教学指导
    ├─ Input: 图片 + 识别任务
    └─ Output: 物质名称、特征、用途、安全提示
    ↓
[Backend] 返回识别结果
    ↓
[Frontend] 显示结果
    ↓
用户查看物质信息
```

---

## 🤖 AI 工具说明

### 使用的 AI 模型

| 模型名称 | 提供商 | 用途 | 特点 |
|---------|------|------|------|
| **Qwen3-VL-30B-A3B-Instruct** | 阿里通义千问 | 文本生成、多模态理解 | 强大的中文理解能力，适合化学教学 |
| **FLUX.1-Krea-dev** | Black Forest Labs | 图像生成 | 高质量图像生成，支持详细描述 |

### 模型调用方式

所有模型调用通过 **LangChain** 框架进行，确保：
- 统一的 API 接口
- 自动错误处理与重试
- 灵活的提示词管理

### API 密钥配置

在 `.env` 文件中配置：

```env
# ModelScope API 配置
modelscope_API_KEY="your-api-key-here"
modelscope_BASE_URL="https://api-inference.modelscope.cn/v1"
modelscope_CHAT_MODEL="Qwen/Qwen3-VL-30B-A3B-Instruct"
```

获取 API 密钥：访问 [ModelScope 控制台](https://www.modelscope.cn/my/myaccesstoken)

---

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pip 包管理器
- 网络连接（调用云端 AI 模型）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd chemistry-ai-teacher
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 API 密钥**
   编辑 `.env` 文件，填入你的 ModelScope API 密钥：
   ```env
   modelscope_API_KEY="your-api-key-here"
   ```

4. **启动应用**

   **方式一：完整应用启动（推荐）**
   ```bash
   python start_app.py
   ```
   自动启动后端和前端，并打开浏览器。

   **方式二：后端单独启动**
   ```bash
   python backend_start.py
   ```
   后端运行在 `http://127.0.0.1:5000`

   **方式三：前端单独启动**
   ```bash
   python frontend_start.py
   ```
   前端运行在 `http://127.0.0.1:8000`

   **方式四：Gradio 应用启动**
   ```bash
   python app.py
   ```
   启动 Gradio 界面版本。

5. **访问应用**
   - 前端地址：`http://127.0.0.1:8000`
   - 后端 API：`http://127.0.0.1:5000`
   - API 文档：`http://127.0.0.1:5000/docs`

---

## 📊 代码流程图

### 后端请求处理流程

```
HTTP Request
    ↓
[FastAPI Router] 路由匹配
    ↓
[Request Validation] Pydantic 模型验证
    ├─ 检查必需字段
    ├─ 验证数据类型
    └─ 验证字段长度
    ↓
[Service Layer] 业务逻辑处理
    ├─ 调用对应功能模块
    ├─ 传递 API 密钥
    └─ 处理异常
    ↓
[Module Layer] 功能实现
    ├─ 构建系统提示词
    ├─ 调用 LLM 模型
    └─ 处理模型响应
    ↓
[Response] 返回结果
    ├─ 成功: { success: true, data: "..." }
    └─ 失败: { success: false, error: "..." }
    ↓
HTTP Response
```

### 前端交互流程

```
用户操作
    ↓
[Event Handler] 事件监听
    ├─ 验证输入
    ├─ 显示加载状态
    └─ 禁用按钮
    ↓
[API Call] 调用后端 API
    ├─ 构建请求
    ├─ 添加 API 密钥
    └─ 发送 HTTP 请求
    ↓
[Response Handler] 处理响应
    ├─ 检查状态码
    ├─ 解析 JSON
    └─ 处理错误
    ↓
[UI Update] 更新界面
    ├─ 隐藏加载状态
    ├─ 显示结果
    ├─ 启用按钮
    └─ 显示成功/错误消息
    ↓
用户查看结果
```

---

## 🔐 安全性考虑

### API 密钥管理

- **不要在代码中硬编码** API 密钥
- 使用 `.env` 文件存储敏感信息
- `.env` 文件已添加到 `.gitignore`，不会被提交到版本控制

### 输入验证

- 所有用户输入都通过 Pydantic 模型验证
- 检查字段长度、类型和格式
- 防止注入攻击

### 错误处理

- 全局异常处理器捕获所有错误
- 不向用户暴露内部错误信息
- 记录详细的错误日志用于调试

---

## 📝 使用示例

### 示例 1：讲解化学反应

```bash
curl -X POST "http://127.0.0.1:5000/api/reaction/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "reaction": "铁与硫酸铜反应",
    "api_key": "your-api-key"
  }'
```

**响应**：
```json
{
  "success": true,
  "data": "【反应名称】铁与硫酸铜的置换反应\n【反应类型】置换反应（氧化还原反应）\n...",
  "error": null
}
```

### 示例 2：配平化学方程式

```bash
curl -X POST "http://127.0.0.1:5000/api/equation/balance" \
  -H "Content-Type: application/json" \
  -d '{
    "equation": "Fe + O2 → Fe2O3",
    "api_key": "your-api-key"
  }'
```

**响应**：
```json
{
  "success": true,
  "data": "【配平结果】4Fe + 3O₂ → 2Fe₂O₃\n【配平步骤】...",
  "error": null
}
```

---

## 🛠️ 开发与扩展

### 添加新功能

1. **创建新模块** `backend/new_feature.py`
2. **在 services.py 中添加方法**
3. **在 routes.py 中添加 API 端点**
4. **在前端添加对应的 UI 和 API 调用**

### 修改 AI 提示词

所有系统提示词都在各功能模块的 `system_prompt` 变量中，可直接修改以调整 AI 行为。

### 更换 AI 模型

在各模块中修改 `ChatOpenAI` 的 `model` 参数：

```python
model = ChatOpenAI(
    api_key=SecretStr(api_key),
    model="your-new-model-name",  # 修改这里
    base_url="https://api-inference.modelscope.cn/v1",
    temperature=0.7
)
```

---

## 📚 依赖说明

| 包名 | 版本 | 用途 |
|-----|------|------|
| gradio | 5.15.0 | Web UI 框架 |
| fastapi | 0.120.0 | 后端 Web 框架 |
| uvicorn | 0.37.0 | ASGI 服务器 |
| pydantic | 2.12.0a1 | 数据验证 |
| langchain | 1.0.2 | LLM 框架 |
| langchain-openai | 1.0.1 | OpenAI 兼容接口 |
| requests | 2.32.5 | HTTP 客户端 |
| python-dotenv | 1.1.1 | 环境变量管理 |

---

## 🐛 常见问题

### Q: 如何获取 ModelScope API 密钥？
A: 访问 [ModelScope 控制台](https://www.modelscope.cn/my/myaccesstoken)，登录后生成访问令牌。

### Q: 应用启动后无法访问？
A: 检查防火墙设置，确保端口 5000 和 8000 未被占用。

### Q: API 调用超时？
A: 检查网络连接，确保能访问 `api-inference.modelscope.cn`。

### Q: 生成的图像质量不好？
A: 尝试修改反应现象描述，提供更详细的视觉细节。

---

## 📞 支持与反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

## 📚 参考资源

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [LangChain 文档](https://python.langchain.com/)
- [ModelScope 文档](https://modelscope.cn/docs)
- [Gradio 文档](https://www.gradio.app/)

---

## 🎓 致谢

感谢阿里通义千问、Black Forest Labs 等 AI 模型提供商的支持。

本项目致力于为乡村教育贡献力量，提升教学质量，弥补资源不足。

---

**最后更新**：2025 年 11 月 17 日
