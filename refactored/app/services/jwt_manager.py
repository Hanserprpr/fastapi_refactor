import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

from datetime import datetime, timedelta, timezone
import jwt

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = {}
    # 设置过期时间
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    to_encode["sub"] = data["user_id"]
    
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)




def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print("Decoded payload in verify_token:", payload)  # 检查解码后的 payload
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
