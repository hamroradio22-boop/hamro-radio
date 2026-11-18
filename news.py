
import feedparser
import json
import re
import html
from datetime import datetime
from zoneinfo import ZoneInfo

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

NEWS_FEEDS = [
    # नेपाल समाचार
    {"url": "https://www.onlinekhabar.com/feed", "category": "नेपाल"},
    {"url": "https://www.setopati.com/feed", "category": "नेपाल"},
    {"url": "https://www.ratopati.com/feed", "category": "नेपाल"},
    {"url": "https://khabarhub.com/feed/", "category": "नेपाल"},
    {"url": "https://www.lokaantar.com/feed/", "category": "नेपाल"},
    {"url": "https://nepalsamaya.com/feed", "category": "नेपाल"},
    {"url": "https://kendrabindu.com/feed", "category": "नेपाल"},
    {"url": "https://arthasarokar.com/feed", "category": "नेपाल"},
    {"url": "https://rajdhanidaily.com/feed", "category": "नेपाल"},
    {"url": "https://newsofnepal.com/feed", "category": "नेपाल"},
    {"url": "https://techmandu.com/feed", "category": "नेपाल"},

    # विश्व समाचार
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "category": "विश्व"},

    # खेलकुद समाचार
    {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "category": "खेलकुद"}
]


def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def get_news():
    all_news = []
    seen = set()

    for source in NEWS_FEEDS:
        try:
            feed = feedparser.parse(source["url"])

            if feed.bozo and not feed.entries:
                print("Feed error:", source["url"])
                continue

            if not feed.entries:
                print("No news:", source["url"])
                continue

            for entry in feed.entries[:15]:
                title = clean_text(entry.get("title", ""))
                link = entry.get("link", "").strip()
                summary = clean_text(entry.get("summary", ""))

                if not title or not link:
                    continue

                key = re.sub(r"[^a-z0-9]", "", title.lower())

                if key in seen or link in seen:
                    continue

                seen.add(key)
                seen.add(link)

                all_news.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "category": source["category"],
                    "source": feed.feed.get("title", "News")
                })

        except Exception as error:
            print("News error:", source["url"], error)

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

    print("\n========== NEWS REPORT ==========")
    print("Total news collected:", len(news))

    for category in ["नेपाल", "विश्व", "खेलकुद"]:
        count = sum(
            1 for item in news
            if item["category"] == category
        )
        print(category, ":", count)

    print("=================================")

    return news


if __name__ == "__main__":
    save_news()
