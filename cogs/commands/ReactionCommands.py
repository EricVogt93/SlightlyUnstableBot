import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class ReactionCommands(commands.Cog):
    """Handles raid signup messages with reactions."""

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="send_raid_signup_msg", description="Sendet Raidanmeldung")
    async def send_raid_signup_msg(self, interaction: Interaction):
        emb_view = self.create_raid_message()
        await self.send_raid_message(emb_view, interaction)

    def create_raid_message(self):
        emb_view = nextcord.Embed(title="raid >datum<", description="abc", color=0xf00000)
        emb_view.add_field(name="Tanks", value="Tanks")
        emb_view.add_field(name="DDs", value="DDs")
        emb_view.add_field(name="Heal", value="Heal")
        return emb_view

    async def send_raid_message(self, emb_view: nextcord.Embed, interaction: Interaction):
        await interaction.send(embed=emb_view)
        await self.add_reactions_to_msg(interaction, emb_view.title)

    async def add_reactions_to_msg(self, interaction: Interaction, title):
        message: nextcord.Message
        async for message in interaction.channel.history():
            if not message.embeds:
                continue
            if message.embeds[0].title == title:
                msg = message
                break
        else:
            # something broke
            return

        await msg.add_reaction("<:WoWTank:840322582338994188>")
        await msg.add_reaction("<:WoWHeal: 840319162941308928>")
        await msg.add_reaction("<:WoWDD: 840323066403094589>")
