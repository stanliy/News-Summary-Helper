import streamlit as st
from utils.summaryNewsTest import summary_news        # 요약문 생성
from utils.summaryNewsTest import decide_summary_len  # 요약문 길이 설정
from utils.generateTitleTest import generate_title    # 제목 생성
from utils.extractor import extract_article_text      # 본문 추출
from utils.language import detect_language            # 언어 감지
from utils.classify_topic import detect_topic         # 분야 분류
from utils.article_memory import save_article         # 기사 자동 저장
from components.related_news_component import suggest_related_news


# 요약 옵션 선택 및 요약 결과를 보여주는 컴포넌트입니다
# Manual
# 1. text, lang, length_option = select_options()
#    : 사이드바에서 본문 입력 방식, 요약문 길이 선택 및 본문 내용, 감지된 언어, 설정 길이 반환
# 2. show_input_news(text, lang): 본문으로부터 감지된 길이와 언어 출력
# 3. show_summary_title(text, lang): 메인 영역에 요약 결과, 감지된 길이, 언어, 동일 분야 기사 출력


def select_options():
    st.sidebar.header('세부사항 선택')
    input_mode = st.sidebar.selectbox("입력 방식 선택", ("URL 입력", "직접 입력"))
    length_option = st.sidebar.selectbox(
        "요약문 길이 선택",
        ("짧게 (약 100~300자)", "중간 (약 200~400자)", "길게 (약 400~600자)"),
    )

    text = ""

    # 본문 입력 방식 처리
    if input_mode == "URL 입력":
        url = st.text_input("URL을 입력하세요",
                            help="url 입력 후 enter를 누르면 본문 길이와 감지된 언어가 표시됩니다",
                            placeholder="예: https://www.example.com/article/...")
        if url.strip():
            try:
                with st.spinner("본문 추출 중입니다..."):
                    text = extract_article_text(url)
            except ValueError as e:
                st.error(str(e))

    elif input_mode == "직접 입력":
        text = st.text_area("뉴스 본문을 입력하세요",
                            help="본문 입력 후 ctrl+enter를 누르면 본문 길이와 감지된 언어가 표시됩니다",
                            placeholder="여기에 본문을 직접 입력하세요", height=300)

    lang = detect_language(text)

    return text, lang, length_option


def show_input_news(text, lang, length_option):
    if text.strip():
        st.write(f"공백 포함 본문 길이: `{len(text)}` | 감지된 언어: `{lang}`")

        # 본문 길이와 설정 길이의 차이에 따른 경고 표시
        if 0 < len(text) < 100:
            st.warning("입력 길이가 너무 짧습니다 (권장 길이: 100~1000자)")

        if length_option == "짧게 (약 100~300자)":
            st.session_state['summary_len'] = 'short'
        elif length_option == "중간 (약 200~400자)":
            if len(text) < 200:
                st.warning("입력 길이가 설정 길이보다 짧습니다")
            st.session_state['summary_len'] = 'medium'
        else:
            if len(text) < 400:
                st.warning("입력 길이가 설정 길이보다 짧습니다")
            st.session_state['summary_len'] = 'long'
    else:
        lang = "unknown"


def show_summary_title(text, lang):
    summary_min, summary_max = decide_summary_len(lang, st.session_state['summary_len']).values()
    with st.spinner("생성 중입니다..."):
        try:
            summary = summary_news(text, lang, summary_min, summary_max)
        except IndexError:
            st.error("입력 길이를 다시 확인해주세요. (권장 길이 100 ~ 2000자)")
            return
        title = generate_title(summary, lang)
        topic = detect_topic(text if len(text) <= 512 else summary)
        try:
            save_article(title, summary, topic, lang)
        except Exception as e:
            st.info(f"기사 자동 저장에 실패하였습니다 ({e})")
        if summary == "error1":
            st.error("언어 감지에 실패하였습니다 (지원 언어: 영어, 한국어)")
        elif summary == "error2":
            st.error("지원하는 언어가 아닙니다 (지원 언어: 영어, 한국어)")
        else:
            st.success("✅ 생성 완료 !")
            st.write(f"**{title}**")
            st.write(summary)
            st.write(f"공백 포함 요약문 길이: `{len(summary)}` | 분야: `{topic}`")

            # 기존에 요약을 진행한 기사 
            # show_similar_articles(topic, summary) 

            # 같은 category에서 유사도가 높은 순서 관련 기사 (components/related_news_component.py)
            suggest_related_news() 



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