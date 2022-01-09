import discord

class EmbededHandler:
    fields = []
    title = None
    colour = None
    url = None

    def __init__(self, title, fields, colour=discord.Colour.red(), url=None):
        self.title = title
        self.colour = colour
        self.url = url
        self.fields = fields

    def generateMsg(self):
        msg = discord.Embed(title=self.title, colour=self.colour)
        for field in self.fields:
            msg.add_field(name=field.getTitle(), value=field.getValue(), inline=field.getInline())

        return msg
