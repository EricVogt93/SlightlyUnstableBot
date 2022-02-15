import discord
from discord.utils import get

from logic.helper.BoolBitConverter import BoolBitConverter


class MemberModel:
    def __init__(self, bot, primary_key, name, discord_id, vacation_start, vacation_end, flask_spend, is_trial):
        self.primary_key = self.format_primary_key(primary_key)
        self.name = self.format_name(name)
        self.discord_id = discord_id
        self.vacation_start = vacation_start
        self.vacation_end = vacation_end
        self.flask_spend = flask_spend
        self.is_trial = self.format_is_trial(is_trial)
        self.member_obj = self.get_member_obj(bot, discord_id)

    @staticmethod
    def get_all_member(bot):
        """
        Ruft alle Member des Discord ab.
        :param bot: Object
        :return: Array::String
        """
        array_members = []
        i = 0
        for guild in bot.guilds:
            for member in guild.members:
                array_members[i] = MemberModel(member.name, member.id, member.roles)
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
    def get_discord_id(member: discord.Member):
        return int(member.id)

    @staticmethod
    def is_trial(member: discord.Member):
        for role in member.roles:
            if role == "Trial":
                return True
        return False

    @staticmethod
    def get_member_obj(bot, id):
        return get(bot.get_all_members(), id=id)

    def format_name(self, name):
        return name.replace("'","")

    def format_primary_key(self, pk):
        return pk.replace("(","")

    def format_is_trial(self, b):
        BoolBitConverter.bit_to_bool(b)
        return BoolBitConverter.bit_to_bool(b)
