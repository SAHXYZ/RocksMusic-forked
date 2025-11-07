# =====================================================
# 🎵 RocksMusic Configuration File (FINAL STABLE)
# 🔹 Maintained by @sahalam | Bot: @RocksMusicAIBot
# 🔹 Fully Compatible with VenomMusic Core (Heroku Ready)
# =====================================================

import os
import re
import asyncio
import aiohttp
from dotenv import load_dotenv
from pyrogram import filters

# =====================================================
# 🔹 Load Environment Variables
# =====================================================
load_dotenv()

# =====================================================
# 📲 Telegram API Configuration
# =====================================================
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 0))

BOT_NAME = "RocksMusic"
BOT_USERNAME = os.getenv("BOT_USERNAME", "RocksMusicAIBot")

# =====================================================
# 🗃️ MongoDB & Logging
# =====================================================
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", 0))

# =====================================================
# ☁️ Heroku Deployment Config
# =====================================================
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")

# =====================================================
# 🎧 YouTube / RocksMusic API Configuration
# =====================================================
API_URL = os.getenv("API_URL", "https://api.thequickearn.xyz")
API_KEY = os.getenv("API_KEY", "30DxNexGenBots275daa")
API_URL_BACKUP = os.getenv("API_URL_BACKUP", "https://pastebin.com/raw/rLsBhAQa")
CURRENT_API_URL = API_URL


# =====================================================
# ⚙️ Auto Loader for Backup API URL
# =====================================================
async def load_backup_api():
    """Fetch backup API URL dynamically (no redeploy needed)."""
    global CURRENT_API_URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL_BACKUP, timeout=15) as response:
                if response.status == 200:
                    backup_url = (await response.text()).strip()
                    if backup_url.startswith("http"):
                        CURRENT_API_URL = backup_url
                        print(f"[CONFIG] ✅ Loaded backup API URL: {CURRENT_API_URL}")
                        return CURRENT_API_URL
                print(f"[CONFIG] ⚠️ Pastebin returned HTTP {response.status}")
    except Exception as e:
        print(f"[CONFIG] ❌ Failed to load backup API URL: {e}")
    return API_URL


# =====================================================
# 🧠 Initialize API Loader on Startup
# =====================================================
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(load_backup_api())
    else:
        loop.run_until_complete(load_backup_api())
except RuntimeError:
    pass


# =====================================================
# 🧾 Bot Configurations & Limits
# =====================================================
DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT_MIN", 300))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))
AUTO_LEAVING_ASSISTANT = bool(os.getenv("AUTO_LEAVING_ASSISTANT", False))

# =====================================================
# 🔄 Git / Upstream Configuration
# =====================================================
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/fessstygee/RocksMusic")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)

# =====================================================
# 🧵 Assistant String Sessions
# =====================================================
STRING1 = os.getenv("STRING_SESSION", None)
STRING2 = os.getenv("STRING_SESSION2", None)
STRING3 = os.getenv("STRING_SESSION3", None)
STRING4 = os.getenv("STRING_SESSION4", None)
STRING5 = os.getenv("STRING_SESSION5", None)

# =====================================================
# 🎧 Spotify Integration
# =====================================================
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", None)

# =====================================================
# 🧩 Compatibility Variables (Required for VenomMusic Core)
# =====================================================
adminlist = {}
confirmer = {}
lyrical = {}
votemode = {}
autoclean = []
BANNED_USERS = filters.user()

# =====================================================
# 🖼️ Image URLs (used by modules)
# =====================================================
START_IMG_URL = os.getenv("START_IMG_URL", "https://files.catbox.moe/bs5gni.jpg")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
PLAYLIST_IMG_URL = os.getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
STATS_IMG_URL = os.getenv("STATS_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
STREAM_IMG_URL = os.getenv("STREAM_IMG_URL", "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg")
SOUNCLOUD_IMG_URL = os.getenv("SOUNCLOUD_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
YOUTUBE_IMG_URL = os.getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
SPOTIFY_ARTIST_IMG_URL = os.getenv("SPOTIFY_ARTIST_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
SPOTIFY_ALBUM_IMG_URL = os.getenv("SPOTIFY_ALBUM_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")
SPOTIFY_PLAYLIST_IMG_URL = os.getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://files.catbox.moe/fa1xas.jpg")

# =====================================================
# 📢 Support & Contact
# =====================================================
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/Pubglovers_Shayri_lovers")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/+2HpAd1kBDRo1NzY1")
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-RocksMusic-08-14")

# =====================================================
# ⏱️ Utility Function: Time Conversion
# =====================================================
def time_to_seconds(time: str) -> int:
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# =====================================================
# 🔍 URL Validation for Support Links
# =====================================================
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL must start with https://")

if SUPPORT_GROUP and not re.match(r"(?:http|https)://", SUPPORT_GROUP):
    raise SystemExit("[ERROR] - SUPPORT_GROUP must start with https://")

# =====================================================
# ✅ Final Log
# =====================================================
print(f"✅ {BOT_NAME} Config Loaded Successfully | @{BOT_USERNAME}")
