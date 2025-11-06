import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# ===============================
# 🎯 REQUIRED ENV VARIABLES
# ===============================
REQUIRED_VARS = {
    # Telegram + Bot
    "API_ID": "Telegram API ID (from my.telegram.org/apps)",
    "API_HASH": "Telegram API Hash (from my.telegram.org/apps)",
    "BOT_TOKEN": "Bot Token (from @BotFather)",

    # Database
    "MONGO_DB_URI": "MongoDB connection string (from cloud.mongodb.com)",
    "LOG_GROUP_ID": "Log group chat ID (example: -100xxxxxxxxxx)",
    "OWNER_ID": "Owner Telegram ID (use /id in @MissRose_Bot)",

    # Heroku
    "HEROKU_APP_NAME": "Heroku app name",
    "HEROKU_API_KEY": "Heroku API key (from dashboard.heroku.com/account)",

    # YouTube / API
    "API_URL": "Music API base URL (e.g. https://api.thequickearn.xyz)",
    "API_KEY": "Music API key (from panel.thequickearn.xyz or nexgenbots)",
}

# ===============================
# ⚙️ OPTIONAL VARIABLES
# ===============================
OPTIONAL_VARS = [
    "YOUTUBE_API_KEY",
    "SPOTIFY_CLIENT_ID",
    "SPOTIFY_CLIENT_SECRET",
    "UPSTREAM_REPO",
    "UPSTREAM_BRANCH",
    "SUPPORT_CHANNEL",
    "SUPPORT_GROUP",
    "PRIVACY_LINK",
    "STRING_SESSION",
    "STRING_SESSION2",
    "STRING_SESSION3",
    "STRING_SESSION4",
    "STRING_SESSION5",
]

# ===============================
# 🌈 COLOR THEMES
# ===============================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
CYAN = "\033[96m"

# ===============================
# 🔍 VERIFICATION
# ===============================
def check_env():
    print(f"\n{CYAN}🔎 ROCKSMUSIC ENVIRONMENT VERIFIER\n{'=' * 45}{RESET}")

    missing = []

    for key, desc in REQUIRED_VARS.items():
        value = os.getenv(key)
        if not value or value.strip() == "":
            print(f"{RED}✖ MISSING → {key}{RESET}  |  {YELLOW}{desc}{RESET}")
            missing.append(key)
        else:
            print(f"{GREEN}✔ OK → {key}{RESET}")

    print(f"\n{CYAN}🧩 Checking optional vars...{RESET}")
    for key in OPTIONAL_VARS:
        if os.getenv(key):
            print(f"{GREEN}✔ {key}{RESET}")
        else:
            print(f"{YELLOW}⚠ Missing optional: {key}{RESET}")

    print(f"\n{'=' * 45}")
    if missing:
        print(f"{RED}❌ {len(missing)} critical variables missing! Fix these before deploying.{RESET}")
        print(f"{YELLOW}🧾 Missing: {', '.join(missing)}{RESET}")
    else:
        print(f"{GREEN}✅ All critical environment variables are properly configured!{RESET}")
    print(f"{'=' * 45}\n")


if __name__ == "__main__":
    check_env()
