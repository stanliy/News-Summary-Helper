import streamlit as st
from utils.generateTitleTest import generateTitle


def run():
    st.title("📝 Generate Title Demo")

    text = st.text_area("뉴스 요약문을 입력하세요:", height=300)

    if st.button("제목 생성"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            with st.spinner("요약 중입니다..."):
                title = generateTitle(text)
                st.success("✅ 제목 생성 완료 !")
                st.write(title)