import os

from datetime import datetime

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from logic import settings
from logic.classes.MessageFilter import MessageFilter
from logic.classes.OutputHandler import OutputHandler
from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.HelpGenerator import HelpHandler
from logic.helper.DateConverter import DateConverter
from logic.models.MemberModel import MemberModel


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

    @nextcord.slash_command(name="w", description="Schreibe privat einen Spieler an.")
    async def w(self, interaction: Interaction, member: nextcord.Member, msg):

        filter = MessageFilter(msg)
        if(filter.check_all()):
            await interaction.response.send_message("Message wurde gefiltert fetter Hurensohn.", ephemeral=True)

        sender_name = interaction.user.name
        receiver_name = MemberModel.get_member_name(member)

        d = datetime.now()
        today = DateConverter.get_current_date()
        time = DateConverter.format_date_for_db(d)
        date = DateConverter.formate_date_for_db(today)

        sql = f"INSERT INTO messages " \
              f"(DATE, TIME, SENDER, MSG, RECEIVER)" \
              f"VALUES(%s, %s, %s, %s, %s);"
        val = (date, time, sender_name, msg, receiver_name)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()

        await OutputHandler.send_pm(member, msg)
        await interaction.response.send_message("Message send.", ephemeral=True)

    async def send_pm(self, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
