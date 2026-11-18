
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
    value = html.unescape(str(value or ""))
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def main():
    now = datetime.now(TZ)
    calendar = get_calendar_info()
    special = get_special_day()
    news = get_news()

    bulletin = []

    bulletin.append("नमस्कार, Hamro Radio मा स्वागत छ।")
    bulletin.append("अब सुन्नुहोस् आजका प्रमुख समाचार।")
    bulletin.append("")
    bulletin.append("नेपाल समय: " + now.strftime("%I:%M %p"))
    bulletin.append("आजको बार: " + calendar["nepali_day"])
    bulletin.append("अंग्रेजी मिति: " + calendar["english_date"])
    bulletin.append("आजको विशेष दिवस: " + special["special_day"])
    bulletin.append("")

    for category in CATEGORIES:
        category_news = [
            item for item in news
            if item.get("category") == category
        ]

        bulletin.append("अब " + category + " समाचार।")

        if category_news:
            for index, item in enumerate(category_news[:5], 1):
                title = clean_text(item.get("title"))
                summary = clean_text(
                    item.get("summary") or item.get("description")
                )

                bulletin.append(f"समाचार {index}: {title}")

                if summary and summary != title:
                    bulletin.append(summary[:400])

                bulletin.append("")
        else:
            bulletin.append("यस शीर्षकका समाचार अहिले उपलब्ध छैनन्।")
            bulletin.append("")

    bulletin.append("यी थिए Hamro Radio का आजका समाचार।")
    bulletin.append("थप समाचारका लागि हामीसँगै रहनुहोस्।")
    bulletin.append("धन्यवाद।")

    output = "\n".join(bulletin)

    with open("bulletin.txt", "w", encoding="utf-8") as file:
        file.write(output)

    print("\n========== HAMRO RADIO BULLETIN ==========")
    print(output)
    print("\nबुलेटिन फाइल तयार भयो: bulletin.txt")
    print("==========================================")

if __name__ == "__main__":
    main()
