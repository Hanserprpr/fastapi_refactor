# GuessNum FastAPI Project

## 项目简介

这是一个基于 `FastAPI` 的数字猜测游戏应用。该项目已经重构(假的)，支持 RESTful API，提供用户注册、登录和游戏记录等功能。

## 依赖项

以下是运行该项目所需的主要依赖项：

- `fastapi` - 高性能 Web 框架，用于构建 API。
- `uvicorn` - ASGI 服务器，用于运行 `FastAPI` 应用。
- `redis` - 用于用户会话管理。
- `mysql-connector-python` - 用于与 MySQL 数据库的连接。
- `bcrypt` - 密码哈希库，用于加密用户密码。
- `pydantic` - 数据验证库，适用于请求数据验证。

## 数据库配置

数据库配置及结构请见 [mysql.md](https://github.com/Hanserprpr/guessnum_fastapi_refactor/blob/main/mysql.md)

## 安装步骤

在项目根目录中创建虚拟环境并安装依赖项：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# 在 Windows 上
venv\Scripts\activate
# 在 macOS 或 Linux 上
source venv/bin/activate

# 安装依赖项
pip install -r requirements.txt
