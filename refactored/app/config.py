from pydantic import BaseSettings

class Settings(BaseSettings):
    # 自动从 .env 文件中读取这些变量
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    secret_key: str = "supersecretkey"  # 默认值，可以在 .env 中覆盖
    debug: bool = True

    class Config:
        env_file = ".env"  # 指定 .env 文件

# 创建配置实例
settings = Settings()
