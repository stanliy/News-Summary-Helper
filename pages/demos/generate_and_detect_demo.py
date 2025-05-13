import streamlit as st

def run():
    st.title("📝 본문 추출 및 언어 감지 Demo")

    text = st.text_area("한국어 URL을 입력하세요:", height=300)

    if st.button("Generate"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            with st.spinner("추출 중입니다..."):
                st.success("✅ 추출 결과:")
                st.write("To-Do")