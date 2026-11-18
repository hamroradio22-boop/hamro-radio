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

    print("\nआजका मुख्य समाचार:")

    news = get_news()

    if news:
        for item in news[:5]:
            print("-", item["title"])
            print("समाचार लिंक:", item["link"])
    else:
        print("अहिले समाचार उपलब्ध छैन।")

    print("\nHamro Radio को घण्टे अपडेट पूरा भयो।")
    print("================================")


if __name__ == "__main__":
    main()
