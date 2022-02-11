class EmbededField:
    title = None
    value = None
    inline = False
    optional = False

    def __init__(self, title, value, inline: bool):
        """
        Konstruktor der Klasse EmbededField
        :rtype: object
        """
        self.title = title
        self.value = value
        self.inline = inline

    def get_title(self):
        """
        Gibt Titel des EmbededFields zurück.
        :return: String
        """
        return self.title

    def get_value(self):
        """
        Gibt Value des EmbededFields zurück.
        :return: String
        """
        return self.value

    def get_inline(self):
        """
        Gibt an ob sich Element inline oder outline befindet.
        :return: Boolean
        """
        return self.inline
