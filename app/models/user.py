from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

# 用户表模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    sex = Column(Enum('M', 'F', 'Other'), nullable=False)
    passwd = Column(String(128), nullable=False)
    QQ = Column(String(10), nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)

    # 关系
    game_attempts = relationship("GameAttempt", back_populates="user")
    game_stats = relationship("GameStats", back_populates="user")
