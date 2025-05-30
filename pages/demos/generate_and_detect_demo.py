import streamlit as st
from utils.extractor import extract_article_text
from utils.language import detect_language

def run():
    st.title("📝 본문 추출 및 언어 감지 Demo")

    url = st.text_area("한국어 URL을 입력하세요:", height=300)

    if st.button("Generate"):
        if not url.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            with st.spinner("추출 중입니다..."):
                text = extract_article_text(url)
                st.success("✅ 추출 결과:")
                lang = detect_language(text)
                st.write(f"🌐 감지된 언어: {lang}")
                st.write(text)

                