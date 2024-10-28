from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # 自动从 .env 文件中读取这些变量
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    secret_key: str = "supersecretkey" 
    debug: bool = True
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db: int = int(os.getenv("REDIS_DB", 0))
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
