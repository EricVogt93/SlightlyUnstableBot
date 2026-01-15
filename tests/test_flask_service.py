"""Tests for FlaskService class."""
import pytest
from datetime import date, timedelta
from unittest.mock import patch

from logic.services.FlaskService import FlaskService, FlaskStatus


class TestFlaskStatus:
    """Tests for FlaskStatus dataclass."""

    def test_creates_status_with_all_fields(self):
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date(2024, 6, 15),
            weeks_ahead=2,
            flasks_owed=0,
            is_overdue=False
        )
        assert status.player_name == "TestPlayer"
        assert status.weeks_ahead == 2
        assert status.is_overdue is False


class TestCalculateStatus:
    """Tests for calculate_status method."""

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_player_paid_ahead(self):
        service = FlaskService()
        future_date = date.today() + timedelta(weeks=3)

        status = service.calculate_status(future_date, "TestPlayer")

        assert status.weeks_ahead >= 2  # At least 2 weeks ahead
        assert status.flasks_owed == 0
        assert status.is_overdue is False

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_player_is_overdue(self):
        service = FlaskService()
        past_date = date.today() - timedelta(weeks=2)

        status = service.calculate_status(past_date, "TestPlayer")

        assert status.weeks_ahead < 0
        assert status.flasks_owed > 0
        assert status.is_overdue is True

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_player_paid_up_to_date(self):
        service = FlaskService()
        today = date.today()

        status = service.calculate_status(today, "TestPlayer")

        assert status.weeks_ahead == 0
        assert status.flasks_owed == 0
        assert status.is_overdue is False

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_none_paid_until_treated_as_overdue(self):
        service = FlaskService()

        status = service.calculate_status(None, "TestPlayer")

        # Should be overdue since None means never paid
        assert status.is_overdue is True

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '10'})
    def test_flasks_owed_calculation(self):
        service = FlaskService()
        # 2 weeks behind
        past_date = date.today() - timedelta(weeks=2)

        status = service.calculate_status(past_date, "TestPlayer")

        # Should owe 2 weeks * 10 flasks/week = 20 flasks
        assert status.flasks_owed == 20


class TestCalculateNewPaidUntil:
    """Tests for calculate_new_paid_until method."""

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_adds_weeks_from_current_date_if_behind(self):
        service = FlaskService()
        past_date = date.today() - timedelta(weeks=5)

        # Pay 36 flasks (2 weeks worth)
        new_date = service.calculate_new_paid_until(past_date, 36)

        # Should start from today and add 2 weeks
        expected = date.today() + timedelta(weeks=2)
        assert new_date == expected

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_adds_weeks_from_paid_until_if_ahead(self):
        service = FlaskService()
        future_date = date.today() + timedelta(weeks=2)

        # Pay 36 flasks (2 weeks worth)
        new_date = service.calculate_new_paid_until(future_date, 36)

        # Should add 2 weeks to the future date
        expected = future_date + timedelta(weeks=2)
        assert new_date == expected

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '18'})
    def test_none_paid_until_starts_from_today(self):
        service = FlaskService()

        new_date = service.calculate_new_paid_until(None, 18)

        expected = date.today() + timedelta(weeks=1)
        assert new_date == expected

    @patch.dict('os.environ', {'FLASK_TAX_PER_WEEK': '10'})
    def test_respects_config_tax_rate(self):
        service = FlaskService()

        # 30 flasks at 10/week = 3 weeks
        new_date = service.calculate_new_paid_until(date.today(), 30)

        expected = date.today() + timedelta(weeks=3)
        assert new_date == expected


class TestGetInitialPaidUntil:
    """Tests for get_initial_paid_until method."""

    def test_returns_today_by_default(self):
        service = FlaskService()

        result = service.get_initial_paid_until()

        assert result == date.today()

    def test_returns_custom_join_date(self):
        service = FlaskService()
        custom_date = date(2024, 1, 15)

        result = service.get_initial_paid_until(custom_date)

        assert result == custom_date


class TestFormatStatusMessage:
    """Tests for format_status_message method."""

    def test_overdue_message(self):
        service = FlaskService()
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date(2024, 1, 1),
            weeks_ahead=-3,
            flasks_owed=54,
            is_overdue=True
        )

        msg = service.format_status_message(status)

        assert "TestPlayer" in msg
        assert "3 weeks behind" in msg
        assert "54 flasks" in msg

    def test_paid_up_message(self):
        service = FlaskService()
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date.today(),
            weeks_ahead=0,
            flasks_owed=0,
            is_overdue=False
        )

        msg = service.format_status_message(status)

        assert "TestPlayer" in msg
        assert "Paid up to date" in msg

    def test_ahead_message(self):
        service = FlaskService()
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date.today() + timedelta(weeks=5),
            weeks_ahead=5,
            flasks_owed=0,
            is_overdue=False
        )

        msg = service.format_status_message(status)

        assert "TestPlayer" in msg
        assert "5 weeks ahead" in msg


class TestFormatReminderMessage:
    """Tests for format_reminder_message method."""

    def test_returns_empty_for_non_overdue(self):
        service = FlaskService()
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date.today(),
            weeks_ahead=0,
            flasks_owed=0,
            is_overdue=False
        )

        msg = service.format_reminder_message(status)

        assert msg == ""

    def test_returns_reminder_for_overdue(self):
        service = FlaskService()
        status = FlaskStatus(
            player_name="TestPlayer",
            paid_until=date(2024, 1, 1),
            weeks_ahead=-2,
            flasks_owed=36,
            is_overdue=True
        )

        msg = service.format_reminder_message(status)

        assert "FLASK TAX REMINDER" in msg
        assert "TestPlayer" in msg
        assert "36" in msg
