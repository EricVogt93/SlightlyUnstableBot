import os
from discord.ext import commands
from logic.classes.ConfigHandler import ConfigHandler

cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "DEFAULT")
token = cfg.getValue("token")

bot = commands.Bot(command_prefix="!")
bot.run(token)
