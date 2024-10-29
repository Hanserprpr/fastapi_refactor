from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.GameService import GameService
from app.services.jwt_manager import verify_token
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from app.models.game import LeaderboardResponse, LeaderboardEntry
from app.services.connsql import Connsql

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class GuessRequest(BaseModel):
    guess: int

@router.post("/start_game")
async def start_game(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    game_service = GameService(db)
    game_service.start_game(user_id)
    return {"message": "欢迎来到猜数字游戏！我已经想好了 1 到 100 之间的一个数字，请开始猜吧！"}

@router.post("/guess")
async def make_guess(guess_request: GuessRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    game_service = GameService(db)
    try:
        message = game_service.make_guess(user_id, guess_request.guess)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# 获取游戏历史记录
@router.get("/history")
async def get_history(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    game_service = GameService(db)
    history = game_service.get_history(user_id)
    if not history:
        return {"message": "你还没有任何游戏记录！"}
    return [{"date": record.played_at, "score": record.score, "attempts": record.attempts} for record in history]

@router.get("/leaderboard", response_model=LeaderboardResponse)
async def leaderboard(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), limit: int = 10):
    user_id = verify_token(token)  
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    game_service = GameService(db)

    # 获取排行榜数据
    leaderboard_entries = game_service.get_leaderboard(limit=limit)

    leaderboard_data = [
        {
            "用户id": entry["用户id"],
            "用户名": entry["用户名"],
            "平均分": entry["平均分"],
            "游戏次数": entry["游戏次数"],
            "排名": entry["排名"]                
        }
        for entry in leaderboard_entries
    ]

    # 构建 Pydantic 实例
    entries = [LeaderboardEntry(**data) for data in leaderboard_data]


    user_rank = game_service.get_user_rank(user_id, game_name="猜数字")

    # 如果没有用户排名信息，设置默认值
    user_rank_value = user_rank["ranking"] if user_rank else -1
    user_average_score_value = user_rank["average_score"] if user_rank else 0.0

    return LeaderboardResponse(
        leaderboard=entries,
        你的排名=user_rank_value,
        平均成绩=user_average_score_value
    )
    
# 获取用户当前排名
@router.get("/rank")
async def get_user_rank(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    game_service = GameService(db)
    user_rank = game_service.get_user_rank(user_id, game_name="猜数字")
    if not user_rank:
        return {"message": "你还没有参与任何游戏，无法显示排名。"}
    return {"你的排名": user_rank["ranking"], "平均成绩": user_rank["average_score"]}