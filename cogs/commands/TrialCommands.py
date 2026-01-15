import asyncio

import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.models.MemberModel import MemberModel


class TrialCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @nextcord.slash_command(name="show_trials", description="Shows all trial members")
    async def show_trials(self, interaction: Interaction):
        await asyncio.sleep(1)
        bit = BoolBitConverter.bool_to_bit(True)
        query = "SELECT * FROM player WHERE IS_TRIAL = %s"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query, (bit,))
        db.close()
        data = MemberModel.parse_data(self.bot, raw_data)

        msg = ""
        i = 1
        for member in data:
            msg += f"{i} - {member.name}; {member.discord_id}\n"
            i += 1

        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @commands.has_role("Officer")
    @nextcord.slash_command(name="make_trial", description="Startet Flask - Reminder")
    async def make_trial(self, interaction: Interaction, member: nextcord.Member):
        await asyncio.sleep(1)
        sql = f"UPDATE player SET IS_TRIAL=%s WHERE DISCORD_ID=%s"
        val = (1, member.id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()

        msg = f"Spieler {member.name} ist jetzt Trial."
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @commands.has_role("Officer")
    @nextcord.slash_command(name="kick_trial", description="Startet Flask - Reminder")
    async def kick_trial(self, interaction: Interaction, member: nextcord.Member, reason=None):
        msg = ""
        if not reason:
            await member.kick()
            msg = f"{member} wurde gekickt."
        else:
            await member.kick(reason=reason)
            msg = f"{member} wurde gekickt. Begründung: {reason}."
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")
