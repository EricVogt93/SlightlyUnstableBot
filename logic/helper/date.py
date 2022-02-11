from datetime import *


class DateHelper:
    @staticmethod
    def get_current_date():
        """
        Gibt aktuelle Datum zurück.
        :return: String
        """
        return date.today()

    @staticmethod
    def concat_dates(date1, date2, separator):
        """
        Verbindet 2 verschiedene Dates.
        :param date1: String
        :param date2: String
        :param separator: String
        :return: String
        """
        return f'{date1} {separator} {date2}'
