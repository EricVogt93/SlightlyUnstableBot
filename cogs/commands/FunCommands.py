import os

from logic.classes.ConfigHandler import ConfigHandler
from discord.ext import commands


class FunCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse FunCommands.Benötigt Instanz vom Discordbot - Objekt.
        :param bot: Object
        """
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "FUNCOMMANDS")
        self.settings = cfg.load()
        self.bot = bot

    @commands.command(pass_context=True)
    async def hurensohns(self, bot):
        await bot.send(self.settings["hurensohn"])

    @commands.command(pass_context=True)
    async def ja(self, bot):
        await bot.send(self.settings["ja"])

    @commands.command(pass_context=True)
    async def nein(self, bot):
        await bot.send(self.settings["nein"])

    @commands.command(pass_context=True)
    async def robinsmutter(self, bot):
        await bot.send(self.settings["robins_mutter"])

    @commands.command(pass_context=True)
    async def whiteknight(self, bot):
        await bot.send(self.settings["whiteknight"])

    @commands.command(pass_context=True)
    async def jeremy(self, bot):
        await bot.send(self.settings["jeremy"])
