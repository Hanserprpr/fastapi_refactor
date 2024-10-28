from pydantic_settings import BaseSettings
from pydantic import RedisDsn
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()  # 手动加载 .env 文件

class Settings(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    debug: bool
    redis_url: Optional[RedisDsn] = None
    secret_key: str
    algorithm: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    redis_host: str
    redis_port: int
    redis_db: int

    class Config:
        env_file = ".env"  # 指定 .env 文件路径
        extra = "ignore"

settings = Settings()
