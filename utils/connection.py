import os
import datetime

import streamlit as st
from dotenv import load_dotenv


# 현재 날짜를 YYYY-MM-DD 형식의 문자열로 반환합니다.
# Returns:
#       str: 현재 날짜 문자열
def get_correct_time():

    correct_time = datetime.datetime.now()
    target_date = correct_time.strftime('%Y-%m-%d')
    return target_date

# Database에 연걸하는 메소드
# Parameter : String sql = 불러오고자 하는 Select문 
# Return : 반환 받은 DataSet을 Dictonary로 파싱 후 반환

def selectDB(sql):
    if os.getenv("GITHUB_ACTIONS") != "true":
        load_dotenv()
        
    conn = st.connection(
        "sql",
        dialect="mysql",
        driver="pymysql",
        host=os.getenv("ODB_HOST"),
        database=os.getenv("DB_NAME"),
        username=os.getenv("ODB_USER"),
        password=os.getenv("ODB_PASSWORD"),
        connect_args={"charset": "utf8mb4"},
    )

    df = conn.query(sql, ttl=0)
    
    return df.to_dict(orient="records")


def updateDB(sql_list, param_list):
    print("update Start!")
    if os.getenv("GITHUB_ACTIONS") != "true":
        load_dotenv()
        
    conn = st.connection(
        "sql",
        dialect="mysql",
        driver="pymysql",
        host=os.getenv("ODB_HOST"),
        database=os.getenv("DB_NAME"),
        username=os.getenv("ODB_USER"),
        password=os.getenv("ODB_PASSWORD"),
        connect_args={"charset": "utf8mb4"},
    )

    try:
        with conn.session as session:
            for sql, params in zip(sql_list, param_list):
                session.execute(sql, params)
                session.commit()
    except Exception as e:
        print(f"Database Update failed : {e}")
        return {"status": "error"}
    return {"status": "success"}    
