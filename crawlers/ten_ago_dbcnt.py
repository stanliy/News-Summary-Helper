import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from CLI.extractor import extract_article_text
from CLI.language import detect_language
from CLI.korean import summarize_korean, generate_korean_headline
from CLI.english import summarize_bart_pipeline, generate_english_headline
from CLI.model_loader import insert_summary_to_mysql

def process_final_results(json_path="final_results.json"):
    """
    final_results.json 파일을 불러와 기사 요약, 제목 생성, DB 저장 수행
    """
    with open(json_path, "r", encoding="utf-8") as f:
        final_results = json.load(f)

    for category, info in final_results.items():
        if not info:
            continue

        url = info["url"]
        article_date = info["date"]

        try:
            print(f"\n📥 [{category}] 기사 처리 중: {url}")

            # 1. 본문 추출
            text = extract_article_text(url)

            # 2. 언어 감지
            lang = detect_language(text)
            print(f"🌐 감지된 언어: {lang}")

            # 3. 요약 및 제목 생성
            if lang == "ko":
                summary = summarize_korean(text)
                headline = generate_korean_headline(summary)
            elif lang == "en":
                summary = summarize_bart_pipeline(text)
                headline = generate_english_headline(summary)
            else:
                print("⚠️ 한국어/영어 외 기사입니다. 스킵합니다.")
                continue

            print(f"\n📰 제목: {headline}")
            print(f"\n📝 요약: {summary}")

            # 4. DB 저장
            insert_summary_to_mysql(category, url, headline, summary, article_date)
            print(f"✅ [{category}] 저장 완료")

        except Exception as e:
            print(f"❌ [{category}] 처리 중 오류 발생: {e}")


if __name__ == "__main__":
    process_final_results("final_results.json")