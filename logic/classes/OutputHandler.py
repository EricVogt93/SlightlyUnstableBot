class OutputHandler:
    @staticmethod
    async def send_pm(user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        await user.send(msg)
