import random
import redis
import json
from sqlalchemy.orm import Session
from app.services.connsql import Connsql
from app.config import settings

# 连接 Redis
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

class GameService:
    def __init__(self, db: Session):
        self.connsql = Connsql(db)

    def start_game(self, user_id: str):
        # 生成目标数字并初始化游戏状态
        target_number = random.randint(1, 100)
        game_state = {"target_number": target_number, "attempts": 0}
        redis_client.set(f"game_state:{user_id}", json.dumps(game_state))  # 将游戏状态存入 Redis
        return target_number

    def make_guess(self, user_id: str, guess: int) -> str:
        # 从 Redis 中读取游戏状态
        game_state_json = redis_client.get(f"game_state:{user_id}")
        if game_state_json is None:
            raise ValueError("游戏尚未开始，请先调用 start_game。")

        # 解析状态
        game_state = json.loads(game_state_json)
        target_number = game_state["target_number"]
        game_state["attempts"] += 1
        attempts = game_state["attempts"]
        score = max(100 - attempts * 10, 0)

        if guess < target_number:
            # 更新 Redis 中的游戏状态
            redis_client.set(f"game_state:{user_id}", json.dumps(game_state))
            return "太小了！再试一次。"
        elif guess > target_number:
            redis_client.set(f"game_state:{user_id}", json.dumps(game_state))
            return "太大了！再试一次。"
        else:
            # 如果猜中，记录游戏结果并清除 Redis 中的状态
            self.connsql.save_game_attempt(user_id, "猜数字", score, attempts)
            self.connsql.update_user_stats(user_id, "猜数字", score, attempts)
            redis_client.delete(f"game_state:{user_id}")  # 游戏结束，删除状态
            return f"恭喜你，猜对了！得分为 {score} 分，尝试次数为 {attempts} 次。"
