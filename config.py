import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables
load_dotenv()

# ===================================================
# 🔹 Telegram API Configuration
# ===================================================

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

# ===================================================
# 🔹 MongoDB & Logging
# ===================================================

MONGO_DB_URI = getenv("MONGO_DB_URI", None)
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", None))
OWNER_ID = int(getenv("OWNER_ID", None))

# ===================================================
# 🔹 Heroku Configuration
# ===================================================

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ===================================================
# 🔹 YouTube & API Configuration
# ===================================================

# ⚡ Hybrid YouTube system:
# 1️⃣ yt-dlp used first (local)
# 2️⃣ NexGenBots API used as fallback
API_URL = getenv("API_URL", "https://api.nexgenbots.xyz")
API_KEY = getenv("API_KEY", "30DxNexGenBots275daa")

# Optional YouTube Data API (for metadata/search)
YOUTUBE_API_KEY = getenv("YOUTUBE_API_KEY", None)

# ===================================================
# 🔹 Spotify Credentials (Optional)
# ===================================================

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# ===================================================
# 🔹 Upstream Repo Configuration
# ===================================================

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/fessstygee/RocksMusic")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = getenv("GIT_TOKEN", None)  # Needed only for private repos

# ===================================================
# 🔹 Support Links & Privacy
# ===================================================

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Pubglovers_Shayri_lovers")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/+2HpAd1kBDRo1NzY1")
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-RocksMusic-08-14")

# ===================================================
# 🔹 Bot Limits & Settings
# ===================================================

try:
    DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 1700))
except ValueError:
    DURATION_LIMIT_MIN = 1700

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# ===================================================
# 🔹 Pyrogram String Sessions
# ===================================================

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# ===================================================
# 🔹 Internal Configuration
# ===================================================

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ===================================================
# 🔹 UI Assets
# ===================================================

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/bs5gni.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
PLAYLIST_IMG_URL = "https://files.catbox.moe/pfjgmf.jpg"
STATS_IMG_URL = "https://files.catbox.moe/st6utj.jpg"
TELEGRAM_AUDIO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
TELEGRAM_VIDEO_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://graph.org//file/2f7debf856695e0ef0607.png"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"

# ===================================================
# 🔹 Time Converter
# ===================================================

def time_to_seconds(time):
    """Convert mm:ss format to seconds."""
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ===================================================
# 🔹 URL Validation
# ===================================================

if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL, must start with https://")

if SUPPORT_GROUP and not re.match("(?:http|https)://", SUPPORT_GROUP):
    raise SystemExit("[ERROR] - Invalid SUPPORT_GROUP URL, must start with https://")
