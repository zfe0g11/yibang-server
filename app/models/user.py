from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    openid = Column(String(45), nullable=True, comment="微信用户唯一标识")
    name = Column(String(32), nullable=True, comment="姓名")
    phone = Column(String(11), nullable=True, comment="手机号")
    password = Column(String(100), nullable=True, comment="密码")
    sex = Column(String(2), nullable=True, comment="性别")
    id_number = Column(String(18), nullable=True, comment="身份证号")
    avatar = Column(String(500), nullable=True, comment="头像")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
