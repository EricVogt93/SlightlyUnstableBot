import asyncio

import discord

from discord.ext import commands

from logic import settings
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.models.MemberModel import MemberModel


class TrialCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @commands.command(pass_context=True)
    async def showTrials(self, ctx):
        await asyncio.sleep(1)
        userid = settings.dictionary["last_message_author"]
        bit = BoolBitConverter.bool_to_bit(True)
        query = f"SELECT * FROM player WHERE IS_TRIAL = {bit}"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()
        data = self.parse_data(raw_data)

        string = ""
        i = 1
        for member in data:
            string += f"{i} - {member.name}; {member.discord_id}\n"
            i += 1
        await self.send_pm(userid, string)

    @commands.command(pass_context=True)
    async def makeTrial(self, ctx, member: discord.Member):
        await asyncio.sleep(1)
        query = f"UPDATE player SET IS_TRIAL=1 WHERE DISCORD_ID = {member.id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()

    @commands.command(pass_context=True)
    async def kickTrial(self, member: discord.Member, reason=None):
        msg = ""
        #TODO delete aus db
        userid = settings.dictionary["last_message_author"]
        if not reason:
            await member.kick()
            msg = f"{member} wurde gekickt."
        else:
            await member.kick(reason=reason)
            msg = f"{member} wurde gekickt. Begründung: {reason}."
        self.send_pm(userid, msg)

    def parse_data(self, raw_data):
        member_list = []
        for row in raw_data:
            data = str(row)
            d = data.split(", ")
            member = MemberModel(bot=self.bot, primary_key=d[0], name=d[1], discord_id=d[2], vacation_start=d[3],
                                 vacation_end=d[4], flask_spend=d[5], is_trial=d[6])
            member_list.append(member)
        return member_list

    async def send_pm(self, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
