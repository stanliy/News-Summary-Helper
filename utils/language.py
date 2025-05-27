from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    """
    입력된 텍스트의 언어를 감지하여 언어 코드를 반환합니다.
    
    텍스트가 너무 짧거나 지원되지 않는 언어일 경우 None을 반환합니다.
    
    Args:
        text: 언어를 감지할 문자열.
    
    Returns:
        감지된 언어의 코드(예: 'ko', 'en'). 감지에 실패하면 None을 반환합니다.
    """
    try:
        return detect(text)      # 입력된 언어 감지
    except LangDetectException:  # 언어 감지 실패 (너무 짧은 입력 or 지원언어 아님)
        return None

