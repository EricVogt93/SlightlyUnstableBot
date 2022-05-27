import asyncio
import os
import requests
import discord
import schedule
import time as t

from discord.ext import commands, tasks

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
        self.flask_scheduler_active = True
        self.remind_flask.start()

    @commands.command(pass_context=True)
    async def stop_flask_reminder(self, ctx):
        self.flask_scheduler_active = False

    @tasks.loop(hours=24)
    async def remind_flask(self):
        query = f"SELECT * FROM player;"
        week_num = DateConverter.get_week_number()

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()
        print("checking...")

        data = MemberModel.parse_data(self.bot, raw_data)

        for member in data:
            msg = self.build_flask_reminder_msg(member, week_num)
            await OutputHandler.send_pm(member.member_obj, msg)

    def build_flask_reminder_msg(self, member: discord.Member, week_num):
        msg = ""
        covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)

        if int(covered_weeks) <= 0:
            msg = f"FLASKSTEUER - REMINDER\n" \
                  f"Hi {member.name}, du bist {int(covered_weeks)} Wochen behind mit deinen Flask.\n" \
                  f"Bitte schicke Grondo oder Samed neue Flask. Bevorzugt per Ingame-Mail."
        else:
            msg = f"FLASKSTEUER - REMINDER\n" \
                  f"Hi {member.name}, du bist noch {int(covered_weeks)} Wochen sicher.\n"

        return msg

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 2) - week_num) + int(id_joined)

    @remind_flask.before_loop
    async def before_flask_reminder(self):
        await self.bot.wait_until_ready()
        print("Finished waiting - flask_reminder")
