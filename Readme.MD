# Python教学平台 - 八年级编程学习网站

## 项目简介

这是一个面向八年级学生的Python编程学习平台，包含以下核心模块：

- **首页模块**：网站入口，展示核心功能导航和教材章节索引
- **教材知识模块**：存放教材章节、知识内容重难点、微课视频、教学课件等
- **在线实践模块**：集成Python在线编辑器，支持语法高亮、代码运行、错误提示，提供分层练习题
- **学习资源模块**：教学课件、微课视频、练习资料下载

## 技术栈

- **前端**：HTML5 + CSS3 + JavaScript（原生）
- **后端**：Python 3（自定义HTTP服务器）
- **数据库**：MySQL（使用 pymysql 驱动）
- **Python执行**：subprocess 调用系统 Python 解释器

## 环境要求

### 必需软件

1. **Python 3.8 或更高版本**
   - 下载地址：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **MySQL 5.7 或更高版本**
   - 下载地址：https://dev.mysql.com/downloads/mysql/
   - 或者使用 phpStudy、小皮面板等集成环境

3. **现代浏览器**
   - 推荐：Chrome、Firefox、Edge 最新版本

### Python依赖包

```powershell
# 安装数据库驱动（必需）
pip install pymysql

# 如果需要使用加密功能（可选，已内置在标准库）
# hashlib 为 Python 标准库，无需安装
```

## 项目结构

```
dw-project/
├── index.html              # 网站首页
├── server.py              # 后端服务器主程序（项目根目录）
├── README.md               # 项目说明文档
│
├── backend/               # 后端代码目录
│   ├── no_site.py         # 无site模块版服务器（备选）
│   ├── requirements.txt  # Python依赖列表
│   └── start_server.bat   # Windows快速启动脚本
│
├── styles/                # CSS样式目录
│   ├── main.css          # 主样式文件
│   └── editor.css        # 代码编辑器样式
│
├── js/                   # JavaScript目录
│   └── main.js           # 主脚本文件
│
└── data/                 # 数据文件目录
    ├── chapters.json     # 章节数据
    └── exercises.json    # 练习题数据
```

## 快速开始

### 1. 安装依赖

```powershell
# 进入项目目录
cd d:\WorkSpace\Vue\cxyjl_en\dw-project

# 安装Python依赖
pip install pymysql
```

### 2. 配置数据库

#### 2.1 创建数据库和表

使用 MySQL 客户端（如 Navicat、phpMyAdmin 或命令行）执行以下SQL：

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS python_learning DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE python_learning;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建代码历史记录表
CREATE TABLE IF NOT EXISTS code_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    code TEXT NOT NULL,
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

#### 2.2 修改数据库连接配置

编辑 `server.py` 文件，修改数据库连接参数：

```python
# 找到约第40行的数据库配置，根据你的实际情况修改：
DB_CONFIG = {
    'host': 'localhost',      # 数据库主机地址
    'user': 'root',           # 数据库用户名
    'password': 'your_password',  # 数据库密码（请修改为你的密码）
    'database': 'python_learning',  # 数据库名称
    'charset': 'utf8mb4'
}
```

### 3. 启动后端服务器

#### 方法一：使用快捷脚本（推荐）

```powershell
# 在项目根目录执行
cd d:\WorkSpace\Vue\cxyjl_en\dw-project
cd backend
start_server.bat
```

#### 方法二：命令行启动

```powershell
# 在项目根目录执行
python -S server.py
```

参数说明：
- `-S`：绕过 site 模块（避免 Windows 环境下的编码问题）

#### 方法三：使用备选服务器

如果主服务器有问题，可以使用 `backend/no_site.py`：

```powershell
cd backend
python -S no_site.py
```

### 4. 访问网站

启动服务器后，打开浏览器访问：

```
http://localhost:5000
```

如果看到网站首页，说明启动成功！

## 功能说明

### 首页模块
- 网站核心功能导航
- 教材章节索引卡片
- 快速开始学习入口

### 教材知识模块
- 左侧章节导航栏
- 知识要点展示
- 重难点解析（含代码示例）
- 学习资源下载链接

### 在线实践模块
- **Python代码编辑器**：语法高亮显示
- **代码运行**：通过后端API执行真实Python代码
- **错误提示**：智能识别常见错误（语法错误、名称错误、类型错误等）
- **分层练习题**：
  - 基础题：基本语法练习
  - 提升题：循环和条件判断
  - 拓展题：综合应用

### 学习资源模块
- 教学课件下载
- 微课视频观看
- 练习资料下载

### 用户系统
- 用户注册和登录
- 代码执行历史记录
- 个人学习进度追踪

## 常见问题

### 问题1：服务器启动报错 "site module"

**错误信息**：
```
Fatal Python error: init_import_site: Failed to import the site module
UnicodeDecodeError: 'gbk' codec can't decode byte 0xaf
```

**解决方法**：
使用 `-S` 参数启动：
```powershell
python -S server.py
```

### 问题2：数据库连接失败

**错误信息**：
```
Connection refused 或 Access denied
```

**解决方法**：
1. 确认 MySQL 服务已启动
2. 检查 `server.py` 中的数据库配置
3. 确认用户名密码正确
4. 确认数据库已创建

```powershell
# 测试数据库连接
mysql -u root -p -e "SHOW DATABASES;"
```

### 问题3：CORS跨域错误

**错误信息**：
```
Access to fetch at 'http://localhost:5000' from origin 'null' 
has been blocked by CORS policy
```

**解决方法**：
确保通过 HTTP 协议访问网站，而不是直接打开 HTML 文件：
```
正确：http://localhost:5000
错误：file:///D:/WorkSpace/.../index.html
```

### 问题4：代码执行显示 "无法连接到后端服务器"

**解决方法**：
1. 确认后端服务器已启动（Terminal 中有启动信息）
2. 检查端口 5000 是否被占用：`netstat -an | findstr 5000`
3. 重启后端服务器

### 问题5：Python代码执行无输出

**可能原因**：
- 代码中没有 print 语句
- 程序异常终止但未捕获

**解决方法**：
确保代码包含输出语句：
```python
print("Hello, World!")
```

## API接口

### 健康检查
```
GET http://localhost:5000/health
```

响应示例：
```json
{
  "status": "ok",
  "time": 1234567890.123
}
```

### 执行Python代码
```
POST http://localhost:5000/execute
Content-Type: application/json

{
  "code": "print('Hello World')"
}
```

响应示例：
```json
{
  "success": true,
  "output": "Hello World\n",
  "error": ""
}
```

### 用户注册
```
POST http://localhost:5000/api/register
Content-Type: application/json

{
  "username": "student1",
  "password": "123456"
}
```

### 用户登录
```
POST http://localhost:5000/api/login
Content-Type: application/json

{
  "username": "student1",
  "password": "123456"
}
```

## 开发指南

### 修改前端代码

1. 编辑 `index.html`、`styles/*.css`、`js/main.js`
2. 修改后刷新浏览器即可看到效果（无需重启服务器）

### 修改后端代码

1. 编辑 `server.py` 或 `backend/no_site.py`
2. 重启后端服务器（Ctrl+C 停止，然后重新启动）

### 添加新的练习题

编辑 `data/exercises.json` 文件，添加新的练习题数据。

### 添加新的章节内容

编辑 `data/chapters.json` 文件，添加新的章节内容。

## 部署说明

### Windows 服务器部署

1. 安装 Python 3.8+
2. 安装 MySQL 5.7+
3. 安装依赖：`pip install pymysql`
4. 配置数据库
5. 启动服务器：`python -S server.py`

### 注意事项

- 服务器默认监听所有网络接口（0.0.0.0），可从局域网访问
- 生产环境建议添加 SSL/TLS 加密
- 建议配置防火墙规则，限制外部访问

## 技术细节

### 代码执行原理

1. 前端发送 Python 代码到后端
2. 后端将代码写入临时文件
3. 使用 subprocess 调用系统 Python 解释器执行
4. 捕获 stdout 和 stderr 输出
5. 返回执行结果到前端

### 安全考虑

- 代码执行设置了 30 秒超时
- 临时文件执行后自动删除
- 禁止访问敏感系统资源
- 数据库密码加密存储

### CORS配置

后端服务器已配置完整的 CORS 支持，允许跨域请求：
- `Access-Control-Allow-Origin: *`
- 支持 GET、POST、OPTIONS 方法
- 支持 Content-Type 请求头

## 版本信息

- 项目版本：1.0.0
- 创建日期：2026-03-31
- 适用年级：八年级

## 联系方式

如有问题，请联系项目开发者。

## 许可证

本项目仅供学习交流使用。
