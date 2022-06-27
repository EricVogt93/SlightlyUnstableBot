import asyncio
import os
import requests
import nextcord
import schedule
import time as t

from nextcord.ext import commands, tasks
from nextcord import Message

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.DateConverter import DateConverter as date_helper, DateConverter
from logic.models.MemberModel import MemberModel


def db_connect_with_query_execute(query):
    db = DatabaseConnector()
    db.connect()
    raw_data = db.fetch_data_query(query)
    return raw_data


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
        self.message = Message

    @nextcord.slash_command(name="test_denis", description="test denis")
    async def remind_raid(self, ctx):
        # Aktuell habe ich noch die filterung auf meinen namen 'Fitzek' drin für release dann rausnehmen
        query = f"SELECT * FROM player AS p LEFT JOIN raid_attendance AS r ON p.PLAYER_ID=r.PLAYER_ID " \
                f"WHERE r.PLAYER_ID IS NULL AND r.IS_ATTENDING IS NULL AND p.PLAYER_NAME = 'Fitzek';"

        raw_data = db_connect_with_query_execute(query)
        msg = f"Bitte mit :white_check_mark: (anmelden) oder :x: (abmelden) reagieren"

        data = MemberModel.parse_data(self.bot, raw_data)
        for discord_member in data:
            msgtest = await OutputHandler.send_pm(discord_member.member_obj, msg)
            # nächste zeile ist ein Test kann wieder rausgenommen werden
            await msgtest.add_reaction(':x:')

    @nextcord.slash_command(name="start_flask_reminder", description="Startet Flask - Reminder")
    @commands.has_role("Officer")
    async def start_flask_reminder(self, ctx):
        self.flask_scheduler_active = True
        self.remind_flask.start()

    # ToDo: Noch keine Funktion
    @nextcord.slash_command(name="start_flask_reminder", description="Stopped Flask - Reminder")
    @commands.has_role("Officer")
    async def stop_flask_reminder(self, ctx):
        self.flask_scheduler_active = False

    # Weekly Reminder
    @tasks.loop(hours=168)
    async def remind_flask(self):
        query = f"SELECT * FROM player;"
        week_num = DateConverter.get_week_number()

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()
        print("checking...")

        data = MemberModel.parse_data(self.bot, raw_data)
        msg = ""
        for member in data:
            covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)
            if covered_weeks <= 0:
                msg = self.build_flask_reminder_msg(member, covered_weeks)
                await OutputHandler.send_pm(member.member_obj, msg)

    def build_flask_reminder_msg(self, member: nextcord.Member, covered_weeks):
        msg = ""

        if int(covered_weeks) <= 0:
            msg = f"FLASKSTEUER - REMINDER\n" \
                  f"Hi {member.name}, du bist {int(covered_weeks)} Wochen behind mit deinen Flask.\n" \
                  f"Bitte schicke Grondo oder Samed neue Flask. Bevorzugt per Ingame-Mail."
        return msg

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 2) - week_num) + int(id_joined)

    @remind_flask.before_loop
    async def before_flask_reminder(self):
        await self.bot.wait_until_ready()
        print("Finished waiting - flask_reminder")

    async def send_pm(self, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
