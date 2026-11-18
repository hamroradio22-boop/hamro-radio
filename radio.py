
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from news import get_news
from special_days import get_special_day
from nepali_calendar import get_calendar_info

TZ = ZoneInfo("Asia/Kathmandu")

def radio_announcement():
    now = datetime.now(TZ)
    news = get_news()
    calendar = get_calendar_info()
    special = get_special_day()

    print("\n========== HAMRO RADIO ==========")
    print("नेपाल समय:", now.strftime("%I:%M %p"))
    print("आजको बार:", calendar["nepali_day"])
    print("अंग्रेजी मिति:", calendar["english_date"])
    print("आजको विशेष दिवस:", special["special_day"])

    if news:
        print("\nआजका मुख्य समाचार:")
        for item in news[:5]:
            print("-", item["title"])

    print("================================\n")

def main():
    print("HAMRO RADIO STARTED")

    while True:
        try:
            radio_announcement()
            time.sleep(3600)
        except Exception as error:
            print("Radio error:", error)
            time.sleep(60)

if __name__ == "__main__":
    main()
