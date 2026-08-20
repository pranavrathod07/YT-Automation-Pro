import os
from dotenv import load_dotenv

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

SONGS_DIR = os.getenv("SONGS_DIR", "songs")
SHORT_DURATION = int(os.getenv("SHORT_DURATION_SECONDS", "20"))
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
PRIVACY_STATUS = os.getenv("PRIVACY_STATUS", "public")

DATA_DIR = "data"
TEMP_DIR = "temp"
LOGS_DIR = "logs"
TOKENS_DIR = "tokens"

# Single account ke liye sirf ek hi name rakho
ACCOUNTS = [
    "main_channel",
]

# Rotating pool of search terms used to fetch sports clips from Pixabay.
SPORT_QUERIES = [
    "football player",
    "cricket player",
    "basketball player",
    "tennis player",
    "boxing athlete",
    "gym workout",
    "sprint runner",
    "soccer goal",
    "badminton player",
    "swimming athlete",
    "skateboarding",
    "martial arts fight",
]
