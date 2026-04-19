from fastapi import APIRouter, Depends,  Header
#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.employee import get_employee_by_username, create_employee as create_employee_db, update_employee, get_employee, get_employee_page_query, update_employee_status
from app.schemas.employee import EmployeeUpdate
from app.core.database import get_db
from common.result.result import Result
# 导入 sky-common 的工具和常量
from common.utils.jwt_util import JwtUtil
from common.utils.password_util import PasswordUtil
from common.constant.message_constant import MessageConstant
from common.exception.base_exception import (
    AccountNotFoundException,
    AccountLockedException,
    PasswordErrorException,
    Account_ALREADY_EXISTS
)
from common.result.result import Result
from common.utils.auth_util import get_current_user
# 导入 sky-pojo 的 DTO 和 VO
from common.dto.employee_dto import EmployeeDTO
from common.dto.employee_login_dto import EmployeeLoginDTO
from common.dto.employee_page_query_dto import EmployeePageQueryDTO
from common.result.page_result import PageResult
# 导入 fastapi-pagination
from fastapi_pagination import  Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from datetime import datetime
from common.context.base_context import BaseContext
from common.utils.redis_util import redis_util

router = APIRouter()


@router.post(
    "/employee/login",
    response_model=dict,
    summary="员工登录",
    description="员工登录接口，验证用户名和密码，返回JWT token",
    responses={
        200: {"description": "登录成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "user_name": "admin", "name": "管理员", "token": "JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}}}}},
        401: {"description": "用户名或密码错误"},
        403: {"description": "账号已禁用"}
    }
)
def login(employee_login: EmployeeLoginDTO, db: Session = Depends(get_db)):
    """员工登录"""
    try:
        fail_count = redis_util.get(f"login_fail:{employee_login.username}")
        if fail_count and int(fail_count) >= 5:
            raise AccountLockedException("登录失败次数过多，账号已锁定")     
        # 查找员工
        employee = get_employee_by_username(db, employee_login.username)
        
# 验证员工是否存在
        if not employee:
            # 记录登录失败
            redis_util.incr(f"login_fail:{employee_login.username}")
            redis_util.setex(f"login_fail:{employee_login.username}", 900, redis_util.get(f"login_fail:{employee_login.username}"))
            raise AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND)
        
        # 验证密码是否正确
        if not PasswordUtil.matches(employee.password, employee_login.password):
            # 记录登录失败
            redis_util.incr(f"login_fail:{employee_login.username}")
            redis_util.setex(f"login_fail:{employee_login.username}", 900, redis_util.get(f"login_fail:{employee_login.username}"))
            raise PasswordErrorException(MessageConstant.PASSWORD_ERROR)
        
        # 验证员工状态
        if employee.status != 1:
            raise AccountLockedException(MessageConstant.ACCOUNT_LOCKED)
        
        # 生成 JWT token
        secret_key = "your-secret-key"
        ttl_millis = 86400000
        token = JwtUtil.create_jwt(secret_key, ttl_millis, {"sub": employee.username, "id": employee.id})
        
        # 存储会话到Redis
        redis_util.setex(f"session:{employee.id}", 86400, token)
        redis_util.setex(f"token:{token}", 86400, employee.id)
        BaseContext.set_current_id(int(employee.id))
        
        # 清除登录失败记录
        redis_util.delete(f"login_fail:{employee_login.username}")
        # 构建返回数据
        data = {
            "id": employee.id,
            "user_name": employee.username,
            "name": employee.name,
            "token": token
        }
        
        # 返回成功结果
        return Result.success(data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()





# 在创建员工的路由中添加拦截器
@router.post(
    "/employee/",
    response_model=dict,
    summary="创建员工",
    description="创建新员工账号",
    responses={
        200: {"description": "创建成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "username": "testuser", "name": "测试用户"}}}}},
        400: {"description": "用户名已存在"}
    }
)
def create_employee(
    employee: EmployeeDTO, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # 添加令牌验证
):
    """创建员工"""
    try:
        # 检查用户名是否已存在
        db_employee = get_employee_by_username(db, employee.username)
        if db_employee:
            raise Account_ALREADY_EXISTS(employee.username + MessageConstant.ALREADY_EXISTS.value)
        
        # 调用数据库创建员工
        new_employee = create_employee_db(db, employee)
        
        # 构建返回数据
        data = {
            "id": new_employee.id,
            "username": new_employee.username,
            "name": new_employee.name,
            "phone": new_employee.phone,
            "sex": new_employee.sex,
            "id_number": new_employee.id_number,
            "status": new_employee.status
        }
        
        # 返回成功结果
        return Result.success(data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
@router.get(
    "/employee/page",
    response_model=dict,
    summary="员工分页查询",
    description="根据条件分页查询员工信息",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "username": "testuser", "name": "测试用户", "phone": "13800138000", "sex": "男", "id_number": "110101199001011234", "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}]}}}}},
        401: {"description": "未授权"}
    }
)
def get_employee_page(
    name: str = None,
    page: int = 1,
    page_size: int = 2,
    db: Session = Depends(get_db),
    #current_user: str = Depends(get_current_user)
):
    """员工分页查询"""
    try:
        cache_key = f"emp_page:{page}:{page_size}:{name or ''}"
        cached_result = redis_util.get(cache_key)
        
        # 如果缓存存在，直接返回
        if cached_result:
            return Result.success(cached_result).to_dict()
        # 构建查询
        query = get_employee_page_query(db, name)
        
        # 使用 fastapi-pagination 分页
        params = Params(page=page, size=page_size)
        page_result = sqlalchemy_paginate(query, params)
        
        # 转换为字典格式
        employee_dicts = []
        for employee in page_result.items:
            employee_dict = {
                "id": employee.id,
                "username": employee.username,
                "name": employee.name,
                "phone": employee.phone,
                "sex": employee.sex,
                "id_number": employee.id_number,
                "status": employee.status,
                "create_time": employee.create_time.strftime("%Y-%m-%d %H:%M:%S") if employee.create_time else None,
                "update_time": employee.update_time.strftime("%Y-%m-%d %H:%M:%S") if employee.update_time else None,
                "create_user": employee.create_user,
                "update_user": employee.update_user
            }
            employee_dicts.append(employee_dict)
        
        # 使用 PageResult 结构体
        page_result = PageResult(total=page_result.total, records=employee_dicts)
        
        # 返回成功结果
        return Result.success(page_result.to_dict()).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.post(
    "/employee/status/{status}",
    response_model=dict,
    summary="员工启用禁用账号",
    description="根据员工ID和状态启用或禁用员工账号",
    responses={
        200: {"description": "操作成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "status": 1}}}}},
        404: {"description": "员工不存在"}
    }
)
def update_employee_status_route(
    status: int,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """员工启用禁用账号"""
    try:
        # 使用 crud 方法更新员工状态
        updated_employee = update_employee_status(db, employee_id, status)
        if not updated_employee:
            raise AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND.value)
        
        # 构建返回数据
        data = {
            "id": updated_employee.id,
            "status": updated_employee.status
        }
        
        # 返回成功结果
        return Result.success(data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()

@router.get(
    "/employee/{id}",
    response_model=dict,
    summary="获取员工详情",
    description="根据员工ID获取员工详细信息",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "username": "testuser", "name": "测试用户", "phone": "13800138000", "sex": "男", "id_number": "110101199001011234", "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}}}}},
        404: {"description": "员工不存在"}
    }
)
def get_employee_detail(
    id: int, 
    db: Session = Depends(get_db), 
    #current_user: str = Depends(get_current_user)
):
    """获取员工详情"""
    try:
        employee = get_employee(db, id)
        if not employee:
            raise AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND.value)
        
        # 构建返回数据
        data = {
            "id": employee.id,
            "username": employee.username,
            "name": employee.name,
            "phone": employee.phone,
            "sex": employee.sex,
            "id_number": employee.id_number,
            "status": employee.status,
            "create_time": employee.create_time.strftime("%Y-%m-%d %H:%M:%S") if employee.create_time else None,
            "update_time": employee.update_time.strftime("%Y-%m-%d %H:%M:%S") if employee.update_time else None,
            "create_user": employee.create_user,
            "update_user": employee.update_user
        }
        
        # 返回成功结果
        return Result.success(data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.put(
    "/employee/{id}",
    response_model=dict,
    summary="更新员工信息",
    description="根据员工ID更新员工信息",
    responses={
        200: {"description": "更新成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "username": "testuser", "name": "测试用户", "phone": "13800138000", "sex": "男", "id_number": "110101199001011234", "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}}}}},
        404: {"description": "员工不存在"}
    }
)
def update_employee_detail(
    id: int, 
    username: str, 
    name: str, 
    phone: str, 
    sex: str, 
    id_number: str, 
    db: Session = Depends(get_db), 
    #current_user: str = Depends(get_current_user)
):
    """更新员工信息"""
    try:
        # 创建 EmployeeUpdate 对象
        employee_update = EmployeeUpdate(
            username=username,
            name=name,
            phone=phone,
            sex=sex,
            id_number=id_number
        )
        
        # 使用 crud 方法更新员工信息
        updated_employee = update_employee(db, id, employee_update)
        if not updated_employee:
            raise AccountNotFoundException(MessageConstant.ACCOUNT_NOT_FOUND.value)
        
        # 构建返回数据
        data = {
            "id": updated_employee.id,
            "username": updated_employee.username,
            "name": updated_employee.name,
            "phone": updated_employee.phone,
            "sex": updated_employee.sex,
            "id_number": updated_employee.id_number,
            "status": updated_employee.status,
            "create_time": updated_employee.create_time.strftime("%Y-%m-%d %H:%M:%S") if updated_employee.create_time else None,
            "update_time": updated_employee.update_time.strftime("%Y-%m-%d %H:%M:%S") if updated_employee.update_time else None,
            "create_user": updated_employee.create_user,
            "update_user": updated_employee.update_user
        }
        
        # 返回成功结果
        return Result.success(data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()

@router.post("/employee/logout")
async def logout(
    token: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db)
):
    """员工登出"""
    try:
        # 从 Redis 中获取员工 ID
        employee_id = redis_util.get(f"token:{token}")
        if employee_id:
            # 删除会话数据
            redis_util.delete(f"token:{token}")
            redis_util.delete(f"session:{employee_id}")
        return Result.success(msg="登出成功").to_dict()
    except Exception as e:
        return Result.error(msg=f"登出失败: {str(e)}").to_dict()
