import asyncio

import discord

from discord.ext import commands

from logic import settings
from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
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
        bit = BoolBitConverter.bool_to_bit(True)
        query = f"SELECT * FROM player WHERE IS_TRIAL = {bit}"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()
        data = MemberModel.parse_data(self.bot, raw_data)

        msg = ""
        i = 1
        for member in data:
            msg += f"{i} - {member.name}; {member.discord_id}\n"
            i += 1
        await self.send_pm(ctx, ctx.author, msg)

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def makeTrial(self, ctx, member: discord.Member):
        await asyncio.sleep(1)
        sql = f"UPDATE player SET IS_TRIAL=%s WHERE DISCORD_ID = %s"
        val = (1, member.id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()

        msg = f"Spieler {member.name} ist jetzt Trial."
        await OutputHandler.send_pm(ctx.author, msg)

    @commands.command(pass_context=True)
    @commands.has_role("Officer")
    async def kickTrial(self, ctx, member: discord.Member, reason=None):
        msg = ""
        #TODO delete aus db
        if not reason:
            await member.kick()
            msg = f"{member} wurde gekickt."
        else:
            await member.kick(reason=reason)
            msg = f"{member} wurde gekickt. Begründung: {reason}."
        OutputHandler.send_pm(ctx.author, msg)

    async def send_pm(self, ctx, user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
