import nextcord
from nextcord.ext import commands

from logic import settings


class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        settings.dictionary["last_message_author"] = message.author
