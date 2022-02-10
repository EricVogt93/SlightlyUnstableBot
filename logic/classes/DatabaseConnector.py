import os
import pyodbc

from ConfigHandler import ConfigHandler


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
                                          f'PWD={self.pw};'
                                          f'Trusted_Connection=yes;')
            self.isConnected = True
        except:
            # ToDo: Auslagern ExceptionManager.py
            self.isConnected = False
            print("DatabaseConnector:connect - Database connection failed")

    def execute_query(self, query):
        if self.isConnected:
            cursor = self.con_obj.cursor()
            cursor.execute(query)
