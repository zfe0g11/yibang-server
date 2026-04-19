from sqlalchemy.orm import Session
from app.models.car_mortgage import CarMortgage
from common.dto.car_mortgage_dto import CarMortgageDTO
from common.dto.car_mortgage_audit_dto import CarMortgageAuditDTO


def create_car_mortgage(db: Session, car_mortgage_dto: CarMortgageDTO) -> CarMortgage:
    """创建车辆抵押申请"""
    # 将图片列表转换为逗号分隔的字符串
    images_str = ",".join(car_mortgage_dto.images) if car_mortgage_dto.images else ""
    
    car_mortgage = CarMortgage(
        openid=car_mortgage_dto.openid,
        car_name=car_mortgage_dto.car_name,
        brand=car_mortgage_dto.brand,
        model=car_mortgage_dto.model,
        description=car_mortgage_dto.description,
        images=images_str,
        status=0  # 初始状态为待审核
    )
    db.add(car_mortgage)
    db.commit()
    db.refresh(car_mortgage)
    return car_mortgage


def get_car_mortgage_by_openid(db: Session, name: str) -> CarMortgage:
    """根据微信号获取车辆抵押申请"""
    return db.query(CarMortgage).filter(CarMortgage.openid == name).first()

def get_car_mortgage_by_id(db: Session, id: int) -> CarMortgage:
    """根据ID获取车辆抵押申请"""
    return db.query(CarMortgage).filter(CarMortgage.id == id).first()

def get_car_mortgage_list(db: Session, openid: str, skip: int = 0, limit: int = 10):
    """获取用户的车辆抵押申请列表"""
    return db.query(CarMortgage).filter(CarMortgage.openid == openid).offset(skip).limit(limit).all()


def get_car_mortgage_page_query(db: Session, car_name: str = None, brand: str = None, model: str = None, status: int = None):
    """分页查询车辆抵押申请"""
    query = db.query(CarMortgage)
    
    if car_name:
        query = query.filter(CarMortgage.car_name.like(f"%{car_name}%"))
    if brand:
        query = query.filter(CarMortgage.brand == brand)
    if model:
        query = query.filter(CarMortgage.model == model)
    if status is not None:
        query = query.filter(CarMortgage.status == status)
    
    return query


def update_car_mortgage_status(db: Session, audit_dto: CarMortgageAuditDTO) -> CarMortgage:
    """更新车辆抵押申请状态"""
    car_mortgage = db.query(CarMortgage).filter(CarMortgage.id == audit_dto.id).first()
    if car_mortgage:
        car_mortgage.status = audit_dto.status
        db.commit()
        db.refresh(car_mortgage)
    return car_mortgage
