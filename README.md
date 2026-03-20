# 哈尼梯田红米文化展示网站

基于 `Vue 3 + Element Plus + FastAPI + MySQL` 的前后端分离文化展示网站初版，实现了动态首页展示、管理员登录以及轮播图 / 板块 / 产品 / 新闻的后台管理。前端展示内容不写死，全部通过 FastAPI RESTful 接口获取；后端启动后可自动建表并注入首批演示数据，便于本地直接联调。

## 技术栈清单

### 前端
- Vue 3
- Vue Router 4
- Element Plus
- Axios
- Vite

### 后端
- FastAPI
- SQLAlchemy 1.4
- PyMySQL
- python-jose
- Passlib
- Pydantic

### 数据库
- MySQL 8.0+（推荐）

## 环境要求

- Node.js `>= 18`，当前开发环境验证版本：`22.13.0`
- npm `>= 9`，当前环境可使用 `npm.cmd`
- Python `>= 3.8`，当前开发环境验证版本：`3.8.7`
- MySQL `>= 8.0`

## 本地部署步骤

### 1. 克隆并进入项目目录

```bash
cd qunzhuWEB
```

### 2. 启动后端

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
Copy-Item backend/.env.example backend/.env
```

修改 `backend/.env` 中的数据库连接、JWT 密钥和管理员账号密码。

### 3. 初始化数据库与演示数据

```bash
python -m backend.scripts.init_db
```

说明：
- 会自动创建数据库表
- 会创建管理员账号
- 会在内容为空时注入演示轮播图、板块、产品和新闻数据

### 4. 启动 FastAPI 服务

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

接口文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 5. 启动前端

```bash
Copy-Item frontend/.env.example frontend/.env
cd frontend
npm.cmd install
npm.cmd run dev
```

前端默认地址：`http://127.0.0.1:5173`

## 默认联调地址

- 前端首页：`http://127.0.0.1:5173/`
- 后台登录：`http://127.0.0.1:5173/admin/login`
- 后端接口：`http://127.0.0.1:8000/api/v1`

## 目录结构说明

```text
qunzhuWEB/
├─ backend/
│  ├─ app/
│  │  ├─ core/        # 配置、数据库、JWT 鉴权
│  │  ├─ crud/        # 通用 CRUD 辅助方法
│  │  ├─ models/      # SQLAlchemy 数据模型
│  │  ├─ routers/     # RESTful 路由
│  │  ├─ schemas/     # Pydantic 请求/响应模型
│  │  ├─ services/    # 初始化种子数据等服务
│  │  ├─ deps.py      # 登录态依赖注入
│  │  └─ main.py      # FastAPI 应用入口
│  ├─ scripts/
│  │  └─ init_db.py   # 初始化数据库与演示数据
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ src/
│  │  ├─ api/         # 接口封装
│  │  ├─ components/  # 首页通用组件
│  │  ├─ router/      # 前端路由
│  │  ├─ styles/      # 全局主题样式
│  │  ├─ utils/       # Token 存取工具
│  │  └─ views/       # 首页与后台页面
│  ├─ package.json
│  └─ vite.config.js
├─ README.md
├─ .gitignore
└─ 项目要求.md
```

## 核心接口文档链接

后端启动后可直接查看 FastAPI 自动生成文档：

- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

常用接口示例：

- `POST /api/v1/auth/login` 管理员登录
- `GET /api/v1/public/home` 获取首页全部展示内容
- `GET /api/v1/banners` 获取轮播图分页列表
- `POST /api/v1/banners` 新增轮播图
- `GET /api/v1/sections` 获取板块分页列表
- `GET /api/v1/products` 获取产品分页列表
- `GET /api/v1/news` 获取新闻分页列表

## 已实现功能

- 首页动态渲染轮播图、文化板块、产品展示、新闻动态
- Element Plus 风格轻量定制，整体偏原生态农耕文化视觉
- 后台管理员登录与 Token 鉴权
- 轮播图 CRUD
- 板块内容 CRUD
- 产品内容 CRUD
- 新闻内容 CRUD
- 首次运行自动建表和首批演示数据注入
- 代码按前后端模块拆分，适合继续扩展上传、权限、SEO 等能力

## 打包部署说明

### 前端打包

```bash
cd frontend
npm.cmd install
npm.cmd run build
```

构建产物位于 `frontend/dist/`。

### 后端部署

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

生产环境建议：
- 使用真实 MySQL 库
- 替换高强度 `JWT_SECRET_KEY`
- 使用 Nginx 反向代理静态资源和 API
- 将图片上传改造为对象存储或本地文件服务

## 常见问题排查

### 1. `npm` 无法执行

PowerShell 可能限制 `npm.ps1` 执行，可改用：

```bash
npm.cmd install
npm.cmd run dev
```

### 2. 后台无法登录

确认：
- `backend/.env` 中配置了正确的 `ADMIN_USERNAME` 和 `ADMIN_PASSWORD`
- 已执行 `python -m backend.scripts.init_db`
- 后端启动时能够连接 MySQL

### 3. 前端无法请求后端接口

确认：
- 后端服务已运行在 `http://127.0.0.1:8000`
- `frontend/.env` 中 `VITE_API_BASE_URL=/api/v1`
- Vite 代理未被修改

### 4. `pip install -r backend/requirements.txt` 失败

如果你使用的是 `Python 3.8.x`，原先的 `uvicorn[standard]==0.34.0` 会报错，因为该版本要求 `Python >= 3.9`。当前项目已经改为兼容 `Python 3.8` 的 `uvicorn[standard]==0.33.0`。

直接重新执行：

```bash
pip install -r backend/requirements.txt
```

如果你之前已经在当前虚拟环境里装过错误版本，也可以先执行：

```bash
pip uninstall uvicorn -y
pip install -r backend/requirements.txt
```

### 5. MySQL 建表失败

确认：
- 已先手动创建数据库，例如 `hani_rice`
- `DATABASE_URL` 用户名、密码、端口正确
- MySQL 字符集建议使用 `utf8mb4`

## 后续建议

当前版本已完成“可展示 + 可管理 + 可部署”的初步开发。下一阶段建议优先补充：

1. 图片上传到本地或对象存储，替代纯链接录入
2. 富文本编辑器，用于新闻正文和文化板块编辑
3. Alembic 数据迁移
4. 更细的后台表单校验与操作日志
5. SEO 元信息、站点页脚、联系表单等扩展内容管理
