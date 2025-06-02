import streamlit as st
from utils.classify_topic import get_topic
from utils.article_filter import filter_condition


# 필터링 옵션 선택 및 저장된 기사를 보여주는 컴포넌트입니다
# Manual
# 1. lang, topic = select_filtering() : 사이드바에서 저장된 기사에 대한 언어/분야별 필터링 옵션 선택 및 반환
# 2. show_articles(lang, topic) : 저장된 기사 메인 영역에 출력


def show_articles(lang, topic):
    articles = st.session_state.get("generated_articles", [])

    if not articles:
        st.info("아직 저장된 기사가 없습니다.")
        return

    filtered_articles = [a for a in articles if filter_condition(a, lang, topic)]

    if not filtered_articles:
        st.info("조건에 맞는 기사가 없습니다.")
    else:
        st.write(f"총 {len(filtered_articles)}개의 기사 결과")
        for article in filtered_articles:
            manage_saved_articles(article)


def select_filtering():
    st.sidebar.header('세부사항 선택')

    lang = st.sidebar.selectbox('언어 선택', ['전체', '한국어', '영어'])
    lang_map = {'전체': None, '한국어': 'ko', '영어': 'en'}

    selected_lang = lang_map[lang]
    selected_topic = st.sidebar.selectbox('분야 선택', ["전체"] + get_topic())

    return selected_lang, selected_topic


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
