from cogs.commands.CharacterCommands import CharacterCommands
from cogs.commands.FunCommands import FunCommands
from cogs.commands.MessageCommands import MessageCommands
from cogs.commands.PlayerCommands import PlayerCommands
from cogs.commands.ReminderCommands import ReminderCommands
from cogs.commands.TrialCommands import TrialCommands
from cogs.commands.ReactionCommands import ReactionCommands
from cogs.events.OnMessage import OnMessage
from cogs.events.OnReady import OnReady


class CommandRegisterService:
    def __init__(self, bot):
        """
        Konstruktor der Klasse CommandRegisterService. Benötigt Instanz vom Discordbot - Objekt.
        :param bot: Object
        """
        self.bot = bot

    def register_commands(self):
        """
        Registriert alle Commands.
        """
        self.bot.add_cog(FunCommands(self.bot))
        self.bot.add_cog(MessageCommands(self.bot))
        self.bot.add_cog(ReminderCommands(self.bot))
        self.bot.add_cog(PlayerCommands(self.bot))
        self.bot.add_cog(TrialCommands(self.bot))
        self.bot.add_cog(CharacterCommands(self.bot))
        self.bot.add_cog(ReactionCommands(self.bot))

    def register_events(self):
        """
        Registriert alle Events.
        """
        self.bot.add_cog(OnReady(self.bot))
        self.bot.add_cog(OnMessage(self.bot))
