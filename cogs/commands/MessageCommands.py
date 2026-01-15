"""Message and information commands."""
import logging
import os
from datetime import datetime
from typing import Optional

import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord.utils import get

from cogs.commands.GeneralCommands import GeneralCommands
from logic.classes.MessageFilter import MessageFilter
from logic.classes.OutputHandler import OutputHandler
from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.DatabaseConnector import get_db
from logic.classes.HelpGenerator import HelpHandler
from logic.helper.DateConverter import DateConverter
from logic.models.MemberModel import MemberModel

logger = logging.getLogger(__name__)


class MessageCommands(commands.Cog):
    """Handles messaging and information commands."""

    def __init__(self, bot):
        cfg_obj = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "URL")
        self.cfg = cfg_obj.load()
        self.bot = bot

    @nextcord.slash_command(name="gildentab", description="Returns link to guild spreadsheet")
    async def gildentab(self, interaction: Interaction):
        """Return guild spreadsheet URL."""
        url = self.cfg.get("spreadsheet_path", "Not configured")
        await interaction.response.send_message(f"Guild spreadsheet: {url}")

    @nextcord.slash_command(name="wowaudit", description="Returns link to WoW Audit")
    async def wowaudit(self, interaction: Interaction):
        """Return WoW Audit URL."""
        url = self.cfg.get("wowaudit_path", "Not configured")
        await interaction.response.send_message(f"Raid signups: {url}")

    @nextcord.slash_command(name="progress", description="Returns link to progress page")
    async def progress(self, interaction: Interaction):
        """Return progress tracking URL."""
        url = self.cfg.get("progstats_path", "Not configured")
        await interaction.response.send_message(f"Progress page: {url}")

    @nextcord.slash_command(name="help", description="Show available commands")
    async def help(self, interaction: Interaction):
        """Show help for all command categories."""
        help_handler = HelpHandler()
        help_embeds = [
            help_handler.get_player_cmd_help(),
            help_handler.get_character_cmd_help(),
            help_handler.get_trial_cmd_help(),
            help_handler.get_message_cmd_help(),
            help_handler.get_fun_cmd_help(),
            help_handler.get_reminder_cmd_help()
        ]

        await interaction.response.defer()
        for embed in help_embeds:
            if embed:
                await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="w", description="Send a whisper message to a player")
    async def w(self, interaction: Interaction, member: nextcord.Member, message: str):
        """Send a private message to another player."""
        sender_name = interaction.user.name

        # Filter messages
        msg_filter = MessageFilter(message, sender_name)
        filter_result = msg_filter.check_all()
        if filter_result:
            await interaction.response.send_message(
                f"Message was filtered: {filter_result}", ephemeral=True
            )
            return

        # Check if receiver has muted the bot
        discord_id = MemberModel.get_discord_id(member)
        if GeneralCommands.get_muted_status(discord_id):
            await interaction.response.send_message(
                "Receiver has muted bot messages.", ephemeral=True
            )
            return

        receiver_name = MemberModel.get_member_name(member)
        now = datetime.now()
        date_str = DateConverter.formate_date_for_db(DateConverter.get_current_date())
        time_str = DateConverter.format_date_for_db(now)

        # Store message in database
        with get_db() as db:
            db.write_data_query(
                "INSERT INTO messages (DATE, TIME, SENDER, MSG, RECEIVER) VALUES (%s, %s, %s, %s, %s)",
                (date_str, time_str, sender_name, message, receiver_name)
            )
            result = db.fetch_data_query(
                "SELECT MSG_ID FROM messages WHERE DATE = %s AND TIME = %s AND SENDER = %s",
                (date_str, time_str, sender_name)
            )
            msg_id = result[0][0] if result else 0

        await OutputHandler.send_pm(member, f"[MessageID:{msg_id}]: {message}")
        await interaction.response.send_message("Message sent.", ephemeral=True)

    @nextcord.slash_command(name="r", description="Reply to a message by ID")
    async def reply(self, interaction: Interaction, msg_id: int, message: str):
        """Reply to a message using its ID."""
        sender_name = interaction.user.name

        # Filter messages
        msg_filter = MessageFilter(message, sender_name)
        filter_result = msg_filter.check_all()
        if filter_result:
            await interaction.response.send_message(
                f"Message was filtered: {filter_result}", ephemeral=True
            )
            return

        # Get original sender
        with get_db() as db:
            result = db.fetch_data_query(
                "SELECT SENDER FROM messages WHERE MSG_ID = %s",
                (msg_id,)
            )

        if not result:
            await interaction.response.send_message(
                "Message not found!", ephemeral=True
            )
            return

        receiver_name = result[0][0]

        # Find the member
        member = None
        for guild in self.bot.guilds:
            member = get(guild.members, name=receiver_name)
            if member:
                break

        if not member:
            await interaction.response.send_message(
                f"Could not find user {receiver_name}.", ephemeral=True
            )
            return

        # Store reply
        now = datetime.now()
        date_str = DateConverter.formate_date_for_db(DateConverter.get_current_date())
        time_str = DateConverter.format_date_for_db(now)

        with get_db() as db:
            db.write_data_query(
                "INSERT INTO messages (DATE, TIME, SENDER, MSG, RECEIVER) VALUES (%s, %s, %s, %s, %s)",
                (date_str, time_str, sender_name, message, receiver_name)
            )
            result = db.fetch_data_query(
                "SELECT MSG_ID FROM messages WHERE DATE = %s AND TIME = %s AND SENDER = %s",
                (date_str, time_str, sender_name)
            )
            new_msg_id = result[0][0] if result else 0

        await OutputHandler.send_pm(member, f"[Reply to {msg_id}][MessageID:{new_msg_id}]: {message}")
        await interaction.response.send_message("Reply sent.", ephemeral=True)

