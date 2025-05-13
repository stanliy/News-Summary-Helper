from newspaper import Article

def extract_article_text(url: str) -> str:
    """
    뉴스 URL에서 본문을 추출하는 함수
    """
    article = Article(url)
    article.download()
    article.parse()
    return article.text
