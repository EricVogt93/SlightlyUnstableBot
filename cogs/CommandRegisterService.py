from cogs.commands.FunCommands import FunCommands
from cogs.events.OnReady import OnReady


class CommandRegisterService:
    def __init__(self, bot):
        self.bot = bot

    def register_commands(self):
        self.bot.add_cog(FunCommands(self.bot))

    def register_events(self):
        self.bot.add_cog(OnReady(self.bot))
