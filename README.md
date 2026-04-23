# NL2SQL - 基于Vanna.AI的自然语言转SQL工具

## 项目简介

NL2SQL是一个基于Vanna.AI框架的自然语言转SQL查询工具，集成了千问大模型和ChromaDB向量数据库。该工具提供了直观的Web界面，支持模型训练、SQL生成和查询执行等功能。

## 功能特性

### 🎯 核心功能
- **自然语言转SQL**: 将自然语言问题转换为SQL查询语句
- **模型训练**: 支持多种类型的数据训练（SQL、DDL、文档、计划）
- **查询执行**: 直接执行SQL查询并展示结果
- **向量存储**: 使用ChromaDB进行高效的向量数据存储

### 🛠️ 技术特性
- **多模型支持**: 集成千问大模型进行自然语言理解
- **RAG架构**: 基于检索增强生成（RAG）的智能问答
- **Web界面**: 基于Streamlit的现代化用户界面
- **API服务**: 提供RESTful API接口
- **数据库连接**: 支持MySQL数据库连接和查询

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   Flask API     │    │   Vanna.AI      │
│   (前端界面)     │◄──►│   (后端服务)     │◄──►│   (核心引擎)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MySQL DB      │    │   ChromaDB      │
                       │   (数据存储)     │    │   (向量存储)     │
                       └─────────────────┘    └─────────────────┘
```

## 安装说明

### 环境要求
- Python 3.8+
- MySQL 数据库
- 千问API密钥

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd text2sql
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据库**
   - 确保MySQL服务正在运行
   - 修改 `vanna_ui.py` 和 `vanna_api.py` 中的数据库配置：
```python
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password',
    'database': 'your_database',
    'cursorclass': DictCursor
}
```

4. **配置API密钥**
   - 在 `vanna_api.py` 中设置千问API密钥：
```python
self.api_key = 'your_qwen_api_key'
```

## 使用方法

### 启动服务

1. **启动API服务**
```bash
python vanna_api.py
```
API服务将在 `http://localhost:5001` 启动

2. **启动Web界面**
```bash
python vanna_ui.py
```
Web界面将在 `http://localhost:8501` 启动

### 功能使用

#### 1. 模型训练
- **SQL训练**: 提供问题和对应的SQL语句进行训练
- **DDL训练**: 添加数据库结构定义
- **文档训练**: 添加业务文档和说明
- **计划训练**: 添加分析计划和策略

#### 2. SQL生成
- 在文本框中输入自然语言问题
- 系统自动生成对应的SQL查询语句
- 支持复杂查询和聚合操作

#### 3. 查询执行
- 直接输入SQL语句
- 实时执行并展示查询结果
- 支持数据表格展示

## API接口文档

### 训练接口

#### 训练SQL数据
```http
POST /train/sql
Content-Type: application/json

{
    "question": "查询所有用户信息",
    "sql": "SELECT * FROM users"
}
```

#### 训练DDL数据
```http
POST /train/ddl
Content-Type: application/json

{
    "ddl": "CREATE TABLE users (id INT, name VARCHAR(255))"
}
```

#### 训练文档数据
```http
POST /train/documentation
Content-Type: application/json

{
    "documentation": "用户表包含用户基本信息"
}
```

### 查询接口

#### 生成SQL
```http
POST /generate-sql
Content-Type: application/json

{
    "question": "查询销售额超过1000的产品"
}
```

#### 执行SQL
```http
POST /run-sql
Content-Type: application/json

{
    "sql": "SELECT * FROM products WHERE price > 100"
}
```

#### 获取训练数据统计
```http
GET /training-data-count
```

## 项目结构

```
text2sql/
├── README.md              # 项目说明文档
├── requirements.txt       # 依赖包列表
├── vanna_api.py          # Flask API服务
├── vanna_ui.py           # Streamlit Web界面
└── test.py               # 测试工具
```

## 核心组件说明

### MyCustomLLM类
- 继承自VannaBase
- 集成千问大模型API
- 处理自然语言理解和生成

### MyVanna类
- 继承ChromaDB_VectorStore和MyCustomLLM
- 实现向量存储和LLM的集成
- 提供统一的训练和查询接口

### Web界面
- 基于Streamlit构建
- 提供直观的用户交互界面
- 支持实时数据展示和操作

## 配置说明

### 端口配置
- API服务默认端口: 5001
- Web界面默认端口: 8501
- 可通过命令行参数自定义端口

### 数据库配置
- 支持MySQL数据库连接
- 使用DictCursor返回字典格式结果
- 支持自定义数据库连接参数

## 注意事项

1. **API密钥安全**: 请妥善保管千问API密钥，不要提交到版本控制系统
2. **数据库权限**: 确保数据库用户具有足够的读写权限
3. **网络连接**: 确保能够访问千问API服务
4. **内存使用**: ChromaDB会占用一定的内存空间，注意监控系统资源

## 故障排除

### 常见问题

1. **API连接失败**
   - 检查千问API密钥是否正确
   - 确认网络连接正常

2. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库连接参数

3. **训练数据提交失败**
   - 检查API服务是否正常运行
   - 确认数据格式是否正确

## 开发计划

- [ ] 支持更多数据库类型
- [ ] 添加数据可视化功能
- [ ] 优化模型训练效果
- [ ] 增加批量导入功能
- [ ] 添加用户权限管理

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目采用MIT许可证。 