import os

from datetime import datetime

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from cogs.commands.GeneralCommands import GeneralCommands
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

    @nextcord.slash_command(name="w", description="Gibt Nachricht an.")
    async def w(self, interaction: Interaction, member: nextcord.Member, msg):
        sender_name = interaction.user.name

        # Filtere Nachrichten nach bestimmten Kriterien
        filter = MessageFilter(msg, sender_name)
        result = filter.check_all()
        if result != "":
            await interaction.response.send_message(f"Message wurde gefiltert fetter Hurensohn. {result}",
                                                    ephemeral=True)
            return
        id = MemberModel.get_discord_id(member)
        if GeneralCommands.get_muted_status(id) == 1:
            await interaction.response.send_message(f"Receiver hat den Bot gemuted.", ephemeral=True)
            return

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
        msg_id = self.get_msg_id(date, time, sender_name)

        await OutputHandler.send_pm(member, f"[MessageID:{msg_id}]: " + msg)
        await interaction.response.send_message("Message send.", ephemeral=True)

    async def r(self, interaction: Interaction, msg_id, msg):
        sender_name = interaction.user.name
        filter = MessageFilter(msg, sender_name)
        result = filter.check_all()
        receiver_name = self.get_sender_from_msg_id(msg_id)

        if result != "":
            await interaction.response.send_message(f"Message wurde gefiltert fetter Hurensohn. {result}", ephemeral=True)
            return

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
        msg_id = self.get_msg_id(date, time, sender_name)

        sender_id = self.get_sender_from_msg_id(msg_id)
        member = MemberModel.get_member_obj(self.bot, sender_id)

        await OutputHandler.send_pm(member, f"[MessageID:{msg_id}]: " + msg)
        await interaction.response.send_message("Message send.", ephemeral=True)

    def get_msg_id(self, date, time, sender_name):
        query = f"SELECT MSG_ID FROM messages WHERE DATE='{date}' AND TIME='{time}' AND SENDER='{sender_name}'"
        db = DatabaseConnector()
        db.connect()
        result = db.fetch_data_query(query)
        db.close()
        return result[0][0]

    def get_sender_from_msg_id(self, msg_id):
        query = f"SELECT SENDER FROM messages WHERE MSG_ID='{msg_id}'"
        db = DatabaseConnector()
        db.connect()
        result = db.fetch_data_query(query)
        db.close()
        return result[0][0]

