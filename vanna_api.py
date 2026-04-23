from flask import Flask, request, jsonify
import vanna
from vanna.base import VannaBase
from vanna.chromadb import ChromaDB_VectorStore
import chromadb
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

class MyCustomLLM(VannaBase):
    def __init__(self, config=None):
        super().__init__(config=config)
        self.model = 'qwen-plus'
        self.api_key = 'sk-5945d2a7cb094d439d9hec5fas314bdf'

    def submit_prompt(self, prompt, **kwargs) -> str:
        # 这里实现与千问大模型的交互逻辑
        # 示例实现可以参考: https://github.com/vanna-ai/vanna/blob/main/src/vanna/mistral/mistral.py
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=prompt,
        )

        return chat_response.choices[0].message.content

class MyVanna(ChromaDB_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)
        
    def assistant_message(self, message: str) -> dict:
        return {"role": "assistant", "content": message}
        
    def system_message(self, message: str) -> dict:
        return {"role": "system", "content": message}
        
    def user_message(self, message: str) -> dict:
        return {"role": "user", "content": message}

# 初始化自定义Vanna实例
vn = MyVanna()

# MySQL数据库连接配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password_here',
    'database': '5945d2a7cb094d439d9hec5fas314bdf',
    'cursorclass': DictCursor
}

# 训练数据收集接口
@app.route('/train/sql', methods=['POST'])
def train_sql():
    data = request.get_json()
    question = data.get('question')
    sql = data.get('sql')
    
    if not question or not sql:
        return jsonify({"error": "Both question and sql are required"}), 400
    
    try:
        vn.train(question=question, sql=sql)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train/ddl', methods=['POST'])
def train_ddl():
    data = request.get_json()
    ddl = data.get('ddl')
    
    if not ddl:
        return jsonify({"error": "DDL is required"}), 400
    
    try:
        vn.add_ddl(ddl=ddl)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train/documentation', methods=['POST'])
def train_documentation():
    data = request.get_json()
    documentation = data.get('documentation')
    
    if not documentation:
        return jsonify({"error": "Documentation is required"}), 400
    
    try:
        vn.add_documentation(documentation=documentation)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/train/plan', methods=['POST'])
def train_plan():
    data = request.get_json()
    plan = data.get('plan')
    
    if not plan:
        return jsonify({"error": "Plan is required"}), 400
    
    try:
        vn.add_documentation(documentation=plan)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# SQL生成接口
@app.route('/generate-sql', methods=['POST'])
def generate_sql():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "question is required"}), 400
    
    try:
        sql = vn.generate_sql(question=question)
        return jsonify({"sql": sql})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 执行SQL查询接口
@app.route('/run-sql', methods=['POST'])
def run_sql():
    data = request.get_json()
    sql = data.get('sql')
    
    if not sql:
        return jsonify({"error": "sql is required"}), 400
    
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)