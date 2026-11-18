
import re
import html
from datetime import datetime
from zoneinfo import ZoneInfo

from news import get_news
from special_days import get_special_day
from nepali_calendar import get_calendar_info

TZ = ZoneInfo("Asia/Kathmandu")

CATEGORIES = [
    "राजनीति",
    "अर्थतन्त्र",
    "प्रविधि",
    "खेलकुद",
    "मौसम",
    "अन्य"
]


def clean_text(value):
    value = str(value or "")

    # HTML entity सफा गर्ने
    for _ in range(3):
        value = html.unescape(value)

    # HTML tag हटाउने
    value = re.sub(r"<[^>]+>", "", value)

    # अधुरो लेखका संकेत हटाउने
    value = re.sub(
        r"\[\s*(?:…|\.{3})\s*\]",
        "",
        value
    )

    # HTML बाँकी संकेत हटाउने
    value = re.sub(r"&#\d+;|&[a-zA-Z]+;", "", value)

    # खाली ठाउँ मिलाउने
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def create_bulletin(news, calendar, special, now):

    bulletin = []

    bulletin.append("नमस्कार, Hamro Radio मा स्वागत छ।")
    bulletin.append("अब सुन्नुहोस् आजका प्रमुख समाचार।")
    bulletin.append("")

    bulletin.append("नेपाल समय: " + now.strftime("%I:%M %p"))
    bulletin.append("आजको बार: " + calendar["nepali_day"])
    bulletin.append("अंग्रेजी मिति: " + calendar["english_date"])
    bulletin.append("आजको विशेष दिवस: " + special["special_day"])
    bulletin.append("")

    bulletin.append("आज प्राप्त समाचार संख्या: " + str(len(news)))
    bulletin.append("")

    for category in CATEGORIES:

        category_news = [
            item for item in news
            if item.get("category") == category
        ]

        bulletin.append("अब " + category + " समाचार।")
        bulletin.append("")

        if category_news:

            for index, item in enumerate(category_news[:5], 1):

                title = clean_text(item.get("title"))

                summary = clean_text(
                    item.get("summary")
                    or item.get("description")
                )

                if not title:
                    continue

                bulletin.append(
                    f"समाचार {index}: {title}"
                )

                if summary and summary != title:

                    # विवरण धेरै लामो भए छोट्याउने
                    summary = summary[:400].strip()

                    bulletin.append(summary)

                bulletin.append("")

        else:
            bulletin.append(
                "यस शीर्षकका समाचार अहिले उपलब्ध छैनन्।"
            )
            bulletin.append("")

    bulletin.append("यी थिए Hamro Radio का आजका समाचार।")
    bulletin.append("थप समाचारका लागि हामीसँगै रहनुहोस्।")
    bulletin.append("धन्यवाद।")

    return "\n".join(bulletin)


def main():

    now = datetime.now(TZ)

    print("========== HAMRO RADIO ==========")

    calendar = get_calendar_info()
    special = get_special_day()

    print("नेपाल समय:", now.strftime("%I:%M %p"))
    print("आजको बार:", calendar["nepali_day"])
    print("अंग्रेजी मिति:", calendar["english_date"])
    print("आजको विशेष दिवस:", special["special_day"])

    news = get_news()

    print("\nजम्मा समाचार संख्या:", len(news))

    bulletin = create_bulletin(
        news,
        calendar,
        special,
        now
    )

    # TXT फाइलमा सुरक्षित गर्ने
    with open(
        "bulletin.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(bulletin)

    # GitHub Actions मा देखाउने
    print("\n========== HAMRO RADIO BULLETIN ==========")
    print(bulletin)

    print("\nबुलेटिन फाइल तयार भयो: bulletin.txt")
    print("==========================================")


if __name__ == "__main__":
    main()
