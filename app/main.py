import sys
import os
from fastapi import FastAPI, Request
from app.api.v1 import employee, category, common, car, user, chat, rag
from common.utils.redis_util import redis_util


from fastapi.middleware.cors import CORSMiddleware
from app.crud.chat import get_rag_chain
from app.crud.rag_crud import get_embeddings,get_doc_processor,get_vector_store
get_doc_processor()  # 预加载文档处理器
get_embeddings()  # 预加载embedding模型
get_vector_store()  # 预加载向量存储
get_rag_chain()  # 预加载RAG链


app = FastAPI(
    title="Sky Take Out",
    description="益邦 - 二手车抵押",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "技术支持",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/doc",  # Swagger UI 路径
    redoc_url="/redoc",  # ReDoc 路径
    openapi_url="/openapi.json"  # OpenAPI JSON 路径
)
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    """会话验证中间件"""
    # 获取 token
    token = request.headers.get("Authorization")
    if token:
        # 验证 token
        employee_id = redis_util.get(f"token:{token}")
        if employee_id:
            # 延长会话过期时间
            redis_util.setex(f"token:{token}", 86400, employee_id)
            redis_util.setex(f"session:{employee_id}", 86400, token)
    # 继续处理请求
    response = await call_next(request)
    return response
# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(employee.router, prefix="/admin", tags=["员工管理"])
app.include_router(category.router, prefix="/admin", tags=["分类管理"])
app.include_router(common.router, prefix="/admin", tags=["通用管理"])
app.include_router(car.router, prefix="/admin", tags=["车辆管理"])
app.include_router(category.router, prefix="/admin",tags=["抵押审核"])
app.include_router(user.router,prefix="/user", tags=["用户端"])
app.include_router(chat.router, prefix="/user", tags=["AI聊天"])
app.include_router(rag.router, prefix="/admin", tags=["知识库构建"])

@app.get("/health", tags=["健康检查"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)