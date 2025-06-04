import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.connection import get_correct_time, selectDB

def step1(title, category):
    """
    주어진 제목과 주제를 기반으로 관련 뉴스 기사를 TF-IDF 유사도로 검색합니다.
    
    Args:
        title (str): 기준이 될 기사 제목
        category (str): 검색할 기사 카테고리
        
    Returns:
        list: 유사도 순으로 정렬된 상위 5개 관련 기사 리스트
    """

    # ✅ 예시 기사 리스트 (딕셔너리 리스트)
    sql = "SELECT * FROM related_news where DATE = '" + get_correct_time() + "' AND category = '" + category + "';"
    # sql = "SELECT * FROM related_news where DATE = '2025-06-02' AND category = '" + category + "';"
    articles = selectDB(sql)

    if not articles:
        return []
    
    # ✅ 기사 본문 리스트 만들기 (content 기준)
    article_contents = [article['content'] for article in articles]

    # ✅ TF-IDF 벡터화
    vectorizer = TfidfVectorizer(max_features=5000)
    article_vectors = vectorizer.fit_transform(article_contents)

    # ✅ 사용자 쿼리
    query_text = title
    query_vector = vectorizer.transform([query_text])

    # ✅ 유사도 계산
    similarities = cosine_similarity(query_vector, article_vectors)[0]
    top_n_idx = np.argsort(similarities)[::-1][:5]
    
    # ✅ 결과 수집
    result = []
    for idx in top_n_idx:
        article = articles[idx]
        result.append(article)
    return result
