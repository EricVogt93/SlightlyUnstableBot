import asyncio

from discord.ext import commands

from logic import settings
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.models.MemberModel import MemberModel


class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse CharacterCommands
        :param bot:
        """
        self.bot = bot

    @commands.command(pass_context=True)
    async def add_character_information(self, ctx, name, klasse, spec, rolle):
        await asyncio.sleep(1)
        member = settings.dictionary["last_message_author"]
        fetch_query = f"SELECT * FROM player WHERE DISCORD_ID={member.id};"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(fetch_query)
        data = MemberModel.parse_data(self.bot, raw_data)

        write_query = f"INSERT INTO characters " \
                      f"(PLAYER_ID_fk, CHAR_NAME, CLASS, SPEC, RAID_ROLE) VALUES " \
                      f"({data[0].primary_key}, '{name}', '{klasse}', '{spec}', '{rolle}');"
        db.write_data_query(write_query)
        db.close()
