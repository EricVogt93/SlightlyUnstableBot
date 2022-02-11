import discord
from discord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("We have logged in.")

        return await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="sich auf wie Murat"))