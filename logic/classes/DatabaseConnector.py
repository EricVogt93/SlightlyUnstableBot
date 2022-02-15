import os
import pyodbc

from logic.classes.ConfigHandler import ConfigHandler


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnector(metaclass=Singleton):

    def __init__(self):
        self.con_obj = None
        self.isConnected = False

        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "DEFAULT")
        self.driver = cfg.get_value("driver")
        self.server = cfg.get_value("server")
        self.database = cfg.get_value("database")
        self.user = cfg.get_value("user")
        self.pw = cfg.get_value("pw")

    def connect(self):
        try:
            self.con_obj = pyodbc.connect(f'Driver={self.driver};'
                                          f'Server={self.server};'
                                          f'Database={self.database};'
                                          f'UID={self.user};'
                                          f'PWD={self.pw};')
            self.isConnected = True
        except:
            # ToDo: Auslagern ExceptionManager.py
            self.isConnected = False
            raise Exception("DatabaseConnector:connect - Database connection failed")

    def close(self):
        try:
            self.con_obj.close()
            self.isConnected = False
        except:
            self.isConnected = True
            raise Exception("DatabaseConnector:connect - Database connection could not be closed.")

    def write_data_query(self, query):
        if self.isConnected:
            cursor = self.con_obj.cursor()
            try:
                cursor.execute(query)
            except:
                raise Exception("DatabaseConnector:write_data_query - Something happenend.")
            self.con_obj.commit()
            cursor.close()

    def fetch_data_query(self, query):
        data = []

        if self.isConnected:
            cursor = self.con_obj.cursor()
            try:
                cursor.execute(query)
                for row in cursor.fetchall():
                    data.append(row)
            except:
                raise Exception("DatabaseConnector:fetch_data_query - Something happenend.")
            cursor.close()
            return data

