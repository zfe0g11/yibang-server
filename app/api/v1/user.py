from fastapi import APIRouter, Depends, Query, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from common.result.result import Result
from common.result.page_result import PageResult
from app.crud.car import get_car_page_query, get_car_by_id
from app.crud.category import get_category_by_name
from app.crud.user import create_user, get_user_by_phone, get_user_by_id
from app.crud.car_mortgage import create_car_mortgage, get_car_mortgage_list, get_car_mortgage_by_openid, get_car_mortgage_page_query, get_car_mortgage_by_id
from app.models.car_mortgage import CarMortgage
from common.dto.user_login_dto import UserLoginDTO
from common.dto.user_register_dto import UserRegisterDTO
from common.dto.car_mortgage_dto import CarMortgageDTO
from common.utils.jwt_util import JwtUtil
from common.utils.password_util import PasswordUtil
from common.constant.message_constant import MessageConstant
from common.exception.base_exception import (
    AccountNotFoundException,
    AccountLockedException,
    PasswordErrorException,
    Account_ALREADY_EXISTS
)
from common.utils.auth_util import get_current_user
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from datetime import datetime
from common.utils.redis_util import redis_util

router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register",
    response_model=dict,
    summary="用户注册",
    description="用户注册接口，创建新用户",
    responses={
        200: {"description": "注册成功", "content": {"application/json": {"example": {"code": 1, "msg": "注册成功", "data": {"id": 1, "name": "张三", "phone": "13800138000"}}}}},
        400: {"description": "注册失败"}
    }
)
async def user_register(
    user_register: UserRegisterDTO,
    db: Session = Depends(get_db)
):
    """用户注册"""
    try:
        # 检查手机号是否已存在
        existing_user = get_user_by_phone(db, user_register.phone)
        if existing_user:
            return Result.error(msg="手机号已被注册").to_dict()
        
        # 创建用户
        new_user = create_user(db, user_register)
        
        # 构建返回数据
        data = {
            "id": new_user.id,
            "name": new_user.name,
            "phone": new_user.phone
        }
        
        return Result(1, msg="注册成功", data=data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.post(
    "/login",
    response_model=dict,
    summary="用户登录",
    description="用户登录接口，验证手机号和密码，返回JWT token",
    responses={
        200: {"description": "登录成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "name": "张三", "phone": "13800138000", "token": "JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}}}}},
        401: {"description": "手机号或密码错误"}
    }
)
async def user_login(
    user_login: UserLoginDTO,
    db: Session = Depends(get_db)
):
    """用户登录"""
    try:
        # 检查登录失败次数
        fail_count = redis_util.get(f"user_login_fail:{user_login.phone}")
        if fail_count and int(fail_count) >= 5:
            return Result.error(msg="登录失败次数过多，账号已锁定").to_dict()
        
        # 查找用户
        user = get_user_by_phone(db, user_login.phone)
        if not user:
            # 记录登录失败
            redis_util.incr(f"user_login_fail:{user_login.phone}")
            redis_util.setex(f"user_login_fail:{user_login.phone}", 900, redis_util.get(f"user_login_fail:{user_login.phone}"))
            return Result.error(msg="手机号或密码错误").to_dict()
        
        # 验证密码
        if not PasswordUtil.matches(user.password, user_login.password):
            # 记录登录失败
            redis_util.incr(f"user_login_fail:{user_login.phone}")
            redis_util.setex(f"user_login_fail:{user_login.phone}", 900, redis_util.get(f"user_login_fail:{user_login.phone}"))
            return Result.error(msg="手机号或密码错误").to_dict()
        
        # 生成 JWT token
        secret_key = "your-secret-key"
        ttl_millis = 86400000
        token = JwtUtil.create_jwt(secret_key, ttl_millis, {"sub": user.phone, "id": user.id})
        
        # 存储会话到Redis
        redis_util.setex(f"user_session:{user.id}", 86400, token)
        redis_util.setex(f"user_token:{token}", 86400, user.id)
        
        # 清除登录失败记录
        redis_util.delete(f"user_login_fail:{user_login.phone}")
        
        # 构建返回数据
        data = {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "token": token
        }
        
        return Result.success(data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/info",
    response_model=dict,
    summary="获取用户信息",
    description="获取当前登录用户的信息",
    responses={
        200: {"description": "获取成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "name": "张三", "phone": "13800138000", "sex": "男", "id_number": "110101199001011234", "avatar": "https://example.com/avatar.jpg"}}}}},
        401: {"description": "未授权"}
    }
)
async def get_user_info(
    Authorization: str = Header(..., description="JWT token"),
    db: Session = Depends(get_db)
):
    """获取用户信息"""
    try:
        # 从token中获取用户ID
        token = Authorization.replace("Bearer ", "")
        user_id = redis_util.get(f"user_token:{token}")
        if not user_id:
            return Result.error(msg="未授权").to_dict()
        
        # 查询用户信息
        user = get_user_by_id(db, int(user_id))
        if not user:
            return Result.error(msg="用户不存在").to_dict()
        
        # 构建返回数据
        data = {
            "id": user.id,
            "name": user.name,
            "phone": user.phone,
            "sex": user.sex,
            "id_number": user.id_number,
            "avatar": user.avatar
        }
        
        return Result.success(data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/car/page",
    response_model=dict,
    summary="用户端车辆分页查询",
    description="用户端车辆分页查询，支持按品牌名称、型号名称、车辆名称搜索",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "name": "特斯拉 Model 3", "brand_id": 1, "brand_name": "特斯拉", "model_id": 2, "model_name": "Model 3", "price": 250000.0, "image": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg", "description": "特斯拉 Model 3 是一款纯电动轿车", "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00"}]}}}}},
        401: {"description": "未授权"}
    }
)
async def get_user_car_page(
    name: str = Query(None, description="车辆名称"),
    brand_name: str = Query(None, description="品牌名称"),
    model_name: str = Query(None, description="型号名称"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页大小"),
    db: Session = Depends(get_db)
):
    """用户端车辆分页查询"""
    try:
        # 将品牌名称转换为ID（使用缓存）
        brand_id = None
        if brand_name:
            # 先从缓存获取
            cache_key = f"category_name:brand:{brand_name}"
            cached_brand_id = redis_util.get(cache_key)
            if cached_brand_id:
                brand_id = cached_brand_id
            else:
                # 从数据库查询
                brand_category = get_category_by_name(db, brand_name)
                if brand_category:
                    brand_id = brand_category.id
                    # 缓存结果
                    redis_util.setex(cache_key, 86400, brand_id)  # 缓存1天
        
        # 将型号名称转换为ID（使用缓存）
        model_id = None
        if model_name:
            # 先从缓存获取
            cache_key = f"category_name:model:{model_name}"
            cached_model_id = redis_util.get(cache_key)
            if cached_model_id:
                model_id = cached_model_id
            else:
                # 从数据库查询
                model_category = get_category_by_name(db, model_name)
                if model_category:
                    model_id = model_category.id
                    # 缓存结果
                    redis_util.setex(cache_key, 86400, model_id)  # 缓存1天
        
        # 构建查询
        cache_key = f"user_car_page:{page}:{page_size}:{name or ''}:{brand_name or ''}:{model_name or ''}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        
        query = get_car_page_query(db, name, model_id, brand_id)
        
        # 使用 fastapi-pagination 分页
        params = Params(page=page, size=page_size)
        page_result = sqlalchemy_paginate(query, params)
        
        # 转换为字典格式
        car_dicts = []
        for car in page_result.items:
            car_dict = {
                "id": car.id,
                "name": car.name,
                #"model_id": car.model_id,
                #"brand_id": car.brand_id,
                "price": car.price,
                "image": car.image,
                "description": car.description,
                "create_time": car.create_time.strftime("%Y-%m-%d %H:%M:%S") if car.create_time else None,
                "update_time": car.update_time.strftime("%Y-%m-%d %H:%M:%S") if car.update_time else None
            }
            car_dicts.append(car_dict)
        
        # 使用 PageResult 结构体
        page_result = PageResult(total=page_result.total, records=car_dicts)
        result_data = page_result.to_dict()
        # 缓存结果，设置过期时间
        redis_util.setex(cache_key, 300, result_data)  # 缓存5分钟
        # 返回成功结果
        return Result.success(data=page_result.to_dict()).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get("/car/{id}")
async def get_user_car_detail(
    id: int, 
    db: Session = Depends(get_db)
):
    """用户端获取车辆详情"""
    try:
        # 构建缓存键
        cache_key = f"user_car_detail:{id}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        
        # 查询数据库
        car = get_car_by_id(db, id)
        if not car:
            return Result.error(msg="车辆不存在").to_dict()
        
        # 构建返回数据
        data = {
            "id": car.id,
            "name": car.name,
            "model_id": car.model_id,
            "brand_id": car.brand_id,
            "price": car.price,
            "image": car.image,
            "description": car.description,
            "create_time": car.create_time.strftime("%Y-%m-%d %H:%M:%S") if car.create_time else None,
            "update_time": car.update_time.strftime("%Y-%m-%d %H:%M:%S") if car.update_time else None
        }
        
        # 缓存结果
        redis_util.setex(cache_key, 3600, data)  # 缓存1小时
        
        # 返回成功结果
        return Result.success(data=data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.post(
    "/car-mortgage",
    response_model=dict,
    summary="上传车辆抵押申请",
    description="用户上传车辆信息进行抵押申请",
    responses={
        200: {"description": "上传成功", "content": {"application/json": {"example": {"code": 1, "msg": "上传成功", "data": {"id": 1, "car_name": "特斯拉Model3", "brand": "特斯拉", "model": "Model3", "description": "我的爱车", "images": ["https://example.com/car1.jpg", "https://example.com/car2.jpg"], "status": 0}}}}},
        401: {"description": "未授权"}
    }
)
async def upload_car_mortgage(
    car_mortgage: CarMortgageDTO,
    Authorization: str = Header(..., description="JWT token"),
    db: Session = Depends(get_db)
):
    """上传车辆抵押申请"""
    try:
        
        # 创建车辆抵押申请
        new_mortgage = create_car_mortgage(db, car_mortgage)
        
        # 构建返回数据
        data = {
            "id": new_mortgage.id,
            "car_name": new_mortgage.car_name,
            "brand": new_mortgage.brand,
            "model": new_mortgage.model,
            "description": new_mortgage.description,
            "images": new_mortgage.images.split(",") if new_mortgage.images else [],
            "status": new_mortgage.status
        }
        
        return Result(1, msg="上传成功", data=data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/car-mortgage/list",
    response_model=dict,
    summary="获取车辆抵押申请列表",
    description="获取用户的车辆抵押申请列表",
    responses={
        200: {"description": "获取成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "car_name": "特斯拉Model3", "brand": "特斯拉", "model": "Model3", "description": "我的爱车", "images": ["https://example.com/car1.jpg"], "status": 0, "create_time": "2023-01-01 12:00:00"}]}}}}},
        401: {"description": "未授权"}
    }
)
async def get_car_mortgage_list_route(
    openid: str = Query(..., description="用户openid"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    db: Session = Depends(get_db)
):
    """获取车辆抵押申请列表"""
    try:

        # 获取用户信息，获取openid
        query = get_car_mortgage_by_openid(db, openid)
        if not query:
            return Result.error(msg="没有车辆抵押信息").to_dict()
        
        # 使用 fastapi-pagination 分页
        params = Params(page=page, size=page_size)
        page_result = sqlalchemy_paginate(query, params)
        
        # 转换为字典格式
        mortgage_dicts = []
        for mortgage in page_result.items:
            mortgage_dict = {
                "id": mortgage.id,
                "car_name": mortgage.car_name,
                "brand": mortgage.brand,
                "model": mortgage.model,
                "description": mortgage.description,
                "images": mortgage.images.split(",") if mortgage.images else [],
                "status": mortgage.status,
                "create_time": mortgage.create_time.strftime("%Y-%m-%d %H:%M:%S") if mortgage.create_time else None
            }
            mortgage_dicts.append(mortgage_dict)
        
        # 使用 PageResult 结构体
        page_result = PageResult(total=page_result.total, records=mortgage_dicts)
        
        # 缓存结果，设置过期时间
       
        # 返回成功结果
        return Result.success(page_result.to_dict()).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/car-mortgage/{id}",
    response_model=dict,
    summary="获取车辆抵押申请详情",
    description="获取车辆抵押申请的详细信息",
    responses={
        200: {"description": "获取成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "car_name": "特斯拉Model3", "brand": "特斯拉", "model": "Model3", "description": "我的爱车", "images": ["https://example.com/car1.jpg"], "status": 0, "create_time": "2023-01-01 12:00:00"}}}}},
        401: {"description": "未授权"},
        404: {"description": "申请不存在"}
    }
)
async def get_car_mortgage_detail_route(
    id: int,
    Authorization: str = Header(..., description="JWT token"),
    db: Session = Depends(get_db)
):
    """获取车辆抵押申请详情"""
    try:
        # 从token中获取用户ID
        token = Authorization.replace("Bearer ", "")
        user_id = redis_util.get(f"user_token:{token}")
        if not user_id:
            return Result.error(msg="未授权").to_dict()
        
        # 获取用户信息，获取openid
        user = get_user_by_id(db, int(user_id))
        if not user:
            return Result.error(msg="用户不存在").to_dict()
        
        # 获取车辆抵押申请详情
        mortgage = get_car_mortgage_by_id(db, id)
        if not mortgage:
            return Result.error(msg="申请不存在").to_dict()
        
        # 验证申请是否属于当前用户
        if mortgage.openid != user.openid:
            return Result.error(msg="无权访问此申请").to_dict()
        
        # 构建返回数据
        data = {
            "id": mortgage.id,
            "car_name": mortgage.car_name,
            "brand": mortgage.brand,
            "model": mortgage.model,
            "description": mortgage.description,
            "images": mortgage.images.split(",") if mortgage.images else [],
            "status": mortgage.status,
            "create_time": mortgage.create_time.strftime("%Y-%m-%d %H:%M:%S") if mortgage.create_time else None
        }
        
        return Result.success(data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
