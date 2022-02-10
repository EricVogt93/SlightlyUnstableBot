class EmbededField:
    title = None
    value = None
    inline = False
    optional = False

    def __init__(self, title, value, inline: bool):
        self.title = title
        self.value = value
        self.inline = inline

    def get_title(self):
        return self.title

    def get_value(self):
        return self.value

    def get_inline(self):
        return self.inline
