import streamlit as st
from utils.classify_topic import get_topic


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


def show_similar_articles(current_topic, current_summary):
    if "generated_articles" not in st.session_state:
        return

    similar_articles = [
        article for article in st.session_state.generated_articles
        if article["topic"] == current_topic and article["summary"] != current_summary
    ]

    if similar_articles:
        st.write("---")
        st.subheader(f"같은 분야({current_topic})의 기사들")
        for article in similar_articles:
            with st.expander(f"**{article['title']}**"):
                st.write(article["summary"])


def manage_saved_articles(article):
    article_key = f"{hash(article['title'] + article['summary'])}"

    with st.container(border=True):
        st.write(f"**{article['title']}**")
        st.write(article["summary"])
        st.write(f"분야: `{article['topic']}` | 언어: `{article['lang']}`")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("수정", key=f"edit_{article_key}", use_container_width=True):
                st.session_state[f"edited_{article_key}"] = True

        with col2:
            if st.button("삭제", key=f"delete_{article_key}", use_container_width=True):
                st.session_state.generated_articles.remove(article)
                st.rerun()

        if st.session_state.get(f"edited_{article_key}", False):
            st.write("---")
            modified_topic = st.selectbox("새로운 분야를 선택하세요", get_topic(), index=get_topic().index(article["topic"]))

            if st.button("저장", use_container_width=True):
                article["topic"] = modified_topic
                st.session_state[f"edited_{article_key}"] = False
                st.rerun()
