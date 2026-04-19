from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
from app.models.Basemodel import BaseModel,before_insert_listener,before_update_listener
from sqlalchemy import event
class Category(BaseModel):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(Integer, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    sort = Column(Integer, default=0)
    status = Column(Integer, default=1)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    create_user = Column(Integer)
    update_user = Column(Integer)

event.listen(Category, 'before_insert', before_insert_listener)
event.listen(Category, 'before_update', before_update_listener)