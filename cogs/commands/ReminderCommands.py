import logging

import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
from nextcord.utils import get

from logic.classes.DatabaseConnector import DatabaseConnector
from logic.classes.OutputHandler import OutputHandler
from logic.services.TaxService import tax_service

logger = logging.getLogger(__name__)


class ReminderCommands(commands.Cog):
    """Handles scheduled reminder commands for tax payments."""

    def __init__(self, bot):
        self.bot = bot
        self.tax_scheduler_active = False

    @commands.has_role("Officer")
    @nextcord.slash_command(name="start_tax_reminder", description="Start daily tax payment reminders")
    async def start_tax_reminder(self, interaction: Interaction):
        """Start the automatic tax reminder task."""
        if self.tax_scheduler_active:
            await interaction.response.send_message("Tax reminder already running!", ephemeral=True)
            return

        self.tax_scheduler_active = True
        self.remind_tax.start()
        await interaction.response.send_message(
            f"Tax reminder started! Will check daily and remind players who are behind.\n"
            f"Current tax rate: {tax_service.tax_per_week} {tax_service.tax_name}/week"
        )

    @commands.has_role("Officer")
    @nextcord.slash_command(name="stop_tax_reminder", description="Stop tax payment reminders")
    async def stop_tax_reminder(self, interaction: Interaction):
        """Stop the automatic tax reminder task."""
        if not self.tax_scheduler_active:
            await interaction.response.send_message("Tax reminder not running!", ephemeral=True)
            return

        self.tax_scheduler_active = False
        self.remind_tax.cancel()
        await interaction.response.send_message("Tax reminder stopped.")

    @tasks.loop(hours=24)
    async def remind_tax(self):
        """Daily task to check and remind players with overdue tax payments."""
        logger.info("Running tax reminder check...")

        db = DatabaseConnector()
        db.connect()
        # Get all players with their Discord ID and paid_until date
        raw_data = db.fetch_data_query(
            "SELECT PLAYER_NAME, DISCORD_ID, TAX_PAID_UNTIL FROM player"
        )
        db.close()

        reminded_count = 0
        for row in raw_data:
            name, discord_id, paid_until = row[0], row[1], row[2]

            # Calculate status using TaxService
            status = tax_service.calculate_status(paid_until, name)

            # Only send reminder if overdue
            if status.is_overdue:
                # Get Discord member object
                member = get(self.bot.get_all_members(), id=int(discord_id))
                if member:
                    reminder_msg = tax_service.format_reminder_message(status)
                    await OutputHandler.send_pm(member, reminder_msg)
                    reminded_count += 1
                    logger.info(f"Sent tax reminder to {name}")

        logger.info(f"Tax reminder complete. Reminded {reminded_count} players.")

    @remind_tax.before_loop
    async def before_tax_reminder(self):
        """Wait for bot to be ready before starting reminder loop."""
        await self.bot.wait_until_ready()
        logger.info("Tax reminder task ready")
