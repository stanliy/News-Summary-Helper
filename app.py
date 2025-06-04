import streamlit as st

# 각 모듈에서 run 함수 import
from pages.features.show_saved_articles import run as show_saved_articles
from pages.features.main import run as main

# 메뉴 구성
features = {
    "Home": main,
    "저장된 기사 요약문 보기" : show_saved_articles,
}

st.set_page_config(
    page_title="뉴스 요약 앱",
    layout="wide",  # 👉 여백 줄이고 넓게 보기
    initial_sidebar_state="expanded"
)

page = st.sidebar.selectbox("Choose a page", features.keys())
features[page]()