"""
Guild tax service - handles all tax payment logic.

The tax system works as follows:
- Each player owes X units per week (configurable via TAX_PER_WEEK)
- Tax can be anything: flasks, gold, materials, etc.
- Players can pay in advance to build up credit
- The system tracks "paid until" date instead of raw counts
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
    pass


@dataclass
class TaxStatus:
    """Represents a player's tax payment status."""
    player_name: str
    paid_until: date
    weeks_ahead: int  # Positive = credit, negative = debt
    amount_owed: int  # 0 if paid up or ahead, positive if behind
    is_overdue: bool


class TaxService:
    """Centralized guild tax logic."""

    def __init__(self):
        self.tax_per_week: int = int(os.getenv("TAX_PER_WEEK", "18"))
        self.tax_name: str = os.getenv("TAX_NAME", "items")

    def calculate_status(self, paid_until: Optional[date], player_name: str = "") -> TaxStatus:
        """
        Calculate a player's tax status based on their paid_until date.

        Args:
            paid_until: Date until which player has paid (None = never paid)
            player_name: Player's name for the status object

        Returns:
            TaxStatus with current standing
        """
        today = date.today()

        if paid_until is None:
            paid_until = date(today.year, 1, 1)

        days_diff = (paid_until - today).days
        weeks_ahead = days_diff // 7

        if weeks_ahead < 0:
            amount_owed = abs(weeks_ahead) * self.tax_per_week
        else:
            amount_owed = 0

        return TaxStatus(
            player_name=player_name,
            paid_until=paid_until,
            weeks_ahead=weeks_ahead,
            amount_owed=amount_owed,
            is_overdue=weeks_ahead < 0
        )

    def calculate_new_paid_until(
        self,
        current_paid_until: Optional[date],
        amount_added: int
    ) -> date:
        """
        Calculate new paid_until date after adding payment.

        Args:
            current_paid_until: Current paid_until date (None = start from today)
            amount_added: Amount being added

        Returns:
            New paid_until date
        """
        today = date.today()

        if current_paid_until is None or current_paid_until < today:
            base_date = today
        else:
            base_date = current_paid_until

        weeks_covered = amount_added // self.tax_per_week
        new_paid_until = base_date + timedelta(weeks=weeks_covered)

        return new_paid_until

    def get_initial_paid_until(self, join_date: Optional[date] = None) -> date:
        """
        Get the initial paid_until date for a new player.

        Args:
            join_date: Date player joined (defaults to today)

        Returns:
            Initial paid_until date
        """
        return join_date or date.today()

    def format_status_message(self, status: TaxStatus) -> str:
        """Format a tax status into a user-friendly message."""
        if status.is_overdue:
            return (
                f"- {status.player_name}: {abs(status.weeks_ahead)} weeks behind, "
                f"owes {status.amount_owed} {self.tax_name} (paid until {status.paid_until})"
            )
        elif status.weeks_ahead == 0:
            return f"- {status.player_name}: Paid up to date (until {status.paid_until})"
        else:
            return (
                f"- {status.player_name}: {status.weeks_ahead} weeks ahead "
                f"(paid until {status.paid_until})"
            )

    def format_reminder_message(self, status: TaxStatus) -> str:
        """Format a reminder message for overdue players."""
        if not status.is_overdue:
            return ""

        return (
            f"TAX REMINDER\n"
            f"Hi {status.player_name}, you are {abs(status.weeks_ahead)} weeks behind "
            f"on tax payments.\n"
            f"Please send {status.amount_owed} {self.tax_name} to the guild bank.\n"
            f"Your last payment covered you until: {status.paid_until}"
        )


# Singleton instance for easy import
tax_service = TaxService()
