import streamlit as st
from components.related_news_component import suggest_related_news

def run():
    st.title("📝 관련 기사 제안 Demo")

    if st.button("Generate", key="related button"):
        suggest_related_news()

