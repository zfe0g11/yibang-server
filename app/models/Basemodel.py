from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import event
from common.context.base_context import BaseContext

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # 抽象基类，不会生成表
    
    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_user = Column(Integer, nullable=False)
    update_user = Column(Integer, nullable=False)

def before_insert_listener(mapper, connection, target):
    """在插入前设置 create_time 和 create_user"""
    target.create_time = datetime.utcnow()
    target.create_user = BaseContext.get_current_id() or 0  # 从BaseContext获取当前用户ID，默认0
    
def before_update_listener(mapper, connection, target):
    """在更新前设置 update_time 和 update_user"""
    target.update_time = datetime.utcnow()
    target.update_user = BaseContext.get_current_id() or 0  # 从BaseContext获取当前用户ID，默认0

