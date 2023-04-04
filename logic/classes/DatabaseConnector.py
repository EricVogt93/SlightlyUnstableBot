import os

import mysql.connector

from logic.classes.ConfigHandler import ConfigHandler


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


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
            self.con_obj = mysql.connector.connect(user="root", password="08E04v1993", host="2.203.255.81",
                                                   port=3306, database="subot")
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

    def write_data_query(self, sql, val):
        if self.isConnected:
            cursor = self.con_obj.cursor()
            try:
                cursor.execute(sql, val)
            except:
                raise Exception("DatabaseConnector:write_data_query - Something happenend.")
            self.con_obj.commit()
            cursor.close()

    def fetch_data_query(self, sql):
        data = []

        if self.isConnected:
            cursor = self.con_obj.cursor()
            try:
                cursor.execute(sql)
                data = cursor.fetchall()
            except:
                raise Exception(
                    f"DatabaseConnector:fetch_data_query - Something happenend.\n Query: {sql}\n")
            cursor.close()
            return data
