
from datetime import datetime
from zoneinfo import ZoneInfo

import nepali_datetime
import requests
import re

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

# चितवनको स्थान
LATITUDE = 27.6766
LONGITUDE = 84.4359

API_URL = (
    "https://nepdate-api.khumnath.com.np/today"
)

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


def to_nepali_digits(value):
    return str(value).translate(DEVANAGARI_DIGITS)


def get_bikram_sambat_date(now):

    bs_date = nepali_datetime.date.from_datetime_date(
        now.date()
    )

    day = to_nepali_digits(bs_date.day)
    year = to_nepali_digits(bs_date.year)

    return (
        f"{year} साल "
        f"{BS_MONTHS[bs_date.month - 1]} "
        f"{day} गते"
    )


def get_panchang():

    result = {
        "tithi": "हाल उपलब्ध छैन",
        "nakshatra": "हाल उपलब्ध छैन",
        "yoga": "हाल उपलब्ध छैन",
        "sunrise": "हाल उपलब्ध छैन",
        "sunset": "हाल उपलब्ध छैन"
    }

    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "tz": 5.75,
        "format": "text",
        "lang": "ne"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=20,
            headers={
                "User-Agent": "HamroRadio/1.0"
            }
        )

        response.raise_for_status()

        text = response.text

        print("पञ्चाङ्ग API सफल भयो।")

        # तिथि
        match = re.search(
            r"(?im)^Tithi:\s*(.+)$",
            text
        )
        if match:
            result["tithi"] = match.group(1).strip()

        # नक्षत्र
        match = re.search(
            r"(?im)^Nakshatra:\s*(.+)$",
            text
        )
        if match:
            result["nakshatra"] = match.group(1).strip()

        # योग
        match = re.search(
            r"(?im)^Yoga:\s*(.+)$",
            text
        )
        if match:
            result["yoga"] = match.group(1).strip()

        # सूर्योदय
        match = re.search(
            r"(?im)^Sunrise:\s*(.+?)(?:\s*\||$)",
            text
        )
        if match:
            result["sunrise"] = match.group(1).strip()

        # सूर्यास्त
        match = re.search(
            r"(?im)Sunset:\s*(.+)$",
            text
        )
        if match:
            result["sunset"] = match.group(1).strip()

    except Exception as error:
        print("पञ्चाङ्ग API समस्या:", error)

    return result


def get_calendar_info():

    now = datetime.now(NEPAL_TZ)

    panchang = get_panchang()

    return {
        "english_date": (
            f"{now.day} "
            f"{MONTHS[now.month - 1]} "
            f"{now.year}"
        ),

        "nepali_day": DAYS[now.weekday()],

        "time": now.strftime("%I:%M %p"),

        "bikram_sambat_date": get_bikram_sambat_date(now),

        "tithi": panchang["tithi"],

        "nakshatra": panchang["nakshatra"],

        "yoga": panchang["yoga"],

        "sunrise": panchang["sunrise"],

        "sunset": panchang["sunset"]
    }


def announce_calendar():

    info = get_calendar_info()

    print("\n========== HAMRO RADIO पात्रो ==========")

    print("बार:", info["nepali_day"])
    print("अंग्रेजी मिति:", info["english_date"])
    print("विक्रम संवत्:", info["bikram_sambat_date"])
    print("नेपाल समय:", info["time"])

    print("\n========== चितवन पञ्चाङ्ग ==========")

    print("तिथि:", info["tithi"])
    print("नक्षत्र:", info["nakshatra"])
    print("योग:", info["yoga"])
    print("सूर्योदय:", info["sunrise"])
    print("सूर्यास्त:", info["sunset"])

    print("========================================")


if __name__ == "__main__":
    announce_calendar()
