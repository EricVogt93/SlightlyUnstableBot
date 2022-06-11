import asyncio

import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.helper.BoolBitConverter import BoolBitConverter
from logic.helper.DateConverter import DateConverter
from logic.models.MemberModel import MemberModel


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        """
        Konstruktor der Klasse PlayerCommands
        :param bot:
        """
        self.bot = bot

    @nextcord.slash_command(name="add_gamer", description="Fügt Spieler zur DB hinzu.")
    @commands.has_role("Officer")
    async def add_gamer(self, interaction: Interaction, member: nextcord.Member, joined_mid_year=True):
        name = str(member.name)
        id = MemberModel.get_discord_id(member)
        is_trial_bool = MemberModel.is_trial(member)
        is_trial = BoolBitConverter.bool_to_bit(is_trial_bool)
        id_joined = self.get_joined_id(joined_mid_year)

        sql = f"INSERT INTO player " \
                f"(PLAYER_NAME, DISCORD_ID, IS_TRIAL, ID_JOINED)" \
                f"VALUES (%s, %s, %s, %s);"
        val = (name, id, is_trial, id_joined)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"Spieler in Datenbank geadded {id}!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    #ToDo: Fixen
    @nextcord.slash_command(name="delete_gamer", description="Löscht Spieler aus Datenbank.")
    @commands.has_role("Officer")
    async def delete_gamer(self, interaction: Interaction, member: nextcord.Member):
        id = MemberModel.get_discord_id(member)
        query = f"DELETE FROM player WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(query)
        db.close()
        msg = f"Spieler mit {id} gelöscht!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="add_vacation", description="Fügt Urlaubsdaten für Spieler hinzu.")
    @commands.has_role("Officer")
    async def add_vacation(self, interaction: Interaction, member: nextcord.Member, vacation_start, vacation_end=None):
        query = ""
        id = MemberModel.get_discord_id(member)
        date_begin = DateConverter.formate_date_for_db(vacation_start)

        if vacation_end is None:
            sql = "UPDATE player SET VACATION_START=%s WHERE DISCORD_ID=%s"
            val = (date_begin, id)
        else:
            date_end = DateConverter.formate_date_for_db(vacation_end)
            sql = "UPDATE player SET VACATION_START=%s, VACATION_END=%s WHERE DISCORD_ID=%s"
            val = (date_begin, date_end, id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"Urlaub added für {id}!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="end_vacation", description="Fügt Urlaubsende für Spieler hinzu.")
    @commands.has_role("Officer")
    async def end_vacation(self, interactions: Interaction, member: nextcord.Member, vacation_end=None):
        id = MemberModel.get_discord_id(member)

        if vacation_end is None:
            vacation_end = DateConverter.get_current_date()

        date = DateConverter.formate_date_for_db(vacation_end)

        sql = "UPDATE player SET VACATION_END=date%s WHERE DISCORD_ID=%s"
        val = (date, id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"Urlaubsende({date}) added für {id}!"
        await OutputHandler.send_pm(interactions.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="get_players_in_vacation", description="Gibt alle Spieler zurück die gerade im Urlaub sind")
    @commands.has_role("Officer")
    async def get_players_in_vacation(self, interaction: Interaction):
        await asyncio.sleep(1)
        today = DateConverter.get_current_date()
        db_today = DateConverter.formate_date_for_db(today)
        sql = f"SELECT * FROM player WHERE VACATION_END>{db_today} OR VACATION_END IS NULL AND VACATION_END<{db_today};"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(sql)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        msg = self.build_vacation_msg(data)
        if msg == "":
            msg = "Niemand ist momentan im Urlaub!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="add_flask", description="Zahlt Flask für Spieler ein.")
    @commands.has_role("Officer")
    async def add_flask(self, interaction: Interaction, member: nextcord.Member, flask):
        id = MemberModel.get_discord_id(member)
        sql = f"UPDATE player SET FLASK_SPEND=%s WHERE DISCORD_ID=%s"
        val = None
        paid_flask_tpl = self.get_paid_flask(interaction, member)
        paid_flask = paid_flask_tpl[0][0]

        if paid_flask is not None:
            val = (int(flask) + int(paid_flask), id)
        else:
            val = (flask, id)

        db = DatabaseConnector()
        db.connect()
        db.write_data_query(sql, val)
        db.close()
        msg = f"{flask} added für {id}!"
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="fetch_all", description="Gibt alle Spieler und ihren Flask-Stand zurück.")
    @commands.has_role("Officer")
    async def fetch_all(self, interaction: Interaction):
        query = f"SELECT * FROM player;"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        week_num = DateConverter.get_week_number()

        msg = self.build_flask_msg(interaction.user, data, week_num)
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    @nextcord.slash_command(name="flask", description="Gibt Flaskstand für einen Spieler zurück.")
    async def flask(self, interaction: Interaction, member: nextcord.Member):
        id = MemberModel.get_discord_id(member)
        query = f"SELECT * FROM player WHERE DISCORD_ID={id};"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(query)
        db.close()

        data = MemberModel.parse_data(self.bot, raw_data)
        week_num = DateConverter.get_week_number()

        msg = self.build_flask_msg(member, data, week_num)
        await OutputHandler.send_pm(interaction.user, msg)
        await interaction.response.send_message("Done.")

    def get_paid_flask(self, ctx, member: nextcord.Member):
        id = MemberModel.get_discord_id(member)
        sql = f"SELECT FLASK_SPEND FROM player WHERE DISCORD_ID={id}"

        db = DatabaseConnector()
        db.connect()
        raw_data = db.fetch_data_query(sql)
        db.close()
        return raw_data


    def get_joined_id(self, joined_mid_year=True):
        week_number = DateConverter.get_week_number()

        if joined_mid_year:
            return week_number
        return 0

    def flask_calculation(self, flask_spend, week_num, id_joined):
        return ((flask_spend / 2) - week_num) + int(id_joined)

    def build_flask_msg(self, member: nextcord.Member, data, week_num):
        msg = ""
        try:
            for member in data:
                covered_weeks = self.flask_calculation(member.flask_spend, week_num, member.joined_id)
                msg += f"- {member.name} ist für {str(covered_weeks)} Wochen save.\n"
        except:
            msg = "PlayerCommands:build_flask_msg -  Leider kam es zu Problemen bei der Verarbeitung."
            raise Exception(f"PlayerCommands:build_flask_msg - Something happenend.")
        return msg

    def build_vacation_msg(self, data):
        msg = ""
        try:
            for member in data:
                if member.vacation_end != "None":
                    vacation_end = member.vacation_end.replace("'", "")
                    d = DateConverter.formate_date_for_bot(vacation_end)
                    msg += f"- {member.name} kommt am {d} zurück.\n"
                else:
                    msg += f"- {member.name} kommt irgendwann zurück.\n"
        except:
            msg = "PlayerCommands:build_vacation_msg -  Leider kam es zu Problemen bei der Verarbeitung."
            raise Exception(f"PlayerCommands:build_vacation_msg - Something happenend.")
        return msg
