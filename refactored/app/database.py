from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Settings


# 创建 Base 用于模型继承
Base = declarative_base()

# 构建数据库 URL
DATABASE_URL = f"mysql+pymysql://{Settings.db_user}:{Settings.db_password}@{Settings.db_host}/{Settings.db_name}"

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)