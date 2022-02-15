import asyncio
from datetime import date

import discord

from discord.ext import commands

from logic import settings
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
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
    async def add_gamer(self, ctx, member: discord.Member, joined_mid_year: bool):
        name = str(member.name)
        id = MemberModel.get_discord_id(member)
        is_trial_bool = MemberModel.is_trial(member)
        is_trial = BoolBitConverter.bool_to_bit(is_trial_bool)
        id_joined = self.get_joined_id(joined_mid_year)

        query = f"INSERT INTO player " \
                f"(PLAYER_NAME, DISCORD_ID, IS_TRIAL, JOINED_ID) VALUES " \
                f"('{name}', {id}, {is_trial}, {id_joined});"

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
    async def add_vacation(self, ctx, member: discord.Member, vacation_start, vacation_end=None):
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
    async def end_vacation(self, ctx, member: discord.Member, vacation_end=None):
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
    async def get_vacation_players(self, ctx):
        await asyncio.sleep(1)
        member = settings.dictionary["last_message_author"]
        today = DateConverter.get_current_date()
        db_today = DateConverter.formate_date_for_db(today)
        query = f"SELECT * FROM player " \
                f"WHERE VACATION_END>'{db_today}' " \
                f"OR VACATION_END IS NULL"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        msg = self.build_vacation_msg(data)
        await OutputHandler.send_pm(member, msg)

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def add_flask(self, ctx, member: discord.Member, flask):
        id = MemberModel.get_discord_id(member)
        query = f"UPDATE player SET FLASK_SPEND={flask} WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def fetch_all(self, ctx):
        await asyncio.sleep(1)
        query = f"SELECT * FROM player;"
        member = settings.dictionary["last_message_author"]

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        week_num = DateConverter.get_week_number()

        msg = self.build_flask_msg(member, data, week_num)
        await OutputHandler.send_pm(member, msg)

    @commands.command(pass_context=True)
    async def flask(self, ctx):
        await asyncio.sleep(1)
        member = settings.dictionary["last_message_author"]
        query = f"SELECT * FROM player WHERE DISCORD_ID={member.id};"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        week_num = DateConverter.get_week_number()

        msg = self.build_flask_msg(member, data, week_num)
        await OutputHandler.send_pm(member, msg)

    def get_joined_id(self, joined_mid_year=True):
        week_number = DateConverter.get_week_number()

        if joined_mid_year:
            return week_number
        return 0

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 2) - week_num) + id_joined

    def build_flask_msg(self, member: discord.Member, data, week_num):
        msg = ""
        try:
            for member in data:
                covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)
                msg += f"- {member.name} ist für {int(covered_weeks)} Wochen save.\n"
        except:
            msg = "PlayerCommands:build_flask_msg -  Leider kam es zu Problemen bei der Verarbeitung."
            raise Exception(f"PlayerCommands:build_flask_msg - Something happenend.")
        return msg

    def build_vacation_msg(self, data):
        msg = ""
        try:
            for member in data:
                if member.vacation_end != "None":
                    vacation_end = member.vacation_end.replace("'", "")
                    d = DateConverter.formate_date_for_bot(vacation_end)
                    msg += f"- {member.name} kommt am {d} zurück.\n"
                else:
                    msg += f"- {member.name} kommt irgendwann zurück.\n"
        except:
            msg = "PlayerCommands:build_vacation_msg -  Leider kam es zu Problemen bei der Verarbeitung."
            raise Exception(f"PlayerCommands:build_vacation_msg - Something happenend.")
        return msg
