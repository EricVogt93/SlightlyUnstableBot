"""Music commands for playing audio in voice channels."""
import logging
from collections import deque
from typing import Optional

import nextcord
from nextcord.ext import commands
from nextcord import Interaction

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

logger = logging.getLogger(__name__)

# FFmpeg options for audio streaming
FFMPEG_OPTIONS = {
    'options': '-vn -nostats -loglevel 0',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

# yt-dlp options
YDL_OPTIONS = {
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


class MusicCommands(commands.Cog):
    """Handles music playback in voice channels."""

    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()

    @nextcord.slash_command(name="join", description="Bot joins your voice channel")
    async def join(self, interaction: Interaction):
        """Join the user's voice channel."""
        if not interaction.user.voice:
            await interaction.response.send_message(
                "You need to be in a voice channel!", ephemeral=True
            )
            return

        channel = interaction.user.voice.channel

        try:
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}!")
        except Exception as e:
            logger.error(f"Failed to join voice channel: {e}")
            await interaction.response.send_message(
                "Failed to join voice channel.", ephemeral=True
            )

    @nextcord.slash_command(name="leave", description="Bot leaves the voice channel")
    async def leave(self, interaction: Interaction):
        """Leave the current voice channel."""
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "I'm not in a voice channel!", ephemeral=True
            )
            return

        try:
            await interaction.guild.voice_client.disconnect()
            self.queue.clear()
            await interaction.response.send_message("Left the voice channel.")
        except Exception as e:
            logger.error(f"Failed to leave voice channel: {e}")
            await interaction.response.send_message(
                "Failed to leave voice channel.", ephemeral=True
            )

    @nextcord.slash_command(name="play", description="Play audio from a URL")
    async def play(self, interaction: Interaction, url: str):
        """Play audio from a YouTube URL."""
        if not YT_DLP_AVAILABLE:
            await interaction.response.send_message(
                "yt-dlp is not installed!", ephemeral=True
            )
            return

        if not interaction.user.voice:
            await interaction.response.send_message(
                "You need to be in a voice channel!", ephemeral=True
            )
            return

        # Auto-join if not already connected
        if not interaction.guild.voice_client:
            try:
                await interaction.user.voice.channel.connect()
            except Exception as e:
                logger.error(f"Failed to auto-join voice channel: {e}")
                await interaction.response.send_message(
                    "Failed to join your voice channel.", ephemeral=True
                )
                return

        await interaction.response.defer()

        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)

                if info is None:
                    await interaction.followup.send("Could not extract audio from URL.")
                    return

                # Handle playlists
                if 'entries' in info:
                    for entry in info['entries']:
                        if entry and 'url' in entry:
                            self.queue.append(entry['url'])
                    await interaction.followup.send(
                        f"Added {len(info['entries'])} tracks to queue."
                    )
                else:
                    self.queue.append(info['url'])
                    title = info.get('title', 'Unknown')
                    await interaction.followup.send(f"Added to queue: {title}")

                # Start playing if not already
                if not interaction.guild.voice_client.is_playing():
                    await self.play_next_in_queue(interaction.guild)

        except Exception as e:
            logger.error(f"Failed to play audio: {e}")
            await interaction.followup.send(f"Failed to play: {str(e)[:100]}")

    @nextcord.slash_command(name="skip", description="Skip the current track")
    async def skip(self, interaction: Interaction):
        """Skip to the next track in queue."""
        if not interaction.guild.voice_client:
            await interaction.response.send_message(
                "Not playing anything!", ephemeral=True
            )
            return

        interaction.guild.voice_client.stop()
        await interaction.response.send_message("Skipped!")

    @nextcord.slash_command(name="queue", description="Show the current queue")
    async def show_queue(self, interaction: Interaction):
        """Show the current music queue."""
        if not self.queue:
            await interaction.response.send_message("Queue is empty!")
            return

        queue_list = list(self.queue)[:10]  # Show max 10
        msg = f"**Queue ({len(self.queue)} tracks):**\n"
        for i, url in enumerate(queue_list, 1):
            msg += f"{i}. {url[:50]}...\n"

        if len(self.queue) > 10:
            msg += f"...and {len(self.queue) - 10} more"

        await interaction.response.send_message(msg)

    async def play_next_in_queue(self, guild: nextcord.Guild) -> None:
        """Play the next track in the queue."""
        if not self.queue:
            if guild.voice_client:
                await guild.voice_client.disconnect()
            return

        if not guild.voice_client:
            return

        url = self.queue.popleft()
        voice_client = guild.voice_client

        try:
            voice_client.stop()
            source = nextcord.FFmpegPCMAudio(
                executable="ffmpeg",
                source=url,
                **FFMPEG_OPTIONS
            )
            voice_client.play(
                source,
                after=lambda e: self.bot.loop.create_task(
                    self.play_next_in_queue(guild)
                )
            )
        except Exception as e:
            logger.error(f"Failed to play next track: {e}")
            # Try next track
            await self.play_next_in_queue(guild)

