
from datetime import datetime
from zoneinfo import ZoneInfo

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

DAYS = [
    "सोमबार", "मंगलबार", "बुधबार",
    "बिहीबार", "शुक्रबार", "शनिबार", "आइतबार"
]

MONTHS = [
    "जनवरी", "फेब्रुअरी", "मार्च", "अप्रिल",
    "मे", "जुन", "जुलाई", "अगस्ट",
    "सेप्टेम्बर", "अक्टोबर", "नोभेम्बर", "डिसेम्बर"
]

def get_calendar_info():
    now = datetime.now(NEPAL_TZ)

    return {
        "english_date": (
            f"{now.day} {MONTHS[now.month - 1]} {now.year}"
        ),
        "nepali_day": DAYS[now.weekday()],
        "time": now.strftime("%I:%M %p")
    }

def announce_calendar():
    info = get_calendar_info()

    print("आजको पात्रो जानकारी")
    print("बार:", info["nepali_day"])
    print("अंग्रेजी मिति:", info["english_date"])
    print("नेपाल समय:", info["time"])

if __name__ == "__main__":
    announce_calendar()
