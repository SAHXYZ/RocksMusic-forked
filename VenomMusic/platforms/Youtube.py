import asyncio
import os
import re
import json
import random
import aiohttp
import yt_dlp
import logging
from datetime import datetime, timedelta
from typing import Union
from urllib.parse import urlparse

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from VenomMusic import app
from VenomMusic.utils.database import is_on_off
from VenomMusic.utils.formatters import time_to_seconds
from config import API_URL, API_KEY


# ============================================================
# 🔹 LOGGER CONFIGURATION
# ============================================================
LOGGER = logging.getLogger("RocksMusic/Youtube")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


# ============================================================
# 🔹 COOKIE HANDLER
# ============================================================
def cookie_txt_file():
    """Return a random cookie file path if available."""
    cookie_dir = os.path.join(os.getcwd(), "cookies")
    os.makedirs(cookie_dir, exist_ok=True)
    cookies_files = [f for f in os.listdir(cookie_dir) if f.endswith(".txt")]
    if not cookies_files:
        LOGGER.warning("No cookie files found in /cookies")
        return None
    return os.path.join(cookie_dir, random.choice(cookies_files))


# ============================================================
# 🔹 AUTO CLEANUP OLD FILES
# ============================================================
def cleanup_old_downloads(hours: int = 6):
    """Delete downloaded files older than given hours."""
    folder = "downloads"
    if not os.path.exists(folder):
        return
    now = datetime.now()
    count = 0
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            modified_time = datetime.fromtimestamp(os.path.getmtime(path))
            if now - modified_time > timedelta(hours=hours):
                os.remove(path)
                count += 1
    if count > 0:
        LOGGER.info(f"🧹 Cleaned {count} old files from /downloads")


# ============================================================
# 🔹 TELEGRAM CDN REUSE
# ============================================================
async def get_telegram_file(telegram_link: str, video_id: str, file_type: str):
    """Fetch from Telegram CDN (if already uploaded)."""
    try:
        parsed = urlparse(telegram_link)
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:
            return None

        channel_name = parts[0]
        message_id = int(parts[1])

        file_ext = ".webm" if file_type == "audio" else ".mkv"
        file_path = os.path.join("downloads", f"{video_id}{file_ext}")
        os.makedirs("downloads", exist_ok=True)

        msg = await app.get_messages(channel_name, message_id)
        await msg.download(file_name=file_path)
        LOGGER.info(f"✅ Telegram file reused: {file_path}")
        return file_path
    except Exception as e:
        LOGGER.error(f"[Telegram CDN] Error: {e}")
        return None


# ============================================================
# 🔹 API DOWNLOAD HANDLER
# ============================================================
async def download_song(link: str):
    """Download song using API, with Telegram CDN reuse if provided."""
    try:
        cleanup_old_downloads()

        video_id = link.split("v=")[-1].split("&")[0]
        DOWNLOAD_DIR = "downloads"
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        for ext in ["mp3", "m4a", "webm"]:
            file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
            if os.path.exists(file_path):
                LOGGER.info(f"[CACHE] File already exists: {file_path}")
                return file_path

        song_url = f"{API_URL}/song/{video_id}?api={API_KEY}"
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(song_url, timeout=60) as response:
                    if response.status != 200:
                        LOGGER.error(f"API error status: {response.status}")
                        return None
                    data = await response.json()
                    status = data.get("status", "").lower()

                    if status == "downloading":
                        await asyncio.sleep(2)
                        continue
                    elif status == "error":
                        LOGGER.error(f"API error: {data.get('error') or data.get('message')}")
                        return None
                    elif status == "done":
                        if "t.me" in str(data.get("link", "")):
                            LOGGER.info("Found Telegram CDN link, downloading from Telegram...")
                            return await get_telegram_file(data["link"], video_id, "audio")
                        download_url = data.get("link")
                        if not download_url:
                            LOGGER.error("No download link in API response")
                            return None
                        break
                    else:
                        LOGGER.warning(f"Unexpected API status: {status}")
                        return None

            file_format = data.get("format", "mp3").lower()
            file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{file_format}")

            async with session.get(download_url, timeout=aiohttp.ClientTimeout(total=300)) as resp:
                if resp.status != 200:
                    LOGGER.error(f"Download failed with status {resp.status}")
                    return None
                with open(file_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        f.write(chunk)
            LOGGER.info(f"🎵 Downloaded: {file_path}")
            return file_path
    except Exception as e:
        LOGGER.error(f"[download_song] Exception: {e}")
        return None


# ============================================================
# 🔹 FILE SIZE CHECK
# ============================================================
async def check_file_size(link):
    cookie = cookie_txt_file()
    if not cookie:
        return None

    proc = await asyncio.create_subprocess_exec(
        "yt-dlp", "--cookies", cookie, "-J", link,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        LOGGER.error(f"yt-dlp error: {stderr.decode()}")
        return None

    info = json.loads(stdout.decode())
    total = sum(f.get("filesize", 0) for f in info.get("formats", []))
    return total or None


# ============================================================
# 🔹 YouTube API CLASS
# ============================================================
class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link, videoid=None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, msg: Message):
        messages = [msg]
        if msg.reply_to_message:
            messages.append(msg.reply_to_message)
        for m in messages:
            if m.entities:
                for entity in m.entities:
                    if entity.type == MessageEntityType.URL:
                        text = m.text or m.caption
                        return text[entity.offset: entity.offset + entity.length]
        return None

    async def details(self, link, videoid=None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for r in (await results.next())["result"]:
            title = r["title"]
            duration = r["duration"] or "0:00"
            thumb = r["thumbnails"][0]["url"].split("?")[0]
            vidid = r["id"]
            duration_sec = int(time_to_seconds(duration))
        return title, duration, duration_sec, thumb, vidid

    async def download(self, link: str, video=False, songaudio=False, songvideo=False):
        """Handles audio/video downloading using API or yt-dlp fallback."""
        loop = asyncio.get_running_loop()

        # SONG
        if songaudio or songvideo:
            fpath = await download_song(link)
            return fpath, bool(fpath)

        # VIDEO
        elif video:
            if await is_on_off(1):
                downloaded = await download_song(link)
                return downloaded, bool(downloaded)
            else:
                size = await check_file_size(link)
                if size and (size / (1024 * 1024)) > 250:
                    LOGGER.warning("File too large (>250MB) — skipping download")
                    return None, False

                def yt_video_dl():
                    opts = {
                        "format": "best[height<=720][width<=1280]",
                        "outtmpl": "downloads/%(id)s.%(ext)s",
                        "quiet": True,
                        "cookiefile": cookie_txt_file(),
                        "geo_bypass": True,
                        "nocheckcertificate": True,
                    }
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(link, download=True)
                        return os.path.join("downloads", f"{info['id']}.{info['ext']}")

                path = await loop.run_in_executor(None, yt_video_dl)
                LOGGER.info(f"🎬 Video downloaded: {path}")
                return path, True

        # DEFAULT
        else:
            fpath = await download_song(link)
            return fpath, bool(fpath)
