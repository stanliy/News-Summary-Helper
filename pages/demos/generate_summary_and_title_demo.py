import streamlit as st
from utils.summaryNewsTest import summary_news        # 요약문 생성
from utils.summaryNewsTest import decide_summary_len  # 요약문 길이 설정
from utils.generateTitleTest import generate_title    # 제목 생성
from langdetect import detect, LangDetectException    # 언어 감지


def run():
    st.title("📝 본문 요약문 및 제목 생성 Demo")

    # TODO: 현재 본문 수동 입력 -> 추후 본문 추출 함수 사용으로 교체 예정
    text = st.text_area("뉴스 본문을 입력하세요", height=300)

    # TODO: 임시 언어 감지 -> 추후 분리된 언어 감지 함수 사용으로 교체 예정
    try:
        lang = detect(text)      # 입력된 언어 감지
    except LangDetectException:  # 언어 감지 실패 (너무 짧은 입력 or 지원언어 아님)
        lang = None

    st.write("공백 포함 본문 길이(ctrl+enter로 반영)", len(text))
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
