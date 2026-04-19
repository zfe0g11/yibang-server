from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admintoor@172.23.216.43/Xxk_yibang?charset=utf8mb4"

# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型
Base = declarative_base()

 # 从BaseContext获取当前用户ID，默认0
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()