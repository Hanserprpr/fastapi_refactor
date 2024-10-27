from fastapi import APIRouter

# 创建 APIRouter 实例
router = APIRouter()

# 示例路由
@router.get("/")
async def read_users():
    return {"message": "List of users"}
