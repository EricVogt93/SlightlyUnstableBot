from BotModel import BotModel


class OutputHandler:
    @staticmethod
    async def send_pm(user, msg):
        """
        Sendet private Nachricht an Message.Author. Benötigt Message.Author.ID und eine Message.
        :param user: Obj
        :param msg: String
        """
        try:
            await user.send(msg)
        except:
            # check if bot got ignored
            await user.send(msg)
