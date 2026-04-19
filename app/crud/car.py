from sqlalchemy.orm import Session
from app.models.car import Car
from common.dto.car_dto import CarDTO


def create_car(db: Session, car_dto: CarDTO) -> Car:
    """创建车辆"""
    car = Car(
        name=car_dto.name,
        model_id=car_dto.model_id,
        brand_id=car_dto.brand_id,
        price=car_dto.price,
        image=car_dto.image,
        description=car_dto.description
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def get_car_by_id(db: Session, car_id: int) -> Car:
    """根据ID获取车辆"""
    return db.query(Car).filter(Car.id == car_id).first()


def get_car_by_name(db: Session, car_name: str) -> Car:
    """根据名称获取车辆"""
    return db.query(Car).filter(Car.name == car_name).first()


def get_car_page_query(db: Session, name: str = None, model_id: int = None, brand_id: int = None):
    """构建车辆分页查询"""
    query = db.query(Car)
    
    # 名称模糊查询
    if name:
        query = query.filter(Car.name.contains(name))
    
    # 型号过滤
    if model_id is not None:
        query = query.filter(Car.model_id == model_id)
    
    # 品牌过滤
    if brand_id is not None:
        query = query.filter(Car.brand_id == brand_id)
    
    return query


def update_car(db: Session, car_id: int, car_dto: CarDTO) -> Car:
    """更新车辆信息"""
    car = db.query(Car).filter(Car.id == car_id).first()
    if car:
        car.name = car_dto.name
        car.model_id = car_dto.model_id
        car.brand_id = car_dto.brand_id
        car.price = car_dto.price
        car.image = car_dto.image
        car.description = car_dto.description
        db.commit()
        db.refresh(car)
    return car


def delete_car(db: Session, car_id: int) -> bool:
    """删除车辆"""
    car = db.query(Car).filter(Car.id == car_id).first()
    if car:
        db.delete(car)
        db.commit()
        return True
    return False
