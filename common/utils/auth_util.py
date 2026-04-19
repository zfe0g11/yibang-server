from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.employee import get_employee
from common.utils.redis_util import redis_util

def get_current_user(
    token: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db)
):
    """获取当前用户"""
    employee_id = redis_util.get(f"token:{token}")

    if not employee_id:
        raise HTTPException(status_code=401, detail="未授权")
    
    # 根据员工 ID 从数据库获取员工信息
    employee = get_employee(db, int(employee_id))
    if not employee:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    return employee