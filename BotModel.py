import logging
import os
from typing import Optional

import nextcord
from nextcord.ext import commands

from cogs.CommandRegisterService import CommandRegisterService
from logic.helper.singleton import Singleton

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)


class BotModel(metaclass=Singleton):
    """Main Discord bot model handling initialization and lifecycle."""

    def __init__(self) -> None:
        self.prefix: str = "/"
        self.intents: nextcord.Intents = nextcord.Intents.all()
        self.bot: Optional[commands.Bot] = None
        self.is_debug_mode: bool = "PYCHARM_HOSTED" in os.environ

    def start_bot(self) -> None:
        """Initialize and start the Discord bot."""
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN environment variable is not set")

        self.bot = commands.Bot(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=self.intents,
            help_command=None
        )
        self.register_cogs()
        self.bot.run(token)

    def get_bot_obj(self) -> Optional[commands.Bot]:
        """Return the Discord bot instance."""
        return self.bot

    def get_debug_mode(self) -> bool:
        """Return whether the bot is running in debug mode."""
        return self.is_debug_mode

    def register_cogs(self) -> None:
        """Register all command cogs with the bot."""
        crs = CommandRegisterService(self.bot)
        crs.register_events()
        crs.register_commands()
