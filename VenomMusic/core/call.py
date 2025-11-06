import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall, TelegramServerError
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config
from VenomMusic import LOGGER, app
from VenomMusic.misc import db
from VenomMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from VenomMusic.utils.exceptions import AssistantErr
from VenomMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from VenomMusic.utils.inline.play import stream_markup
from VenomMusic.utils.stream.autoclear import auto_clean
from VenomMusic.utils.thumbnails import gen_thumb
from strings import get_string

import yt_dlp

autoend = {}
counter = {}


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


# ======= New YouTube extractor using yt-dlp =======
async def extract_youtube_audio(video_id: str):
    """Extract best audio URL from YouTube using yt-dlp."""
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get("url"), info.get("title")
    except Exception as e:
        LOGGER("VenomMusic").error(f"❌ YouTube extraction failed: {e}")
        return None, None


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="VenomAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            name="VenomAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            name="VenomAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            name="VenomAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            name="VenomAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
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
            raise AssistantErr("❌ Unable to extract audio link from YouTube.")

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

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        if config.STRING4:
            pings.append(await self.four.ping)
        if config.STRING5:
            pings.append(await self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
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
