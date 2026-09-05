<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# USELESS WEATHER 🎯


## Basic Details
### Team Name: ELECTRONS


### Team Members
- Team Lead: Archana Sunil K - SCMS SCHOOL OF ENGINEERING AND TECHNOLOGY
- Member 2: Malavika A - SCMS SCHOOL OF ENGINEERING AND TECHNOLOGY

### Project Description
Random World Pings is a Telegram bot that randomly selects a country and sends subscribers a fun weather update from that location.

It fetches real-time weather and local time information and sends unexpected "news flashes" from around the world at random intervals. Because apparently, nobody asked to know the weather in Finland at 2 AM. 🌍😂

### The Problem (that doesn't exist)
People are constantly checking the weather in places they don't live in.

Our project solves the extremely serious problem of not knowing the current weather in a completely random country at completely random times.

For example:

"Why don't I know what's happening in Colombia right now?"

Now you can.

### The Solution (that nobody asked for)
We created a Telegram bot that:

Randomly chooses a country.
Gets its current weather.
Gets the local time.
Sends the information to everyone subscribed to the bot.
Sends updates at random intervals.
Allows users to subscribe using /start.
Allows users to unsubscribe using /stop.
Allows multiple users to receive the same random update.

The bot basically provides completely unnecessary information that somehow becomes entertaining. 🌎

## Technical Details
### Technologies/Components Used
For Software:
- Python
- Telegram Bot API
GitHub Actions
- requests
Python standard libraries: random, time, json, os
- Visual Studio Code
Git
GitHub
GitHub Actions
PowerShell
Python 3.13

For Hardware:
- No special hardware is required.

### Implementation
For Software:
# Installation
Clone the repository:
git clone https://github.com/archanasunilk/useless-weather.git
cd useless-weather

Install the required Python package:
pip install -r requirements.txt

Set the Telegram bot token as an environment variable.

Windows PowerShell
$env:BOT_TOKEN="YOUR_BOT_TOKEN"

# Run
python random_country_notifier.py

### Project Documentation
For Software:

# Screenshots (Add at least 3)
<img width="1920" height="1080" alt="VS Code terminal" src="https://github.com/user-attachments/assets/31f31c58-6aa8-415d-8bf4-f4fdc9caad09" />
*The bot running and sending random country weather updates to multiple subscribers.*

<img width="591" height="1280" alt="Telegram" src="https://github.com/user-attachments/assets/ae8af9ec-b5da-48fc-894f-80dddeab9e61" />
*Telegram showing the subscription confirmation and random weather notifications.*

<img width="1920" height="913" alt="GitHub Actions" src="https://github.com/user-attachments/assets/3a2284fa-5101-49c1-8257-38b447834e64" />
*GitHub Actions running the Random World Pings Bot in the cloud.*

# Diagrams
                 ┌─────────────────────┐
                 │   Telegram Users    │
                 │  /start or /stop    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Telegram API     │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │  Random World Pings Bot  │
              │         Python           │
              └────────────┬─────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     ┌─────────────────┐       ┌─────────────────┐
     │ Random Country  │       │   Open-Meteo    │
     │    Selection    │       │  Weather API    │
     └────────┬────────┘       └────────┬────────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                  ┌─────────────────┐
                  │ Message Builder │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Telegram Users  │
                  └─────────────────┘

                    🔁 Repeat
*System Workflow: The bot receives Telegram commands, randomly selects a country, retrieves its weather information from Open-Meteo, builds a notification, and broadcasts it to all active subscribers.*

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos

- Telegram Bot: https://t.me/random_world_pings_bot
- GitHub Repository: https://github.com/archanasunilk/useless-weather

## Team Contributions
- [Name 1]: [Specific contributions]
- [Name 2]: [Specific contributions]
- [Name 3]: [Specific contributions]

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



