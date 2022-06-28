import nextcord
from nextcord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in.")
        print("-------------------------")

        return await self.bot.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="sich auf wie Murat"))
