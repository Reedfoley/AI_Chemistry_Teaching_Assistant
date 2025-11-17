# 🧪 乡村化学教师AI教学助手

一个为乡村教育设计的智能化学教学辅助系统，利用大模型技术提升教学效率，弥补实验资源不足。

## ✨ 核心功能

### 1. 🎓 化学反应智能讲解
- 输入化学反应名称或描述
- 获取通俗易懂的反应原理说明
- 适配不同学龄的讲解深度

### 2. ⚖️ 化学方程式自动配平
- 输入未配平的化学方程式
- 自动完成配平并显示步骤
- 支持复杂多步反应

### 3. 🎨 反应现象文生图展示
- 输入反应现象描述
- 生成逼真的反应现象图像
- 用于课堂直观展示实验效果

### 4. 🔍 实验物质识别
- 上传化学物质或实验器材图片
- AI自动识别物质并生成说明
- 包括化学名称、性质及安全信息

## 📋 项目结构

```
AI_Chemistry_Teaching_Assistant/
├── backend/                    # FastAPI 后端服务
│   ├── main.py                # 应用主文件
│   ├── routes.py              # API 路由定义
│   ├── models.py              # 数据模型
│   ├── services.py            # 业务逻辑服务
│   ├── reaction_explainer.py  # 反应讲解模块
│   ├── equation_balancer.py   # 方程式配平模块
│   ├── reaction_image_generator.py  # 图像生成模块
│   └── material_recognizer.py # 物质识别模块
│
├── frontend/                   # 前端应用
│   ├── index.html             # 主页面
│   └── assets/
│       ├── css/               # 样式文件
│       │   ├── variables.css
│       │   ├── base.css
│       │   ├── layout.css
│       │   ├── components.css
│       │   ├── animations.css
│       │   └── responsive.css
│       └── js/                # JavaScript 文件
│           ├── config.js      # 配置文件
│           ├── api.js         # API 调用
│           ├── ui.js          # UI 操作
│           └── app.js         # 应用主逻辑
│
├── app.py                      # Gradio 应用（魔搭平台部署）
├── app.bat                     # Windows 启动脚本
├── app.sh                      # macOS/Linux 启动脚本
├── start_app.py                # Python 统一启动脚本
├── backend_start.py            # 后端单独启动脚本
├── frontend_start.py           # 前端单独启动脚本
├── requirements.txt            # Python 依赖
└── README.md                   # 项目说明
```

## 🚀 快速开始

### 前置要求

- Python 3.11+
- pip 包管理器
- ModelScope API Key（获取地址：https://www.modelscope.cn/my/myaccesstoken）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

#### 方式一：Python 统一启动（推荐）

```bash
python start_app.py
```

这会同时启动：
- 前端服务：http://127.0.0.1:8000
- 后端服务：http://127.0.0.1:5000
- 自动打开浏览器

#### 方式二：分别启动

**启动后端：**
```bash
python backend_start.py
```
后端地址：http://127.0.0.1:5000
API 文档：http://127.0.0.1:5000/docs

**启动前端（新终端）：**
```bash
python frontend_start.py
```
前端地址：http://127.0.0.1:8000

#### 方式三：Windows 批处理脚本

```bash
app.bat
```

#### 方式四：macOS/Linux Shell 脚本

```bash
bash app.sh
```

#### 方式五：直接打开 HTML

在文件浏览器中双击 `frontend/index.html` 即可打开应用。

#### 方式六：Gradio 应用（魔搭平台部署）

```bash
python app.py
```

## 📖 使用指南

### 1. 设置 API Key

首次使用时需要设置 ModelScope API Key：

1. 访问 https://www.modelscope.cn/my/myaccesstoken
2. 复制你的访问令牌
3. 在应用中输入 API Key 并点击"保存并进入主界面"

### 2. 化学反应智能讲解

1. 切换到"化学反应智能讲解"标签页
2. 输入化学反应描述（如"铁与硫酸铜反应"）
3. 点击"生成讲解"
4. 等待 AI 生成详细的反应原理说明

### 3. 化学方程式自动配平

1. 切换到"化学方程式自动配平"标签页
2. 输入未配平的方程式（如"Fe + O2 → Fe2O3"）
3. 点击"配平方程式"
4. 查看配平结果和步骤

### 4. 反应现象文生图展示

1. 切换到"反应现象文生图展示"标签页
2. 输入反应现象描述（如"产生红棕色沉淀，剧烈冒泡并放热"）
3. 点击"生成图像"
4. 等待生成反应现象图像

### 5. 实验物质识别

1. 切换到"实验物质识别"标签页
2. 点击图片区域选择要识别的图片
3. 点击"识别物质"
4. 查看 AI 识别结果和物质说明

## 🔌 API 文档

### 基础信息

- **基础 URL**：http://127.0.0.1:5000
- **API 前缀**：/api
- **文档地址**：http://127.0.0.1:5000/docs

### 健康检查

```
GET /api/health
```

### 化学反应讲解

```
POST /api/reaction/explain

请求体：
{
    "reaction": "铁与硫酸铜反应",
    "api_key": "your_api_key"
}

响应：
{
    "success": true,
    "data": "反应讲解内容..."
}
```

### 方程式配平

```
POST /api/equation/balance

请求体：
{
    "equation": "Fe + O2 → Fe2O3",
    "api_key": "your_api_key"
}

响应：
{
    "success": true,
    "data": "配平结果..."
}
```

### 反应现象图生成

```
POST /api/reaction/image

请求体：
{
    "prompt": "产生红棕色沉淀，剧烈冒泡并放热",
    "api_key": "your_api_key"
}

响应：
{
    "success": true,
    "data": "image_url"
}
```

### 物质识别

```
POST /api/material/recognize

请求体：
{
    "image_url": "data:image/jpeg;base64,...",
    "api_key": "your_api_key"
}

响应：
{
    "success": true,
    "data": "识别结果..."
}
```

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI
- **服务器**：Uvicorn
- **数据验证**：Pydantic
- **AI 集成**：LangChain + ModelScope

### 前端
- **HTML5**：页面结构
- **CSS3**：响应式设计
- **JavaScript**：交互逻辑
- **无框架依赖**：轻量级实现

### 部署
- **Gradio**：魔搭平台部署
- **Docker**：容器化部署（可选）

## 📦 依赖说明

```
# 核心Web框架
gradio==5.15.0          # Gradio 应用框架
fastapi==0.120.0        # FastAPI 框架
uvicorn==0.37.0         # ASGI 服务器
pydantic==2.12.0a1      # 数据验证

# AI与大模型集成
langchain==1.0.2        # LLM 框架
langchain-openai==1.0.1 # OpenAI 集成
langchain-community==1.0.0a1  # 社区集成

# 互联网与HTTP
requests==2.32.5        # HTTP 请求库
httpx==0.28.1           # 异步 HTTP 库

# 工具与配置
python-dotenv==1.1.1    # 环境变量管理
```

## 🔐 安全建议

1. **API Key 管理**
   - 不要在代码中硬编码 API Key
   - 使用环境变量或配置文件管理
   - 定期更新和轮换 API Key

2. **CORS 配置**
   - 生产环境应限制具体的域名
   - 不要使用 `allow_origins=["*"]`

3. **输入验证**
   - 所有用户输入都经过 Pydantic 验证
   - 后端进行二次验证

## 🐛 故障排除

### 后端启动失败

**问题**：`ModuleNotFoundError: No module named 'backend'`

**解决**：
```bash
# 确保在项目根目录运行
cd /path/to/AI_Chemistry_Teaching_Assistant
python start_app.py
```

### 前端无法连接后端

**问题**：API 请求返回 CORS 错误

**解决**：
1. 确保后端服务正在运行
2. 检查后端地址是否正确（默认 http://127.0.0.1:5000）
3. 查看浏览器控制台的具体错误信息

### API Key 无效

**问题**：`401 Unauthorized`

**解决**：
1. 访问 https://www.modelscope.cn/my/myaccesstoken
2. 确认 API Key 有效且未过期
3. 重新输入 API Key

### 图像生成超时

**问题**：请求超时

**解决**：
1. 检查网络连接
2. 尝试简化提示词
3. 增加超时时间（修改 config.js 中的 TIMEOUTS）

## 📝 开发指南

### 添加新功能

1. **后端**：在 `backend/` 中添加新模块
2. **前端**：在 `frontend/assets/js/` 中添加新逻辑
3. **API**：在 `backend/routes.py` 中定义新端点

### 本地开发

```bash
# 启用热重载
python backend_start.py  # 后端支持 --reload
python frontend_start.py # 前端自动刷新
```

### 代码规范

- Python：PEP 8
- JavaScript：ES6+
- CSS：BEM 命名规范

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- 项目地址：https://github.com/Reedfoley/AI_Chemistry_Teaching_Assistant
- 问题反馈：提交 GitHub Issue

## 🎯 未来计划

- [ ] 支持更多化学反应类型
- [ ] 添加实验视频演示
- [ ] 支持离线模式
- [ ] 移动端应用
- [ ] 教师管理后台
- [ ] 学生学习进度追踪

## 📚 参考资源

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [LangChain 文档](https://python.langchain.com/)
- [ModelScope 文档](https://modelscope.cn/docs)
- [Gradio 文档](https://www.gradio.app/)

---

**专为乡村教育设计，提升教学效率，弥补实验资源不足** 🌾✨
