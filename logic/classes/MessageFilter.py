import nextcord

class MessageFilter:

    def __init__(self, message):
        self.msg = message

    def check_all(self, msg):
        return self.filter_187()

    def filter_187(self, msg):
        if " 187 " in msg or " 187" in msg or "einsachtsieben" in msg:
            return True
        return False
