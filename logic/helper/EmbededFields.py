class EmbededField:
    title = None
    value = None
    inline = False
    optional = False

    def __init__(self, title, value, inline: bool):
        self.title = title
        self.value = value
        self.inline = inline

    def getTitle(self):
        return self.title

    def getValue(self):
        return self.value

    def getInline(self):
        return self.inline
