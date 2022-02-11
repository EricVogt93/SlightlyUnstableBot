import os

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.HelpGenerator import HelpHandler
from discord.ext import commands


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse MessageCommands. Benötigt Instanz vom Discordbot - Objekt.
        :param bot:
        """
        cfg_obj = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "URL")
        self.cfg = cfg_obj.load()
        self.bot = bot

    @commands.command(pass_context=True)
    async def gildentab(self):
        """
        Gibt Gildenexcel - URL zurück.
        """
        userid = self.bot.user.id
        url = self.cfg["spreadsheet_path"]
        msg = f"Gildentabelle: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def wowaudit(self):
        """
        Gibt WoWAudit - URL zurück.
        """
        userid = self.bot.user.id
        url = self.cfg["wowaudit_path"]
        msg = f"Raidanmeldungen: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def progress(self):
        """
        Gibt Progress - Pfad zurück.
        """
        userid = self.bot.user.id
        url = self.cfg["progstats_path"]
        msg = f"Progressseite: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def help(self):
        """
        Gibt Hilfekontext zurück.
        """
        helper = HelpHandler()
        # ToDo: Message Author Rolle filtern und entsprechende Hilfe ausgeben
        embView = helper.getHelpTextOfficer()
        await self.bot.send(embed=embView)

    async def send_pm(self, userid, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param userid: Int
        :param msg: String
        """
        await self.bot.send_message(userid, msg)
