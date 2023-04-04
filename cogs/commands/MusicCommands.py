import os
from collections import deque

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import yt_dlp

from logic.classes.ConfigHandler import ConfigHandler

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse FunCommands.Benötigt Instanz vom Discordbot - Objekt.
        :param bot: Object
        """
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "FUNCOMMANDS")
        self.settings = cfg.load()
        self.bot = bot
        self.queue = deque()

    @nextcord.slash_command(name="join", description="Bot joined den Channel.")
    async def join(self, interaction: Interaction):
        channel = interaction.user.voice.channel
        await channel.connect()

    @nextcord.slash_command(name="leave", description="Bot verlässt den Channel.")
    async def leave(self, interaction: Interaction):
        await interaction.guild.voice_client.disconnect()

    @nextcord.slash_command(name="play", description="Spielt Musik ab.")
    async def play(self, interaction: Interaction, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'noplaylist': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    self.queue.append(entry['url'])
            else:
                self.queue.append(info['url'])

            if not interaction.guild.voice_client.is_playing():
                await self.play_next_in_queue(interaction.guild)

    async def play_next_in_queue(self, guild):
        if self.queue:
            url2 = self.queue.popleft()
            FFMPEG_OPTIONS = {
                'options': '-vn -nostats -loglevel 0',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            }
            voice_client = guild.voice_client
            voice_client.stop()
            voice_client.play(nextcord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **FFMPEG_OPTIONS), after=lambda e: self.bot.loop.create_task(self.play_next_in_queue(guild)))
        else:
            await guild.voice_client.disconnect()

