from mysql.connector import connect
from .config import Config

settings = Config()

db_config = {
    "host": settings.db_host,
    "user": settings.db_user,
    "password": settings.db_password,
    "database": settings.db_name
}

def get_db_connection():
    return connect(**db_config)
