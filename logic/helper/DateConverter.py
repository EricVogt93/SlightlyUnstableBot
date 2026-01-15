from datetime import date, datetime


class DateConverter:
    """Utility class for date formatting and conversion."""

    @staticmethod
    def get_current_date() -> str:
        """Return current date in DD.MM.YYYY format."""
        return date.today().strftime('%d.%m.%Y')

    @staticmethod
    def formate_date_for_db(date_string: str) -> str:
        """Convert DD.MM.YYYY to YYYY-MM-DD for database storage."""
        d = datetime.strptime(date_string, '%d.%m.%Y')
        return d.strftime('%Y-%m-%d')

    @staticmethod
    def formate_date_for_bot(date_string: str) -> str:
        """Convert YYYY-MM-DD to DD.MM.YYYY for display."""
        d = datetime.strptime(date_string, '%Y-%m-%d')
        return d.strftime('%d.%m.%Y')

    @staticmethod
    def concat_dates(date1: str, date2: str, separator: str) -> str:
        """Concatenate two date strings with a separator."""
        return f'{date1} {separator} {date2}'

    @staticmethod
    def get_week_number() -> int:
        """Return current ISO week number."""
        curr_date = date.today()
        year, week_num, day_of_week = curr_date.isocalendar()
        return week_num

    @staticmethod
    def format_date_for_db(time_obj: datetime) -> str:
        """Format datetime object to HH:MM:SS string."""
        return time_obj.strftime("%H:%M:%S")
