from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_classifier():
    try:
        classifier = pipeline("text-classification",
                              model="classla/multilingual-IPTC-news-topic-classifier",
                              device=-1, max_length=512, truncation=True)
    except Exception as e:
        raise RuntimeError(f"분류 모델 로딩에 실패했습니다 : {e}")

    return classifier


def detect_topic(text):
    classifier = load_classifier()
    result = classifier(text)[0]["label"]
    return result


def get_topic():
    topic = ['education', 'human interest', 'society', 'sport', 'crime, law and justice',
             'disaster, accident and emergency incident', 'arts, culture, entertainment and media',
             'politics', 'economy, business and finance', 'lifestyle and leisure', 'science and technology',
             'health', 'labour', 'religion', 'weather', 'environment', 'conflict, war and peace']

    return topic

    # 상세 주제를 한국어 카테고리로 매핑합니다.

    # Args:
    #     topic (str): 분류된 주제 문자열
        
    # Returns:
    #     str: 해당하는 한국어 카테고리 또는 None

def topic_to_category(topic):
    social_topics = {'human interest', 'society', 'crime, law and justice', 'disaster, accident and emergency incident', 'labour', 'religion'}
    culture_topics = {'arts, culture, entertainment and media', 'lifestyle and leisure'}
    science_topics = {'education', 'science and technology', 'health', 'weather', 'environment'}

    if topic == 'economy, business and finance':
        return "경제"
    if topic == 'politics':
        return "정치"
    if topic in social_topics:
        return "사회"
    if topic == 'conflict, war and peace':
        return "국제"
    if topic in culture_topics:
        return "문화"
    if topic == 'sport':
        return "스포츠"
    if topic in science_topics:
        return "과학"
    return none;