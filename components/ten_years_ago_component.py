import streamlit as st
import time, datetime
from dateutil.relativedelta import relativedelta
from utils.connection import selectDB

# 10년 전 오늘 데이터를 출력하는 컴포넌트입니다 ( data 호출은 따로 )
# Manual
# 1. df = get_10years_ago_news 호출 : 10년 전 기사 데이터 가져옴
# 2. con(df) or sidebarCon(df) : 가져온 데이터로 컴포넌트 생성

def get_10years_ago_news():

    correct_time = datetime.datetime.now() - relativedelta(years=10)
    # target_date = "2015-05-17"                          # 데이터가 없어서 날짜 부분 하드코딩
    target_date = correct_time.strftime('%Y-%m-%d')

    # st.write(correct_time.strftime('%Y-%m-%d')) 

    df = selectDB(f"select * from news_summary WHERE article_date ='{target_date}'" ) 
    return df

def con(df):
    st.info("✅ 10년 전 오늘")
    for i in df:
        # st.caption(str(i['id']) + ":" + i['category'])
        with st.expander(i['title_summary']):
            st.markdown("[" + i['body_summary'] + "](" + i['url'] + ")")

def sidebarCon(df):
    with st.sidebar:
        with st.container(border=True):
            st.info("✅ 10년 전 오늘")
            with st.container(border=True):
                for i in df:
                    st.markdown(str(i['category']) + " : [" + i['title_summary'][:18] + "..." + "](" + i['url'] + ")")
                    # st.metric(str(i['id']), i['title_summary'][:20], i['category'])
                # st.caption("This is a string that explains something above.")