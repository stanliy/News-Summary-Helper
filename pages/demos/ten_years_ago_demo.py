import streamlit as st
from components.news_summary_process import select_options, show_input_news, show_summary_title
from components.ten_years_ago_component import get_10years_ago_news, con, sidebarCon

def run():
    st.title("📝 10년 전 오늘 Demo")
    df = get_10years_ago_news() # 10년 전 기사 데이터 불러오기 (/components/ten_years_ago_component)

    # con(df)     # Case 1 : 페이지 우측면에 출력 (/components/ten_years_ago_component)
    sidebarCon(df)  # Case 2 : Sidebar에 출력 (/components/ten_years_ago_component)

