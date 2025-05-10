import streamlit as st
from utils.summaryNewsTest import summaryNews

def run():
    st.title("📝 KoBART News Summary Demo")

    text = st.text_area("한국어 뉴스 원문을 입력하세요:", height=300)

    if st.button("요약하기"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            with st.spinner("요약 중입니다..."):
                summary = summaryNews(text)
                st.success("✅ 요약 결과:")
                st.write(summary)