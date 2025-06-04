import streamlit as st
from components.saved_articles_component import select_filtering, show_articles


def run():
    st.title("📝저장된 기사 보기")
    lang, topic = select_filtering()
    show_articles(lang, topic)  # 저장된 기사 메인영역에 출력 (/components/show_saved_articles_component)
