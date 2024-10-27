from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import get_user_profile, update_user_profile
from pydantic import BaseModel
from app.services.jwt_manager import verify_token

router = APIRouter()

class UserProfile(BaseModel):
    name: str = None
    sex: str = None
    password: str = None

# Route to get user profile with full timestamp details
@router.get("/profile")
async def get_profile(token: str, db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user_profile = get_user_profile(db, user_id)
    return {
        "user": {
            "name": user_profile["name"],
            "sex": user_profile["sex"],
            "email": user_profile["email"],
            "created_at": user_profile["created_at"],
            "updated_at": user_profile["updated_at"],
            "last_login_at": user_profile["last_login_at"]
        }
    }

# Route to update user profile
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
            "updated_at": updated_user.updated_at  # Returning updated timestamp
        }
    }
