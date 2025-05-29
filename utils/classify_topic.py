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
