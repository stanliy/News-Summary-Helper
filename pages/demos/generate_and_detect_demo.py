import streamlit as st
from components.generate_and_detect_component import generate_and_detect

def run():
    st.title("📝 본문 추출 및 언어 감지 Demo")

    url = st.text_area("한국어 URL을 입력하세요:", height=300)

    if st.button("Generate"):
        if not url.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            generate_and_detect(url)

                