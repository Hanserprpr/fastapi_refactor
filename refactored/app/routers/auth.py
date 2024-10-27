from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user
from app.database import get_db
from app.services.status import ConnRedis
router = APIRouter()

class LoginRequest(BaseModel):
    identifier: str  # 用户名或邮箱
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    sex: str
    password: str
    qq: str

class LoginRequest(BaseModel):
    identifier: str  # 可以是用户名或邮箱
    password: str

# 初始化 ConnRedis 实例
async def get_redis_conn():
    redis_conn = ConnRedis()
    await redis_conn.init_redis()
    try:
        yield redis_conn
    finally:
        await redis_conn.close()

@router.post("/register", response_model=dict)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    redis_conn: ConnRedis = Depends(get_redis_conn)
):
    try:
        # 将 redis_conn 传入 register_user
        user = await register_user(db, redis_conn, request.name, request.email, request.sex, request.password, request.qq)
        return {"message": "Registration successful", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=dict)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return await login_user(db, request.identifier, request.password)

@router.post("/edit", response_model=dict)
async def edit(
    
)