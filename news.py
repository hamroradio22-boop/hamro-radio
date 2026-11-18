
import feedparser
import json
import re
import html
from datetime import datetime
from zoneinfo import ZoneInfo

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

NEWS_FEEDS = [
    {"url": "https://www.onlinekhabar.com/feed", "region": "नेपाल"},
    {"url": "https://www.setopati.com/feed", "region": "नेपाल"},
    {"url": "https://www.ratopati.com/feed", "region": "नेपाल"},
    {"url": "https://khabarhub.com/feed/", "region": "नेपाल"},
    {"url": "https://www.lokaantar.com/feed/", "region": "नेपाल"},
    {"url": "https://nepalsamaya.com/feed", "region": "नेपाल"},
    {"url": "https://kendrabindu.com/feed", "region": "नेपाल"},
    {"url": "https://arthasarokar.com/feed", "region": "नेपाल"},
    {"url": "https://rajdhanidaily.com/feed", "region": "नेपाल"},
    {"url": "https://newsofnepal.com/feed", "region": "नेपाल"},
    {"url": "https://techmandu.com/feed", "region": "नेपाल"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "region": "विश्व"},
    {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "region": "विश्व"}
]

TOPIC_KEYWORDS = {
    "खेलकुद": [
        "cricket", "football", "sport", "match", "player",
        "tournament", "खेल", "क्रिकेट", "फुटबल", "खेलकुद",
        "खेलाडी", "विश्वकप", "गोल"
    ],
    "मौसम": [
        "weather", "forecast", "rain", "storm", "flood",
        "temperature", "climate", "मौसम", "वर्षा", "बाढी",
        "पहिरो", "हिमपात", "तापक्रम"
    ],
    "प्रविधि": [
        "technology", "tech", "ai", "artificial intelligence",
        "computer", "mobile", "internet", "software",
        "technology", "प्रविधि", "मोबाइल", "इन्टरनेट",
        "कृत्रिम बुद्धिमत्ता", "सफ्टवेयर"
    ],
    "अर्थतन्त्र": [
        "economy", "economic", "business", "market", "bank",
        "finance", "investment", "stock", "price", "trade",
        "अर्थतन्त्र", "अर्थव्यवस्था", "व्यापार", "बैंक",
        "बजार", "लगानी", "सेयर", "मूल्य", "आर्थिक"
    ],
    "राजनीति": [
        "politics", "political", "government", "minister",
        "election", "parliament", "party", "president",
        "राजनीति", "सरकार", "मन्त्री", "निर्वाचन",
        "संसद", "दल", "राष्ट्रपति", "प्रधानमन्त्री"
    ]
}


def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def classify_news(title, summary):
    text = (title + " " + summary).lower()

    for category, keywords in TOPIC_KEYWORDS.items():
        if any(word in text for word in keywords):
            return category

    return "अन्य"


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
                    "region": source["region"],
                    "category": classify_news(title, summary),
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

    for category in [
        "राजनीति", "अर्थतन्त्र", "प्रविधि",
        "खेलकुद", "मौसम", "अन्य"
    ]:
        count = sum(
            1 for item in news
            if item["category"] == category
        )
        print(category, ":", count)

    print("=================================")
    return news


if __name__ == "__main__":
    save_news()
