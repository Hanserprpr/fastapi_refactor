from typing import Dict
from app.services.connsql import Connsql
from app.services.status import ConnRedis
from app.services.jwt_manager import create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .passwd import passwd
passwd_service = passwd
async def register_user(db: Session, name: str, email: str, sex: str, password: str, qq: str) -> Dict:
    connsql = Connsql(db)
    if connsql.search_id(name=name) or connsql.search_id(email=email) or connsql.search_id(QQ=qq):
        raise ValueError("Username, email, or QQ is already taken")
    
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
    return {"access_token": access_token, "token_type": "bearer"}
