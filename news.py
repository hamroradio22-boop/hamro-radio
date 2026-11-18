
import feedparser
import json
import re
import html
import calendar
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

# कति समयभित्र प्रकाशित समाचार मात्र लिने?
MAX_NEWS_AGE_HOURS = 48

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
    {"url": "https://www.thehimalayantimes.com/rssFeed/31", "region": "नेपाल"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "region": "विश्व"},
    {"url": "https://feeds.bbci.co.uk/sport/rss.xml", "region": "विश्व"}
]

KEYWORDS = {
    "राजनीति": [
        "politics", "political", "government", "minister",
        "election", "parliament", "president", "prime minister",
        "opposition", "coalition", "cabinet", "sanctions",
        "diplomatic", "diplomacy", "foreign policy",
        "war", "military", "army", "ceasefire", "invasion",
        "airstrike", "missile", "attack", "geopolitical",
        "trump", "putin", "zelensky", "israel", "palestinian",
        "ukraine", "russia", "iran", "china", "settlements",
        "ट्रम्प", "पुटिन", "जेलेन्स्की",
        "राजनीति", "राजनीतिक", "सरकार", "मन्त्री",
        "निर्वाचन", "चुनाव", "संसद", "राष्ट्रपति",
        "प्रधानमन्त्री", "ओली", "देउवा", "प्रचण्ड",
        "एमाले", "कांग्रेस", "माओवादी", "विपक्षी",
        "सभामुख", "प्रदेशसभा", "सांसद", "प्रतिबन्ध",
        "कूटनीति", "युद्ध", "सेना", "आक्रमण",
        "इजरायल", "प्यालेस्टाइन", "युक्रेन", "रुस",
        "अमेरिका", "चीन", "भारत", "फिलिपिन्स",
        "सहकार्य", "सम्झौता"
    ],

    "अर्थतन्त्र": [
        "economy", "economic", "business", "market",
        "sales", "soaring sales", "revenue", "earnings",
        "company profits", "profit", "loss", "investment",
        "investor", "stock market", "share market",
        "stock exchange", "share price", "inflation",
        "interest rate", "central bank", "banking",
        "finance", "budget", "tax", "customs",
        "remittance", "export", "imports", "trade",
        "अर्थतन्त्र", "अर्थव्यवस्था", "आर्थिक",
        "आर्थिक वृद्धि", "मुद्रास्फीति", "ब्याजदर",
        "सेयर बजार", "सेयर मूल्य", "लगानी",
        "लगानीकर्ता", "बैंक", "वित्तीय", "बजेट",
        "राजस्व", "कर", "भन्सार", "रेमिट्यान्स",
        "नाफा", "घाटा", "बिक्री", "व्यापार",
        "आम्दानी", "कम्पनीको कारोबार"
    ],

    "प्रविधि": [
        "technology", "tech", "artificial intelligence",
        "software", "smartphone", "mobile phone",
        "internet", "computer", "electric vehicle",
        "robot", "semiconductor", "chip technology",
        "cybersecurity", "intelligent driving",
        "autonomous driving", "driver assistance",
        "self-driving", "driving system",
        "प्रविधि", "कृत्रिम बुद्धिमत्ता", "सफ्टवेयर",
        "मोबाइल", "इन्टरनेट", "कम्प्युटर",
        "विद्युतीय गाडी", "इलेक्ट्रिक कार",
        "एआई", "रोबोट", "चिप प्रविधि",
        "इन्टेलिजेन्ट ड्राइभिङ", "स्वचालित ड्राइभिङ"
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
        "monsoon", "meteorological", "thunderstorm",
        "मौसम", "वर्षा", "बाढी", "पहिरो",
        "हिमपात", "तापक्रम", "हावाहुरी",
        "चक्रवात", "शीतलहर", "गर्मी",
        "मनसुन", "मौसम पूर्वानुमान"
    ]
}

POLITICAL_CONTEXT = [
    "sanctions", "war", "military", "ceasefire",
    "invasion", "airstrike", "missile", "attack",
    "shot dead", "killed", "shooting", "settlements",
    "foreign policy", "diplomatic", "trump", "putin",
    "zelensky", "israel", "palestinian", "ukraine",
    "russia", "iran", "ट्रम्प", "पुटिन",
    "युद्ध", "आक्रमण", "प्रतिबन्ध", "हत्या",
    "गोली", "इजरायल", "प्यालेस्टाइन",
    "युक्रेन", "रुस", "कूटनीति"
]


def clean_text(text):
    text = str(text or "")

    for _ in range(3):
        text = html.unescape(text)

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_published_date(entry):
    """
    RSS बाट प्रकाशित मिति निकाल्ने।
    प्रकाशित मिति नभए अपडेट मिति प्रयोग गर्ने।
    """

    date_value = (
        entry.get("published_parsed")
        or entry.get("updated_parsed")
    )

    if not date_value:
        return None

    try:
        timestamp = calendar.timegm(date_value)
        published = datetime.fromtimestamp(
            timestamp,
            timezone.utc
        )

        return published.astimezone(NEPAL_TZ)

    except (ValueError, TypeError, OverflowError):
        return None


def has_keyword(text, keyword):
    keyword = keyword.lower()

    if re.fullmatch(r"[a-zA-Z0-9 ]+", keyword):
        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(keyword)
            + r"(?![a-zA-Z0-9])"
        )

        return re.search(
            pattern,
            text,
            re.IGNORECASE
        ) is not None

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

    if "feeds.bbci.co.uk/sport/" in url:
        return "खेलकुद"

    if "techmandu.com" in url:
        return "प्रविधि"

    political = count_keywords(
        title,
        KEYWORDS["राजनीति"]
    )

    political_context = count_keywords(
        title,
        POLITICAL_CONTEXT
    )

    economy = count_keywords(
        title,
        KEYWORDS["अर्थतन्त्र"]
    )

    technology = count_keywords(
        title,
        KEYWORDS["प्रविधि"]
    )

    sports = count_keywords(
        title,
        KEYWORDS["खेलकुद"]
    )

    weather = count_keywords(
        title,
        KEYWORDS["मौसम"]
    )

    if political_context > 0 or political > 0:
        return "राजनीति"

    if economy > 0:
        return "अर्थतन्त्र"

    if technology > 0:
        return "प्रविधि"

    if sports > 0:
        return "खेलकुद"

    if weather > 0:
        return "मौसम"

    full_text = title + " " + summary

    for category in [
        "राजनीति",
        "अर्थतन्त्र",
        "प्रविधि",
        "खेलकुद",
        "मौसम"
    ]:
        if count_keywords(
            full_text,
            KEYWORDS[category]
        ) >= 2:
            return category

    return "अन्य"


def get_news():

    all_news = []
    seen = set()

    now = datetime.now(NEPAL_TZ)

    cutoff = now - timedelta(
        hours=MAX_NEWS_AGE_HOURS
    )

    old_count = 0
    undated_count = 0
    error_count = 0

    for source in NEWS_FEEDS:

        try:
            feed = feedparser.parse(source["url"])

            if feed.bozo and not feed.entries:
                print("Feed error:", source["url"])
                error_count += 1
                continue

            if not feed.entries:
                print("No news:", source["url"])
                continue

            for entry in feed.entries[:30]:

                title = clean_text(
                    entry.get("title", "")
                )

                link = entry.get("link", "").strip()

                summary = clean_text(
                    entry.get("summary", "")
                    or entry.get("description", "")
                )

                if not title or not link:
                    continue

                # प्रकाशित मिति जाँच
                published = get_published_date(entry)

                if published is None:
                    undated_count += 1
                    continue

                # ४८ घण्टाभन्दा पुरानो समाचार हटाउने
                if published < cutoff:
                    old_count += 1
                    continue

                # भविष्यको मिति भएको समाचार हटाउने
                if published > now + timedelta(hours=1):
                    continue

                # दोहोरिएको समाचार हटाउने
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
                    "source": feed.feed.get(
                        "title",
                        "News"
                    ),
                    "published": published.isoformat()
                })

        except Exception as error:
            print(
                "News error:",
                source["url"],
                error
            )

            error_count += 1

    # नयाँ प्रकाशित समाचार पहिले
    all_news.sort(
        key=lambda item: item["published"],
        reverse=True
    )

    print("\n========== FILTER REPORT ==========")
    print("पुराना समाचार हटाइयो:", old_count)
    print("मिति नभएका समाचार हटाइयो:", undated_count)
    print("Feed समस्या:", error_count)
    print("४८ घण्टाभित्रका समाचार:", len(all_news))
    print("===================================")

    return all_news


def save_news():

    news = get_news()

    data = {
        "radio": "Hamro Radio",
        "updated": datetime.now(
            NEPAL_TZ
        ).isoformat(),
        "total_news": len(news),
        "news": news
    }

    with open(
        "news.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n========== NEWS REPORT ==========")
    print("Total news collected:", len(news))

    for category in [
        "राजनीति",
        "अर्थतन्त्र",
        "प्रविधि",
        "खेलकुद",
        "मौसम",
        "अन्य"
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
