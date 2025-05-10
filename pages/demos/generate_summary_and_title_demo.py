import streamlit as st


def run():
    st.title("📝 본문 내용 요약문 및 제목 생성 Demo")

    text = st.text_area("뉴스 본문을 입력하세요:", height=300)

    if st.button("Generate"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            with st.spinner("생성 중입니다..."):
                st.success("✅ 생성 완료 !")
                st.write("To-Do")