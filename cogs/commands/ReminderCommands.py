import os
import requests
import discord

from datetime import *
from discord.ext import commands

from logic.classes.ConfigHandler import ConfigHandler
from logic.classes.EmbededFieldBuilder import EmbededHandler
from logic.models.EmbededFields import EmbededField
from logic.helper.DateConverter import DateConverter as date_helper


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

    @commands.command(pass_context=True)
    async def remind_flask(self):
        # ToDo: Add Log, in dem alle Notifications gespeichert werden.
        return None

    @commands.command(pass_context=True)
    async def remind_raid_signup(self):
        """
        Startpunkt für Raiderinnerungen.
        """
        data = self.get_raid_object()
        self.extract_raid_information(data)
        await self.send_reminder(self.raid_dictionary)
        # ToDo: Add Log, in dem alle Notifications gespeichert werden.

    def get_raid_object(self):
        """
        Holt alle Daten aus WoWAudit und gibt diese als JSON zurück.
        :return: String::JSON
        """
        curr_date = date_helper.get_current_date()

        #ToDo: Strings ersetzen durch Config val
        r = requests.get(
            "https://www.wowaudit.com/v1/raids/?api_key=" + "8b338a074f0c66c3980dcf0ef98546fdeb0e54e787d32a0cae99e46409109c8a")
        data = r.json()
        id = data["raids"][0]["id"]
        raid = requests.get("https://www.wowaudit.com/v1/raids/" + str(
            id) + "/?api_key=" + "8b338a074f0c66c3980dcf0ef98546fdeb0e54e787d32a0cae99e46409109c8a")
        raid = raid.json()
        if raid["date"] == str(curr_date):
            id = data["raids"][1]["id"]
            raid = requests.get("https://www.wowaudit.com/v1/raids/" + str(
                id) + "/?api_key=" + "8b338a074f0c66c3980dcf0ef98546fdeb0e54e787d32a0cae99e46409109c8a")
            raid = raid.json()
        return raid

    def extract_raid_information(self, raid_obj):
        """
        Filtert aus JSON alle relevanten Informationen und lädt diese in ein Dictionary.
        :param raid_obj: String::JSON
        """
        unformatted_date = raid_obj["date"]
        self.raid_dictionary["raidDate"] = datetime.strptime(unformatted_date, '%Y-%m-%d').strftime('%d.%m.%y')
        self.raid_dictionary["raidStart"] = raid_obj["start_time"]
        self.raid_dictionary["raidEnd"] = raid_obj["end_time"]
        self.raid_dictionary["raidDifficulty"] = raid_obj["difficulty"]
        self.raid_dictionary["acceptedMember"] = self.get_raid_member(raid_obj, 0)
        self.raid_dictionary["tentativeMember"] = self.get_raid_member(raid_obj, 1)
        self.raid_dictionary["awayMember"] = self.get_raid_member(raid_obj, 2)

    def get_raid_member(self, raid_obj, switch):
        """
        Filtert alle Raidanmeldungen und unterteilt Member in entsprechende Arrays.
        :param raid_obj: String::JSON
        :param switch: Int
        :return: Array::String
        """
        present_raider_array = []
        tentative_raider_array = []
        away_raider_array = []
        index = 0

        #ToDo: Überarbeiten. Unnötigt und furchtbar Performance intensiv.
        #Listen in Map übergeben und dict rückgeben dict <string, array::string>
        for member in raid_obj["signups"]:
            name = member["character"]["name"] + "-" + member["character"]["realm"]

            if member["status"] == "Present" or member["status"] == "Late":
                present_raider_array[index] = name
            elif member["status"] == "Tentative" or member["status"] == "Unknown":
                tentative_raider_array[index] = name
            else:
                away_raider_array[index] = name
            index = + 1

        if switch == 0:
            return present_raider_array
        elif switch == 1:
            return tentative_raider_array
        else:
            return away_raider_array

    async def send_reminder(self, data):
        """
        Sendet private Nachricht an Member, welche noch erinnert werden müssen.
        :param data: Dictionary<string, string>
        """
        user = None
        raid_url = f'{self.cfg["wowaudit_raid"]}{self.raid_dictionary["raidDate"]}'
        raid_time = date_helper.concat_dates(self.raid_dictionary["raidStart"], self.raid_dictionary["raidEnd"], '-')

        # ToDo Dynamischer machen; keine festen Channel - Angaben
        channel = self.bot.get_channel(548962606438809620)
        for d in data:
            try:
                # ToDo: Strings in Config aufnehmen und Code changen
                emfields = {
                    EmbededField(title="URL", value=raid_url, inline=False),
                    EmbededField(title="Datum", value=self.raid_dictionary["raidDate"], inline=False),
                    EmbededField(title="Uhrzeit", value=raid_time, inline=False),
                }
                emb_handler = EmbededHandler("Raidanmeldung", emfields)
                msg = emb_handler.generate_msg()

                user = self.bot.get_user(d)
                await user.send(embed=msg)
            except discord.Forbidden:
                await channel.send(user)
