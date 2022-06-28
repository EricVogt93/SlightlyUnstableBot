import os

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from logic import settings
from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.HelpGenerator import HelpHandler


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse MessageCommands. Benötigt Instanz vom Discordbot - Objekt.
        :param bot:
        """
        cfg_obj = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "URL")
        self.cfg = cfg_obj.load()
        self.bot = bot

    @nextcord.slash_command(name="gildentab", description="Gibt Link zur (deprecated) Gildenexcel zurück.")
    async def gildentab(self, interaction: Interaction):
        """
        Gibt Gildenexcel - URL zurück.
        """
        user_obj = settings.dictionary["last_message_author"]
        url = self.cfg["spreadsheet_path"]
        msg = f"Gildentabelle: {url}"
        await self.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="wowaudit", description="Gibt Link zu wowaudit zurück.")
    async def wowaudit(self, interaction: Interaction):
        """
        Gibt WoWAudit - URL zurück.
        """
        url = self.cfg["wowaudit_path"]
        msg = f"Raidanmeldungen: {url}"
        await self.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="progress", description="Gibt Link zur Progress-Seite zurück.")
    async def progress(self, interaction: Interaction):
        """
        Gibt Progress - Pfad zurück.
        """
        url = self.cfg["progstats_path"]
        msg = f"Progressseite: {url}"
        await self.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="help", description="Gibt Hilfe zurück.")
    async def help(self, interaction: Interaction):
        """
        Gibt Hilfekontext zurück.
        """
        helplist = list()
        helplist.append(HelpHandler().get_player_cmd_help())
        helplist.append(HelpHandler().get_character_cmd_help())
        helplist.append(HelpHandler().get_trial_cmd_help())
        helplist.append(HelpHandler().get_message_cmd_help())
        helplist.append(HelpHandler().get_fun_cmd_help())
        helplist.append(HelpHandler().get_reminder_cmd_help())

        for embView in helplist:
            await interaction.send(embed=embView)

    async def send_pm(self, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
