import streamlit as st
from utils.extractor import extract_article_text
from utils.language import detect_language

def generate_and_detect(url):
    with st.spinner("추출 중입니다..."):
        text = extract_article_text(url)
        st.success("✅ 추출 결과:")
        lang = detect_language(text)
        st.write(f"🌐 감지된 언어: {lang}")
        st.write(text)