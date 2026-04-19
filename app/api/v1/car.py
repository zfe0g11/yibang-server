from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from common.result.result import Result
from common.result.page_result import PageResult
from common.dto.car_dto import CarDTO
from app.crud.car import create_car, get_car_page_query, delete_car, update_car, get_car_by_id, get_car_by_name
from app.crud.category import get_category_by_name
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from datetime import datetime
from common.utils.redis_util import redis_util
router = APIRouter()


@router.post(
    "/car",
    response_model=dict,
    summary="新增车辆",
    description="新增车辆信息，图片需要先通过通用文件上传接口上传",
    responses={
        200: {"description": "新增成功", "content": {"application/json": {"example": {"code": 1, "msg": "新增成功", "data": {"id": 1, "name": "特斯拉 Model 3", "image": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg"}}}}},
        400: {"description": "新增失败"}
    }
)
async def create_car_route(
    name: str = Query(..., description="车辆名称"),
    brand_name: str = Query(..., description="品牌名称"),
    model_name: str = Query(..., description="型号名称"),
    price: float = Query(None, description="价格"),
    image: str = Query(None, description="图片URL"),
    description: str = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """新增车辆"""
    try:
        # 1. 根据品牌名称查询分类ID
        brand_category = get_category_by_name(db, brand_name)
        if not brand_category:
            return Result.error(msg=f"品牌「{brand_name}」不存在，请先添加品牌分类").to_dict()
        
        # 2. 根据型号名称查询分类ID
        model_category = get_category_by_name(db, model_name)
        if not model_category:
            return Result.error(msg=f"型号「{model_name}」不存在，请先添加型号分类").to_dict()
        
        # 3. 构建 CarDTO 对象
        car_dto = CarDTO(
            name=name,
            brand_id=brand_category.id,
            model_id=model_category.id,
            price=price,
            image=image,
            description=description
        )
        
        # 4. 执行数据库操作，插入车辆信息
        created_car = create_car(db, car_dto)
        
        # 5. 清除缓存
        redis_util.delete("car_page:*")
        redis_util.delete(f"category_name:brand:{brand_name}")
        redis_util.delete(f"category_name:model:{model_name}")
        # 6. 返回结果
        data = {
            "id": created_car.id,
            "name": created_car.name,
            "brand_name": brand_name,
            "model_name": model_name,
            "image": created_car.image
        }
        redis_util.delete(f"car_page:*")
        return Result(1, msg="新增成功", data=data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/car/page",
    response_model=dict,
    summary="车辆分页查询",
    description="根据条件分页查询车辆信息，支持按品牌名称或型号名称搜索",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "name": "特斯拉 Model 3", "brand_id": 1, "brand_name": "特斯拉", "model_id": 2, "model_name": "Model 3", "price": 250000.0, "image": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg", "description": "特斯拉 Model 3 是一款纯电动轿车", "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}]}}}}},
        401: {"description": "未授权"}
    }
)
async def get_car_page(
    name: str = Query(None, description="车辆名称"),
    brand_name: str = Query(None, description="品牌名称"),
    model_name: str = Query(None, description="型号名称"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(2, description="每页大小"),
    db: Session = Depends(get_db)
):
    """车辆分页查询"""
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
        cache_key = f"car_page:{page}:{page_size}:{name or ''}:{brand_name or ''}:{model_name or ''}"
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
                ##"model_id": car.model_id,
               # "brand_id": car.brand_id,
                "price": car.price,
                "image": car.image,
                "description": car.description,
                "create_time": car.create_time.strftime("%Y-%m-%d %H:%M:%S") if car.create_time else None,
                "update_time": car.update_time.strftime("%Y-%m-%d %H:%M:%S") if car.update_time else None,
                "create_user": car.create_user,
                "update_user": car.update_user
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


@router.delete(
    "/car/{car_name}",
    response_model=dict,
    summary="删除车辆",
    description="根据车辆名称删除车辆",
    responses={
        200: {"description": "删除成功", "content": {"application/json": {"example": {"code": 1, "msg": "删除成功", "data": {"id": 1}}}}},
        404: {"description": "车辆不存在"}
    }
)
async def delete_car_route(
    car_name: str = Path(..., description="车辆名称"),
    db: Session = Depends(get_db)
):
    """删除车辆"""
    try:
        # 从缓存获取车辆ID
        cache_key = f"car_name_to_id:{car_name}"
        car_id = redis_util.get(cache_key)
        
        if not car_id:
            # 从数据库查询车辆ID
            car = get_car_by_name(db, car_name)
            if not car:
                return Result.error(msg="车辆不存在").to_dict()
            car_id = car.id
            # 缓存结果
            redis_util.setex(cache_key, 86400, car_id)  # 缓存1天
        
        # 执行数据库操作，删除车辆
        deleted = delete_car(db, car_id)
        
        if deleted:
            # 返回成功结果
            data = {
                "id": car_id
            }
            # 清除缓存
            redis_util.delete_pattern(f"car_detail:{car_id}")
            redis_util.delete_pattern("car_page:*")
            redis_util.delete_pattern(f"user_car_page:*")
            redis_util.delete_pattern(f"car_name_to_id:{car_name}")
            return Result(1, msg="删除成功", data=data).to_dict()
        else:
            # 返回车辆不存在的错误
            return Result.error(msg="车辆不存在").to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.put(
    "/car/{car_name}",
    response_model=dict,
    summary="修改车辆",
    description="根据车辆名称修改车辆信息",
    responses={
        200: {"description": "修改成功", "content": {"application/json": {"example": {"code": 1, "msg": "修改成功", "data": {"id": 1, "name": "特斯拉 Model 3", "image": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg"}}}}},
        404: {"description": "车辆不存在"}
    }
)
async def update_car_route(
    car_name: str = Path(..., description="车辆名称"),
    name: str = Query(None, description="车辆名称"),
    brand_name: str = Query(None, description="品牌名称"),
    model_name: str = Query(None, description="型号名称"),
    price: float = Query(None, description="价格"),
    image: str = Query(None, description="图片URL"),
    description: str = Query(None, description="描述"),
    db: Session = Depends(get_db)
):
    """修改车辆"""
    try:
        # 从缓存获取车辆ID
        cache_key = f"car_name_to_id:{car_name}"
        car_id = redis_util.get(cache_key)
        
        if not car_id:
            # 从数据库查询车辆ID
            car = get_car_by_name(db, car_name)
            if not car:
                return Result.error(msg="车辆不存在").to_dict()
            car_id = car.id
            # 缓存结果
            redis_util.setex(cache_key, 86400, car_id)  # 缓存1天
        
        # 构建 CarDTO 对象
        car_dto = CarDTO()
        car_dto.name = name
        
        # 处理品牌和型号
        if brand_name:
            # 从缓存获取品牌ID
            brand_cache_key = f"category_name:brand:{brand_name}"
            brand_id = redis_util.get(brand_cache_key)
            if not brand_id:
                brand_category = get_category_by_name(db, brand_name)
                if brand_category:
                    brand_id = brand_category.id
                    redis_util.setex(brand_cache_key, 86400, brand_id)
            car_dto.brand_id = brand_id
        
        if model_name:
            # 从缓存获取型号ID
            model_cache_key = f"category_name:model:{model_name}"
            model_id = redis_util.get(model_cache_key)
            if not model_id:
                model_category = get_category_by_name(db, model_name)
                if model_category:
                    model_id = model_category.id
                    redis_util.setex(model_cache_key, 86400, model_id)
            car_dto.model_id = model_id
        
        car_dto.price = price
        car_dto.image = image
        car_dto.description = description
        
        # 执行数据库操作，更新车辆
        updated_car = update_car(db, car_id, car_dto)
        if updated_car:
            # 构建返回数据
            data = {
                "id": updated_car.id,
                "name": updated_car.name,
                "image": updated_car.image,
                "description": updated_car.description
            }
            # 清除缓存
            redis_util.delete_pattern(f"car_detail:{car_id}")
            redis_util.delete_pattern("car_page:*")
            redis_util.delete_pattern(f"user_car_page:*")
            redis_util.delete_pattern(f"car_name_to_id:{car_name}")
            if name:
                redis_util.delete_pattern(f"car_name_to_id:{name}")
            return Result(1, msg="修改成功", data=data).to_dict()
        else:
            # 返回车辆不存在的错误
            return Result.error(msg="车辆不存在").to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
    
@router.get("/car/{car_name}")
async def get_car_detail(
    car_name: str = Path(..., description="车辆名称"),
    db: Session = Depends(get_db)
):
    """获取车辆详情"""
    try:
        # 从缓存获取车辆ID
        cache_key = f"car_name_to_id:{car_name}"
        car_id = redis_util.get(cache_key)
        
        if not car_id:
            # 从数据库查询车辆ID
            car = get_car_by_name(db, car_name)
            if not car:
                return Result.error(msg="车辆不存在").to_dict()
            car_id = car.id
            # 缓存结果
            redis_util.setex(cache_key, 86400, car_id)  # 缓存1天
        
        # 构建缓存键
        detail_cache_key = f"car_detail:{car_id}"
        # 尝试从缓存获取
        cached_result = redis_util.get(detail_cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        
        # 查询数据库
        car = get_car_by_id(db, car_id)
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
            "update_time": car.update_time.strftime("%Y-%m-%d %H:%M:%S") if car.update_time else None,
            "create_user": car.create_user,
            "update_user": car.update_user
        }
        
        # 缓存结果
        redis_util.setex(detail_cache_key, 3600, data)  # 缓存1小时
        
        # 返回成功结果
        return Result.success(data=data).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
