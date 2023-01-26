import nextcord

class MessageFilter:

    def __init__(self, sender, message):
        self.msg = message
        self.sender = sender

    def check_all(self, ):
        return self.filter_187()

    def filter_187(self):
        if "einsachtsieben" in self.msg or "187" in self.msg:
            return "[Detail - Bad Word: 187]"
        return ""

    def filter_spammer(self):
        if self.sender == "Napcake":
            return "[Details - Banned wegen Spam]"
        if self.sender == "Synergy":
            return "[Details - Banned wegen Spam]"
        return ""
