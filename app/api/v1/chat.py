from fastapi import APIRouter, Depends, Header, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.sky_common.result.result import Result
from app.crud import rag_crud
from app.sky_pojo.dto.chat_query_dto import ChatQueryDTO

router = APIRouter()


@router.post(
    "/chat/query",
    response_model=dict,
    summary="AI聊天查询",
    description="用户与AI聊天助手进行对话",
    responses={
        200: {"description": "查询成功"},
        401: {"description": "未授权"}
    }
)
async def chat_query(
    chat_query: ChatQueryDTO,
    Authorization: str = Header(None, description="JWT token"),
    db: Session = Depends(get_db)
):
    """AI聊天查询"""
    try:
        # 调用聊天服务进行处理
        response = await rag_crud.chat_query(db, chat_query, Authorization)
        return Result.success(data=response).to_dict()
    except Exception as e:
        return Result.error(msg=str(e)).to_dict()


@router.get(
    "/chat/history",
    response_model=dict,
    summary="获取聊天历史",
    description="获取用户的聊天历史记录",
    responses={
        200: {"description": "获取成功"},
        401: {"description": "未授权"}
    }
)
async def get_chat_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    Authorization: str = Header(None, description="JWT token"),
    db: Session = Depends(get_db)
):
    """获取聊天历史"""
    try:
        # 获取聊天历史
        history = rag_crud.get_chat_history(db, Authorization, page, page_size)
        return Result.success(data=history).to_dict()
    except Exception as e:
        return Result.error(msg=str(e)).to_dict()


@router.delete(
    "/chat/history/{session_id}",
    response_model=dict,
    summary="删除聊天会话",
    description="删除指定的聊天会话",
    responses={
        200: {"description": "删除成功"},
        401: {"description": "未授权"}
    }
)
async def delete_chat_session(
    session_id: str,
    Authorization: str = Header(None, description="JWT token"),
    db: Session = Depends(get_db)
):
    """删除聊天会话"""
    try:
        rag_crud.delete_chat_session(db, Authorization, session_id)
        return Result.success(msg="删除成功").to_dict()
    except Exception as e:
        return Result.error(msg=str(e)).to_dict()

