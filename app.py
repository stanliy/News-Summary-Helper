import streamlit as st

# 각 모듈에서 run 함수 import
from pages.samples.kobart_summary_sample import run as kobart_summary
from pages.samples.generate_title_sample import run as generate_title
from pages.demos.generate_and_detect_demo import run as generate_and_detect
from pages.demos.generate_summary_and_title_demo import run as generate_summary_and_title
from pages.demos.show_saved_articles import run as show_saved_articles
from pages.demos.ten_years_ago_demo import run as ten_years_ago_demo

def intro():
    st.title("Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")
    st.write(
        """
        This app showcases different Streamlit features.
        Choose a demo from the sidebar to begin!
        """
    )

# 메뉴 구성
samples = {
    "Home": intro,
    "Kobart News Summary Demo": kobart_summary,
    "Generate Summary Title Demo": generate_title
}
demos = {
    "본문 추출 및 언어 감지 Sample" : generate_and_detect,
    "본문 내용 요약문 및 제목 생성 Sample" : generate_summary_and_title,
    "저장된 기사 요약문 보기 Sample" : show_saved_articles,
    "10년 전 오늘 Sample" : ten_years_ago_demo
}


st.set_page_config(
    page_title="뉴스 요약 앱",
    layout="wide",  # 👉 여백 줄이고 넓게 보기
    initial_sidebar_state="expanded"
)
pages = {**samples, **demos}  # 두 dict 병합
page = st.sidebar.selectbox("Choose a page", pages.keys())
pages[page]()