import asyncio
import os
import requests
import discord
import schedule
import time as t

from discord.ext import commands

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.DateConverter import DateConverter as date_helper, DateConverter
from logic.models.MemberModel import MemberModel


class ReminderCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse ReminderCommands
        :param bot:
        """
        cfg_obj = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "URL")
        self.cfg = cfg_obj.load()
        self.bot = bot
        self.raid_dictionary = {}
        self.flask_scheduler_active = False

    @commands.command()
    async def start_flask_reminder(self, ctx):
        schedule.every(1).day.at("18:00").do(self.remind_flask)
        self.flask_scheduler_active = True

        while self.flask_scheduler_active:
            schedule.run_pending()
            t.sleep(1)

    @commands.command(pass_context=True)
    async def stop_flask_reminder(self, ctx):
        self.flask_scheduler_active = False

    def remind_flask(self):
        query = f"SELECT * FROM player;"
        week_num = DateConverter.get_week_number()

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)

        for member in data:
            msg = self.build_flask_reminder_msg(member, week_num)
            OutputHandler.send_pm(member.member_obj, msg)

    def build_flask_reminder_msg(self, member: discord.Member, week_num):
        covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)
        msg = f"Hi {member.name}, du bist bereits {int(covered_weeks)} Wochen behind.\n " \
              f"Bitte schicke Grondo oder Samed neue Flasks. Bevorzugt per Ingame-Mail."
        return msg

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 2) - week_num) + id_joined
