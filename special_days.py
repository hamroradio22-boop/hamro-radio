
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Kathmandu")

SPECIAL_DAYS = {
    "01-01": "नयाँ वर्ष",
    "05-01": "अन्तर्राष्ट्रिय श्रमिक दिवस",
    "09-20": "संविधान दिवस (नेपाल)",
    "12-25": "क्रिसमस दिवस"
}

def get_special_day():
    today = datetime.now(TZ)
    key = today.strftime("%m-%d")

    special = SPECIAL_DAYS.get(
        key,
        "आजका लागि सूचीमा विशेष दिवस उल्लेख छैन।"
    )

    return {
        "date": today.strftime("%Y-%m-%d"),
        "special_day": special
    }

def announce_special_day():
    info = get_special_day()
    print("आजको विशेष दिवस:", info["special_day"])

if __name__ == "__main__":
    announce_special_day()
