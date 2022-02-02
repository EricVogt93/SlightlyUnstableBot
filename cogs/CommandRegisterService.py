from commands.FunCommands import *


class CommandRegisterService:
    def __init__(self, bot):
        bot.add_cog(FunCommands(bot))
