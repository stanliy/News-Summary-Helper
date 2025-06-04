import streamlit as st
from components.news_summary_process import select_options, show_input_news, show_summary_title
from components.ten_years_ago_component import get_10years_ago_news, con, sidebarCon


def run():
    """뉴스 요약 메인 페이지를 실행합니다."""
    st.title("📝뉴스 요약하기")
    df = get_10years_ago_news()
        
    text, lang, length_option = select_options()
    show_input_news(text, lang, length_option)

    if st.button("Generate"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            show_summary_title(text, lang)
    sidebarCon(df)

