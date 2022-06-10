import os
import nextcord
from nextcord.ext import commands
from logic.classes.ConfigHandler import ConfigHandler
from cogs.CommandRegisterService import CommandRegisterService


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BotModel(metaclass=Singleton):
    def __init__(self):
        """
        Konstruktor der Klasse Bot
        """
        self.prefix = "/"
        self.intents = nextcord.Intents.all()
        self.bot = None
        self.isDebugMode = True

        # Check ob Bot aus Pycharm gestarted wurde.
        if "PYCHARM_HOSTED" in os.environ:
            self.isDebugMode = True
        else:
            self.isDebugMode = False

    def start_bot(self):
        """
        Funktion startet Discord Bot.
        """
        #ToDo: Scuffed Implementierung. BotModel in Modelordner -> Pfad join funktioniert dann nicht mehr
        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "DEFAULT")
        token = cfg.get_value("token")

        self.bot = commands.Bot(command_prefix=self.prefix, case_insensitive=True, intents=self.intents,
                                help_command=None)
        self.register_cogs()
        self.bot.run(token)

    def get_bot_obj(self):
        """
        Gibt Instanz vom Discord Bot zurück
        :return: Object
        """
        return self.bot

    def get_debug_mode(self):
        """
        Gibt DebugMode Boolean zurück.
        :return: Boolean
        """
        return self.isDebugMode

    def register_cogs(self):
        """
        Startpunkt für CommandRegisterService.
        """
        crs = CommandRegisterService(self.bot)
        crs.register_events()
        crs.register_commands()

