from sqlalchemy.orm import Session
from app.schemas.employee import  EmployeeUpdate
from common.dto.employee_dto import EmployeeDTO
from app.models.employee import Employee
from common.context.base_context import BaseContext



def get_employee(db: Session, employee_id: int):
    """根据ID获取员工信息"""
    return db.query(Employee).filter(Employee.id == employee_id).first()


def update_employee_status(db: Session, employee_id: int, status: int):
    """更新员工状态"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return None
    
    employee.status = status
    employee.update_time = datetime.utcnow()
    employee.update_user = BaseContext.get_current_id() or 0
    db.commit()
    db.refresh(employee)
    
    return employee


def get_employee_by_username(db: Session, username: str):
    """根据用户名获取员工信息"""
    return db.query(Employee).filter(Employee.username == username).first()


from app.utils.password_util import md5_encrypt
from datetime import datetime

def create_employee(db: Session, employee_dto: EmployeeDTO):
    """创建员工"""
    employee = Employee(
        username=employee_dto.username,
        password=md5_encrypt("123456"),
        name=employee_dto.name,
        phone=employee_dto.phone,
        sex=employee_dto.sex,
        id_number=employee_dto.id_number,
        status= 1
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    """更新员工信息"""
    db_employee = get_employee(db, employee_id)
    if db_employee:
        if employee.name:
            db_employee.name = employee.name
        if employee.phone:
            db_employee.phone = employee.phone
        if employee.sex:
            db_employee.sex = employee.sex
        if employee.id_number:
            db_employee.id_number = employee.id_number
        if employee.status is not None:
            db_employee.status = employee.status
        db_employee.update_time = datetime.utcnow()
        db_employee.update_user = BaseContext.get_current_id() or 1  # 从BaseContext获取当前用户ID，默认1
        db.commit()
        db.refresh(db_employee)
    return db_employee


def get_employee_page_query(db: Session, name: str = None):
    """构建员工分页查询"""
    query = db.query(Employee)
    
    # 姓名模糊查询，使用contains避免SQL注入
    if name:
        query = query.filter(Employee.name.contains(name))
    
    return query