"""
Flask taxation service - handles all flask payment logic.

The flask system works as follows:
- Each player owes X flasks per week (configurable via FLASK_TAX_PER_WEEK)
- Players can pay in advance to build up credit
- The system tracks "paid until" date instead of raw flask counts
- This avoids year-boundary issues with week numbers
"""
import os
from datetime import date, timedelta
from typing import Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, rely on actual env vars


@dataclass
class FlaskStatus:
    """Represents a player's flask payment status."""
    player_name: str
    paid_until: date
    weeks_ahead: int  # Positive = credit, negative = debt
    flasks_owed: int  # 0 if paid up or ahead, positive if behind
    is_overdue: bool


class FlaskService:
    """Centralized flask taxation logic."""

    def __init__(self):
        self.tax_per_week: int = int(os.getenv("FLASK_TAX_PER_WEEK", "18"))

    def calculate_status(self, paid_until: Optional[date], player_name: str = "") -> FlaskStatus:
        """
        Calculate a player's flask status based on their paid_until date.

        Args:
            paid_until: Date until which player has paid (None = never paid)
            player_name: Player's name for the status object

        Returns:
            FlaskStatus with current standing
        """
        today = date.today()

        if paid_until is None:
            # Never paid - calculate from beginning of year as fallback
            paid_until = date(today.year, 1, 1)

        # Calculate difference in days, then convert to weeks
        days_diff = (paid_until - today).days
        weeks_ahead = days_diff // 7

        # Calculate flasks owed (only if behind)
        if weeks_ahead < 0:
            flasks_owed = abs(weeks_ahead) * self.tax_per_week
        else:
            flasks_owed = 0

        return FlaskStatus(
            player_name=player_name,
            paid_until=paid_until,
            weeks_ahead=weeks_ahead,
            flasks_owed=flasks_owed,
            is_overdue=weeks_ahead < 0
        )

    def calculate_new_paid_until(
        self,
        current_paid_until: Optional[date],
        flasks_added: int
    ) -> date:
        """
        Calculate new paid_until date after adding flasks.

        Args:
            current_paid_until: Current paid_until date (None = start from today)
            flasks_added: Number of flasks being added

        Returns:
            New paid_until date
        """
        today = date.today()

        # If never paid or paid_until is in the past, start from today
        if current_paid_until is None or current_paid_until < today:
            base_date = today
        else:
            base_date = current_paid_until

        # Calculate weeks covered by the flasks
        weeks_covered = flasks_added // self.tax_per_week

        # Add weeks to base date
        new_paid_until = base_date + timedelta(weeks=weeks_covered)

        return new_paid_until

    def get_initial_paid_until(self, join_date: Optional[date] = None) -> date:
        """
        Get the initial paid_until date for a new player.

        New players start with their join date as paid_until,
        meaning they owe nothing yet but need to pay going forward.

        Args:
            join_date: Date player joined (defaults to today)

        Returns:
            Initial paid_until date
        """
        return join_date or date.today()

    def format_status_message(self, status: FlaskStatus) -> str:
        """Format a flask status into a user-friendly message."""
        if status.is_overdue:
            return (
                f"- {status.player_name}: {abs(status.weeks_ahead)} weeks behind, "
                f"owes {status.flasks_owed} flasks (paid until {status.paid_until})"
            )
        elif status.weeks_ahead == 0:
            return f"- {status.player_name}: Paid up to date (until {status.paid_until})"
        else:
            return (
                f"- {status.player_name}: {status.weeks_ahead} weeks ahead "
                f"(paid until {status.paid_until})"
            )

    def format_reminder_message(self, status: FlaskStatus) -> str:
        """Format a reminder message for overdue players."""
        if not status.is_overdue:
            return ""

        return (
            f"FLASK TAX REMINDER\n"
            f"Hi {status.player_name}, you are {abs(status.weeks_ahead)} weeks behind "
            f"on flask payments.\n"
            f"Please send {status.flasks_owed} 'Potion of Power (Rank 3)' to the guild bank.\n"
            f"Your last payment covered you until: {status.paid_until}"
        )


# Singleton instance for easy import
flask_service = FlaskService()
