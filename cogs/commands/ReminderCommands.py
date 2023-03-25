import os
import os

import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.DateConverter import DateConverter
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

    @commands.has_role("Officer")
    @nextcord.slash_command(name="start_flask_reminder", description="Startet Flask - Reminder")
    async def start_flask_reminder(self, interaction: Interaction):
        self.flask_scheduler_active = True
        self.remind_flask.start()
        await interaction.response.send_message("Done.")

    # Weekly Reminder
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
        msg = ""
        for member in data:
            covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)
            if covered_weeks <= 0 or covered_weeks is None or covered_weeks == "null":
                msg = self.build_flask_reminder_msg(member, covered_weeks)
                await OutputHandler.send_pm(member.member_obj, msg)

    def build_flask_reminder_msg(self, member: nextcord.Member, covered_weeks):
        msg = ""

        if int(covered_weeks) <= 0:
            msg = f"FLASKSTEUER - REMINDER\n" \
                  f"Hi {member.name}, du bist {int(covered_weeks)} Wochen behind mit deinen 'Potion of Power (R3)'.\n" \
                  f"Bitte schicke Samed (Kerokrawall) neue 'Potion of Power (Rank3)'. Bevorzugt per Ingame-Mail."
        return msg

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 18) - week_num) + int(id_joined)

    @remind_flask.before_loop
    async def before_flask_reminder(self):
        await self.bot.wait_until_ready()
        print("Finished waiting - flask_reminder")
