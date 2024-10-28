from sqlalchemy.orm import Session
from ..models.user import User 
from ..models.game import GameAttempt, GameStats
from datetime import datetime
import re
from sqlalchemy import func


class Connsql:
    def __init__(self, db_session: Session):
        """初始化 Connsql 类，使用依赖注入传入数据库会话"""
        self.db = db_session

    def signup(self, name: str, email: str, sex: str, passwd: str, QQ: str):
        """注册新用户"""
        new_user = User(name=name, email=email, sex=sex, passwd=passwd, QQ=QQ)
        self.db.add(new_user)
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error during signup: {e}")
    
    def search_passwd(self, identifier: str) -> str:
        """根据用户名或邮箱查询密码"""
        query_field = User.email if re.match(r"[^@]+@[^@]+\.[^@]+", identifier) else User.name
        user = self.db.query(User).filter(query_field == identifier).first()
        return user.passwd if user else None

    def search_id(self, name: str = None, QQ: str = None, email: str = None) -> int:
        """根据名称、QQ 或邮箱查询用户 ID"""
        query_filter = User.name == name if name else User.QQ == QQ if QQ else User.email == email
        user = self.db.query(User).filter(query_filter).first()
        return user.id if user else None

    def search_name(self, QQ: str = None, user_id: int = None) -> str:
        """根据 QQ 或用户 ID 查询用户名"""
        user = None
        if QQ:
            user = self.db.query(User).filter(User.QQ == QQ).first()
        elif user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
        return user.name if user else None

    def get_me(self, QQ: str = None, user_id: str = None) -> dict:
        """查询用户个人信息"""
        user = None
        if QQ:
            user = self.db.query(User).filter(User.QQ == QQ).first()
        elif user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
        
        if user:
            return {
                "用户ID": user.id,
                "用户名": user.name,
                "邮箱": user.email,
                "性别": "男" if user.sex == "M" else "女" if user.sex == "F" else "其他",
                "QQ": user.QQ,
                "账号状态": "活跃" if user.status == 1 else "禁用",
                "注册时间": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "最后更新时间": user.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "最后登录时间": user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "N/A"
            }
        return {"detail": "用户不存在"}

    def update_last_login(self, QQ: str = None, user_id: str = None):
        """更新用户最后登录时间"""
        user = None
        if QQ:
            user = self.db.query(User).filter(User.QQ == QQ).first()
        elif user_id:
            user = self.db.query(User).filter(User.id == user_id).first()
        
        if user:
            user.last_login = datetime.now()
            self.db.commit()

    def update_user_info(self, QQ: str, name: str = None, passwd: str = None, sex: str = None):
        """更新用户信息"""
        user = self.db.query(User).filter(User.QQ == QQ).first()
        if user:
            if name:
                user.name = name
            if passwd:
                user.passwd = passwd
            if sex:
                user.sex = sex
            user.updated_at = datetime.now()
            self.db.commit()

    def save_game_attempt(self, user_id: int, game_name: str, score: int, attempts: int):
        """保存用户的游戏尝试结果"""
        new_attempt = GameAttempt(user_id=user_id, game_name=game_name, score=score, attempts=attempts, result="win")
        self.db.add(new_attempt)
        self.db.commit()

    def update_user_stats(self, user_id: int, game_name: str, score: int, attempts: int):
        """更新用户的游戏统计数据"""
        stats = self.db.query(GameStats).filter(GameStats.user_id == user_id, GameStats.game_name == game_name).first()
        
        if stats:
            stats.total_score += score
            stats.games_played += 1
            stats.average_score = stats.total_score / stats.games_played
            stats.min_attempts = min(stats.min_attempts, attempts)
            stats.max_attempts = max(stats.max_attempts, attempts)
            stats.play_count += 1
            stats.last_played = datetime.now()
        else:
            new_stats = GameStats(
                user_id=user_id, game_name=game_name, total_score=score,
                games_played=1, average_score=score, wins=1, play_count=1,
                min_attempts=attempts, max_attempts=attempts, last_played=datetime.now()
            )
            self.db.add(new_stats)
        self.db.commit()

    def fetch_game_history(self, user_id: int, game_name: str):
        """获取用户的游戏历史记录"""
        history = self.db.query(GameAttempt).filter(GameAttempt.user_id == user_id, GameAttempt.game_name == game_name).order_by(GameAttempt.played_at.desc()).limit(10).all()
        return history

    def fetch_leaderboard(self, game_name: str, limit: int = 10):
        """获取游戏排行榜"""
        leaderboard = (
            self.db.query(GameStats.user_id, GameStats.average_score, GameStats.games_played, User.name.label("username"))
            .join(User, GameStats.user_id == User.id)
            .filter(GameStats.game_name == game_name)
            .order_by(GameStats.average_score.desc())
            .limit(limit)
            .all()
        )
        
        # 打印查询结果
        print("Leaderboard query result:", leaderboard)

        # 将查询结果转换为字典格式，使用元组索引访问字段
        return [
            {
                "用户id": entry[0],          # entry[0] 对应 user_id
                "用户名": entry[3],           # entry[3] 对应 username
                "平均分": entry[1],           # entry[1] 对应 average_score
                "游戏次数": entry[2],         # entry[2] 对应 games_played
                "排名": idx + 1               # 自动排名
            }
            for idx, entry in enumerate(leaderboard)
        ]


    def get_user_rank(self, user_id: int, game_name: str):
        """获取用户在游戏中的排名"""

        # 使用子查询获取用户的排名信息
        subquery = (
            self.db.query(GameStats.user_id, GameStats.average_score, func.rank().over(order_by=GameStats.average_score.desc()).label("ranking"))
            .filter(GameStats.game_name == game_name)
            .subquery()
        )
        rank_info = self.db.query(subquery).filter(subquery.c.user_id == user_id).first()
        # 如果 rank_info 存在，将其转换为字典
        if rank_info:
            return {
                "ranking": rank_info.ranking,
                "average_score": rank_info.average_score,
            }
        else:
            return None




    def get_user_by_identifier(self, identifier: str) -> User:
        """通过用户名或邮箱获取完整用户对象"""
        query_field = User.email if re.match(r"[^@]+@[^@]+\.[^@]+", identifier) else User.name
        return self.db.query(User).filter(query_field == identifier).first()
