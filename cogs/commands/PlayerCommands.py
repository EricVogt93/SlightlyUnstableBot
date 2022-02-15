import discord

from discord.ext import commands
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.helper.DateConverter import DateConverter
from logic.models.MemberModel import MemberModel


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def add_gamer(self, ctx, member: discord.Member):
        name = str(member.name)
        id = MemberModel.get_discord_id(member)
        is_trial_bool = MemberModel.is_trial(member)
        is_trial = BoolBitConverter.bool_to_bit(is_trial_bool)

        query = f"INSERT INTO player (PLAYER_NAME, DISCORD_ID, IS_TRIAL) VALUES ('{name}', {id}, {is_trial});"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def delete_gamer(self, ctx, member: discord.Member):
        id = MemberModel.get_discord_id(member)
        query = f"DELETE FROM player WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def add_vacation(self, ctx, member: discord.Member, vacation_start, vacation_end = None):
        query = ""
        id = MemberModel.get_discord_id(member)
        date_begin = DateConverter.formate_date_for_db(vacation_start)

        if vacation_end is None:
            query = f"UPDATE player SET VACATION_START='{date_begin}' WHERE DISCORD_ID={id}"
        else:
            date_end = DateConverter.formate_date_for_db(vacation_end)
            query = f"UPDATE player SET VACATION_START='{date_begin}', VACATION_END='{date_end}' WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def end_vacation(self, ctx, member: discord.Member, vacation_end = None):
        id = MemberModel.get_discord_id(member)

        if vacation_end is None:
            vacation_end = DateConverter.get_current_date()

        date = DateConverter.formate_date_for_db(vacation_end)

        query = f"UPDATE player SET VACATION_END='{date}' WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def add_flask(self, ctx, member: discord.Member, flask):
        id = MemberModel.get_discord_id(member)
        query = f"UPDATE player SET FLASK_SPEND={flask} WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()
