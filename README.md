# GuessNum FastAPI 项目

## 项目概述

这是一个使用 `FastAPI` 构建的数字猜测游戏应用。该项目已经重构，支持 RESTful API，提供用户注册、登录和游戏记录等功能。

## 依赖项

以下是运行该项目所需的主要依赖项：

- `fastapi`：用于构建 API 的高性能 Web 框架。
- `uvicorn`：用于运行 `FastAPI` 应用的 ASGI 服务器。
- `redis`：用于管理用户会话。
- `mysql-connector-python`：用于连接 MySQL 数据库。
- `bcrypt`：用于安全加密用户密码的哈希库。
- `pydantic`：用于请求数据验证的数据验证库。

## 数据库配置

有关数据库配置和结构，请参阅 [mysql.md](https://github.com/Hanserprpr/guessnum_fastapi_refactor/blob/main/mysql.md)。

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

# 启动项目（允许非本地访问）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 功能特性

- **用户注册和登录**：允许用户安全注册和登录，使用 `bcrypt` 对密码进行加密管理。
- **游戏玩法**：一个数字猜测游戏，用户尝试猜测一个数字，根据猜测次数提供反馈。
- **游戏统计**：存储用户的游戏表现数据，如猜测次数，并根据表现对玩家进行排名。
- **RESTful API**：所有操作都通过 REST 端点提供，便于与其他前端客户端或服务集成。
- **会话管理**：通过 `Redis` 管理用户的登录状态。

## 项目结构

```
├── app
│   ├── main.py       # 应用程序入口
│   ├── models.py     # 数据库模型
│   ├── routes        # 不同模块的 API 路由
│   ├── utils         # 实用函数，如令牌创建、哈希
│   └── ...
├── requirements.txt  # 项目依赖项
├── mysql.md          # MySQL 配置和架构详细信息
├── .env              # 环境变量（不应包含在公共仓库中）
└── README.md         # 项目文档
```

## 环境变量

项目需要在 `.env` 文件中配置一些环境变量以正常运行。以下是 `.env` 文件的示例内容：

```env
DATABASE_URL=mysql://username:password@localhost:3306/guessnum
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost
JWT_ALGORITHM=HS256
```

## 运行测试

可以运行测试来验证应用程序的完整性：

```bash
# 安装测试依赖项
pip install pytest pytest-asyncio

# 运行测试
pytest
```

## API 文档

项目提供了交互式 API 文档，运行应用程序时可以访问以下端点：

- **Swagger UI**：[http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**：[http://localhost:8000/redoc](http://localhost:8000/redoc)

## 详细 API 参考

### 用户注册

- **URL**: `/api/auth/register`
- **方法**: `POST`
- **请求体**:

  ```json
  {
    "name": "string",
    "email": "string",
    "sex": "string",
    "password": "string",
    "qq": "string"
  }
  ```

- **响应**:
  - **状态码 201**: 注册成功

    ```json
    {
      "message": "Registration successful",
      "user": {
        "name": "string",
        "email": "string",
        "sex": "string",
        "qq": "string"
      }
    }
    ```

  - **状态码 400**: 注册失败，例如用户名已存在

    ```json
    {
      "detail": "Username already exists."
    }
    ```

### 用户登录

- **URL**: `/api/auth/login`
- **方法**: `POST`
- **请求体**:

  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **响应**:
  - **状态码 200**: 登录成功

    ```json
    {
      "access_token": "string",
      "token_type": "bearer"
    }
    ```

  - **状态码 401**: 登录失败，例如用户名或密码错误

    ```json
    {
      "detail": "Invalid credentials."
    }
    ```

### 获取用户资料

- **URL**: `/api/user/profile`
- **方法**: `GET`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **响应**:
  - **状态码 200**: 获取成功

    ```json
    {
      "user": {
        "name": "string",
        "sex": "string",
        "email": "string",
        "qq": "string"
      }
    }
    ```

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```

  - **状态码 404**: 用户不存在

    ```json
    {
      "detail": "User not found"
    }
    ```

### 更新用户资料

- **URL**: `/api/user/profile`
- **方法**: `PUT`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **请求体**:

  ```json
  {
    "name": "string",
    "sex": "string",
    "password": "string"
  }
  ```

- **响应**:
  - **状态码 200**: 更新成功

    ```json
    {
      "message": "Profile updated successfully",
      "user": {
        "name": "string",
        "sex": "string",
        "updated_at": "string"
      }
    }
    ```

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```

### 开始游戏

- **URL**: `/api/game/start`
- **方法**: `POST`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **响应**:
  - **状态码 200**: 游戏开始成功

    ```json
    {
      "message": "Game started. Guess a number between 1 and 100."
    }
    ```

### 猜数字

- **URL**: `/api/game/guess`
- **方法**: `POST`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **请求体**:

  ```json
  {
    "guess": "integer"
  }
  ```

- **响应**:
  - **状态码 200**: 猜测结果

    ```json
    {
      "message": "Too high! Try again."
    }
    ```

    或

    ```json
    {
      "message": "Correct! You've guessed the number in X attempts."
    }
    ```

### 游戏统计

- **URL**: `/api/game/stats`
- **方法**: `GET`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **响应**:
  - **状态码 200**: 游戏统计信息

    ```json
    {
      "total_games": "integer",
      "average_attempts": "float",
      "best_game": "integer"
    }
    ```

### 用户排行榜

- **URL**: `/api/game/leaderboard`
- **方法**: `GET`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **响应**:
  - **状态码 200**: 获取排行榜成功

    ```json
    [
      {
        "username": "string",
        "average_attempts": "float",
        "total_games": "integer"
      },
      {
        "username": "string",
        "average_attempts": "float",
        "total_games": "integer"
      }
    ]
    ```

### 个人排名

- **URL**: `/api/game/rank`
- **方法**: `GET`
- **请求头**:
  - `Authorization`: `Bearer <token>`
- **响应**:
  - **状态码 200**: Successful Response

    ```json
    [
      {
        "message": "你还没有参与任何游戏，无法显示排名。"
      },或
      {
      "你的排名": 1,
      "平均成绩": 30
      }
    ]
    ```

## 未来改进

- **游戏分析**：增加更多统计信息，如每局游戏的平均得分、最快完成游戏等。
- **Web 前端**：使用现代框架（如 React）开发前端，使应用程序更加用户友好。
- **邮箱验证**：在用户注册过程中添加邮箱验证步骤。

## 贡献

欢迎贡献！如果您有任何建议或改进，请 fork 此仓库并创建一个 pull request。
