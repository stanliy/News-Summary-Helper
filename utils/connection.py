import streamlit as st
import os
from dotenv import load_dotenv

# Database에 연걸하는 메소드
# Parameter : String sql = 불러오고자 하는 Select문 
# Return : 반환 받은 DataSet을 Dictonary로 파싱 후 반환

def connectDB(sql):
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
        query={
        # "driver": "MySQL ODBC 8.0 ANSI Driver",  # 또는 "MySQL ODBC 8.0 Unicode Driver"
        "charset": "utf8mb4",
        # "ssl-mode": "REQUIRED",  # (필요한 경우)
        },
    )

    df = conn.query(sql, ttl=0)
    return df.to_dict(orient="records")