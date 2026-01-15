from datetime import date

import nextcord
from nextcord.utils import get

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.helper.BoolBitConverter import BoolBitConverter


class MemberModel:
    def __init__(self, bot, primary_key, name, discord_id, vacation_start, vacation_end,
                 flask_spend, is_trial, joined_id):
        self.primary_key = self.format_primary_key(primary_key)
        self.name = self.format_name(name)
        self.discord_id = discord_id
        self.vacation_start = vacation_start
        self.vacation_end = vacation_end
        self.flask_spend = self.format_flask(flask_spend)
        self.is_trial = self.format_is_trial(is_trial)
        self.member_obj = self.get_member_obj(bot, discord_id)
        self.joined_id = self.format_id_joined(joined_id)

    @staticmethod
    def get_all_member(bot):
        """
        Ruft alle Member des Discord ab.
        :param bot: Object
        :return: Array::String
        """
        array_members = []
        today = date.today()
        i = 0
        for guild in bot.guilds:
            for member in guild.members:
                array_members[i] = MemberModel(bot, i, member.name, member.id, "", "", "0", False, today)
                i = i + 1
        return array_members

    @staticmethod
    def filter_member_by_role(array_data, role):
        """
        Filtert Discord Member bei der gegebenen Rolle
        :param array_data: Array::String
        :param role: Discord::Role
        :return: Array::String
        """
        array_members = []
        i = 0

        for member in array_data:
            for r in member.roles:
                if r == role:
                    array_members[i] = member
                    i = i + 1
        return array_members

    @staticmethod
    def get_discord_id(member: nextcord.Member):
        return int(member.id)

    @staticmethod
    def get_member_name(member: nextcord.Member):
        return member.name

    @staticmethod
    def is_trial(member: nextcord.Member):
        for role in member.roles:
            if role == "Trial":
                return True
        return False

    def get_member_obj(self, bot, id):
        return get(iterable=bot.get_all_members(), id=int(id))

    def get_member_id_from_name(self, name: str) -> int:
        """Get player ID from database by name."""
        query = "SELECT * FROM player WHERE PLAYER_NAME = %s"
        db = DatabaseConnector()
        db.connect()
        result = db.fetch_data_query(query, (name,))
        db.close()
        return result[0][0]

    def format_name(self, name):
        return name.replace("'", "")

    def format_primary_key(self, pk):
        return pk.replace("(", "")

    def format_id_joined(self, id):
        if id != 'None':
            return int(id.replace(")", ""))
        return "21"

    def format_is_trial(self, b):
        return BoolBitConverter.bit_to_bool(b)

    def format_flask(self, flask):
        if ")" in flask:
            flask = flask.replace(")", "")
        if flask != "None":
            return float(flask)
        return 0

    @staticmethod
    def parse_data(bot, raw_data):
        member_list = []
        for row in raw_data:
            data = str(row)
            d = data.split(", ")

            vacation_start = ""
            vacation_end = ""
            flask_spend = ""
            joined_id = ""
            is_trial = ""
            if d[3].startswith("datetime.date"):
                vacation_start = f"{d[3].replace('datetime.date(', '')}-{d[4]}-{d[5].replace(')', '')}"
                flask_spend = d[7]
                joined_id = d[8]
                is_trial = d[9]
            else:
                vacation_start = "NULL"
                flask_spend = d[5]
                joined_id = d[6]
                is_trial = d[7]
            if d[3].startswith("datetime.date") and d[6].startswith("datetime.date"):
                vacation_end = f"{d[6].replace('datetime.date(', '')}-{d[7]}-{d[8].replace(')', '')}"
                flask_spend = d[9]
                joined_id = d[10]
                is_trial = d[11]
            else:
                vacation_end = "NULL"

            member = MemberModel(bot=bot, primary_key=d[0], name=d[1], discord_id=d[2], vacation_start=vacation_start,
                                 vacation_end=vacation_end, flask_spend=flask_spend, joined_id=joined_id,
                                 is_trial=is_trial)
            member_list.append(member)
        return member_list
