from logic.models.MemberModel import MemberModel as Member


class DiscordDataModel:
    RAIDER_ROLE = "Raider"

    def __init__(self, bot):
        """
        Konstruktor der Klasse DiscordDataModel
        :param bot: Object
        """
        self.DiscordMember = Member.get_all_member(bot)
        self.Raider = Member.filter_member_by_role(self.DiscordMember, self.RAIDER_ROLE)
