from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import event
from app.models.Basemodel import BaseModel,before_insert_listener,before_update_listener
Base = declarative_base()

class Employee(BaseModel):
    __tablename__ = "employee"  # 表名
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    sex = Column(String(10), nullable=False)
    id_number = Column(String(20), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    create_user = Column(Integer, nullable=False)
    update_user = Column(Integer, nullable=False)
    
event.listen(Employee, 'before_insert', before_insert_listener)
event.listen(Employee, 'before_update', before_update_listener)