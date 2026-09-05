import requests

BOT_USERNAME = "random_world_pings_bot"  # no @ symbol

bot_link = f"https://t.me/{BOT_USERNAME}"

qr_api_url = "https://api.qrserver.com/v1/create-qr-code/"
params = {
    "size": "400x400",
    "data": bot_link,
}

response = requests.get(qr_api_url, params=params, timeout=10)
response.raise_for_status()

with open("bot_qr.png", "wb") as f:
    f.write(response.content)

print(f"QR code saved as bot_qr.png")
print(f"It links to: {bot_link}")
print("Scan it, tap Start, and you're subscribed.")