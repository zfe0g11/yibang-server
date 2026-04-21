import uuid
import requests
import os
import tempfile
from sqlalchemy.orm import Session
from config.ai_config import ai_config
from common.dto.chat_query_dto import ChatQueryDTO
import threading
from fastapi import UploadFile
import threading
from config.ai_config import ai_config
from common.utils.rag_chain import BasicRAGChain
from common.utils.redis_util import redis_util
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
# 导入必要的库
try:
    from common.utils.document_processor import UniversalDocumentProcessor
except ImportError:
    print("Warning: Document processor not found. Using fallback processing.")

def get_user_id_from_token(Authorization: str) -> str:
    """从token中获取用户ID"""
    if Authorization:
        token = Authorization.replace("Bearer ", "")
        user_id = redis_util.get(f"user_token:{token}")
        return user_id if user_id else "anonymous"
    return "anonymous"

global_ragchain = None
rag_chain_lock = threading.Lock()
def get_rag_chain():
    """获取全局RAG链，如果未初始化则初始化"""
    global global_rag_chain
    with rag_chain_lock:
        if global_rag_chain is None:
            global_rag_chain = BasicRAGChain(
                embedding_model=ai_config.EMBEDDING_LLM_MODEL,
                llm_model=ai_config.LLM_MODEL,
                api_key=ai_config.XUNFEI_API_KEY,
                api_base=ai_config.XUNFEI_API_BASE
            )
    return global_rag_chain

from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory
from datetime import datetime

def save_chat_history(db: Session, session_id: str, user_id: str, query: str, response: str) -> None:
    """保存聊天历史到数据库"""
    chat_history = ChatHistory(
        session_id=session_id,
        user_id=user_id,
        query=query,
        response=response,
        created_at=datetime.utcnow()
    )
    
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)
    
    print(f"聊天历史保存成功，ID: {chat_history.id}")

async def chat_query(db: Session, chat_query_dto: ChatQueryDTO, Authorization: str) -> dict:
    """
    处理AI聊天查询
    1. 根据query生成embedding
    2. 在QDRANT中检索相关文档
    3. 调用LLM生成回复
    """
    user_id = redis_util.get(f"user_token:{Authorization}")

    # 生成session_id
    session_id = Authorization

    # 生成embedding
    rag_chain = get_rag_chain()
    response = rag_chain.run(chat_query_dto.query)

    save_chat_history(db, user_id, session_id, chat_query_dto.query, response)

    return {
        "session_id": session_id,
        "response": response
    }


'''
def save_chat_history(db: Session, user_id: str, session_id: str, query: str, response: str):
    """保存聊天记录"""
    # 这里可以扩展为保存到数据库
    from app.sky_common.utils.redis_util import redis_util

    # 使用Redis缓存聊天记录
    chat_key = f"chat_history:{user_id}:{session_id}"
    chat_record = {
        "query": query,
        "response": response,
        "timestamp": str(uuid.uuid4())
    }

    # 获取现有历史
    history = redis_util.get(chat_key) or []
    history.append(chat_record)

    # 只保留最近20条记录
    if len(history) > 20:
        history = history[-20:]

    # 保存回Redis
    redis_util.setex(chat_key, 86400 * 7, history)  # 保留7天
'''
def get_chat_history(db: Session, Authorization: str, page: int = 1, page_size: int = 10, user_id: str = None) -> dict:
    """
    获取聊天历史，优先从Redis缓存中获取，缓存不存在则从数据库中查找
    管理员可以通过user_id参数指定要查找的用户
    """
    # 管理员可以通过user_id参数指定要查找的用户
    user_id = redis_util.get(f"user_token:{Authorization}")
        # 普通用户模式，查找当前用户的聊天历史
    # 尝试从Redis缓存中获取
    cache_key = f"chat_history:{user_id}:{page}:{page_size}:{user_id or ''}"
    if cache_key:
        cached_result = redis_util.get(cache_key)
    
    if cached_result:
        return cached_result
    
    # 从数据库中查找
    query = db.query(ChatHistory)\
        .filter(ChatHistory.user_id == user_id)\
        .order_by(ChatHistory.created_at.desc())
    
    # 使用 fastapi-pagination 分页
    params = Params(page=page, size=page_size)
    page_result = sqlalchemy_paginate(query, params)
    
    # 转换为字典格式
    chat_history_dicts = []
    for chat_history in page_result.items:
        chat_history_dict = {
            "id": chat_history.id,
            "session_id": chat_history.session_id,
            "user_id": chat_history.user_id,
            "query": chat_history.query,
            "response": chat_history.response,
            "created_at": chat_history.created_at.strftime("%Y-%m-%d %H:%M:%S") if chat_history.created_at else None
        }
        chat_history_dicts.append(chat_history_dict)
    
    # 构建分页结果
    page_result = {
        "total": page_result.total,
        "page": page_result.page,
        "page_size": page_result.size,
        "records": chat_history_dicts
    }
    
    # 缓存结果
    redis_util.setex(cache_key, 86400, page_result)
    
    return page_result
    
def delete_chat_session(db: Session, Authorization: str):
    """删除聊天会话，包括Redis缓存和数据库中的记录"""
    user_id = redis_util.get(f"user_token:{Authorization}")    
    # 删除数据库中的聊天记录
    db.query(ChatHistory)\
        .filter(ChatHistory.user_id == user_id)\
        .filter(ChatHistory.session_id == Authorization)\
        .delete()
    
    db.commit()
    
    return {"message": "聊天会话删除成功"}
    