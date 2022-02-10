import os

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.HelpGenerator import HelpHandler
from discord.ext import commands


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "URL").load()
        self.settings = cfg.load()
        self.bot = bot

    @commands.command(pass_context=True)
    async def gildentab(self):
        userid = self.bot.user.id
        url = self.cfg["spreadsheet_path"]
        msg = f"Gildentabelle: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def wowaudit(self):
        userid = self.bot.user.id
        url = self.cfg["wowaudit_path"]
        msg = f"Raidanmeldungen: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def progress(self):
        userid = self.bot.user.id
        url = self.cfg["progstats_path"]
        msg = f"Progressseite: {url}"
        self.send_pm(userid, msg)

    @commands.command(pass_context=True)
    async def help(self):
        helper = HelpHandler()
        # ToDo: Message Author Rolle filtern und entsprechende Hilfe ausgeben
        embView = helper.getHelpTextOfficer()
        await self.bot.send(embed=embView)

    async def send_pm(self, userid, msg):
        await self.bot.send_message(userid, msg)
