from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from app.config import Settings

# 实例化 Settings
settings = Settings()

DATABASE_URL = f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
