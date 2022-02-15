import discord

from discord.ext import commands
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.models.MemberModel import MemberModel


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @commands.command(pass_context=True)
    async def add_gamer(self, ctx, member: discord.Member):
        name = str(member.name)
        id = MemberModel.get_discord_id(member)
        is_trial_bool = MemberModel.is_trial(member)
        is_trial = BoolBitConverter.bool_to_bit(is_trial_bool)

        query = f"INSERT INTO player (PLAYER_NAME, DISCORD_ID, IS_TRIAL) VALUES ('{name}', {id}, {is_trial});"

        db = DatabaseConnector()
        db.connect()
        db.execute_query(query)
        db.close()
