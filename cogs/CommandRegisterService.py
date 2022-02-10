from cogs.commands.FunCommands import FunCommands
from cogs.commands.MessageCommands import MessageCommands
from cogs.events.OnReady import OnReady


class CommandRegisterService:
    def __init__(self, bot):
        self.bot = bot

    def register_commands(self):
        self.bot.add_cog(FunCommands(self.bot))
        self.bot.add_cog(MessageCommands(self.bot))

    def register_events(self):
        self.bot.add_cog(OnReady(self.bot))
