from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from common.result.result import Result
from common.utils.ali_oss_util import ali_oss_util
import os
import uuid
from datetime import datetime

router = APIRouter()


@router.post(
    "/common/upload",
    response_model=dict,
    summary="文件上传",
    description="上传文件到阿里云 OSS",
    responses={
        200: {"description": "上传成功", "content": {"application/json": {"example": {"code": 1, "msg": "", "data": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg"}}}},
        400: {"description": "上传失败"}
    }
)
async def upload_file(
    file: UploadFile = File(..., description="要上传的文件"),
    db: Session = Depends(get_db)
):
    """文件上传"""
    try:
        # 读取文件内容
        contents = await file.read()
        
        # 生成唯一的文件名
        # 1. 提取文件后缀
        file_extension = os.path.splitext(file.filename)[1]
        # 2. 生成唯一的 UUID 并转换为字符串
        unique_id = str(uuid.uuid4())
        # 3. 拼接文件名和后缀
        unique_filename = f"{unique_id}{file_extension}"
        
        # 按日期组织文件路径
        date_path = datetime.now().strftime("%Y/%m/%d")
        object_name = f"{date_path}/{unique_filename}"
        
        # 上传文件到阿里云 OSS
        file_url = ali_oss_util.upload(contents, object_name)
        
        if file_url:
            return Result.success(data=file_url).to_dict()
        else:
            return Result.error(msg="上传失败").to_dict()
    except Exception as e:
        return Result.error(msg=f"上传失败: {str(e)}").to_dict()
