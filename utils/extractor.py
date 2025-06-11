from newspaper import Article
from newspaper.article import ArticleException

def extract_article_text(url: str) -> str:
    """
    뉴스 URL에서 본문을 추출하는 함수
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except ArticleException:
        raise ValueError("url 형식을 다시 확인해 주세요")