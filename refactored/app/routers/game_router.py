from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.GameService import GameService
from app.services.jwt_manager import verify_token
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class GuessRequest(BaseModel):
    guess: int

@router.post("/start_game")
async def start_game(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    game_service = GameService(db)
    game_service.start_game(user_id)
    return {"message": "欢迎来到猜数字游戏！请开始猜吧！"}

@router.post("/guess")
async def make_guess(guess_request: GuessRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    game_service = GameService(db)
    try:
        message = game_service.make_guess(user_id, guess_request.guess)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/restart_game")
async def restart_game(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    game_service = GameService(db)
    return await start_game(token=token, db=db)
