from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import get_user_profile, update_user_profile
from pydantic import BaseModel
from app.services.jwt_manager import verify_token
from fastapi.security import OAuth2PasswordBearer
from app.services.connsql import Connsql
router = APIRouter()

class UserProfile(BaseModel):
    name: str = None
    sex: str = None
    password: str = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    connsql = Connsql(db)
    user_profile = connsql.get_me(user_id=user_id)
    
    if user_profile == "用户不存在":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"user": user_profile}


@router.put("/profile")
async def update_profile(user_data: UserProfile, token: str, db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    updated_user = update_user_profile(db, user_id, name=user_data.name, sex=user_data.sex, password=user_data.password)
    return {
        "message": "Profile updated successfully",
        "user": {
            "name": updated_user.name,
            "sex": updated_user.sex,
            "updated_at": updated_user.updated_at  
        }
    }
