from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    뉴스 본문의 언어를 감지하는 함수 ('ko', 'en' 등)
    """
    try:
        return detect(text)      # 입력된 언어 감지
    except LangDetectException:  # 언어 감지 실패 (너무 짧은 입력 or 지원언어 아님)
        return None

