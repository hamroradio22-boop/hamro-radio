
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import nepali_datetime
import requests
import re

NEPAL_TZ = ZoneInfo("Asia/Kathmandu")

LATITUDE = 27.6766
LONGITUDE = 84.4359

API_URL = "https://nepdate-api.khumnath.com.np/today"

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
    "0123456789", "०१२३४५६७८९"
)


def to_nepali_digits(value):
    return str(value).translate(DEVANAGARI_DIGITS)


def get_bikram_sambat_date(now):
    bs = nepali_datetime.date.from_datetime_date(now.date())

    return (
        f"{to_nepali_digits(bs.year)} साल "
        f"{BS_MONTHS[bs.month - 1]} "
        f"{to_nepali_digits(bs.day)} गते"
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
            headers={"User-Agent": "HamroRadio/1.0"}
        )
        response.raise_for_status()

        text = response.text

        patterns = {
            "tithi": r"(?im)^Tithi:\s*(.+)$",
            "nakshatra": r"(?im)^Nakshatra:\s*(.+)$",
            "yoga": r"(?im)^Yoga:\s*(.+)$",
            "sunrise": r"(?im)^Sunrise:\s*(.+?)(?:\s*\||$)",
            "sunset": r"(?im)Sunset:\s*(.+)$"
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                result[key] = match.group(1).strip()

        print("पञ्चाङ्ग API सफल भयो।")

    except Exception as error:
        print("पञ्चाङ्ग API समस्या:", error)

    return result


def parse_clock(value, date):
    parsed = datetime.strptime(value.strip(), "%I:%M %p")

    return datetime(
        date.year,
        date.month,
        date.day,
        parsed.hour,
        parsed.minute,
        tzinfo=NEPAL_TZ
    )


def format_clock(value):
    return value.strftime("%I:%M %p")


def calculate_muhurta(now, sunrise_text, sunset_text):

    result = {
        "rahu_kal": "उपलब्ध छैन",
        "yamaganda": "उपलब्ध छैन",
        "gulika": "उपलब्ध छैन",
        "abhijit": "उपलब्ध छैन",
        "brahma": "उपलब्ध छैन"
    }

    try:
        sunrise = parse_clock(sunrise_text, now.date())
        sunset = parse_clock(sunset_text, now.date())

        if sunset <= sunrise:
            raise ValueError("सूर्योदय र सूर्यास्तको समय मिलेन")

        day_duration = sunset - sunrise
        one_part = day_duration / 8

        # Python weekday: Monday=0, Sunday=6
        weekday = now.weekday()

        rahu_parts = [2, 7, 5, 6, 4, 3, 8]
        yama_parts = [4, 3, 2, 1, 7, 6, 5]
        gulika_parts = [6, 5, 4, 3, 2, 1, 7]

        def period(part):
            start = sunrise + one_part * (part - 1)
            end = start + one_part
            return f"{format_clock(start)} - {format_clock(end)}"

        result["rahu_kal"] = period(rahu_parts[weekday])
        result["yamaganda"] = period(yama_parts[weekday])
        result["gulika"] = period(gulika_parts[weekday])

        # ब्रह्म मुहूर्त: सूर्योदयभन्दा 96 देखि 48 मिनेट अगाडि
        brahma_start = sunrise - timedelta(minutes=96)
        brahma_end = sunrise - timedelta(minutes=48)

        result["brahma"] = (
            f"{format_clock(brahma_start)} - "
            f"{format_clock(brahma_end)}"
        )

        # अभिजित: स्थानीय मध्याह्न वरिपरि 48 मिनेट
        midday = sunrise + day_duration / 2

        abhijit_start = midday - timedelta(minutes=24)
        abhijit_end = midday + timedelta(minutes=24)

        if weekday == 2:
            result["abhijit"] = (
                "बुधबारको परम्पराअनुसार नदेखाइएको"
            )
        else:
            result["abhijit"] = (
                f"{format_clock(abhijit_start)} - "
                f"{format_clock(abhijit_end)}"
            )

    except Exception as error:
        print("मुहूर्त गणना समस्या:", error)

    return result


def get_calendar_info():

    now = datetime.now(NEPAL_TZ)

    panchang = get_panchang()

    muhurta = calculate_muhurta(
        now,
        panchang["sunrise"],
        panchang["sunset"]
    )

    info = {
        "english_date": (
            f"{now.day} {MONTHS[now.month - 1]} {now.year}"
        ),
        "nepali_day": DAYS[now.weekday()],
        "time": now.strftime("%I:%M %p"),
        "bikram_sambat_date": get_bikram_sambat_date(now),

        "tithi": panchang["tithi"],
        "nakshatra": panchang["nakshatra"],
        "yoga": panchang["yoga"],
        "sunrise": panchang["sunrise"],
        "sunset": panchang["sunset"],

        "rahu_kal": muhurta["rahu_kal"],
        "yamaganda": muhurta["yamaganda"],
        "gulika": muhurta["gulika"],
        "abhijit": muhurta["abhijit"],
        "brahma": muhurta["brahma"]
    }

    print("\n========== चितवन शुभ-अशुभ समय ==========")
    print("राहुकाल:", info["rahu_kal"])
    print("यमगण्ड:", info["yamaganda"])
    print("गुलिक काल:", info["gulika"])
    print("अभिजित मुहूर्त:", info["abhijit"])
    print("ब्रह्म मुहूर्त:", info["brahma"])
    print("========================================")

    return info


def announce_calendar():

    info = get_calendar_info()

    print("\nआजको पात्रो जानकारी")
    print("बार:", info["nepali_day"])
    print("अंग्रेजी मिति:", info["english_date"])
    print("विक्रम संवत्:", info["bikram_sambat_date"])
    print("नेपाल समय:", info["time"])


if __name__ == "__main__":
    announce_calendar()
