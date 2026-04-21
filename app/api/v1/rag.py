from fastapi import APIRouter, Depends, Header, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from common.result.result import Result
from app.crud import rag_crud

router = APIRouter()

@router.post(
    "/vector/add/single",
    response_model=dict,
    summary="上传文件到RAG向量库",
    description="上传单个文件到RAG向量库进行处理和索引",
    responses={
        200: {"description": "上传成功"},
        401: {"description": "未授权"}
    }
)
async def add_file_to_vector_db(
    file: UploadFile = File(..., description="要上传的文件"),
    Authorization: str = Header(None, description="JWT token"),
    db: Session = Depends(get_db)
):
    """上传文件到RAG向量库"""
    try:
        result = await rag_crud.add_file_to_vector_db(db, file, Authorization)
        return Result.success(data=result).to_dict()
    except Exception as e:
        return Result.error(msg=str(e)).to_dict()