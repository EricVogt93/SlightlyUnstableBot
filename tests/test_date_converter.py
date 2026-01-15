"""Tests for DateConverter utility class."""
import pytest
from datetime import date, datetime
from logic.helper.DateConverter import DateConverter


class TestGetCurrentDate:
    """Tests for get_current_date method."""

    def test_returns_string(self):
        result = DateConverter.get_current_date()
        assert isinstance(result, str)

    def test_format_is_correct(self):
        result = DateConverter.get_current_date()
        # Should be DD.MM.YYYY format
        parts = result.split('.')
        assert len(parts) == 3
        assert len(parts[0]) == 2  # day
        assert len(parts[1]) == 2  # month
        assert len(parts[2]) == 4  # year


class TestFormateDateForDb:
    """Tests for formate_date_for_db method."""

    def test_converts_german_to_iso_format(self):
        result = DateConverter.formate_date_for_db("15.03.2024")
        assert result == "2024-03-15"

    def test_handles_single_digit_day_month(self):
        result = DateConverter.formate_date_for_db("01.01.2024")
        assert result == "2024-01-01"


class TestFormateDateForBot:
    """Tests for formate_date_for_bot method."""

    def test_converts_iso_to_german_format(self):
        result = DateConverter.formate_date_for_bot("2024-03-15")
        assert result == "15.03.2024"

    def test_handles_single_digit_day_month(self):
        result = DateConverter.formate_date_for_bot("2024-01-01")
        assert result == "01.01.2024"


class TestConcatDates:
    """Tests for concat_dates method."""

    def test_concatenates_with_separator(self):
        result = DateConverter.concat_dates("01.01.2024", "15.01.2024", "-")
        assert result == "01.01.2024 - 15.01.2024"

    def test_handles_custom_separator(self):
        result = DateConverter.concat_dates("start", "end", "to")
        assert result == "start to end"


class TestGetWeekNumber:
    """Tests for get_week_number method."""

    def test_returns_integer(self):
        result = DateConverter.get_week_number()
        assert isinstance(result, int)

    def test_returns_valid_week_number(self):
        result = DateConverter.get_week_number()
        assert 1 <= result <= 53


class TestFormatDateForDbTime:
    """Tests for format_date_for_db (time version) method."""

    def test_formats_datetime_to_time_string(self):
        dt = datetime(2024, 3, 15, 14, 30, 45)
        result = DateConverter.format_date_for_db(dt)
        assert result == "14:30:45"

    def test_handles_midnight(self):
        dt = datetime(2024, 3, 15, 0, 0, 0)
        result = DateConverter.format_date_for_db(dt)
        assert result == "00:00:00"
