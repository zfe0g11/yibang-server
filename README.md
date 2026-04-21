# yibang-server - 二手车抵押平台后端

## 一、项目概述

益邦二手车抵押平台是一个基于FastAPI开发的后端服务，集成了AI功能的二手车抵押业务全流程管理平台。除了传统的车辆信息管理、抵押申请、审批流程等功能外，还新增了AI聊天和RAG检索增强生成功能，为用户提供智能化的服务体验。

## 二、技术栈

### 核心技术
- **FastAPI**: 高性能Python Web框架
- **SQLAlchemy**: ORM数据库框架
- **MySQL**: 关系型数据库
- **Redis**: 缓存和会话管理
- **JWT**: 身份认证
- **Qdrant**: 向量数据库
- **LLM**: 大语言模型（支持讯飞星火）

### 辅助工具
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI服务器
- **OSS**: 对象存储
- **FastAPI-Pagination**: 分页支持
- **LangChain**: 开发语言模型应用框架

## 三、项目结构

```
d:\AI开发\yibang-server-python\
├── app/                     # 主应用目录
│   ├── api/                 # API路由
│   │   └── v1/              # 版本1
│   │       ├── car.py       # 车辆API
│   │       ├── car-mortgage.py # 车辆抵押API
│   │       ├── category.py  # 分类API
│   │       ├── chat.py      # AI聊天API
│   │       ├── common.py    # 通用API
│   │       ├── employee.py  # 员工API
│   │       ├── rag.py       # RAG检索API
│   │       └── user.py      # 用户API
│   ├── core/                # 核心配置
│   │   └── database.py      # 数据库配置
│   ├── crud/                # 数据操作层
│   │   ├── car.py           # 车辆CRUD
│   │   ├── car_mortgage.py  # 车辆抵押CRUD
│   │   ├── category.py      # 分类CRUD
│   │   ├── chat.py          # AI聊天CRUD
│   │   ├── employee.py      # 员工CRUD
│   │   ├── rag_crud.py      # RAG检索CRUD
│   │   └── user.py          # 用户CRUD
│   ├── models/              # 数据库模型
│   │   ├── Basemodel.py     # 基础模型
│   │   ├── car.py           # 车辆模型
│   │   ├── car_mortgage.py  # 车辆抵押模型
│   │   ├── category.py      # 分类模型
│   │   ├── chat_history.py  # 聊天历史模型
│   │   ├── employee.py      # 员工模型
│   │   └── user.py          # 用户模型
│   ├── schemas/             # 数据验证模型
│   │   └── employee.py      # 员工验证模型
│   ├── __init__.py
│   └── main.py              # 应用入口
├── common/                  # 通用组件
│   ├── constant/            # 常量定义
│   ├── context/             # 上下文管理
│   ├── dto/                 # 数据传输对象
│   ├── entity/              # 实体类
│   ├── enumeration/         # 枚举类型
│   ├── exception/           # 异常处理
│   ├── json/                # JSON工具
│   ├── properties/          # 属性配置
│   ├── result/              # 统一返回结果
│   ├── utils/               # 工具类
│   │   ├── document_processor.py # 文档处理工具
│   │   ├── rag_chain.py     # RAG链工具
│   │   └── vector_store.py  # 向量存储工具
│   └── vo/                  # 视图对象
├── config/                  # 配置文件
│   └── ai_config.py         # AI配置
├── .env                     # 环境变量配置
├── requirements.txt         # 依赖清单
└── README.md                # 项目文档
```

## 四、核心功能模块

### 1. 员工管理模块
- 员工登录认证
- 员工信息管理
- 权限控制
- 会话管理

### 2. 车辆分类管理模块
- 品牌分类管理
- 型号分类管理
- 树形结构展示

### 3. 车辆管理模块
- 车辆信息录入
- 车辆图片上传
- 车辆信息查询
- 车辆状态管理

### 4. 车辆抵押模块
- 抵押申请提交
- 抵押审批流程
- 抵押状态跟踪
- 还款管理

### 5. 用户管理模块
- 用户注册登录
- 用户信息管理
- 个人中心

### 6. AI聊天模块
- 智能问答
- 聊天历史记录
- 多轮对话
- 上下文理解

### 7. RAG检索增强生成模块
- 文档检索
- 知识问答
- 信息抽取
- 智能推荐

## 五、快速开始

### 1. 环境准备
- Python 3.10+
- MySQL 5.7+
- Redis 6.0+
- Qdrant 1.0+

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置文件
创建`.env`文件：
```env
# Redis配置
REDIS_HOST=
REDIS_PORT=
REDIS_DB=0
REDIS_PASSWORD=

# 数据库配置
DATABASE_URL=

# 阿里云 OSS 配置
ALI_OSS_ENDPOINT=
ALI_OSS_ACCESS_KEY_ID=
ALI_OSS_ACCESS_KEY_SECRET=
ALI_OSS_BUCKET_NAME=

# QDRANT 向量数据库配置
QDRANT_URL=
QDRANT_COLLECTION_NAME=
QDRANT_SUMMARY_COLLECTION_NAME=
SQL_XXK_YIBANG_COLLECTION_NAME=

# MySQL数据库配置
MYSQL_HOST_URL=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DATABASE=

# 文档处理配置
DOCUMENT_PATH_DIR=
DELIMITER_BASED_CHUNKING_SIZE=
DELIMITER_BASED_CHUNK_OVERLAP=
CHUNK_SIZE=
CHUNK_OVERLAP=

# LLM模型配置
LLM_MODEL=
XUNFEI_API_BASE=
XUNFEI_API_KEY=

# 嵌入模型配置
EMBEDDING_LLM_MODEL=
EMBEDDING_XUNFEI_API_BASE=
EMBEDDING_XUNFEI_API_KEY=

# JWT配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 4. 启动服务
```bash
cd d:\AI开发\yibang-server-python
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 5. 访问API文档
- Swagger UI: http://localhost:8080/doc
- ReDoc: http://localhost:8080/redoc

## 六、API示例

### 1. 员工登录
```bash
curl -X POST "http://localhost:8080/admin/employee/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123456"}'
```

### 2. 新增车辆
```bash
curl -X POST "http://localhost:8080/admin/car" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "特斯拉 Model 3", "model_id": 1, "brand_id": 1, "price": 250000, "image": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/2023/01/01/123456.jpg", "description": "特斯拉 Model 3 是一款纯电动轿车"}'
```

### 3. AI聊天
```bash
curl -X POST "http://localhost:8080/admin/chat" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"message": "推荐几款适合抵押的二手车", "user_id": 1}'
```

### 4. RAG检索
```bash
curl -X POST "http://localhost:8080/admin/rag/query" \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"query": "二手车抵押流程", "user_id": 1}'
```

## 七、缓存策略

### 1. Redis应用场景
- 会话管理：存储JWT Token
- 数据缓存：缓存车辆信息、员工信息
- 性能优化：缓存分页查询结果
- 安全防护：登录失败次数限制

### 2. 缓存键设计
| 缓存类型       | 键名格式               | 过期时间 |
|----------------|------------------------|----------|
| 会话管理       | `session:{user_id}`    | 24小时   |
| 数据缓存       | `employee:{user_id}`   | 1小时    |
| 分页缓存       | `car_page:{page}:{size}`| 10分钟   |
| 登录限制       | `login_fail:{username}`| 15分钟   |

## 八、AI功能架构

### 1. RAG检索流程
```
用户查询 → 向量检索 → 文档匹配 → 上下文构建 → LLM生成 → 结果返回
```

### 2. 文档处理流程
```
文档上传 → 文本提取 → 分段处理 → 向量化 → 向量存储
```

### 3. 聊天流程
```
用户消息 → 历史记录 → 上下文构建 → LLM生成 → 结果返回 → 历史存储
```

## 九、部署建议

### 1. 开发环境
- 使用`--reload`参数自动重载代码
- 开启Swagger UI方便调试

### 2. 测试环境
- 使用Gunicorn + Uvicorn部署
- 配置日志记录

### 3. 生产环境
- 使用Docker容器化部署
- 配置负载均衡
- 开启HTTPS
- 配置向量数据库集群

## 十、技术亮点

### 1. 性能优化
- Redis缓存减少数据库查询
- FastAPI异步处理提高并发能力
- 分页查询优化
- 向量检索加速

### 2. 安全防护
- JWT身份认证
- 登录失败次数限制
- 接口限流
- 数据加密存储

### 3. AI能力
- 集成LLM模型
- RAG检索增强生成
- 智能问答系统

### 4. 可扩展性
- 模块化设计便于功能扩展
- 统一返回结果格式
- 完善的异常处理机制
- 支持多模型切换

## 十一、后续规划

### 1. 功能扩展
- 实现车辆评估功能
- 添加还款计划管理
- 实现报表统计功能
- 增强AI聊天功能
- 扩展RAG知识库

### 2. 性能优化
- 实现数据库读写分离
- 添加消息队列处理异步任务
- 优化图片存储和加载
- 向量数据库性能优化
- LLM模型微调

### 3. 安全加固
- 实现细粒度权限控制
- 添加操作日志记录
- 数据加密存储
- AI内容安全审核

### 4. AI升级
- 多模型集成
- 多模态处理
- 个性化推荐
- 智能决策支持

## 十二、联系方式

- 技术支持：support@example.com
- 项目地址：http://example.com

## 十三、许可证

Apache 2.0 License