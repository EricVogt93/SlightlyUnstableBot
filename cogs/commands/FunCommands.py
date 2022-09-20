import os

import nextcord
from nextcord.ext import commands
from random import randrange

from logic.classes.ConfigHandler import ConfigHandler


class FunCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse FunCommands.Benötigt Instanz vom Discordbot - Objekt.
        :param bot: Object
        """
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "FUNCOMMANDS")
        self.settings = cfg.load()
        self.bot = bot

    @nextcord.slash_command(name="hurensohn", description="Hurensohn des Monats.")
    async def hurensohn(self, bot):
        await bot.send(self.settings["hurensohn"])

    @nextcord.slash_command(name="ja", description="Ja.")
    async def ja(self, bot):
        await bot.send(self.settings["ja"])

    @nextcord.slash_command(name="nein", description="Nein.")
    async def nein(self, bot):
        await bot.send(self.settings["nein"])

    @nextcord.slash_command(name="robinsmutter", description="Titten von Robins Mutter.")
    async def robinsmutter(self, bot):
        await bot.send(self.settings["robins_mutter"])

    @nextcord.slash_command(name="whiteknight", description="Whiteknight des Monats.")
    async def whiteknight(self, bot):
        await bot.send(self.settings["whiteknight"])

    @nextcord.slash_command(name="motherjokes", description="Direkt auf Mutter.")
    async def motherjoke(self, bot):
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "MOMJOKES")
        jokes = cfg.load()
        index = randrange(55)
        joke = jokes[str(index)]
        await bot.send(joke)