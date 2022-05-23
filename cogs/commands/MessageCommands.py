import os

from logic import settings
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
    async def gildentab(self, ctx):
        """
        Gibt Gildenexcel - URL zurück.
        """
        user_obj = settings.dictionary["last_message_author"]
        url = self.cfg["spreadsheet_path"]
        msg = f"Gildentabelle: {url}"
        await self.send_pm(ctx, ctx.author, msg)

    @commands.command(pass_context=True)
    async def wowaudit(self, ctx):
        """
        Gibt WoWAudit - URL zurück.
        """
        url = self.cfg["wowaudit_path"]
        msg = f"Raidanmeldungen: {url}"
        await self.send_pm(ctx, ctx.author, msg)

    @commands.command(pass_context=True)
    async def progress(self, ctx):
        """
        Gibt Progress - Pfad zurück.
        """
        url = self.cfg["progstats_path"]
        msg = f"Progressseite: {url}"
        await self.send_pm(ctx, ctx.author, msg)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        """
        Gibt Hilfekontext zurück.
        """
        helper = HelpHandler()
        # ToDo: Message Author Rolle filtern und entsprechende Hilfe ausgeben
        embView = helper.getHelpTextOfficer()
        await ctx.send(embed=embView)

    async def send_pm(self, ctx, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)