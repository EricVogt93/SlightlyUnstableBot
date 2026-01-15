import logging

import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
from nextcord.utils import get

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.services.FlaskService import flask_service

logger = logging.getLogger(__name__)


class ReminderCommands(commands.Cog):
    """Handles scheduled reminder commands for flask payments."""

    def __init__(self, bot):
        self.bot = bot
        self.flask_scheduler_active = False

    @commands.has_role("Officer")
    @nextcord.slash_command(name="start_flask_reminder", description="Start daily flask payment reminders")
    async def start_flask_reminder(self, interaction: Interaction):
        """Start the automatic flask reminder task."""
        if self.flask_scheduler_active:
            await interaction.response.send_message("Flask reminder already running!", ephemeral=True)
            return

        self.flask_scheduler_active = True
        self.remind_flask.start()
        await interaction.response.send_message(
            f"Flask reminder started! Will check daily and remind players who are behind.\n"
            f"Current tax rate: {flask_service.tax_per_week} flasks/week"
        )

    @commands.has_role("Officer")
    @nextcord.slash_command(name="stop_flask_reminder", description="Stop flask payment reminders")
    async def stop_flask_reminder(self, interaction: Interaction):
        """Stop the automatic flask reminder task."""
        if not self.flask_scheduler_active:
            await interaction.response.send_message("Flask reminder not running!", ephemeral=True)
            return

        self.flask_scheduler_active = False
        self.remind_flask.cancel()
        await interaction.response.send_message("Flask reminder stopped.")

    @tasks.loop(hours=24)
    async def remind_flask(self):
        """Daily task to check and remind players with overdue flask payments."""
        logger.info("Running flask reminder check...")

        db = DatabaseConnector()
        db.connect()
        # Get all players with their Discord ID and paid_until date
        raw_data = db.fetch_data_query(
            "SELECT PLAYER_NAME, DISCORD_ID, FLASK_PAID_UNTIL FROM player"
        )
        db.close()

        reminded_count = 0
        for row in raw_data:
            name, discord_id, paid_until = row[0], row[1], row[2]

            # Calculate status using FlaskService
            status = flask_service.calculate_status(paid_until, name)

            # Only send reminder if overdue
            if status.is_overdue:
                # Get Discord member object
                member = get(self.bot.get_all_members(), id=int(discord_id))
                if member:
                    reminder_msg = flask_service.format_reminder_message(status)
                    await OutputHandler.send_pm(member, reminder_msg)
                    reminded_count += 1
                    logger.info(f"Sent flask reminder to {name}")

        logger.info(f"Flask reminder complete. Reminded {reminded_count} players.")

    @remind_flask.before_loop
    async def before_flask_reminder(self):
        """Wait for bot to be ready before starting reminder loop."""
        await self.bot.wait_until_ready()
        logger.info("Flask reminder task ready")
