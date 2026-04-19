from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CarMortgage(Base):
    __tablename__ = "car_mortgage"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    openid = Column(String(45), nullable=False, comment="微信用户唯一标识")
    car_name = Column(String(100), nullable=False, comment="车辆名称")
    brand = Column(String(50), nullable=False, comment="品牌")
    model = Column(String(50), nullable=False, comment="车型")
    description = Column(String(500), nullable=True, comment="描述")
    images = Column(String(1000), nullable=False, comment="图片URL，多个图片用逗号分隔")
    status = Column(Integer, nullable=False, default=0, comment="状态：0-待审核，1-审核通过，2-审核拒绝")
    create_time = Column(DateTime, nullable=True, default=datetime.now)
