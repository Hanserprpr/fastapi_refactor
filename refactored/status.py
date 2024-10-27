import redis.asyncio as aioredis
from app.config import settings

class ConnRedis:
    def __init__(self):
        self.redis = None  # 初始化 redis 属性

    async def init_redis(self):
        """初始化 Redis 连接"""
        self.redis = await aioredis.from_url(settings.redis_url)

    async def close(self):
        """关闭 Redis 连接"""
        if self.redis:
            await self.redis.close()

    async def set_user_logged_in(self, qq_id: str, user_id: str):
        """设置用户登录状态，并存储 QQ 号与用户 ID 的对应关系"""
        await self.redis.set(f"user_session:{user_id}", "logged_in", ex=3600)
        await self.redis.set(f"qq_to_user:{qq_id}", user_id, ex=3600)
        await self.redis.set(f"user_to_qq:{user_id}", qq_id, ex=3600)

    async def extend_user_session(self, user_id: str):
        """续期用户的登录状态"""
        await self.redis.expire(f"user_session:{user_id}", 3600)

    async def set_user_logged_out(self, user_id: str):
        """将用户登出状态从 Redis 中移除"""
        qq_id = await self.redis.get(f"user_to_qq:{user_id}")
        await self.redis.delete(f"user_session:{user_id}")
        await self.redis.delete(f"qq_to_user:{qq_id}")
        await self.redis.delete(f"user_to_qq:{user_id}")

    async def is_user_logged_in(self, user_id: str) -> bool:
        """检查用户是否已登录，并在登录时续期"""
        try:
            status = await self.redis.get(f"user_session:{user_id}")
            if status and status.decode() == "logged_in":
                await self.extend_user_session(user_id)
                return True
            return False
        except Exception as e:
            print(f"检查用户登录状态时发生错误: {e}")
            return False

    async def get_user_id_from_qq(self, qq_id: str) -> str:
        """根据 QQ 号获取用户 ID"""
        return await self.redis.get(f"qq_to_user:{qq_id}")

    async def get_qq_from_user_id(self, user_id: str) -> str:
        """根据用户 ID 获取 QQ 号"""
        return await self.redis.get(f"user_to_qq:{user_id}")
