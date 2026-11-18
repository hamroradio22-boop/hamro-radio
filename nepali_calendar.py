
from datetime import datetime
from zoneinfo import ZoneInfo
import nepali_datetime

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

BS_MONTHS = [
    "बैशाख", "जेठ", "असार", "साउन",
    "भदौ", "असोज", "कात्तिक", "मंसिर",
    "पुष", "माघ", "फागुन", "चैत"
]

DEVANAGARI_DIGITS = str.maketrans(
    "0123456789",
    "०१२३४५६७८९"
)


def get_calendar_info():
    now = datetime.now(NEPAL_TZ)

    # अंग्रेजी मितिबाट विक्रम संवत् मिति निकाल्ने
    bs_date = nepali_datetime.date.from_datetime_date(
        now.date()
    )

    bs_day = str(bs_date.day).translate(DEVANAGARI_DIGITS)
    bs_year = str(bs_date.year).translate(DEVANAGARI_DIGITS)

    bikram_sambat_date = (
        f"{bs_year} साल "
        f"{BS_MONTHS[bs_date.month - 1]} "
        f"{bs_day} गते"
    )

    return {
        "english_date": (
            f"{now.day} {MONTHS[now.month - 1]} {now.year}"
        ),
        "nepali_day": DAYS[now.weekday()],
        "time": now.strftime("%I:%M %p"),
        "bikram_sambat_date": bikram_sambat_date
    }


def announce_calendar():
    info = get_calendar_info()

    print("आजको पात्रो जानकारी")
    print("बार:", info["nepali_day"])
    print("अंग्रेजी मिति:", info["english_date"])
    print("विक्रम संवत्:", info["bikram_sambat_date"])
    print("नेपाल समय:", info["time"])


if __name__ == "__main__":
    announce_calendar()
