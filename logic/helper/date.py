from datetime import *


class DateHelper:
    @staticmethod
    def get_current_date():
        return date.today()

    @staticmethod
    def concat_dates(date1, date2, separator):
        return f'{date1} {separator} {date2}'
