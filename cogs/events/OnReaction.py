import nextcord
from nextcord.ext import commands

from logic import settings


class OnReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user != client.user:
            if str(reaction.emoji) == "➡️":
                # fetch new results from the Spotify API
                newSearchResult = nextcord.Embed(...)
                await reaction.message.edit(embed=newSearchResult)
            if str(reaction.emoji) == "⬅️":
                # fetch new results from the Spotify API
                newSearchResult = nextcord.Embed(...)
                await reaction.message.edit(embed=newSearchResult)
