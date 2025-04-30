import os
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

# Telegram Token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Entwicklungsmodus aktivieren
IS_DEV_MODE = False

# Farben (nur relevant für pygame)
COLOR_ACTIVE = (255, 255, 255)
COLOR_INACTIVE = (100, 100, 100)
BG_COLOR = (0, 0, 0)