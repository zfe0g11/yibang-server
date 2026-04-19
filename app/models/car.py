from sqlalchemy import Column, Integer, String, Float, Text
from app.models.Basemodel import BaseModel
from app.models.Basemodel import BaseModel,before_insert_listener,before_update_listener
from sqlalchemy import event
class Car(BaseModel):
    """车辆模型"""
    __tablename__ = "car"
    
    id = Column(Integer, primary_key=True, index=True, comment="车辆ID")
    name = Column(String(100), nullable=False, comment="车辆名称")
    model_id = Column(Integer, nullable=False, comment="型号ID")
    brand_id = Column(Integer, nullable=False, comment="品牌ID")
    price = Column(Float, nullable=False, comment="价格")
    image = Column(String(500), nullable=False, comment="图片URL")
    description = Column(Text, nullable=True, comment="描述")

event.listen(Car, 'before_insert', before_insert_listener)
event.listen(Car, 'before_update', before_update_listener)
