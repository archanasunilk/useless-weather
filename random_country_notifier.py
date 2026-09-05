import requests
import random
import time
import json
import os

# ============================================================
# CONFIGURATION
# ============================================================

# DO NOT put your real bot token directly in this file.
# Set it in PowerShell before running:
#
# $env:BOT_TOKEN="YOUR_NEW_BOT_TOKEN"
#
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set.\n"
        "In PowerShell, run:\n"
        '$env:BOT_TOKEN="YOUR_BOT_TOKEN"'
    )

MIN_INTERVAL_SEC = 15
MAX_INTERVAL_SEC = 60

SUBSCRIBERS_FILE = "subscribers.json"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ============================================================
# COUNTRIES
# ============================================================

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


# ============================================================
# WEATHER CODES
# ============================================================

WEATHER_CODES = {
    0: "clear sky",
    1: "mostly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "heavy drizzle",
    56: "freezing drizzle",
    57: "heavy freezing drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "freezing rain",
    67: "heavy freezing rain",
    71: "light snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "light rain showers",
    81: "moderate rain showers",
    82: "heavy rain showers",
    85: "light snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with light hail",
    99: "thunderstorm with heavy hail",
}


# ============================================================
# SUBSCRIBER STORAGE
# ============================================================

def load_subscribers():
    """Load subscriber chat IDs from subscribers.json."""

    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()

    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load subscribers: {error}")
        return set()


def save_subscribers(subscribers):
    """Save subscriber chat IDs."""

    try:
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as file:
            json.dump(list(subscribers), file, indent=2)

    except OSError as error:
        print(f"Could not save subscribers: {error}")


# ============================================================
# TELEGRAM
# ============================================================

def telegram_request(method, params=None, timeout=10):
    """Make a request to the Telegram Bot API."""

    url = f"{TELEGRAM_API}/{method}"

    response = requests.get(
        url,
        params=params or {},
        timeout=timeout
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(
            data.get("description", "Telegram API request failed")
        )

    return data["result"]


def poll_new_subscribers(offset, subscribers):
    """
    Check Telegram for new messages.

    Anyone who sends /start gets added as a subscriber.
    """

    params = {
        "timeout": 5
    }

    if offset is not None:
        params["offset"] = offset

    try:
        updates = telegram_request(
            "getUpdates",
            params=params,
            timeout=10
        )

    except Exception as error:
        print(f"Telegram polling error: {error}")
        return offset, subscribers

    new_offset = offset
    changed = False

    for update in updates:

        update_id = update.get("update_id")

        if update_id is not None:
            new_offset = update_id + 1

        message = update.get("message")

        if not message:
            continue

        text = message.get("text", "").strip().lower()

        chat = message.get("chat", {})
        chat_id = chat.get("id")

        if not chat_id:
            continue

        # ----------------------------------------------------
        # /start
        # ----------------------------------------------------

        if text == "/start":

            if chat_id not in subscribers:

                subscribers.add(chat_id)
                changed = True

                print(
                    f"New subscriber added: {chat_id}"
                )

            try:
                send_telegram_message(
                    chat_id,
                    "🌍 You're subscribed!\n\n"
                    "I'll randomly send you weather updates "
                    "from around the world.\n\n"
                    "Yes, this is completely unnecessary."
                )

            except Exception as error:
                print(
                    f"Could not send welcome message "
                    f"to {chat_id}: {error}"
                )

        # ----------------------------------------------------
        # /stop
        # ----------------------------------------------------

        elif text == "/stop":

            if chat_id in subscribers:

                subscribers.remove(chat_id)
                changed = True

                print(
                    f"Subscriber removed: {chat_id}"
                )

                try:
                    send_telegram_message(
                        chat_id,
                        "🛑 Unsubscribed.\n\n"
                        "No more random weather spam."
                    )

                except Exception as error:
                    print(
                        f"Could not send goodbye message: {error}"
                    )

    if changed:
        save_subscribers(subscribers)

    return new_offset, subscribers


# ============================================================
# WEATHER
# ============================================================

def get_weather_and_time(lat, lon):
    """Get current weather and local time from Open-Meteo."""

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current_weather"]

    return {
        "temp_c": current["temperature"],
        "wind_kmh": current["windspeed"],
        "condition": WEATHER_CODES.get(
            current["weathercode"],
            "unknown conditions"
        ),
        "local_time": current["time"],
    }


# ============================================================
# MESSAGE
# ============================================================

def build_message(country, info):

    local_time = info["local_time"].replace("T", " ")

    return (
        f"🌍 Random dispatch from {country}\n\n"
        f"🕒 Local time: {local_time}\n"
        f"🌡️ Temperature: {info['temp_c']}°C\n"
        f"☁️ Conditions: {info['condition']}\n"
        f"💨 Wind: {info['wind_kmh']} km/h\n\n"
        f"(you didn't ask for this. that's the point.)"
    )


# ============================================================
# SEND MESSAGE
# ============================================================

def send_telegram_message(chat_id, text):
    """Send a Telegram message."""

    url = f"{TELEGRAM_API}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": chat_id,
            "text": text,
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(
            data.get("description", "Telegram send failed")
        )


# ============================================================
# BROADCAST
# ============================================================

def broadcast(text, subscribers):
    """Send the message to every subscriber."""

    removed = set()

    for chat_id in list(subscribers):

        try:

            send_telegram_message(
                chat_id,
                text
            )

            print(
                f"Message sent to {chat_id}"
            )

        except requests.HTTPError as error:

            print(
                f"Telegram error for {chat_id}: {error}"
            )

            # Telegram commonly returns 400 when the user
            # blocked the bot or the chat no longer exists.
            if error.response is not None:
                if error.response.status_code == 400:
                    removed.add(chat_id)

        except Exception as error:

            print(
                f"Failed to send to {chat_id}: {error}"
            )

    if removed:

        subscribers.difference_update(removed)

        save_subscribers(subscribers)

        print(
            f"Removed {len(removed)} invalid subscriber(s)."
        )


# ============================================================
# MAIN LOOP
# ============================================================

def run_forever():

    print("=" * 60)
    print("🌍 Random Country Notifier")
    print("=" * 60)
    print("Bot started.")
    print("Press Ctrl+C to stop.")
    print()

    subscribers = load_subscribers()

    print(
        f"Loaded {len(subscribers)} subscriber(s)."
    )

    offset = None

    while True:

        try:

            # ------------------------------------------------
            # Check for new /start and /stop commands
            # ------------------------------------------------

            offset, subscribers = poll_new_subscribers(
                offset,
                subscribers
            )

            # ------------------------------------------------
            # No subscribers
            # ------------------------------------------------

            if not subscribers:

                print(
                    "No subscribers yet. "
                    "Waiting for someone to press Start..."
                )

            # ------------------------------------------------
            # Send random weather notification
            # ------------------------------------------------

            else:

                country = random.choice(COUNTRIES)

                print(
                    f"Getting weather for "
                    f"{country['name']}..."
                )

                try:

                    info = get_weather_and_time(
                        country["lat"],
                        country["lon"]
                    )

                    message = build_message(
                        country["name"],
                        info
                    )

                    broadcast(
                        message,
                        subscribers
                    )

                    print(
                        f"✅ Sent update for "
                        f"{country['name']} "
                        f"to {len(subscribers)} subscriber(s)."
                    )

                except Exception as error:

                    print(
                        f"❌ Weather/send error: {error}"
                    )

            # ------------------------------------------------
            # Random delay
            # ------------------------------------------------

            wait_seconds = random.randint(
                MIN_INTERVAL_SEC,
                MAX_INTERVAL_SEC
            )

            print(
                f"💤 Sleeping {wait_seconds} seconds..."
            )
            print()

            time.sleep(wait_seconds)

        except KeyboardInterrupt:

            print()
            print("Bot stopped.")
            break

        except Exception as error:

            print(
                f"Unexpected error: {error}"
            )

            print(
                "Retrying in 10 seconds..."
            )

            time.sleep(10)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_forever()