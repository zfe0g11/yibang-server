from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.car import Car
from common.dto.category_dto import CategoryDTO


def create_category(db: Session, category_dto: CategoryDTO) -> Category:
    """创建分类"""
    category = Category(
        type=category_dto.type,
        name=category_dto.name,
        sort=category_dto.sort
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category_by_id(db: Session, category_id: int) -> Category:
    """根据ID获取分类"""
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Category:
    """根据名称获取分类"""
    return db.query(Category).filter(Category.name == name).first()

def get_category_list(db: Session, category_type: int) -> list[Category]:
    """获取分类列表"""
    return db.query(Category).filter(Category.type == category_type).order_by(Category.sort).all()


def update_category(db: Session, category_id: int, category_dto: CategoryDTO) -> Category:
    """更新分类"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.type = category_dto.type
        category.id = category_dto.id
        category.name = category_dto.name
        category.sort = category_dto.sort
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> bool:
    """删除分类"""
    # 检查是否有车辆属于该分类
    # 检查 brand_id 或 model_id 是否等于分类 ID
    car_count = db.query(Car).filter(
        (Car.brand_id == category_id) | (Car.model_id == category_id)
    ).count()
    
    if car_count > 0:
        # 有车辆属于该分类，不能删除
        return False
    
    # 没有车辆属于该分类，可以删除
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False


def get_category_page_query(db: Session, name: str = None, category_type: int = None):
    """构建分类分页查询"""
    query = db.query(Category)
    
    # 名称模糊查询，使用contains避免SQL注入
    if name:
        query = query.filter(Category.name.contains(name))
    
    # 分类类型过滤
    if category_type is not None:
        query = query.filter(Category.type == category_type)
    
    return query


def update_category_status(db: Session, category_id: int, status: int) -> Category:
    """更新分类状态"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.status = status
        db.commit()
        db.refresh(category)
    return category
