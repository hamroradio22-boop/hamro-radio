
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo

CONFIG_FILE = "config.json"
TZ = ZoneInfo("Asia/Kathmandu")

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def nepali_time():
    now = datetime.now(TZ)
    hour = now.hour
    minute = now.minute

    if hour < 12:
        period = "बिहान"
    elif hour < 17:
        period = "दिउँसो"
    elif hour < 20:
        period = "साँझ"
    else:
        period = "राति"

    return (
        f"नेपालको समयअनुसार अहिले "
        f"{period} {hour} बजेर {minute} मिनेट गएको छ।"
    )

def radio_status(config):
    print("=" * 40)
    print(config["radio_name"])
    print(nepali_time())
    print("नेपाली गीत + समाचार + AI प्रस्तोता")
    print("पुरुष र महिला प्रस्तोता सक्रिय")
    print("रेडियो सिस्टम तयार छ।")
    print("=" * 40)

def main():
    config = load_config()
    print("HAMRO RADIO SYSTEM STARTED")

    while True:
        radio_status(config)
        time.sleep(3600)

if __name__ == "__main__":
    main()
