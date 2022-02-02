class MemberModel:
    def __init__(self, name, ident, roles):
        self.name = name
        self.id = ident
        self.roles = roles

    @staticmethod
    def get_all_member(bot):
        array_members = []
        i = 0
        for guild in bot.guilds:
            for member in guild.members:
                array_members[i] = MemberModel(member.name, member.id, member.roles)
                i = i + 1
        return array_members

    @staticmethod
    def filter_member_by_role(array_data, role):
        array_members = []
        i = 0

        for member in array_data:
            for r in member.roles:
                if r == role:
                    array_members[i] = member
                    i = i + 1
        return array_members
