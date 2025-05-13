from langdetect import detect

def detect_language(text: str) -> str:
    """
    뉴스 본문의 언어를 감지하는 함수 ('ko', 'en' 등)
    """
    return detect(text)
