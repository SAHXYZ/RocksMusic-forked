import os
import asyncio
import aiohttp
from dotenv import load_dotenv

# =====================================================
# 🔹 Load Environment Variables
# =====================================================
load_dotenv()

# 🔸 Telegram API
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# 🔸 MongoDB & Logging
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", 0))
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# 🔸 Heroku Config
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "")

# =====================================================
# 🔹 YouTube / RocksMusic API Configuration
# =====================================================
# Primary API (Direct)
API_URL = os.getenv("API_URL", "https://api.thequickearn.xyz")
API_KEY = os.getenv("API_KEY", "30DxNexGenBots275daa")

# Backup source (Pastebin link for fallback auto-load)
API_URL_BACKUP = os.getenv("API_URL_BACKUP", "https://pastebin.com/raw/rLsBhAQa")

# Global cache for current API
CURRENT_API_URL = API_URL


# =====================================================
# 🔹 Auto Loader for API URL (Dynamic)
# =====================================================
async def load_backup_api():
    """
    Fetch backup API URL from Pastebin if main URL fails.
    This allows changing API endpoints without redeploying the bot.
    """
    global CURRENT_API_URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL_BACKUP, timeout=15) as response:
                if response.status == 200:
                    backup_url = (await response.text()).strip()
                    if backup_url.startswith("http"):
                        CURRENT_API_URL = backup_url
                        print(f"[CONFIG] ✅ Loaded backup API URL from Pastebin: {CURRENT_API_URL}")
                        return CURRENT_API_URL
                print(f"[CONFIG] ⚠️ Pastebin returned HTTP {response.status}")
    except Exception as e:
        print(f"[CONFIG] ❌ Failed to load backup API URL: {e}")
    return API_URL  # fallback to primary


# =====================================================
# 🔹 Auto Initialize on Startup
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
# 🔹 Other Optional Bot Configs
# =====================================================
# Example for song duration limits, admin IDs, etc.
DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT_MIN", 300))
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/RocksMusicUpdates")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/RocksMusicSupport")

# =====================================================
# 🔹 Git / Upstream Configuration
# =====================================================
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/fessstygee/RocksMusic")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)
