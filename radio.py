
from datetime import datetime
from zoneinfo import ZoneInfo

from news import get_news
from special_days import get_special_day
from nepali_calendar import get_calendar_info

TZ = ZoneInfo("Asia/Kathmandu")

def main():
    now = datetime.now(TZ)

    print("========== HAMRO RADIO ==========")
    print("नेपाल समय:", now.strftime("%I:%M %p"))

    calendar = get_calendar_info()
    special = get_special_day()

    print("आजको बार:", calendar["nepali_day"])
    print("अंग्रेजी मिति:", calendar["english_date"])
    print("आजको विशेष दिवस:", special["special_day"])

    news = get_news()

    print("\nजम्मा समाचार संख्या:", len(news))

    categories = ["नेपाल", "विश्व", "खेलकुद"]

    for category in categories:
        category_news = [
            item for item in news
            if item.get("category") == category
        ]

        print("\n==========", category, "समाचार ==========")
        print("समाचार संख्या:", len(category_news))

        if category_news:
            for item in category_news[:5]:
                print("-", item["title"])
                print("समाचार लिंक:", item["link"])
        else:
            print("अहिले समाचार उपलब्ध छैन।")

    print("\nHamro Radio को घण्टे अपडेट पूरा भयो।")
    print("================================")

if __name__ == "__main__":
    main()
