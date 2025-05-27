import streamlit as st
from utils.summaryNewsTest import summary_news        # 요약문 생성
from utils.summaryNewsTest import decide_summary_len  # 요약문 길이 설정
from utils.generateTitleTest import generate_title    # 제목 생성
from utils.extractor import extract_article_text      # 본문 추출
from utils.language import detect_language            # 언어 감지


def run():
    """
    Streamlit 앱에서 뉴스 기사 본문을 입력받아 요약문과 제목을 생성합니다.
    
    URL 입력 또는 직접 입력 방식으로 본문을 받아 언어를 감지하고, 원하는 요약문 길이를 선택할 수 있습니다. 입력된 본문과 선택된 옵션에 따라 요약문과 제목을 생성하여 결과를 표시합니다. 입력이 너무 짧거나 지원하지 않는 언어일 경우 경고 또는 오류 메시지를 제공합니다.
    """
    st.title("📝 본문 요약문 및 제목 생성 Demo")

    input_mode = st.radio("입력 방식을 선택하세요", ("URL 입력", "직접 입력"), horizontal=True)

    text = ""

    if input_mode == "URL 입력":
        url = st.text_input("URL을 입력하세요", placeholder="예: https://www.example.com/article/...")
        if url.strip():
            try:
                with st.spinner("본문 추출 중입니다..."):
                    text = extract_article_text(url)
            except ValueError as e:
                st.error(str(e))

        st.write("공백 포함 본문 길이(enter로 반영)", len(text))

    elif input_mode == "직접 입력":
        text = st.text_area("뉴스 본문을 입력하세요", placeholder="여기에 본문을 직접 입력하세요", height=300)
        st.write("공백 포함 본문 길이(ctrl+enter로 반영)", len(text))

    if text.strip():
        lang = detect_language(text)
        st.write("감지된 언어: ", lang)
    else:
        lang = "unknown"

    if 0 < len(text) < 100:
        st.warning("입력 길이가 너무 짧습니다 (권장 길이: 100~1000자)")


    length_option = st.radio(
        "요약문 길이를 선택하세요",
        ("짧게 (약 100~300자)", "중간 (약 200~400자)", "길게 (약 400~600자)"),
        horizontal=True
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
                if summary == "error1":
                    st.error("언어 감지에 실패하였습니다 (지원 언어: 영어, 한국어)")
                elif summary == "error2":
                    st.error("지원하는 언어가 아닙니다 (지원 언어: 영어, 한국어)")
                else:
                    st.success("✅ 생성 완료 !")
                    st.write(title)
                    st.write(summary)
                    st.write("공백 포함 요약문 길이", len(summary))
