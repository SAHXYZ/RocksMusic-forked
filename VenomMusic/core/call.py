import asyncio
import os
from datetime import datetime, timedelta
from typing import Union
import requests
import yt_dlp

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.types.stream import StreamAudioEnded

import config
from VenomMusic import LOGGER, app
from VenomMusic.misc import db
from VenomMusic.utils.database import (
    add_active_chat,
    get_lang,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
)
from VenomMusic.utils.exceptions import AssistantErr
from strings import get_string

autoend = {}
counter = {}

# =============== HYBRID YOUTUBE AUDIO FETCHER ==================
async def extract_youtube_audio(video_id: str):
    """Try yt-dlp first; if blocked, fallback to NexGenBots API."""
    # 1️⃣ Try yt-dlp
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            if info and info.get("url"):
                LOGGER("VenomMusic").info(f"✅ yt-dlp worked for {info.get('title')}")
                return info["url"], info.get("title")
    except Exception as e:
        LOGGER("VenomMusic").warning(f"⚠️ yt-dlp failed, falling back to NexGen API ({e})")

    # 2️⃣ Fallback: NexGenBots API
    try:
        api_url = f"https://api.nexgenbots.xyz/api/info?id={video_id}&apikey=30DxNexGenBots6533fd"
        res = requests.get(api_url, timeout=10).json()
        if "url" in res and res["url"]:
            LOGGER("VenomMusic").info(f"✅ NexGen API success for {res.get('title', 'Unknown')}")
            return res["url"], res.get("title", "Unknown Title")
        else:
            LOGGER("VenomMusic").error(f"❌ NexGen API returned no URL: {res}")
    except Exception as e:
        LOGGER("VenomMusic").error(f"❌ NexGen API failed: {e}")

    return None, None


# ===================== BASE CALL CLASS ==========================
class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="VenomAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await remove_active_chat(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def stream_call(self, video_id):
        """Stream YouTube video in log group for verification"""
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        link, title = await extract_youtube_audio(video_id)
        if not link:
            LOGGER("VenomMusic").error("❌ No valid YouTube link found to play.")
            return
        try:
            await assistant.join_group_call(
                config.LOG_GROUP_ID,
                AudioPiped(link, audio_parameters=HighQualityAudio()),
                stream_type=StreamType().pulse_stream,
            )
            await asyncio.sleep(3)
            await assistant.leave_group_call(config.LOG_GROUP_ID)
            LOGGER("VenomMusic").info(f"✅ Verified working audio stream for {title}")
        except Exception as e:
            LOGGER("VenomMusic").error(f"❌ Stream error: {e}")

    async def join_call(self, chat_id: int, original_chat_id: int, video_id: str):
        """Main function to join and stream from YouTube."""
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        link, title = await extract_youtube_audio(video_id)
        if not link:
            raise AssistantErr("❌ Unable to extract audio link from YouTube or API.")

        stream = AudioPiped(link, audio_parameters=HighQualityAudio())

        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
            await add_active_chat(chat_id)
            await music_on(chat_id)
            LOGGER("VenomMusic").info(f"🎵 Streaming started for: {title}")
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])
        except Exception as e:
            LOGGER("VenomMusic").error(f"❌ Unknown stream error: {e}")

    async def ping(self):
        """Check average ping of assistants."""
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        return str(round(sum(pings) / len(pings), 3)) if pings else "0.000"

    async def start(self):
        LOGGER(__name__).info("🎧 Starting PyTgCalls Client...")
        if config.STRING1:
            await self.one.start()

    async def decorators(self):
        """Auto-stop on stream end or userbot leave."""
        @self.one.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.one.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        async def stream_end_handler1(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.stop_stream(update.chat_id)


Venom = Call()
