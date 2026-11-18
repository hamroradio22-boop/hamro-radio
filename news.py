
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
        "opposition", "coalition", "cabinet", "senate",
        "sanctions", "diplomatic", "diplomacy", "foreign policy",
        "war", "military", "army", "ceasefire", "invasion",
        "airstrike", "missile", "attack", "geopolitical",
        "trump", "putin", "zelensky", "israel", "palestinian",
        "ukraine", "russia", "iran", "china", "settlements",
        "राजनीति", "राजनीतिक", "सरकार", "मन्त्री",
        "निर्वाचन", "चुनाव", "संसद", "राष्ट्रपति",
        "प्रधानमन्त्री", "ओली", "देउवा", "प्रचण्ड",
        "एमाले", "कांग्रेस", "माओवादी", "विपक्षी",
        "सभामुख", "प्रदेशसभा", "सांसद", "प्रतिबन्ध",
        "कूटनीति", "युद्ध", "सेना", "आक्रमण",
        "इजरायल", "प्यालेस्टाइन", "युक्रेन", "रुस",
        "अमेरिका", "चीन", "भारत"
    ],

    "अर्थतन्त्र": [
        "economy", "economic growth", "inflation",
        "interest rate", "stock market", "share market",
        "stock exchange", "share price", "market price",
        "central bank", "monetary policy", "fiscal policy",
        "gross domestic product", "gdp", "revenue",
        "profit", "loss", "investment", "investor",
        "banking", "bank", "finance", "budget",
        "tax", "customs", "remittance", "tourism revenue",
        "export earnings", "import bill",
        "अर्थतन्त्र", "अर्थव्यवस्था", "आर्थिक वृद्धि",
        "मुद्रास्फीति", "ब्याजदर", "सेयर बजार",
        "सेयर मूल्य", "लगानी", "लगानीकर्ता",
        "बैंक", "वित्तीय", "बजेट", "राजस्व",
        "कर", "भन्सार", "रेमिट्यान्स", "नाफा",
        "घाटा", "आर्थिक"
    ],

    "प्रविधि": [
        "technology", "artificial intelligence",
        "software", "smartphone", "mobile phone",
        "internet", "computer", "electric vehicle",
        "robot", "semiconductor", "chip technology",
        "cybersecurity", "app launch", "digital technology",
        "प्रविधि", "कृत्रिम बुद्धिमत्ता", "सफ्टवेयर",
        "मोबाइल", "इन्टरनेट", "कम्प्युटर",
        "विद्युतीय गाडी", "इलेक्ट्रिक कार",
        "एआई", "रोबोट", "चिप प्रविधि"
    ],

    "खेलकुद": [
        "cricket", "football", "sports", "sport",
        "tournament", "player", "goal", "tennis",
        "olympic", "world cup", "league", "coach",
        "खेलकुद", "खेलाडी", "क्रिकेट", "फुटबल",
        "विश्वकप", "गोल", "प्रतियोगिता",
        "टुर्नामेन्ट", "खेल"
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

# यी शब्दले अन्तर्राष्ट्रिय/राजनीतिक विषयको संकेत गर्छन्।
POLITICAL_CONTEXT = [
    "sanctions", "war", "military", "ceasefire",
    "invasion", "airstrike", "missile", "attack",
    "shot dead", "killed", "shooting", "settlements",
    "government investigation", "foreign policy",
    "diplomatic", "trump", "putin", "zelensky",
    "israel", "palestinian", "ukraine", "russia",
    "iran", "युद्ध", "आक्रमण", "प्रतिबन्ध",
    "हत्या", "गोली", "इजरायल", "प्यालेस्टाइन",
    "युक्रेन", "रुस"
]


def clean_text(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def has_keyword(text, keyword):
    keyword = keyword.lower()

    if re.fullmatch(r"[a-zA-Z0-9 ]+", keyword):
        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(keyword)
            + r"(?![a-zA-Z0-9])"
        )
        return re.search(pattern, text, re.IGNORECASE) is not None

    return keyword in text.lower()


def count_keywords(text, keywords):
    return sum(
        1 for word in keywords
        if has_keyword(text, word)
    )


def classify_news(title, summary, source_url):
    title = title.lower()
    summary = summary.lower()
    url = source_url.lower()

    # निश्चित स्रोतका वर्ग
    if "feeds.bbci.co.uk/sport/" in url:
        return "खेलकुद"

    if "techmandu.com" in url:
        return "प्रविधि"

    # शीर्षकलाई बढी महत्त्व दिने
    political_title = count_keywords(
        title, KEYWORDS["राजनीति"]
    )

    political_summary = count_keywords(
        summary, KEYWORDS["राजनीति"]
    )

    economy_title = count_keywords(
        title, KEYWORDS["अर्थतन्त्र"]
    )

    economy_summary = count_keywords(
        summary, KEYWORDS["अर्थतन्त्र"]
    )

    political_context = count_keywords(
        title, POLITICAL_CONTEXT
    )

    tech_title = count_keywords(
        title, KEYWORDS["प्रविधि"]
    )

    sports_title = count_keywords(
        title, KEYWORDS["खेलकुद"]
    )

    weather_title = count_keywords(
        title, KEYWORDS["मौसम"]
    )

    # राजनीति र अन्तर्राष्ट्रिय घटनालाई प्राथमिकता
    if political_context > 0:
        return "राजनीति"

    if political_title > 0 and political_title >= economy_title:
        return "राजनीति"

    # अर्थतन्त्रका स्पष्ट संकेत भएमा मात्र अर्थतन्त्र
    if economy_title >= 1:
        return "अर्थतन्त्र"

    if economy_summary >= 2 and political_title == 0:
        return "अर्थतन्त्र"

    # अन्य विषय
    if tech_title > 0:
        return "प्रविधि"

    if sports_title > 0:
        return "खेलकुद"

    if weather_title > 0:
        return "मौसम"

    # विवरणमा भएका संकेत
    full_text = title + " " + summary

    for category in [
        "राजनीति", "अर्थतन्त्र",
        "प्रविधि", "खेलकुद", "मौसम"
    ]:
        if count_keywords(full_text, KEYWORDS[category]) >= 2:
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

                key = re.sub(
                    r"[^a-z0-9]",
                    "",
                    title.lower()
                )

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
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

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
