---
title: 乡村化学教师AI教学助手
description: 专为乡村教育设计的智能化学教学辅助系统，集成AI讲解、方程式配平、现象可视化和物质识别等功能
author: Datawhale
version: 2.0.0
language: zh-CN
tags:
  - Chemistry
  - Education
  - AI Assistant
  - Flask Backend
  - HTML5 Frontend
  - ModelScope API
platform: ModelScope Studio
repository: https://www.modelscope.cn/studios/Datawhale/AI_assistant_Demo
license: Apache License 2.0
keywords:
  - 化学教育
  - AI助手
  - 乡村教育
  - 实验辅助
  - 智能讲解
created: 2025-10-27
updated: 2025-10-27
entry_file：gradio_app.py
---

# 乡村化学教师AI教学助手

> 智能讲解 · 方程式配平 · 反应现象可视化 · 实验物质识别

一个专为乡村教育设计的智能化学教学辅助系统，利用大语言模型和视觉AI技术，帮助化学教师提升教学效率，弥补实验资源不足的问题。

## 🌟 核心功能

### 1. 化学反应智能讲解
- 输入任意化学反应名称或描述
- 支持初中和高中两个教学阶段
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

```
.
├── frontend/                 # 前端资源目录
│   ├── assets/
│   │   ├── css/             # 样式文件
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
├── backend/                  # 后端服务目录
│   ├── __init__.py          # 包初始化
│   ├── main.py              # FastAPI应用主入口
│   ├── routes.py            # API路由定义
│   ├── models.py            # 数据模型定义
│   └── services.py          # 业务逻辑实现
│
├── app.py                    # 跨平台启动脚本（Python）
├── app.bat                   # Windows启动脚本
├── app.sh                    # Linux/Mac启动脚本
├── backend_start.py          # 后端独立启动脚本
└── README.md                 # 项目文档
```

## 🚀 快速开始

### 前置要求

- Python 3.8+ 或 3.10+
- 现代Web浏览器（Chrome、Firefox、Edge等）
- ModelScope API密钥（[获取地址](https://www.modelscope.cn/my/myaccesstoken)）

### 安装依赖

```bash
# Windows PowerShell 或 Linux/Mac bash
pip install fastapi uvicorn python-multipart
pip install langchain langchain-openai requests
```

### 启动应用

#### 方式一：使用统一启动脚本（推荐）

**Windows:**
```bash
python app.py
```

**Linux/Mac:**
```bash
bash app.sh
```

#### 方式二：后端独立启动

```bash
# 在项目根目录执行
python backend_start.py

# 或使用uvicorn命令
cd backend
python main.py
```

启动后，应用将自动打开浏览器，默认地址为 `http://localhost:5000`

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
  "level": "junior",
  "api_key": "your_modelscope_api_key"
}
```

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| reaction | string | 化学反应描述 | "铁与硫酸铜反应" |
| level | string | 教学阶段 | "junior"(初中) 或 "senior"(高中) |
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
- **CSS3** - 样式美化（含Flexbox、Grid、CSS变量）
- **JavaScript (ES6+)** - 交互逻辑
- **无框架** - 原生实现，轻量级

### 后端
- **Python 3.8+** - 编程语言
- **FastAPI** - Web框架
- **Uvicorn** - ASGI服务器
- **Pydantic** - 数据验证
- **LangChain** - AI工具链集成
- **ModelScope API** - 大语言模型调用
- **Qwen/Qwen3-VL** - 视觉语言模型

### 外部服务
- **ModelScope** - 提供API接口和大语言模型
- **FLUX.1-Krea-dev** - 文生图模型

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
        "level": "junior",
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
        level: 'junior',
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
    "level": "junior",
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

## 🌐 部署到ModelScope

1. 配置入口文件为 `frontend/index.html`
2. 项目类型选择 **Static HTML**
3. 添加 `.modelscope_config.json` 配置文件
4. 配置正确的CORS允许域名

## 📝 开发规范

### 后端架构
后端采用标准四层架构：
- **main.py** - 应用层：FastAPI初始化、中间件配置
- **routes.py** - 路由层：HTTP端点定义
- **models.py** - 数据模型层：Pydantic请求/响应模型
- **services.py** - 业务逻辑层：核心算法和API调用

### 前端模块
- **config.js** - 全局配置和常量
- **api.js** - 后端API通信
- **ui.js** - DOM操作和UI交互
- **app.js** - 应用主逻辑和事件处理

## 📄 许可证

MIT License

## 🙏 贡献

欢迎提交Issue和Pull Request！

---

**最后更新:** 2025年10月27日  
**版本:** 2.0.0  
**专为乡村教育设计，提升教学效率，弥补实验资源不足**
