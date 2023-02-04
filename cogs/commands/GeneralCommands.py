import asyncio

import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.helper.BoolBitConverter import BoolBitConverter


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @nextcord.slash_command(name="mute_bot", description="Mute alle Nachrichten vom Bot.")
    async def mute_bot(self, interaction: Interaction):
        await asyncio.sleep(1)
        val = 1

        if self.get_muted_status(interaction.user.id):
            val = 0
        else:
            val = 1

        sql = f"UPDATE player SET IS_MUTED=%s WHERE DISCORD_ID=%s"
        values = (val, interaction.user.id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, values)
        db.close()

        await interaction.response.send_message("Done.")

    @staticmethod
    def get_muted_status(id):
        db = DatabaseConnector()
        db.connect()
        query = f"SELECT IS_MUTED FROM player WHERE DISCORD_ID={id};"
        value = db.fetch_data_query(query)
        db.close()
        return BoolBitConverter.bit_to_bool(value[0][0])
