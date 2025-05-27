from newspaper import Article, ArticleException

def extract_article_text(url: str) -> str:
    """
    주어진 뉴스 기사 URL에서 본문 텍스트를 추출합니다.
    
    Args:
        url: 뉴스 기사 페이지의 URL 문자열.
    
    Returns:
        추출된 뉴스 기사 본문 텍스트.
    
    Raises:
        ValueError: URL 형식이 올바르지 않거나 기사 본문을 추출할 수 없는 경우 발생합니다.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        raise ValueError("url 형식을 다시 확인해 주세요")