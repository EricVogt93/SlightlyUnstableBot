from datetime import *


class DateConverter:
    @staticmethod
    def get_current_date():
        """
        Gibt aktuelle Datum zurück.
        :return: String
        """
        return date.today().strftime('%d.%m.%Y')

    @staticmethod
    def formate_date_for_db(date_string):
        d = datetime.strptime(date_string, '%d.%m.%Y')
        return d.strftime('%Y-%m-%d')

    @staticmethod
    def formate_date_for_bot(date_string):
        d = datetime.strptime(date_string, '%Y-%m-%d')
        return d.strftime('%d.%m.%Y')

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

    @staticmethod
    def get_week_number():
        curr_date = date.today()
        year, week_num, day_of_week = curr_date.isocalendar()
        return week_num
