import nextcord

class MessageFilter:

    def __init__(self, message):
        self.msg = message

    def check_all(self, msg):
        return self.filter_187(msg)

    def filter_187(self, msg):
        if "einsachtsieben" in msg or "187" in msg:
            return True
        return False
