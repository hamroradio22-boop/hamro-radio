
import feedparser
import json
from datetime import datetime
from zoneinfo import ZoneInfo

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

NEWS_FEEDS = [
    "https://www.onlinekhabar.com/feed",
    "https://www.setopati.com/feed",
]

def get_news():
    all_news = []

    for url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", "").strip()

                if title and link:
                    all_news.append({
                        "title": title,
                        "summary": summary,
                        "link": link
                    })

        except Exception as error:
            print("News error:", error)

    return all_news

def save_news():
    news = get_news()

    data = {
        "radio": "Hamro Radio",
        "updated": datetime.now(NEPAL_TZ).isoformat(),
        "total_news": len(news),
        "news": news
    }

    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("Total news collected:", len(news))

    return news

if __name__ == "__main__":
    save_news()
