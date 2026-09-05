
import requests
import random
import time
import json
import os

# ---------- CONFIG ----------
BOT_TOKEN = "8766701989:AAEmTxfINz6kfkLWrcarQkTCIv0DHD9KXvM"

MIN_INTERVAL_SEC = 15   # minimum seconds between notifications
MAX_INTERVAL_SEC = 60   # maximum seconds between notifications (1 min cap)

SUBSCRIBERS_FILE = "subscribers.json"
# -----------------------------

COUNTRIES = [
    {"name": "Canada", "lat": 45.42, "lon": -75.70},
    {"name": "Japan", "lat": 35.68, "lon": 139.69},
    {"name": "Brazil", "lat": -15.79, "lon": -47.88},
    {"name": "Kenya", "lat": -1.29, "lon": 36.82},
    {"name": "Iceland", "lat": 64.15, "lon": -21.94},
    {"name": "New Zealand", "lat": -41.29, "lon": 174.78},
    {"name": "Mongolia", "lat": 47.92, "lon": 106.92},
    {"name": "Chile", "lat": -33.45, "lon": -70.67},
    {"name": "Norway", "lat": 59.91, "lon": 10.75},
    {"name": "Egypt", "lat": 30.04, "lon": 31.24},
    {"name": "Thailand", "lat": 13.75, "lon": 100.50},
    {"name": "Argentina", "lat": -34.60, "lon": -58.38},
    {"name": "South Africa", "lat": -25.75, "lon": 28.19},
    {"name": "Finland", "lat": 60.17, "lon": 24.94},
    {"name": "Vietnam", "lat": 21.03, "lon": 105.85},
    {"name": "Peru", "lat": -12.05, "lon": -77.04},
    {"name": "Morocco", "lat": 34.02, "lon": -6.84},
    {"name": "Philippines", "lat": 14.60, "lon": 120.98},
    {"name": "Portugal", "lat": 38.72, "lon": -9.14},
    {"name": "Fiji", "lat": -18.14, "lon": 178.44},
    {"name": "Nepal", "lat": 27.72, "lon": 85.32},
    {"name": "Greece", "lat": 37.98, "lon": 23.73},
    {"name": "Colombia", "lat": 4.71, "lon": -74.07},
    {"name": "Sweden", "lat": 59.33, "lon": 18.07},
    {"name": "Indonesia", "lat": -6.21, "lon": 106.85},
]

WEATHER_CODES = {
    0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
    45: "foggy", 48: "foggy", 51: "light drizzle", 61: "light rain",
    63: "moderate rain", 65: "heavy rain", 71: "light snow", 73: "moderate snow",
    75: "heavy snow", 80: "rain showers", 95: "thunderstorm",
}


# ---------- subscriber storage ----------
def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()
    with open(SUBSCRIBERS_FILE, "r") as f:
        return set(json.load(f))


def save_subscribers(subs):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subs), f)


# ---------- telegram polling for new /start's ----------
def poll_new_subscribers(offset, subscribers):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 0}
    if offset is not None:
        params["offset"] = offset
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    results = resp.json()["result"]

    new_offset = offset
    added_any = False
    for update in results:
        new_offset = update["update_id"] + 1
        message = update.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")
        if chat_id and text.strip().lower() == "/start":
            if chat_id not in subscribers:
                subscribers.add(chat_id)
                added_any = True
                print(f"New subscriber added: {chat_id}")

    if added_any:
        save_subscribers(subscribers)

    return new_offset, subscribers

# ---------- weather ----------
def get_weather_and_time(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()["current_weather"]
    return {
        "temp_c": data["temperature"],
        "wind_kmh": data["windspeed"],
        "condition": WEATHER_CODES.get(data["weathercode"], "unknown conditions"),
        "local_time": data["time"],
    }


def build_message(country, info):
    return (
        f"🌍 Random dispatch from {country}\n"
        f"🕒 Local time: {info['local_time'].replace('T', ' ')}\n"
        f"🌡️ {info['temp_c']}°C, {info['condition']}\n"
        f"💨 Wind: {info['wind_kmh']} km/h\n\n"
        f"(you didn't ask for this. that's the point.)"
    )


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={"chat_id": chat_id, "text": text})
    resp.raise_for_status()


def broadcast(text, subscribers):
    for chat_id in list(subscribers):
        try:
            send_telegram_message(chat_id, text)
        except Exception as e:
            print(f"Failed to send to {chat_id}: {e}")


def run_forever():
    print("Random Country Notifier (multi-subscriber) started. Ctrl+C to stop.")
    subscribers = load_subscribers()
    print(f"Loaded {len(subscribers)} existing subscriber(s).")
    offset = None

    while True:
        # check for anyone who just scanned the QR / hit Start
        offset, subscribers = poll_new_subscribers(offset, subscribers)

        if not subscribers:
            print("No subscribers yet. Waiting...")
        else:
            country = random.choice(COUNTRIES)
            try:
                info = get_weather_and_time(country["lat"], country["lon"])
                message = build_message(country["name"], info)
                broadcast(message, subscribers)
                print(f"Sent update for {country['name']} to {len(subscribers)} subscriber(s)")
            except Exception as e:
                print(f"Failed this round ({country['name']}): {e}")

        wait_seconds = random.randint(MIN_INTERVAL_SEC, MAX_INTERVAL_SEC)
        print(f"Sleeping {wait_seconds} seconds...")
        time.sleep(wait_seconds)


if name == "main":
    run_forever()

    