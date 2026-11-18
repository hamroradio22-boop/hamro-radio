
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

KEYWORDS = {
    "राजनीति": [
        "politics", "political", "government", "minister",
        "election", "parliament", "president", "prime minister",
        "party", "opposition", "coalition", "cabinet",
        "राजनीति", "राजनीतिक", "सरकार", "मन्त्री",
        "निर्वाचन", "चुनाव", "संसद", "राष्ट्रपति",
        "प्रधानमन्त्री", "ओली", "देउवा", "प्रचण्ड",
        "एमाले", "कांग्रेस", "माओवादी", "विपक्षी",
        "सभामुख", "प्रदेशसभा", "सांसद"
    ],
    "अर्थतन्त्र": [
        "economy", "economic", "business", "market",
        "bank", "finance", "investment", "stock",
        "inflation", "budget", "trade", "company",
        "अर्थतन्त्र", "अर्थव्यवस्था", "आर्थिक",
        "व्यापार", "बैंक", "लगानी", "सेयर",
        "बजेट", "महँगी", "मुद्रास्फीति", "राजस्व",
        "भन्सार", "उद्योग", "व्यवसाय"
    ],
    "प्रविधि": [
        "technology", "tech", "artificial intelligence",
        "software", "smartphone", "mobile", "internet",
        "computer", "electric vehicle", "robot",
        "प्रविधि", "कृत्रिम बुद्धिमत्ता", "सफ्टवेयर",
        "मोबाइल", "इन्टरनेट", "कम्प्युटर",
        "विद्युतीय गाडी", "इलेक्ट्रिक कार", "एआई"
    ],
    "खेलकुद": [
        "cricket", "football", "sport", "sports",
        "match", "tournament", "player", "goal",
        "tennis", "olympic", "world cup",
        "खेलकुद", "खेलाडी", "क्रिकेट", "फुटबल",
        "विश्वकप", "गोल", "प्रतियोगिता", "टुर्नामेन्ट"
    ],
    "मौसम": [
        "weather", "forecast", "rainfall", "rain",
        "storm", "flood", "temperature", "snowfall",
        "cyclone", "heatwave", "landslide",
        "मौसम", "वर्षा", "बाढी", "पहिरो",
        "हिमपात", "तापक्रम", "हावाहुरी",
        "चक्रवात", "शीतलहर", "गर्मी"
    ]
}


def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def has_keyword(text, keyword):
    if re.fullmatch(r"[a-zA-Z0-9 ]+", keyword):
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(keyword) + r"(?![a-zA-Z0-9])"
        return re.search(pattern, text, re.IGNORECASE) is not None

    return keyword.lower() in text.lower()


def classify_news(title, summary, source_url):
    text = (title + " " + summary).lower()
    url = source_url.lower()

    # स्रोतअनुसार निश्चित वर्ग
    if "feeds.bbci.co.uk/sport/" in url:
        return "खेलकुद"

    if "techmandu.com" in url:
        return "प्रविधि"

    # शीर्षक र विवरणका शब्दअनुसार वर्गीकरण
    for category in [
        "राजनीति",
        "अर्थतन्त्र",
        "प्रविधि",
        "खेलकुद",
        "मौसम"
    ]:
        if any(
            has_keyword(text, word)
            for word in KEYWORDS[category]
        ):
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

                category = classify_news(
                    title,
                    summary,
                    source["url"]
                )

                all_news.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "region": source["region"],
                    "category": category,
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
