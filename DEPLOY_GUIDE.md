# 乡村化学教师AI教学助手 - 部署指南

## 🚀 快速开始（推荐）

### 使用一键部署脚本

项目提供了三种平台的一键部署脚本，可自动检查环境、安装依赖并启动应用。

#### Windows 用户

```batch
# 在PowerShell或CMD中运行
python deploy.py

# 或直接运行批处理脚本
deploy.bat
```

#### Linux/macOS 用户

```bash
# 添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh

# 或使用Python脚本（跨平台）
python deploy.py
```

#### 跨平台（推荐）

```bash
python deploy.py
```

---

## 📋 部署脚本功能

一键部署脚本会自动完成以下步骤：

1. **环境检查** - 检查Python和Git是否已安装
2. **虚拟环境** - 创建并配置Python虚拟环境
3. **依赖安装** - 自动安装项目所有依赖
4. **启动选择** - 提供多种启动选项

### 脚本提供的选项

| 选项 | 用途 | 访问地址 |
|------|------|--------|
| 1 - Gradio应用 | 在线部署到创空间 | http://localhost:7860 |
| 2 - FastAPI后端 | 本地开发和测试 | http://localhost:5000 |
| 3 - 推送到创空间 | 上传代码到ModelScope | https://www.modelscope.cn/studios |
| 4 - 退出 | 结束部署流程 | - |

---

## 🔧 手动部署步骤

如果选择不使用一键脚本，也可以手动部署：

### 1. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 选择启动方式

#### 方式A：Gradio UI（创空间部署）

```bash
python gradio_app.py
```

浏览器会自动打开 `http://localhost:7860`

#### 方式B：HTML5前端 + FastAPI后端（本地开发）

**启动后端：**
```bash
python backend_start.py
# 或
uvicorn backend.main:app --reload --port 5000
```

**启动前端：**
```bash
# 在新的终端中
python -m http.server 8000 --directory frontend
```

访问 `http://localhost:8000`

---

## 🌐 部署到ModelScope创空间

### 前置要求

- Git已安装并配置
- 有效的ModelScope账户
- 项目已推送到ModelScope仓库

### 自动部署

使用部署脚本的选项3：

```bash
python deploy.py
# 选择 [3] 上传到创空间
```

### 手动部署

```bash
# 1. 初始化Git（如果还没有）
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# 2. 添加所有文件
git add .

# 3. 提交更改
git commit -m "Update: Gradio UI v3.0.0"

# 4. 推送到创空间
git push -u origin main
```

### 验证部署

访问 https://www.modelscope.cn/studios/Datawhale/AI_Chemistry_Teaching_Assistant

---

## 🔑 配置API密钥

### 获取ModelScope API密钥

1. 访问 [ModelScope控制台](https://www.modelscope.cn/my/myaccesstoken)
2. 登录您的账户
3. 复制您的访问令牌（API Key）

### 在应用中设置

1. 启动应用后，在首页找到"⚙️ API密钥设置"
2. 粘贴您的API密钥
3. 点击"💾 保存"按钮
4. 看到✓成功提示后即可使用

---

## ❌ 常见问题排查

### 问题1：依赖安装失败

**症状：** `pip install -r requirements.txt` 失败

**解决方案：**
```bash
# 更换pip源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 重新安装
pip install -r requirements.txt
```

### 问题2：端口被占用

**症状：** `Address already in use: ('0.0.0.0', 7860)` 或类似错误

**解决方案：**
```bash
# Gradio（修改启动脚本中的端口号）
python gradio_app.py --share  # 使用公共URL

# FastAPI
uvicorn backend.main:app --port 8001
```

### 问题3：Git推送失败

**症状：** `fatal: remote origin not configured`

**解决方案：**
```bash
# 检查远程仓库配置
git remote -v

# 添加远程仓库
git remote add origin https://github.com/user/repo.git

# 或更新现有远程
git remote set-url origin https://github.com/user/repo.git

# 重新推送
git push -u origin main
```

### 问题4：Python/Git未找到

**症状：** `command not found: python` 或 `command not found: git`

**解决方案：**

**Python：**
- Windows: [下载安装](https://www.python.org/downloads/)，勾选"Add Python to PATH"
- macOS: `brew install python3`
- Linux: `sudo apt-get install python3`

**Git：**
- Windows: [下载安装](https://git-scm.com/download/win)
- macOS: `brew install git`
- Linux: `sudo apt-get install git`

### 问题5：API调用失败

**症状：** `Error code: 401` 或 `Invalid API Key`

**解决方案：**
1. 验证API密钥是否正确
2. 检查API密钥是否已过期
3. 确保网络连接正常
4. 在ModelScope控制台检查API配额

---

## 📚 项目架构

### 后端API接口

所有API接口都在 `http://localhost:5000`

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/reaction/explain` | POST | 化学反应讲解 |
| `/api/equation/balance` | POST | 方程式配平 |
| `/api/reaction/image` | POST | 文生图 |
| `/api/material/recognize` | POST | 物质识别 |
| `/docs` | GET | Swagger API文档 |
| `/redoc` | GET | ReDoc API文档 |

### 数据流向

```
用户输入
   ↓
Gradio UI / HTML前端
   ↓
FastAPI后端 (routes.py)
   ↓
业务逻辑层 (services.py + 功能模块)
   ↓
ModelScope API 调用
   ↓
大语言模型处理
   ↓
返回结果
   ↓
前端展示
```

---

## 🔐 安全建议

1. **不要在代码中保存API密钥** - 使用环境变量或UI设置
2. **定期更换API密钥** - 在ModelScope控制台重新生成
3. **生产环境部署** - 使用HTTPS而非HTTP
4. **隐藏错误详情** - 在生产环境禁用debug模式

---

## 📞 获取帮助

如遇问题，请：

1. 查看 [README.md](./README.md) 了解项目详情
2. 检查 [常见问题](#常见问题排查) 部分
3. 查看运行日志了解错误信息
4. 在ModelScope讨论区提问
5. 提交Issue或PR（如果使用GitHub）

---

## 🎓 后续步骤

部署完成后，您可以：

1. **访问应用** - 打开浏览器访问部署地址
2. **输入API密钥** - 在设置区域配置您的ModelScope API密钥
3. **测试功能** - 尝试各个教学助手功能
4. **分享应用** - 分享部署链接给同事使用
5. **自定义调整** - 修改UI或功能满足特定需求

---

**最后更新:** 2025年10月31日  
**版本:** 3.0.0  
**支持平台:** Windows, Linux, macOS
