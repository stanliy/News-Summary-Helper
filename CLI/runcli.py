from .extractor import extract_article_text
from .language import detect_language
from .korean import summarize_korean, generate_korean_headline
from .english import summarize_bart_pipeline, generate_english_headline

def main():
    url = input("📥 기사 URL을 입력하세요: ").strip()

    try:
        # STEP 1: 본문 추출
        text = extract_article_text(url)
        print("\n✅ [기사 본문 일부 출력]")
        print(text[:500] + "...\n")

        # STEP 2: 언어 감지
        lang = detect_language(text)
        print(f"🌐 감지된 언어: {lang}")

        if lang == "ko":
            print("\n✂️ 한국어 기사 → 요약 중...")
            summary = summarize_korean(text)
            print("\n🧠 제목 생성 중...")
            headline = generate_korean_headline(summary)

            print(f"\n📰 생성된 제목:\n{headline}")
            print(f"\n📝 요약 결과:\n{summary}")

        elif lang == "en":
            print("\n✂️ 영어 기사 → 요약 중...")
            summary = summarize_bart_pipeline(text)
            print("\n🧠 제목 생성 중...")
            headline = generate_english_headline(summary)

            print(f"\n📰 Generated Headline:\n{headline}")
            print(f"\n📝 Summary:\n{summary}")

        else:
            print("⚠️ 현재는 한국어/영어 기사만 지원됩니다.")
            return

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()
