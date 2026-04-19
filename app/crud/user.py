from sqlalchemy.orm import Session
from app.models.user import User
from common.dto.user_register_dto import UserRegisterDTO
from common.utils.password_util import PasswordUtil


def create_user(db: Session, user_dto: UserRegisterDTO) -> User:
    """创建用户"""
    # 密码加密
    hashed_password = PasswordUtil.encrypt(user_dto.password)
    
    user = User(
        name=user_dto.name,
        phone=user_dto.phone,
        password=hashed_password,
        sex=user_dto.sex,
        id_number=user_dto.id_number,
        avatar=user_dto.avatar
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_phone(db: Session, phone: str) -> User:
    """根据手机号获取用户"""
    return db.query(User).filter(User.phone == phone).first()


def get_user_by_id(db: Session, user_id: int) -> User:
    """根据ID获取用户"""
    return db.query(User).filter(User.id == user_id).first()



def update_user(db: Session, user_id: int, user_dto: UserRegisterDTO) -> User:
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = user_dto.name
        user.phone = user_dto.phone
        if user_dto.password:
            user.password = PasswordUtil.hash_password(user_dto.password)
        user.sex = user_dto.sex
        user.id_number = user_dto.id_number
        user.avatar = user_dto.avatar
        db.commit()
        db.refresh(user)
    return user
