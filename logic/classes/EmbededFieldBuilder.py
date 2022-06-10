import nextcord

class EmbededHandler:
    fields = []
    title = None
    colour = None
    url = None

    def __init__(self, title, fields, colour=nextcord.Colour.red(), url=None):
        self.title = title
        self.colour = colour
        self.url = url
        self.fields = fields

    def generate_msg(self):
        msg = nextcord.Embed(title=self.title, colour=self.colour)
        for field in self.fields:
            msg.add_field(name=field.get_title(), value=field.get_value(), inline=field.get_inline())

        return msg
