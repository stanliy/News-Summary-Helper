import streamlit as st


# 생성된 요약 결과들 세션에 저장
def save_article(title: str, summary: str, topic:str, lang:str) -> None:
    if title is None:  # 정상적으로 생성된 요약문만 저장되도록
        return

    if "generated_articles" not in st.session_state:
        st.session_state.generated_articles = []

    # 기사 중복 저장 방지
    for article in st.session_state.generated_articles:
        if article["title"] == title.strip() and article["summary"] == summary.strip():
            return

    st.session_state.generated_articles.append({
        "title": title.strip(),
        "summary": summary.strip(),
        "topic": topic,
        "lang": lang
    })
