import os
from pymongo import MongoClient
from ConfigHandler import ConfigHandler

class DatabaseConnector:

    def __init__(self):
        self.isConnected = False

        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "DEFAULT")
        self.cfg_data = cfg.load()
        self.connection_string = self.cfg_data("connection_string")
        self.database_table = self.cfg_data("db_table_name")


    def connect(self):
        cluster = MongoClient(self.connection_string)
        db = cluster[self.database_table]



