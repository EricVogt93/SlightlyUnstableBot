import asyncio
from datetime import date

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.helper.DateConverter import DateConverter
from logic.models.MemberModel import MemberModel
from logic.services.TaxService import tax_service


class PlayerCommands(commands.Cog):
    """Handles player management commands."""

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="add_gamer", description="Add a player to the database")
    @commands.has_role("Officer")
    async def add_gamer(self, interaction: Interaction, member: nextcord.Member):
        name = str(member.name)
        discord_id = MemberModel.get_discord_id(member)
        is_trial = BoolBitConverter.bool_to_bit(MemberModel.is_trial(member))
        # New players start with today as their paid_until date (no debt yet)
        initial_paid_until = tax_service.get_initial_paid_until()

        sql = """INSERT INTO player
                 (PLAYER_NAME, DISCORD_ID, IS_TRIAL, TAX_PAID_UNTIL)
                 VALUES (%s, %s, %s, %s)"""
        val = (name, discord_id, is_trial, initial_paid_until)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()

        msg = f"Player {member.name} added to database! Tax payments start from {initial_paid_until}."
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="delete_gamer", description="Löscht Spieler aus Datenbank.")
    @commands.has_role("Officer")
    async def delete_gamer(self, interaction: Interaction, member: nextcord.Member):
        id = MemberModel.get_discord_id(member)
        query = f"DELETE FROM player WHERE DISCORD_ID=(%s)"
        val = (id,)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query, val)
        db.close()
        msg = f"Spieler {member.name} gelöscht!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="add_vacation", description="Fügt Urlaubsdaten für Spieler hinzu.")
    @commands.has_role("Officer")
    async def add_vacation(self, interaction: Interaction, member: nextcord.Member, vacation_start, vacation_end=None):
        query = ""
        id = MemberModel.get_discord_id(member)
        date_begin = DateConverter.formate_date_for_db(vacation_start)

        if vacation_end is None:
            sql = "UPDATE player SET VACATION_START=%s WHERE DISCORD_ID=%s"
            val = (date_begin, id)
        else:
            date_end = DateConverter.formate_date_for_db(vacation_end)
            sql = "UPDATE player SET VACATION_START=%s, VACATION_END=%s WHERE DISCORD_ID=%s"
            val = (date_begin, date_end, id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"Urlaub added für {member.name}!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="end_vacation", description="Fügt Urlaubsende für Spieler hinzu.")
    @commands.has_role("Officer")
    async def end_vacation(self, interaction: Interaction, member: nextcord.Member, vacation_end=None):
        id = MemberModel.get_discord_id(member)

        if vacation_end is None:
            vacation_end = DateConverter.get_current_date()

        date = DateConverter.formate_date_for_db(vacation_end)

        sql = "UPDATE player SET VACATION_END=%s WHERE DISCORD_ID=%s"
        val = (date, id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"Urlaubsende({date}) added für {member.name}!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="get_players_in_vacation",
                            description="Returns all players currently on vacation")
    @commands.has_role("Officer")
    async def get_players_in_vacation(self, interaction: Interaction):
        await asyncio.sleep(1)
        today = DateConverter.get_current_date()
        db_today = DateConverter.formate_date_for_db(today)
        sql = "SELECT * FROM player WHERE VACATION_END > %s OR (VACATION_END IS NULL AND VACATION_START < %s)"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(sql, (db_today, db_today))
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        msg = self.build_vacation_msg(data)
        if msg == "":
            msg = "Niemand ist momentan im Urlaub!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="add_tax", description="Record tax payment for a player")
    @commands.has_role("Officer")
    async def add_tax(self, interaction: Interaction, member: nextcord.Member, amount: int):
        """
        Add tax payment for a player. Updates their paid_until date.

        Args:
            member: The player who paid
            amount: Amount of tax paid
        """
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive!", ephemeral=True)
            return

        discord_id = MemberModel.get_discord_id(member)

        # Get current paid_until date
        db = DatabaseConnector()
        db.connect()
        result = db.fetch_data_query(
            "SELECT TAX_PAID_UNTIL FROM player WHERE DISCORD_ID = %s",
            (discord_id,)
        )

        if not result:
            db.close()
            await interaction.response.send_message(f"Player {member.name} not found!", ephemeral=True)
            return

        current_paid_until = result[0][0]  # Could be None or a date

        # Calculate new paid_until date
        new_paid_until = tax_service.calculate_new_paid_until(current_paid_until, amount)

        # Update database
        db.write_data_query(
            "UPDATE player SET TAX_PAID_UNTIL = %s WHERE DISCORD_ID = %s",
            (new_paid_until, discord_id)
        )
        db.close()

        # Get updated status
        status = tax_service.calculate_status(new_paid_until, member.name)

        msg = f"Added {amount} {tax_service.tax_name} for {member.name}!\n{tax_service.format_status_message(status)}"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="fetch_all", description="Show tax status for all players")
    @commands.has_role("Officer")
    async def fetch_all(self, interaction: Interaction):
        """Show tax payment status for all players."""
        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(
            "SELECT PLAYER_NAME, TAX_PAID_UNTIL FROM player ORDER BY TAX_PAID_UNTIL ASC"
        )
        db.close()

        if not raw_data:
            await interaction.response.send_message("No players found!", ephemeral=True)
            return

        msg = "**Tax Status Overview**\n\n"
        for row in raw_data:
            name, paid_until = row[0], row[1]
            status = tax_service.calculate_status(paid_until, name)
            msg += tax_service.format_status_message(status) + "\n"

        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="tax", description="Check tax status for a player")
    async def tax(self, interaction: Interaction, member: nextcord.Member):
        """Check tax payment status for a specific player."""
        discord_id = MemberModel.get_discord_id(member)

        db = DatabaseConnector()
        db.connect()
        result = db.fetch_data_query(
            "SELECT TAX_PAID_UNTIL FROM player WHERE DISCORD_ID = %s",
            (discord_id,)
        )
        db.close()

        if not result:
            await interaction.response.send_message(f"Player {member.name} not found!", ephemeral=True)
            return

        paid_until = result[0][0]
        status = tax_service.calculate_status(paid_until, member.name)

        msg = f"**Tax Status for {member.name}**\n\n"
        msg += tax_service.format_status_message(status)
        msg += f"\n\nTax rate: {tax_service.tax_per_week} {tax_service.tax_name}/week"

        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    def build_vacation_msg(self, data) -> str:
        """Build a message showing vacation status for members."""
        msg = ""
        try:
            for member in data:
                if member.vacation_end != "None":
                    vacation_end = member.vacation_end.replace("'", "")
                    d = DateConverter.formate_date_for_bot(vacation_end)
                    msg += f"- {member.name} returns on {d}.\n"
                else:
                    msg += f"- {member.name} returns at some point.\n"
        except (AttributeError, TypeError) as e:
            raise RuntimeError(f"Failed to build vacation message: {e}")
        return msg
