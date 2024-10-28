import sys
from pathlib import Path

# 将项目的根目录添加到 sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.jwt_manager import verify_token

user_id = verify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAxMjcyNjYsInN1YiI6IjEifQ.hFmg239JwFpuMZVmXU29TnGpbWvfp-sb435upKuV1XE")
print(user_id)