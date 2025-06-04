import feedparser
import time, datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.connection import updateDB
from newspaper import Article
from sqlalchemy import text

# 📌 RSS 피드 설정
RSS_FEED = [
    ("https://www.khan.co.kr/rss/rssdata/economy_news.xml", "경제"),
    ("https://www.khan.co.kr/rss/rssdata/politic_news.xml", "정치"),
    ("https://www.khan.co.kr/rss/rssdata/society_news.xml", "사회"),
    ("https://www.khan.co.kr/rss/rssdata/kh_world.xml", "국제"),
    ("https://www.khan.co.kr/rss/rssdata/culture_news.xml", "문화"),
    ("https://www.khan.co.kr/rss/rssdata/kh_sports.xml", "스포츠"),
    ("https://www.khan.co.kr/rss/rssdata/science_news.xml", "과학"),
]

for rss_feed in RSS_FEED:
    # 1️⃣ RSS 피드에서 기사 URL 가져오기
    feed = feedparser.parse(rss_feed[0])
    print("RSS URL:", rss_feed[0])

    print("Feed keys:", feed.keys())  # feed.entries 외에 어떤 키가 있는지 보기
    print("Entries 개수:", len(feed.entries))

    print(f"RSS에서 {len(feed.entries)}개의 기사 발견!")

    # 2️⃣ 각 기사 크롤링
    sqlList = []
    paramList = []
    crawl_count = 10
    if len(feed.entries) < 10:
        crawl_count = len(feed.entries)
    for ii in range(0, crawl_count):
        entry = feed.entries[ii]
        url = entry.link
        print(f"\n[기사 URL] {url}")

        try:
            # newspaper3k 사용
            article = Article(url, language='ko')
            article.download()
            article.parse()


            print(f"제목: {article.title}")
            print(f"분야: {rss_feed[1]}")
            print(f"날짜: {str(article.publish_date)[:10]}")
            print(f"본문 (10자): {article.text[:10]}...")

            # ✅ 여기서 DB 저장 or 파일 저장 가능 (예: CSV, SQLite 등)
            sql = text("""
            INSERT INTO related_news (url, category, title, date, content)
            VALUES (:url, :category, :title, :date, :content)
            """)

            params = {
                "url": entry.link,
                "category": rss_feed[1],
                "title": article.title,
                "date": str(article.publish_date)[:10],
                "content": article.text
            }

            # 금일 기사만 크롤링하도록 필터링
            # if str(article.publish_date)[:10] == str(datetime.datetime.now())[:10]:
            #     print('this is today news')
            sqlList.append(sql)
            paramList.append(params)

        except Exception as e:
            print(f"크롤링 실패: {e}")

        time.sleep(1)  # polite crawling (1초 대기)
    result = updateDB(sqlList, paramList)
    if result['status'] == "success":
        print("done!")