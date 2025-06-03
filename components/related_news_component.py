import streamlit as st
from utils.related_news import step1
from utils.classify_topic import topic_to_category

def suggest_related_news():
    """
    세션 상태에 저장된 첫 번째 기사를 기반으로 관련 뉴스를 추천합니다.
    
    세션 상태의 'generated_articles' 키에서 기사 목록을 가져와서
    첫 번째 기사의 제목과 카테고리를 사용하여 관련 기사를 검색하고 표시합니다.
    """

    articles = st.session_state.get("generated_articles", [])

    if not articles:
        st.info("아직 저장된 기사가 없습니다.")
        return

    # print("ARTICLES : ", articles)
    idx = len(articles) - 1;
    result = step1(articles[idx]['title'], topic_to_category(articles[idx]['topic']))

    if not result:
        st.info("관련된 기사가 업데이트 되지 않았습니다.")
    else:
        # print(result)
        for article in result:
            with st.expander(f"**{article['title']}, {article['category']}**"):
                st.write(article["content"])