import streamlit as st
from utils.summaryNewsTest import summary_news        # 요약문 생성
from utils.summaryNewsTest import decide_summary_len  # 요약문 길이 설정
from utils.generateTitleTest import generate_title    # 제목 생성
from utils.extractor import extract_article_text      # 본문 추출
from utils.language import detect_language            # 언어 감지
from utils.classify_topic import detect_topic         # 분야 분류
from utils.article_memory import save_article,show_similar_articles  # 동일 분야 기사 출력


def run():
    st.title("📝 본문 요약문 및 제목 생성 Demo")

    st.sidebar.header('세부사항 선택')
    input_mode = st.sidebar.selectbox("입력 방식 선택", ("URL 입력", "직접 입력"))

    text = ""

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

    if text.strip():
        lang = detect_language(text)
        st.write(f"공백 포함 본문 길이: `{len(text)}` | 감지된 언어: `{lang}`")
    else:
        lang = "unknown"

    if 0 < len(text) < 100:
        st.warning("입력 길이가 너무 짧습니다 (권장 길이: 100~1000자)")

    length_option = st.sidebar.selectbox(
        "요약문 길이 선택",
        ("짧게 (약 100~300자)", "중간 (약 200~400자)", "길게 (약 400~600자)"),
    )

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

    if st.button("Generate"):
        if not text.strip():
            st.warning("텍스트를 입력해주세요.")
        else:
            summary_min, summary_max = decide_summary_len(lang, st.session_state['summary_len']).values()
            with st.spinner("생성 중입니다..."):
                summary = summary_news(text, lang, summary_min, summary_max)
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
                    show_similar_articles(topic, summary)
