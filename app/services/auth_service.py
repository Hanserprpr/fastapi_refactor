from typing import Dict
from app.services.connsql import Connsql
from app.services.status import ConnRedis
from app.services.jwt_manager import create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .passwd import passwd
import re
passwd_service = passwd
async def register_user(db: Session, name: str, email: str, sex: str, password: str, qq: str) -> Dict:
    connsql = Connsql(db)
    if connsql.search_id(name=name) or connsql.search_id(email=email) or connsql.search_id(QQ=qq):
        raise ValueError("Username, email, or QQ is already taken")
    
    def validate_password(password: str) -> bool:
        has_upper = re.search(r'[A-Z]', password) is not None
        has_lower = re.search(r'[a-z]', password) is not None
        has_digit = re.search(r'\d', password) is not None
        has_special = re.search(r'[\W_]', password) is not None  # 匹配非字母数字字符
        
        # 统计符合条件的类型
        count = sum([has_upper, has_lower, has_digit, has_special])
        return count >= 2

    if not validate_password(password):
        raise ValueError("密码必须包含以下两种字符中的至少两种：大写字母、小写字母、数字、特殊字符。")

    
    encrypted_password = await passwd.encrypt(password)
    connsql.signup(name, email, sex, encrypted_password, qq)
    user_id = connsql.search_id(QQ=qq)

    
    return {"id": user_id, "name": name, "email": email, "sex": sex, "QQ": qq}

async def login_user(db: Session, username: str, password: str) -> str:
    connsql = Connsql(db)
    user = connsql.get_user_by_identifier(username)
    if not user or not await passwd.decrypt(password, username, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    connsql.update_last_login(user_id=user.id)
    # 返回 token 或者用户 session 信息
    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "expires_in" : 1800 }
