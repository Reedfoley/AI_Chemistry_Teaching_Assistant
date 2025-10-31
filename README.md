---
title: 乡村化学教师AI教学助手
description: 专为乡村教育设计的智能化学教学辅助系统，集成AI讲解、方程式配平、现象可视化和物质识别等功能
author: Datawhale
version: 3.0.0
language: zh-CN
tags:
  - Chemistry
  - Education
  - AI Assistant
  - Gradio UI
  - FastAPI Backend
  - ModelScope API
platform: ModelScope Studio
repository: https://www.modelscope.cn/studios/Datawhale/AI_Chemistry_Teaching_Assistant
license: Apache License 2.0
keywords:
  - 化学教育
  - AI助手
  - 乡村教育
  - 实验辅助
  - 智能讲解
  - Gradio应用
created: 2025-10-27
updated: 2025-10-31
entry_file: gradio_app.py
---

# 乡村化学教师AI教学助手

> 智能讲解 · 方程式配平 · 反应现象可视化 · 实验物质识别

一个专为乡村教育设计的智能化学教学辅助系统，利用大语言模型和视觉AI技术，帮助化学教师提升教学效率，弥补实验资源不足的问题。

## 🌟 核心功能

### 1. 化学反应智能讲解

- 输入任意化学反应名称或描述
- 生成通俗易懂的反应原理说明
- **示例**: 输入"铁与硫酸铜反应" → 获得详细的反应机制、条件和应用意义

### 2. 化学方程式自动配平

- 支持输入未配平的化学方程式
- 自动完成配平并返回平衡方程式
- 提供详细的配平步骤说明
- **示例**: 输入"Fe + O2 → Fe2O3" → 生成"4Fe + 3O2 → 2Fe2O3"及配平过程

### 3. 反应现象文生图展示

- 根据反应现象描述生成逼真的化学反应图像
- AI优化提示词，生成高保真的实验现象图片
- 可用于课堂直观展示实验效果
- **示例**: 输入"产生红棕色沉淀，剧烈冒泡" → 生成对应的反应现象图像

### 4. 实验物质图生文识别

- 上传化学物质或实验器材的图片
- AI自动识别物质并生成说明
- 包括化学名称、性质、准备方法和安全指南
- **示例**: 上传化学试剂图片 → 识别物质并获得详细信息

## 📋 项目结构

```tree
.
├── gradio_app.py            # Gradio UI应用入口（创空间部署用）
│
├── frontend/                # 原生HTML5前端（本地开发用）
│   ├── assets/
│   │   ├── css/             # CSS样式文件
│   │   │   ├── variables.css      # CSS变量定义
│   │   │   ├── base.css           # 基础样式
│   │   │   ├── layout.css         # 布局样式
│   │   │   ├── components.css     # 组件样式
│   │   │   ├── animations.css     # 动画效果
│   │   │   └── responsive.css     # 响应式设计
│   │   └── js/              # JavaScript模块
│   │       ├── config.js          # 配置管理
│   │       ├── api.js             # API通信
│   │       ├── ui.js              # UI交互
│   │       └── app.js             # 应用主逻辑
│   └── index.html           # 主页面入口
│
├── backend/                 # FastAPI后端（核心服务）
│   ├── __init__.py
│   ├── main.py              # FastAPI应用主入口
│   ├── routes.py            # API路由定义
│   ├── models.py            # Pydantic数据模型
│   ├── services.py          # 业务逻辑统一入口
│   ├── reaction_explainer.py      # 反应讲解模块
│   ├── equation_balancer.py       # 方程式配平模块
│   ├── reaction_image_generator.py # 文生图模块
│   └── material_recognizer.py     # 物质识别模块
│
├── app.py                   # 统一启动脚本（Python）
├── app.bat                  # Windows启动脚本
├── app.sh                   # Linux/Mac启动脚本
├── backend_start.py         # 后端独立启动脚本
├── .modelscope_config.json  # 创空间部署配置
├── requirements.txt         # Python依赖清单
└── README.md                # 项目文档
```

## 🏗️ 架构说明

### 部署模式

项目支持两种部署模式：

| 模式 | 入口文件 | 用途 | 环境 |
|------|---------|------|------|
| **Gradio UI** | `gradio_app.py` | 创空间在线部署 | 云端 |
| **HTML5前端** | `frontend/index.html` | 本地开发测试 | 本地 |

### 后端四层架构

后端采用标准四层分层架构，确保代码职责分离：

1. **应用层 (main.py)**
   - FastAPI应用初始化
   - CORS中间件配置
   - 异常处理器设置
   - 启动/关闭事件

2. **路由层 (routes.py)**
   - HTTP API端点定义
   - 请求验证和响应封装
   - 健康检查和配置接口

3. **数据模型层 (models.py)**
   - Pydantic请求/响应模型
   - 数据验证规则
   - API文档定义

4. **业务逻辑层 (services.py + 功能模块)**
   - services.py：统一服务入口
   - reaction_explainer.py：化学反应讲解
   - equation_balancer.py：方程式配平
   - reaction_image_generator.py：文生图功能
   - material_recognizer.py：物质识别



## 🚀 快速开始

### 前置要求

- Python 3.8+ 或 3.10+
- 现代Web浏览器（Chrome、Firefox、Edge等）
- ModelScope API密钥（[获取地址](https://www.modelscope.cn/my/myaccesstoken)）

### 安装依赖

```bash
# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows PowerShell

# 安装所有依赖
pip install -r requirements.txt
```

### 启动应用

#### 方式一：Gradio UI（推荐用于创空间部署）

```bash
# 启动Gradio应用（自动打开浏览器）
python gradio_app.py

# 访问地址：http://localhost:7860
```

#### 方式二：HTML5前端 + FastAPI后端（推荐用于本地开发）

**启动后端：**

```bash
# 方式1：使用统一启动脚本
python app.py

# 方式2：后端独立启动
python backend_start.py

# 方式3：直接运行FastAPI
cd backend
python main.py
# 或
uvicorn main:app --reload --port 5000
```

**启动前端：**

在另一个终端中，启动前端HTTP服务器：

```bash
# Python内置HTTP服务器
python -m http.server 8000 --directory frontend

# 访问地址：http://localhost:8000
```

### 配置API Key

1. 前往 [ModelScope控制台](https://www.modelscope.cn/my/myaccesstoken) 获取您的API密钥
2. 在应用首页的"设置API KEY"界面输入并保存
3. 验证成功后即可开始使用


## 🔧 API参数详解

### 1. 化学反应讲解接口

**端点:** `POST /api/reaction/explain`

**请求参数:**
```json
{
  "reaction": "铁与硫酸铜反应",
  "api_key": "your_modelscope_api_key"
}
```

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| reaction | string | 化学反应描述 | "铁与硫酸铜反应" |
| api_key | string | ModelScope API密钥 | 必需 |

**响应示例:**
```json
{
  "success": true,
  "data": "铁与硫酸铜反应是一个置换反应。反应方程式为：Fe + CuSO4 → FeSO4 + Cu..."
}
```

### 2. 方程式配平接口

**端点:** `POST /api/equation/balance`

**请求参数:**
```json
{
  "equation": "Fe + O2 → Fe2O3",
  "api_key": "your_modelscope_api_key"
}
```

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| equation | string | 未配平的方程式 | "Fe + O2 → Fe2O3" |
| api_key | string | ModelScope API密钥 | 必需 |

**响应示例:**
```json
{
  "success": true,
  "data": {
    "balanced_equation": "4Fe + 3O2 → 2Fe2O3",
    "steps": ["1. 氧原子: 右边2个，左边需要3个O2...", "2. 铁原子: 左边4个，右边需要2个Fe2O3..."]
  }
}
```

### 3. 反应现象图像生成接口

**端点:** `POST /api/reaction/image`

**请求参数:**
```json
{
  "prompt": "产生红棕色沉淀，剧烈冒泡并放热",
  "api_key": "your_modelscope_api_key"
}
```

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| prompt | string | 反应现象描述 | "产生红棕色沉淀，剧烈冒泡" |
| api_key | string | ModelScope API密钥 | 必需 |

**响应示例:**
```json
{
  "success": true,
  "data": "https://api-inference.modelscope.cn/...image_url..."
}
```

### 4. 物质识别接口

**端点:** `POST /api/material/recognize`

**请求参数:**
```json
{
  "image_url": "data:image/jpeg;base64,...",
  "api_key": "your_modelscope_api_key"
}
```

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| image_url | string | 图片URL或Base64编码 | data URL 或 http URL |
| api_key | string | ModelScope API密钥 | 必需 |

**响应示例:**
```json
{
  "success": true,
  "data": {
    "name": "硫酸铜",
    "aliases": ["CuSO4"],
    "properties": "蓝色晶体，易溶于水...",
    "preparation": "通常由铜与浓硫酸反应得到...",
    "safety": "有毒，避免接触皮肤..."
  }
}
```

## 📱 技术栈

### 前端
- **HTML5** - 页面结构
- **CSS3** - 样式美化（Flexbox、Grid、CSS变量）
- **JavaScript (ES6+)** - 交互逻辑
- **无框架** - 原生实现，轻量级
- **Gradio** - AI应用UI框架（创空间部署）

### 后端
- **Python 3.8+** - 编程语言
- **FastAPI** - 高性能Web框架
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证
- **LangChain** - AI工具链框架
- **ModelScope API** - 大语言模型服务

### 使用的AI模型
- **Qwen/Qwen3-VL-30B-A3B-Instruct** - 文本和图像理解
- **FLUX.1-Krea-dev** - 文本到图像生成

### 外部服务
- **ModelScope** - 提供API接口和模型调用
- **HTTPS** - 安全通信协议


## ⚙️ 配置说明

### 前端超时配置 (config.js)

根据网络情况调整API超时时间：
```javascript
MEDIUM_TIMEOUT = 120000   // 中等超时：120秒
LONG_TIMEOUT = 300000     // 长超时：300秒
```

### 后端HTTP连接保活

所有API响应包含以下头部，支持长连接：
```
Connection: keep-alive
Keep-Alive: timeout=300, max=1000
```

### 跨域配置 (CORS)

FastAPI 已配置CORS中间件，允许跨域请求：
```python
allow_origins = ["*"]  # 开发环境
allow_methods = ["*"]
allow_headers = ["*"]
```

## 🔌 集成示例

### Python 后端调用

```python
import requests
import json

BASE_URL = "http://localhost:5000"
API_KEY = "your_modelscope_api_key"

# 讲解化学反应
response = requests.post(
    f"{BASE_URL}/api/reaction/explain",
    json={
        "reaction": "铁与硫酸铜反应",
        "api_key": API_KEY
    },
    timeout=120
)
print(response.json())
```

### JavaScript 前端调用

```javascript
const apiKey = localStorage.getItem('api_key');

fetch('http://localhost:5000/api/reaction/explain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        reaction: '铁与硫酸铜反应',
        api_key: apiKey
    })
})
.then(res => res.json())
.then(data => console.log(data.data));
```

### cURL 命令测试

```bash
# 测试健康检查
curl http://localhost:5000/api/health

# 测试讲解接口
curl -X POST http://localhost:5000/api/reaction/explain \
  -H "Content-Type: application/json" \
  -d '{
    "reaction": "铁与硫酸铜反应",
    "api_key": "your_api_key"
  }'
```

## 📖 验证清单

- [ ] Python 3.8+ 已安装
- [ ] 所有依赖已成功安装（`pip list` 确认）
- [ ] 获取了ModelScope API密钥
- [ ] 应用可成功启动（检查`http://localhost:5000`）
- [ ] 能在UI界面输入API Key并保存
- [ ] 化学反应讲解功能正常工作
- [ ] 方程式配平功能正常工作
- [ ] 图像生成功能正常工作
- [ ] 物质识别功能正常工作

## 🐛 常见问题

### Q: 启动时出现"端口被占用"错误
**A:** 修改 `backend_start.py` 中的端口号，或关闭占用5000端口的其他应用。

### Q: API请求超时
**A:** 
- 检查网络连接
- 增加 `config.js` 中的超时时间
- 确认ModelScope API密钥有效

### Q: 图像生成失败
**A:**
- 确保API Key有效且配额充足
- 检查提示词内容（避免特殊字符）
- 查看浏览器控制台的详细错误信息

### Q: 物质识别无法识别图片
**A:**
- 确保上传的是清晰的物质或器材图片
- 图片格式应为常见格式（JPG、PNG等）
- 检查API Key的权限

## 📚 API文档

启动后端后，可访问以下文档：
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`
- OpenAPI JSON: `http://localhost:5000/openapi.json`

## 🌐 部署到ModelScope创空间

### 自动部署（推荐）

项目已配置为创空间部署。只需执行：

```bash
git add .
git commit -m "Update Gradio app with improved UI design"
git push
```

创空间会自动识别 `.modelscope_config.json` 配置文件，使用 `gradio_app.py` 作为入口，启动Gradio应用。

### 手动配置

如需手动部署：

1. **配置文件检查**
   ```json
   // .modelscope_config.json
   {
     "entry_file": "gradio_app.py",
     "app_type": "gradio"
   }
   ```

2. **依赖文件检查**
   - 确保 `requirements.txt` 包含所有必需的包

3. **环境变量设置**
   - 创空间会自动配置 `GRADIO_PORT` 和 `PORT` 环境变量

### 本地测试创空间部署

```bash
# 测试Gradio应用
python gradio_app.py

# 浏览器访问：http://localhost:7860
```


## 📝 开发规范

### 项目约定

- **本地开发**：使用 HTML5 前端 + FastAPI 后端
- **云端部署**：使用 Gradio 应用（创空间）
- **共用后端**：两种部署方式都调用同一套后端服务

### 后端模块职责

```
backend/
├── main.py              # 应用层：初始化、配置、异常处理
├── routes.py            # 路由层：HTTP端点、请求分发
├── models.py            # 数据模型层：Pydantic模型
├── services.py          # 服务入口：路由到具体功能模块
└── [功能模块]
    ├── reaction_explainer.py        # 反应讲解
    ├── equation_balancer.py         # 方程式配平
    ├── reaction_image_generator.py  # 文生图
    └── material_recognizer.py       # 物质识别
```

### 前端模块职责

```
frontend/
├── assets/css/          # 样式管理
│   ├── variables.css    # 全局变量
│   ├── base.css         # 基础样式
│   ├── layout.css       # 布局框架
│   └── components.css   # 组件样式
└── assets/js/           # 逻辑管理
    ├── config.js        # 全局配置
    ├── api.js           # HTTP通信
    ├── ui.js            # DOM操作
    └── app.js           # 应用入口
```

### 编码规范

- **Python**: 遵循PEP 8
- **JavaScript**: 使用ES6+，避免全局变量
- **CSS**: 使用BEM命名法
- **Git**: 提交信息要清晰明确


## 📄 许可证

MIT License

## 🙏 贡献

欢迎提交Issue和Pull Request！

---

**最后更新:** 2025年10月31日  
**版本:** 3.0.0  
**当前部署方式:** Gradio应用（创空间） + FastAPI后端 + HTML5前端  
**专为乡村教育设计，提升教学效率，弥补实验资源不足**
