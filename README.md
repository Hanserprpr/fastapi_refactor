# GuessNum FastAPI 项目

## 项目概述

这是一个使用 `FastAPI` 构建的数字猜测游戏应用。该项目已经重构，支持 RESTful API，提供用户注册、登录和游戏记录等功能。

## 依赖项

以下是运行该项目所需的主要依赖项：

- **annotated-types**：用于支持 Python 3.9+ 的注解类型。
- **anyio**：用于异步 I/O，提供高层次的异步编程 API。
- **bcrypt**：用于安全加密用户密码的哈希库。
- **email_validator**：用于验证电子邮件地址的库。
- **fastapi**：用于构建 API 的高性能 Web 框架。
- **h11**：用于 HTTP/1.1 协议的库。
- **pydantic**：用于请求数据验证的数据验证库。
- **pydantic-settings**：用于管理 Pydantic 配置。
- **pydantic-core**：Pydantic 的核心库，处理数据验证和序列化。
- **PyJWT**：用于创建和验证 JSON Web Tokens。
- **PyMySQL**：用于连接 MySQL 数据库的纯 Python 实现。
- **python-dotenv**：用于加载环境变量的库。
- **python-multipart**：用于处理 multipart 表单数据的库。
- **redis**：用于管理用户猜数字状态。
- **SQLAlchemy**：用于数据库 ORM 操作的库。
- **uvicorn**：用于运行 FastAPI 应用的 ASGI 服务器。

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
- **会话管理**：通过 `Redis` 管理用户的游戏状态。

## 项目结构

```python

├── app
│   ├── main.py        # 应用程序入口
│   ├── config.py      # 配置文件
│   ├── database.py     # 数据库连接和配置
│   ├── dependencies.py # 依赖项管理
│   ├── test.py        # 测试文件
│   ├── models         # 数据库模型
│   │   ├── game.py    # 游戏模型
│   │   ├── user.py    # 用户模型
│   │   └── __init__.py # 初始化文件
│   ├── routers        # 不同模块的 API 路由
│   │   ├── auth.py    # 认证路由
│   │   ├── game_router.py  # 游戏相关路由
│   │   └── user_router.py  # 用户相关路由
│   └── services       # 业务逻辑和服务
│       ├── auth_service.py # 认证服务
│       ├── connsql.py      # 数据库连接服务
│       ├── GameService.py   # 游戏服务
│       ├── jwt_manager.py   # JWT 管理
│       ├── passwd.py        # 密码处理
│       └── user_service.py  # 用户服务
│
├── requirements.txt   # 项目依赖项
├── mysql.md           # MySQL 配置和架构详细信息
├── .env               # 环境变量
└── README.md          # 项目文档
```

## 环境变量

项目需要在 `.env` 文件中配置一些环境变量以正常运行。以下是 `.env` 文件的示例内容：

```env
DATABASE_URL=mysql://username:password@localhost:3306/guessnum
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost
JWT_ALGORITHM=HS256
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
  - **状态码 200**: 注册成功

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
    "detail": "Username, email, or QQ is already taken"
    }
    ```

### 用户登录

- **URL**: `/api/auth/login`
- **方法**: `POST`
- **URL**: `/api/login`
- **方法**: `POST`
- **请求头**:
  - `Content-Type: application/x-www-form-urlencoded`
- **请求体**:

  ```plaintext
  username=<string>&password=<string>
  ```

  | 参数     | 类型   | 描述               |
  |----------|--------|--------------------|
  | username | string | 用户名             |
  | password | string | 用户密码           |

### 响应

#### 成功响应

- **状态码**: `200 OK`
- **响应体**:

  ```json
  {
    "access_token": "<token>",
    "token_type": "bearer",
    "expires_in": 1800
  }
  ```

  | 参数        | 类型   | 描述                  |
  |-------------|--------|-----------------------|
  | access_token| string | 用户的访问令牌        |
  | token_type  | string | 令牌类型（如 bearer） |
  | expires_in  | int    | 令牌的有效时间（秒）  |

#### 失败响应

- **状态码**: `401 Unauthorized`
- **响应体**:

  ```json
  {
    "detail": "Invalid username or password"
  }
  ```

  | 参数    | 类型   | 描述                           |
  |---------|--------|--------------------------------|
  | detail  | string | 错误信息                       |

### 示例

#### 请求示例

```bash
curl -X POST "http://127.0.0.1/api/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=user123&password=pass123"
```

#### 响应示例

```json
{
  "access_token": "abc123",
  "token_type": "bearer",
  "expires_in": 1800
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

- 请求体参数可**只选其一**

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
      "message": "欢迎来到猜数字游戏！我已经想好了 1 到 100 之间的一个数字，请开始猜吧！"
    }
    ```

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
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
    "guess": "num"
  }
  ```

- **响应**:
  - **状态码 200**: 猜测结果

    ```json
    {
      "message": "太大了！再试一次。"
    }
    ```

    或

    ```json
    {
      "message": "恭喜你，猜对了！你的得分为 {score} 分，尝试次数为 {attempts} 次。"
    }
    ```

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```

### 游戏统计

- **URL**: `/api/game/history`
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

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
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

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
    }
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

  - **状态码 401**: 未授权

    ```json
    {
      "detail": "Invalid or expired token"
    }
    ```

## 未来改进

- **游戏分析**：增加更多统计信息，如每局游戏的平均得分、最快完成游戏等。
- **Web 前端**：使用现代框架（如 React）开发前端，使应用程序更加用户友好。
- **邮箱验证**：在用户注册过程中添加邮箱验证步骤。

## 贡献

欢迎贡献！如果您有任何建议或改进，请 fork 此仓库并创建一个 pull request。
