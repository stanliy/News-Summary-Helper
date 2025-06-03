from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import pytz
import time
import json

CATEGORY_LIST = ["정치", "경제", "사회", "국제", "문화", "스포츠", "과학·환경"]


def dedup_preserve_order(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def collect_khan_news_10_years_ago(keyword="", page_count=1):
    kr_tz = pytz.timezone("Asia/Seoul")
    now_kr = datetime.now(kr_tz)
    try:
        target_date = now_kr.replace(year=now_kr.year - 10)
    except ValueError:
        target_date = now_kr.replace(month=2, day=28, year=now_kr.year - 10)

    target_str = target_date.strftime("%Y-%m-%d")
    urls = []

    service = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    for page in range(1, page_count + 1):
        search_url = (
            f"https://search.khan.co.kr/?q={keyword}"
            f"&media=khan&section=0&term=5"
            f"&startDate={target_str}&endDate={target_str}"
            f"&page={page}&sort=0"
        )

        print(f"\n🔍 [{keyword}] 검색 날짜: {target_str}")
        print("🌐 URL:", search_url)

        driver.get(search_url)
        time.sleep(2)

        articles = driver.find_elements(By.CSS_SELECTOR, "article a")
        print("📰 기사 수:", len(articles))

        for article in articles:
            link = article.get_attribute('href')
            if link and link.startswith("https://www.khan.co.kr/article/"):
                print("✅ 수집된 링크:", link)
                urls.append(link)

    driver.quit()
    return dedup_preserve_order(urls)


def find_first_article_by_category(driver, urls, target_category):
    for idx, url in enumerate(urls, 1):
        print(f"\n🔎 ({idx}/{len(urls)}) [{target_category}] 기사 확인 중: {url}")
        try:
            driver.get(url)
            time.sleep(1)

            try:
                tag = driver.find_element(By.CSS_SELECTOR, "a.category")
                category = tag.get_attribute("title") or tag.text
            except:
                tag = driver.find_element(By.CSS_SELECTOR, "ul.breadcrumb > li:nth-child(2)")
                category = tag.text.strip()

            category = ' '.join(category.strip().split())
            print(f"✅ [{category}] {url}")

            if category == target_category:
                print(f"🎯 [{category}] 기사 발견! → {url}")
                return url

        except Exception as e:
            print(f"❌ 확인 실패: {url}\n⛔ {e}")
            continue

    return None


def find_articles_for_all_categories(page_count=1):
    results = {}

    CATEGORY_KEYWORD_MAP = {
        "정치": "정치",
        "경제": "경제",
        "사회": "사회",
        "국제": "국제",
        "문화": "문화",
        "스포츠": "축구",
        "과학·환경": "환경",  # ✅ 검색 키워드만 바꿈
    }

    # ✅ 날짜 계산 (10년 전 오늘)
    kr_tz = pytz.timezone("Asia/Seoul")
    now_kr = datetime.now(kr_tz)
    try:
        target_date = now_kr.replace(year=now_kr.year - 10)
    except ValueError:
        target_date = now_kr.replace(month=2, day=28, year=now_kr.year - 10)
    target_str = target_date.strftime("%Y-%m-%d")

    # ✅ 크롬 드라이버 실행
    service = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for category, keyword in CATEGORY_KEYWORD_MAP.items():
            urls = collect_khan_news_10_years_ago(keyword=keyword, page_count=page_count)
            url = find_first_article_by_category(driver, urls, target_category=category)
            results[category] = {
                "url": url,
                "date": target_str
            } if url else None
    finally:
        driver.quit()

    return results


if __name__ == "__main__":
    final_results = find_articles_for_all_categories(page_count=2)
    
    with open("final_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print("\n📌 분야별 대표 기사:")
    for cat, url in final_results.items():
        print(f"{cat}: {url if url else '❌ 없음'}")