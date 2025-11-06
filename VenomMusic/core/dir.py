import os
import time
from ..logging import LOGGER


def dirr():
    """
    Ensures required directories exist, cleans old or leftover files,
    and prevents FileNotFoundError during downloads or ffmpeg processing.
    """

    # ───────────────────────────────
    # 🧹 Clean root image clutter
    # ───────────────────────────────
    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg", ".png")):
            try:
                os.remove(file)
            except Exception as e:
                LOGGER(__name__).warning(f"⚠️ Could not remove {file}: {e}")

    # ───────────────────────────────
    # 📁 Ensure all required folders exist
    # ───────────────────────────────
    required_dirs = ["downloads", "cache", "logs", "raw_files", "temp"]
    for folder in required_dirs:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder, exist_ok=True)
                LOGGER(__name__).info(f"📂 Created missing folder: {folder}")
            except Exception as e:
                LOGGER(__name__).warning(f"⚠️ Could not create folder {folder}: {e}")

    # ───────────────────────────────
    # ⏳ Auto-clean files older than 1 hour
    # ───────────────────────────────
    clean_old_files(["downloads", "cache", "temp", "raw_files"])

    # ───────────────────────────────
    # ✅ Final confirmation log
    # ───────────────────────────────
    LOGGER(__name__).info("✅ Directories Verified, Cleaned, and Ready For Use.")


def clean_old_files(folders):
    """
    Deletes files older than 1 hour (3600s) inside specified folders.
    Prevents Heroku's ephemeral disk from filling up.
    """
    now = time.time()
    one_hour = 3600  # seconds

    for folder in folders:
        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            try:
                if os.path.isfile(path) and now - os.path.getmtime(path) > one_hour:
                    os.remove(path)
                    LOGGER(__name__).info(f"🗑️ Removed old file: {path}")
            except Exception as e:
                LOGGER(__name__).warning(f"⚠️ Error removing {path}: {e}")
