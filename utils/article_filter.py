def filter_condition(article, lang, topic):
    # 언어 필터 적용
    if lang is None or lang == article.get("lang"):
        lang_filter = True
    else:
        lang_filter = False
    # 분야 필터 적용
    if topic == "전체" or topic == article.get("topic"):
        topic_filter = True
    else:
        topic_filter = False

    return lang_filter and topic_filter
