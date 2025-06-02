import streamlit as st
from components.news_summary_process import select_options, show_input_news, show_summary_title


def run():
    st.title("📝 본문 요약문 및 제목 생성 Demo")
    text, lang, length_option = select_options()
    show_input_news(text, lang, length_option)

    if st.button("Generate"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            show_summary_title(text, lang)
