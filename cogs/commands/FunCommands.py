import os

from logic.classes.ConfigHandler import ConfigHandler
from discord.ext import commands


class FunCommands:
    def __init__(self, bot):
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "FUNCOMMANDS")
        self.settings = cfg.load()
        self.bot = bot

    @commands.command(pass_context=True)
    async def hurensohn(self, ctx):
        await ctx.send(self.settings["hurensohn"])

    @commands.command(pass_context=True)
    async def ja(self, ctx):
        await ctx.send(self.settings["ja"])

    @commands.command(pass_context=True)
    async def nein(self, ctx):
        await ctx.send(self.settings["nein"])

    @commands.command(pass_context=True)
    async def robinsmutter(self, ctx):
        await ctx.send(self.settings["robins_mutter"])

    @commands.command(pass_context=True)
    async def whiteknight(self, ctx):
        await ctx.send(self.settings["whiteknight"])

    @commands.command(pass_context=True)
    async def jeremy(self, ctx):
        await ctx.send(self.settings["jeremy"])
