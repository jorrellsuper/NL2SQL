import streamlit as st
import requests
import pymysql
from pymysql.cursors import DictCursor
import argparse

# 默认端口配置
DEFAULT_PORT = 8501

# MySQL数据库连接配置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password_here',
    'database': '5945d2a7cb094d439d9hec5fas314bdf',
    'cursorclass': DictCursor
}

# API基础URL
API_BASE_URL = "http://localhost:5001"

def main():
    st.title('Vanna.AI 训练界面')
    menu = st.sidebar.selectbox('功能选择', ['训练模型', '生成SQL', '执行查询'])

    if menu == '训练模型':
        st.header('训练RAG模型')
        train_type = st.radio('训练数据类型', ['SQL', 'DDL', 'Documentation', 'Plan'])
        
        if train_type == 'SQL':
            question = st.text_area('输入问题', help='例如: 查询所有用户信息')
            sql = st.text_area('输入对应的SQL语句', help='例如: SELECT * FROM users')
            
            if st.button('提交训练'):
                if question and sql:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/train/sql",
                            json={"question": question, "sql": sql}
                        )
                        if response.status_code == 200:
                            st.success('SQL训练数据提交成功!')
                        else:
                            st.error(f'训练失败: {response.json().get("error")}')
                    except Exception as e:
                        st.error(f'训练失败: {str(e)}')
                else:
                    st.warning('问题和SQL语句都不能为空')
        
        elif train_type == 'DDL':
            ddl = st.text_area('输入DDL语句', help='例如: CREATE TABLE users (id INT, name VARCHAR(255))')
            
            if st.button('提交训练'):
                if ddl:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/train/ddl",
                            json={"ddl": ddl}
                        )
                        if response.status_code == 200:
                            st.success('DDL训练数据提交成功!')
                        else:
                            st.error(f'训练失败: {response.json().get("error")}')
                    except Exception as e:
                        st.error(f'训练失败: {str(e)}')
                else:
                    st.warning('DDL语句不能为空')
        
        elif train_type == 'Documentation':
            documentation = st.text_area('输入文档内容', help='例如: 用户表包含用户基本信息')
            
            if st.button('提交训练'):
                if documentation:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/train/documentation",
                            json={"documentation": documentation}
                        )
                        if response.status_code == 200:
                            st.success('文档训练数据提交成功!')
                        else:
                            st.error(f'训练失败: {response.json().get("error")}')
                    except Exception as e:
                        st.error(f'训练失败: {str(e)}')
                else:
                    st.warning('文档内容不能为空')
        
        elif train_type == 'Plan':
            plan = st.text_area('输入计划内容', help='例如: 分析用户购买行为')
            
            if st.button('提交训练'):
                if plan:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/train/plan",
                            json={"plan": plan}
                        )
                        if response.status_code == 200:
                            st.success('计划训练数据提交成功!')
                        else:
                            st.error(f'训练失败: {response.json().get("error")}')
                    except Exception as e:
                        st.error(f'训练失败: {str(e)}')
                else:
                    st.warning('计划内容不能为空')

    elif menu == '生成SQL':
        st.header('根据问题生成SQL')
        question = st.text_area('输入您的问题', help='例如: 查询销售额超过1000的产品')
        
        if st.button('生成SQL'):
            if question:
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/generate-sql",
                        json={"question": question}
                    )
                    if response.status_code == 200:
                        sql = response.json().get("sql")
                        st.code(sql, language='sql')
                    else:
                        st.error(f'生成SQL失败: {response.json().get("error")}')
                except Exception as e:
                    st.error(f'生成SQL失败: {str(e)}')
            else:
                st.warning('请输入问题')

    elif menu == '执行查询':
        st.header('执行SQL查询')
        sql = st.text_area('输入SQL语句', help='例如: SELECT * FROM products WHERE price > 100')
        
        if st.button('执行查询'):
            if sql:
                try:
                    connection = pymysql.connect(**db_config)
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        result = cursor.fetchall()
                    connection.close()
                    st.dataframe(result)
                except Exception as e:
                    st.error(f'查询执行失败: {str(e)}')
            else:
                st.warning('请输入SQL语句')

    try:
        response = requests.get(f"{API_BASE_URL}/training-data-count")
        if response.status_code == 200:
            count = response.json().get("count")
            st.sidebar.info(f'当前训练数据量: {count}')
        else:
            st.sidebar.warning('无法获取训练数据量')
    except:
        st.sidebar.warning('无法获取训练数据量')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='指定Streamlit运行端口')
    args = parser.parse_args()
    
    # 设置Streamlit运行端口
    import os
    os.environ["STREAMLIT_SERVER_PORT"] = str(args.port)
    main()