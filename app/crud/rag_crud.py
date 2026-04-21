import os
import tempfile
from sqlalchemy.orm import Session
from config.ai_config import ai_config
import threading
from fastapi import UploadFile
# 导入必要的库
try:
    from common.utils.document_processor import UniversalDocumentProcessor
except ImportError:
    print("Warning: Document processor not found. Using fallback processing.")

def get_user_id_from_token(Authorization: str) -> str:
    """从token中获取用户ID"""
    from common.utils import redis_util
    if Authorization:
        token = Authorization.replace("Bearer ", "")
        user_id = redis_util.get(f"user_token:{token}")
        return user_id if user_id else "anonymous"
    return "anonymous"

global_embeddings = None

def get_embeddings():
    """获取全局embedding模型，如果未初始化则初始化"""
    global global_embeddings
    if global_embeddings is None:
        from langchain_openai import OpenAIEmbeddings
        global_embeddings = OpenAIEmbeddings(
            model=ai_config.EMBEDDING_LLM_MODEL,
            api_key=ai_config.EMBEDDING_XUNFEI_API_KEY,
            base_url=ai_config.EMBEDDING_XUNFEI_API_BASE
        )
    return global_embeddings

global_doc_processor = None

def get_doc_processor():
    """获取全局文档处理器，如果未初始化则初始化"""
    global global_doc_processor
    if global_doc_processor is None:
        from common.utils.document_processor import UniversalDocumentProcessor
        global_doc_processor = UniversalDocumentProcessor()
    return global_doc_processor



# 全局向量存储
global_vector_store = None
vector_store_lock = threading.Lock()

def get_vector_store():
    """获取全局向量存储，如果未初始化则初始化"""
    global global_vector_store
    with vector_store_lock:
        if global_vector_store is None:
            from app.sky_common.utils.vector_store import QdrantVectorStore
            global_vector_store = QdrantVectorStore()
            global_vector_store.connect(ai_config.QDRANT_URL)
        else:
            # 检查连接是否有效
            try:
                # 执行一个简单的查询来检查连接
                global_vector_store.client.get_collections()
            except Exception as e:
                # 连接无效，重新连接
                print(f"数据库连接失效，重新连接: {e}")
                global_vector_store.connect(ai_config.QDRANT_URL)
    return global_vector_store

get_vector_store()  # 预加载向量存储



async def add_file_to_vector_db(db: Session, file: UploadFile, Authorization: str) -> dict:
    """
    上传文件到RAG向量库
    1. 保存临时文件
    2. 使用文档处理器处理文件
    3. 生成embedding
    4. 存储到QDRANT
    5. 清理临时文件
    """
    user_id = get_user_id_from_token(Authorization)
    total_chunks = 0
    stored_chunks = 0

    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # 初始化文档处理器
        try:
            doc_processor = get_doc_processor()
            # 重置文件指针到开头
            if hasattr(file, 'seek'):
                file.seek(0)
            # 使用文档处理器处理文件
            split_docs = doc_processor.process_document(
                file=file,
                filename=file.filename,
                chunk_size=ai_config.CHUNK_SIZE,
                chunk_overlap=ai_config.CHUNK_OVERLAP
            )
            print(f"文档处理完成，共生成 {len(split_docs)} 个文档块")
            total_chunks = len(split_docs)
            print(f"文档处理完成，共生成 {len(split_docs)} 个文档块")   
            if not split_docs:
                print(f"文件 {file.filename} 处理后为空，跳过")
            
                                # 添加文档到内容集合
            print("开始添加文档到内容集合...")
            qdrant_docs = []
            embeddings = get_embeddings()
            for j, doc in enumerate(split_docs):
                vector = embeddings.embed_query(doc.page_content)
                qdrant_doc = {
                    "id": j+1,
                    "vector": vector,
                    "payload": {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                }
                qdrant_docs.append(qdrant_doc)

        except Exception as e:
            print(f"文档处理器使用失败，跳过: {e}")


        # 生成embedding并存储
        try:
            vector_store = get_vector_store()
            vector_store.ensure_collection_exists(ai_config.QDRANT_COLLECTION_NAME)
            # 确保集合存在
            vector_store.add_documents(
                collection_name=ai_config.QDRANT_COLLECTION_NAME,
                documents=qdrant_docs
            )
            print("文档内容添加完成")
        except Exception as e:
            print(f"Error storing to QDRANT: {e}")
            raise

    finally:
        # 清理临时文件
        if os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass

    return {
        "filename": file.filename,
        "total_chunks": total_chunks,
        "stored_chunks": stored_chunks,
        "message": f"文件 {file.filename} 处理完成，成功存储 {stored_chunks}/{total_chunks} 个块到向量库"
    }

