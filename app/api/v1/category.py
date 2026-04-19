from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.category import create_category, get_category_page_query, delete_category, update_category, update_category_status, get_category_list, get_category_by_id
from app.models.category import Category
from common.dto.category_dto import CategoryDTO
from common.dto.category_page_query_dto import CategoryPageQueryDTO
from common.result.result import Result
from common.result.page_result import PageResult
# 导入 fastapi-pagination
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from datetime import datetime
from common.utils.redis_util import redis_util

router = APIRouter()

TYPE_NAME_TO_VALUE = {
    "品牌": 1,
    "车型": 2,
}

TYPE_VALUE_TO_NAME = {
    1: "品牌",
    2: "车型",
}


@router.post("/category/")
async def add_category(
    name: str = Query(..., description="分类名称"),
    type_name: str = Query(..., description="分类类型名称，如：品牌、车型"),
    sort: int = Query(None, description="排序号"),
    db: Session = Depends(get_db)
):
    """新增分类"""
    try:
        # 将类型名称转换为数字值
        type_value = TYPE_NAME_TO_VALUE.get(type_name)
        if type_value is None:
            return Result.error(msg=f"不支持的类型名称：{type_name}，支持的类型有：品牌、车型").to_dict()
        
        # 构建 CategoryDTO 对象
        category_dto = CategoryDTO(
            name=name,
            type=type_value,
            sort=sort
        )
        
        # 调用数据库操作创建分类
        new_category = create_category(db, category_dto)
        
        # 清除相关缓存
        # 清除分页缓存
        redis_util.delete("category_page:*")
        # 清除列表缓存
        redis_util.delete(f"category_list:{type_value}")
        
        return Result.success(data=new_category).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/category/page",
    response_model=dict,
    summary="分类分页查询",
    description="根据条件分页查询分类信息，支持按类型名称筛选",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": {"total": 10, "records": [{"id": 1, "type": 1, "typeName": "品牌", "name": "宝马", "sort": 1, "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}]}}}}},
        401: {"description": "未授权"}
    }
)
async def get_category_page(
    name: str = None,
    page: int = 1,
    page_size: int = 10,
    type_name: str = Query(None, description="分类类型名称，如：品牌、车型"),
    db: Session = Depends(get_db)
):
    """分类分页查询"""
    try:
        # 将类型名称转换为数字值
        type_value = TYPE_NAME_TO_VALUE.get(type_name) if type_name else None
        
        # 构建缓存键
        cache_key = f"category_page:{page}:{page_size}:{name or ''}:{type_name or ''}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(data=cached_result).to_dict()
        # 构建查询
        query = get_category_page_query(db, name=name, category_type=type_value)
        
        # 使用 fastapi-pagination 分页
        params = Params(page=page, size=page_size)
        page_result = sqlalchemy_paginate(query, params)
        
        # 转换为字典格式
        category_dicts = []
        for category in page_result.items:
            category_dict = {
                "id": category.id,
                #"type": category.type,
                "typeName": TYPE_VALUE_TO_NAME.get(category.type, "未知"),
                "name": category.name,
                "sort": category.sort,
                "status": category.status,
                "create_time": category.create_time.strftime("%Y-%m-%d %H:%M:%S") if category.create_time else None,
                "update_time": category.update_time.strftime("%Y-%m-%d %H:%M:%S") if category.update_time else None,
                "create_user": category.create_user,
                "update_user": category.update_user
            }
            category_dicts.append(category_dict)
        
        # 构建分页结果
        page_result = PageResult(total=page_result.total, records=category_dicts)
        # 缓存结果
        redis_util.setex(cache_key, 86400, page_result.to_dict())
        
        # 返回成功结果
        return Result.success(page_result.to_dict()).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.delete(
    "/category/{id}",
    response_model=dict,
    summary="删除分类",
    description="根据ID删除分类",
    responses={
        200: {"description": "删除成功", "content": {"application/json": {"example": {"code": 1, "msg": "删除成功", "data": None}}}},
        404: {"description": "分类不存在"}
    }
)
async def delete_category_by_id(
    id: int = Path(..., description="分类ID", ge=1),
    db: Session = Depends(get_db)
):
    """删除分类"""
    try:
        # 先获取分类信息，用于后续清除缓存
        category = get_category_by_id(db, id)
        # 调用数据库操作删除分类
        success = delete_category(db, id)
        if success:
            # 清除相关缓存
            # 清除分页缓存
            redis_util.delete("category_page:*")
            # 清除列表缓存
            if category:
                redis_util.delete(f"category_list:{category.type}")
                # 清除分类名称到ID的缓存
                redis_util.delete(f"category_name:*:{category.name}")
            return Result(1, msg="删除成功", data=id).to_dict()
        else:
            # 检查分类是否存在
            if category:
                # 分类存在但有车辆属于该分类
                return Result.error(msg="该分类下存在车辆，不能删除").to_dict()
            else:
                # 分类不存在
                return Result.error(msg="分类不存在").to_dict()
        
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.put(
    "/category/{id}",
    response_model=dict,
    summary="修改分类",
    description="根据ID修改分类信息",
    responses={
        200: {"description": "修改成功", "content": {"application/json": {"example": {"code": 1, "msg": "修改成功", "data": {"id": 1, "type": 1, "typeName": "品牌", "name": "宝马", "sort": 1, "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}}}}},
        404: {"description": "分类不存在"}
    }
)
async def update_category_by_id(
    id: int = Path(..., description="分类ID", ge=1),
    name: str = Query(None, description="分类名称"),
    type_name: str = Query(None, description="分类类型名称，如：品牌、车型"),
    sort: int = Query(None, description="排序号"),
    db: Session = Depends(get_db)
):
    """修改分类"""
    try:
        # 将类型名称转换为数字值（如果提供了 type_name）
        type_value = None
        if type_name:
            type_value = TYPE_NAME_TO_VALUE.get(type_name)
            if type_value is None:
                return Result.error(msg=f"不支持的类型名称：{type_name}，支持的类型有：品牌、车型").to_dict()
        
        # 构建 CategoryDTO 对象
        category_dto = CategoryDTO(
            name=name,
            type=type_value,
            sort=sort
        )
        
        # 调用数据库操作更新分类
        updated_category = update_category(db, id, category_dto)
        if updated_category:
            # 清除相关缓存
            # 清除分页缓存
            redis_util.delete("category_page:*")
            # 清除列表缓存
            redis_util.delete(f"category_list:{updated_category.type}")
            # 清除分类名称到ID的缓存
            redis_util.delete(f"category_name:*:{updated_category.name}")
            
            # 转换为字典格式
            category_dict = {
                "id": updated_category.id,
                #"type": updated_category.type,
                "typeName": TYPE_VALUE_TO_NAME.get(updated_category.type, "未知"),
                "name": updated_category.name,
                "sort": updated_category.sort,
                "status": updated_category.status,
                "create_time": updated_category.create_time.strftime("%Y-%m-%d %H:%M:%S") if updated_category.create_time else None,
                "update_time": updated_category.update_time.strftime("%Y-%m-%d %H:%M:%S") if updated_category.update_time else None,
                "create_user": updated_category.create_user,
                "update_user": updated_category.update_user
            }
            return Result(1, msg="修改成功", data=category_dict).to_dict()
        else:
            return Result.error(msg="分类不存在").to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.post(
    "/category/status/{status}",
    response_model=dict,
    summary="启用禁用分类",
    description="根据ID启用或禁用分类",
    responses={
        200: {"description": "操作成功", "content": {"application/json": {"example": {"code": 1, "msg": "操作成功", "data": {"id": 1, "status": 1}}}}},
        404: {"description": "分类不存在"}
    }
)
async def update_category_status_route(
    status: int = Path(..., description="状态", ge=0, le=1),
    id: int = Query(..., description="分类ID", ge=1),
    db: Session = Depends(get_db)
):
    """启用禁用分类"""
    try:
        # 调用数据库操作更新分类状态
        updated_category = update_category_status(db, id, status)
        if updated_category:
            # 清除相关缓存
            # 清除分页缓存
            redis_util.delete("category_page:*")
            # 清除列表缓存
            redis_util.delete(f"category_list:{updated_category.type}")
            
            # 构建返回数据
            data = {
                "id": updated_category.id,
                "status": updated_category.status
            }
            return Result(1, msg="操作成功", data=data).to_dict()
        else:
            return Result.error(msg="分类不存在").to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()


@router.get(
    "/category/list",
    response_model=dict,
    summary="根据类型查询分类",
    description="根据类型名称查询分类列表，支持的品牌类型有：品牌、车型",
    responses={
        200: {"description": "查询成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": [{"id": 1, "type": 1, "typeName": "品牌", "name": "宝马", "sort": 1, "status": 1, "create_time": "2023-01-01 00:00:00", "update_time": "2023-01-01 00:00:00", "create_user": 1, "update_user": 1}]}}}}
    }
)
async def get_category_list_route(
    type_name: str = Query(..., description="分类类型名称，如：品牌、车型"),
    db: Session = Depends(get_db)
):
    """根据类型名称查询分类"""
    try:
        # 将类型名称转换为数字值
        type_value = TYPE_NAME_TO_VALUE.get(type_name)
        if type_value is None:
            return Result.error(msg=f"不支持的类型名称：{type_name}，支持的类型有：品牌、车型").to_dict()
        
        # 构建缓存键
        cache_key = f"category_list:{type_value}"
        # 尝试从缓存获取
        cached_result = redis_util.get(cache_key)
        if cached_result:
            return Result.success(cached_result).to_dict()
        
        # 调用数据库操作获取分类列表
        categories = get_category_list(db, type_value)
        
        # 转换为字典格式
        category_dicts = []
        for category in categories:
            category_dict = {
                "id": category.id,
                #"type": category.type,
                "typeName": TYPE_VALUE_TO_NAME.get(category.type, "未知"),
                "name": category.name,
                "sort": category.sort,
                "status": category.status,
                "create_time": category.create_time.strftime("%Y-%m-%d %H:%M:%S") if category.create_time else None,
                "update_time": category.update_time.strftime("%Y-%m-%d %H:%M:%S") if category.update_time else None,
                "create_user": category.create_user,
                "update_user": category.update_user
            }
            category_dicts.append(category_dict)
        
        # 缓存结果
        redis_util.setex(cache_key, 86400, category_dicts)
        
        return Result.success(data=category_dicts).to_dict()
    except Exception as e:
        # 返回错误结果
        return Result.error(str(e.message) if hasattr(e, 'message') else str(e.value) if hasattr(e, 'value') else str(e)).to_dict()
