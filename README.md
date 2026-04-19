# yibang-server - 二手车抵押平台后端

## 一、项目概述

益邦二手车抵押平台是一个基于FastAPI开发的后端服务，提供二手车抵押业务的全流程管理，包括车辆信息管理、抵押申请、审批流程等功能。

## 二、技术栈

### 核心技术
- **FastAPI**: 高性能Python Web框架
- **SQLAlchemy**: ORM数据库框架
- **MySQL**: 关系型数据库
- **Redis**: 缓存和会话管理
- **JWT**: 身份认证

### 辅助工具
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI服务器
- **OSS**: 对象存储
- **FastAPI-Pagination**: 分页支持

## 三、项目结构

```
\yibang-server-python\
├── app/                     # 主应用目录
│   ├── api/                 # API路由
│   │   └── v1/              # 版本1
│   │       ├── car.py       # 车辆API
│   │       ├── car-mortgage.py # 车辆抵押API
│   │       ├── category.py  # 分类API
│   │       ├── common.py    # 通用API
│   │       ├── employee.py  # 员工API
│   │       └── user.py      # 用户API
│   ├── core/                # 核心配置
│   │   └── database.py      # 数据库配置
│   ├── crud/                # 数据操作层
│   │   ├── car.py           # 车辆CRUD
│   │   ├── car_mortgage.py  # 车辆抵押CRUD
│   │   ├── category.py      # 分类CRUD
│   │   ├── employee.py      # 员工CRUD
│   │   └── user.py          # 用户CRUD
│   ├── models/              # 数据库模型
│   │   ├── Basemodel.py     # 基础模型
│   │   ├── car.py           # 车辆模型
│   │   ├── car_mortgage.py  # 车辆抵押模型
│   │   ├── category.py      # 分类模型
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
│   └── vo/                  # 视图对象
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

## 五、快速开始

### 1. 环境准备
- Python 3.10+
- MySQL 5.7+
- Redis 6.0+

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置文件
创建`.env`文件：
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:admintoor@host/database?charset=utf8mb4

# Redis配置
REDIS_HOST=
REDIS_PORT=
REDIS_DB=0
REDIS_PASSWORD=

# JWT配置
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 4. 启动服务
```bash
cd yibang-server-python
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

### 3. 车辆分页查询
```bash
curl -X GET "http://localhost:8080/admin/car/page?page=1&page_size=10" \
  -H "Authorization: Bearer your-token"
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

## 八、部署建议

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

## 九、技术亮点

### 1. 性能优化
- Redis缓存减少数据库查询
- FastAPI异步处理提高并发能力
- 分页查询优化

### 2. 安全防护
- JWT身份认证
- 登录失败次数限制
- 接口限流

### 3. 可扩展性
- 模块化设计便于功能扩展
- 统一返回结果格式
- 完善的异常处理机制

## 十、后续规划

### 1. 功能扩展
- 实现车辆评估功能
- 添加还款计划管理
- 实现报表统计功能

### 2. 性能优化
- 实现数据库读写分离
- 添加消息队列处理异步任务
- 优化图片存储和加载

### 3. 安全加固
- 实现细粒度权限控制
- 添加操作日志记录
- 数据加密存储

## 十一、联系方式

- 技术支持：support@example.com
- 项目地址：http://example.com

## 十二、许可证

Apache 2.0 License