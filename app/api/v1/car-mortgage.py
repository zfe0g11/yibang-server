from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from common.result.result import Result
from common.result.page_result import PageResult
from app.crud.car_mortgage import get_car_mortgage_page_query, get_car_mortgage_by_id, update_car_mortgage_status
from app.crud.user import get_user_by_id
from common.dto.car_mortgage_page_query_dto import CarMortgagePageQueryDTO
from common.dto.car_mortgage_audit_dto import CarMortgageAuditDTO
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from datetime import datetime
from common.utils.redis_util import redis_util

router = APIRouter()


@router.get(
    "/car-mortgage/page",
    response_model=dict,
    summary="管理端车辆抵押申请分页查询",
    description="管理端车辆抵押申请分页查询，支持按车辆名称、品牌、型号、状态搜索",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "car_name": "特斯拉Model3", "brand": "特斯拉", "model": "Model3", "description": "我的爱车", "images": ["https://example.com/car1.jpg"], "status": 0, "create_time": "2023-01-01 12:00:00", "user_info": {"id": 1, "name": "张三", "phone": "13800138000"}}]}}}}}
    }
)
async def get_admin_car_mortgage_page(
    car_name: str = Query(None, description="车辆名称"),
    brand: str = Query(None, description="品牌"),
    model: str = Query(None, description="型号"),
    status: int = Query(None, description="状态：0-待审核，1-审核通过，2-审核拒绝"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页大小"),
    db: Session = Depends(get_db)
):
    """管理端车辆抵押申请分页查询"""
    try:
        # 构建查询
        cache_key = f"admin_car_mortgage_page:{page}:{page_size}:{car_name or ''}:{brand or ''}:{model or ''}:{status or ''}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        
        query = get_car_mortgage_page_query(db, car_name, brand, model, status)
        
        # 使用 fastapi-pagination 分页
        params = Params(page=page, size=page_size)
        page_result = sqlalchemy_paginate(query, params)
        
        # 转换为字典格式
        mortgage_dicts = []
        for mortgage in page_result.items:
            # 获取用户信息
            user = get_user_by_id(db, mortgage.user_id)
            user_info = {
                "id": user.id if user else None,
                "name": user.name if user else None,
                "phone": user.phone if user else None
            }
            
            mortgage_dict = {
                "id": mortgage.id,
                "car_name": mortgage.car_name,
                "brand": mortgage.brand,
                "model": mortgage.model,
                "description": mortgage.description,
                "images": mortgage.images.split(",") if mortgage.images else [],
                "status": mortgage.status,
                "create_time": mortgage.create_time.strftime("%Y-%m-%d %H:%M:%S") if mortgage.create_time else None,
                "user_info": user_info
            }
            mortgage_dicts.append(mortgage_dict)
        
        # 使用 PageResult 结构体
        page_result = PageResult(total=page_result.total, records=mortgage_dicts)
        result_data = page_result.to_dict()
        # 缓存结果，设置过期时间
        redis_util.setex(cache_key, 300, result_data)  # 缓存5分钟
        # 返回成功结果
        return Result.success(data=page_result.to_dict()).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/car-mortgage/{id}",
    response_model=dict,
    summary="管理端获取车辆抵押申请详情",
    description="管理端获取车辆抵押申请的详细信息",
    responses={
        200: {"description": "获取成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"id": 1, "car_name": "特斯拉Model3", "brand": "特斯拉", "model": "Model3", "description": "我的爱车", "images": ["https://example.com/car1.jpg"], "status": 0, "create_time": "2023-01-01 12:00:00", "user_info": {"id": 1, "name": "张三", "phone": "13800138000"}}}}},
        404: {"description": "申请不存在"}
    }
    }
)
async def get_admin_car_mortgage_detail(
    id: int = Path(..., description="申请ID"),
    db: Session = Depends(get_db)
):
    """管理端获取车辆抵押申请详情"""
    try:
        # 构建缓存键
        cache_key = f"admin_car_mortgage_detail:{id}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        
        # 获取车辆抵押申请详情
        mortgage = get_car_mortgage_by_id(db, id)
        if not mortgage:
            return Result.error(msg="申请不存在").to_dict()
        
        # 获取用户信息
        user = get_user_by_id(db, mortgage.user_id)
        user_info = {
            "id": user.id if user else None,
            "name": user.name if user else None,
            "phone": user.phone if user else None
        }
        
        # 构建返回数据
        data = {
            "id": mortgage.id,
            "car_name": mortgage.car_name,
            "brand": mortgage.brand,
            "model": mortgage.model,
            "description": mortgage.description,
            "images": mortgage.images.split(",") if mortgage.images else [],
            "status": mortgage.status,
            "create_time": mortgage.create_time.strftime("%Y-%m-%d %H:%M:%S") if mortgage.create_time else None,
            "user_info": user_info
        }
        
        # 缓存结果
        redis_util.setex(cache_key, 3600, data)  # 缓存1小时
        
        return Result.success(data=data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.put(
    "/car-mortgage/audit",
    response_model=dict,
    summary="管理端审核车辆抵押申请",
    description="管理端审核车辆抵押申请，设置审核状态",
    responses={
        200: {"description": "审核成功", "content": {"application/json": {"example": {"code": 1, "msg": "审核成功", "data": {"id": 1, "status": 1}}}}},
        404: {"description": "申请不存在"}
    }
)
async def audit_car_mortgage(
    audit_dto: CarMortgageAuditDTO,
    db: Session = Depends(get_db)
):
    """管理端审核车辆抵押申请"""
    try:
        # 更新车辆抵押申请状态
        updated_mortgage = update_car_mortgage_status(db, audit_dto)
        if not updated_mortgage:
            return Result.error(msg="申请不存在").to_dict()
        
        # 清除相关缓存
        redis_util.delete(f"admin_car_mortgage_detail:{audit_dto.id}")
        redis_util.delete("admin_car_mortgage_page:*")
        
        # 构建返回数据
        data = {
            "id": updated_mortgage.id,
            "status": updated_mortgage.status
        }
        
        return Result(1, msg="审核成功", data=data).to_dict()
    except Exception as e:
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
