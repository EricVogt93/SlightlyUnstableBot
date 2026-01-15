import nextcord


class HelpHandler:

    @staticmethod
    def get_player_cmd_help():
        emb_view = nextcord.Embed(title="Spielerbezogene Commands", description="Slightly Unbotable", color=0xf00000)
        emb_view.add_field(name="/add_gamer", value="(Parm: @member, datum[dd-MM-yyyy]) - Fügt Spieler zur DB hinzu.",
                          inline=False)
        emb_view.add_field(name="/delete_gamer", value="(Parm: @member) - Entfernt Spieler aus der DB.", inline=False)
        emb_view.add_field(name="/add_vacation",
                          value="(Parm: @member,  vacation start datum[dd-MM-yyyy, OPTIONAL: vacation ende datum[dd-MM-yyyy])- Setzt Urlaubsdaten.",
                          inline=False)
        emb_view.add_field(name="/add_vacation",
                          value="(Parm: @member,  vacation ende datum[dd-MM-yyyy]) - Setzt  Urlaubsende.", inline=False)
        emb_view.add_field(name="/get_vacation_players", value="Gibt alle Urlaube aller Spieler zurück.", inline=False)
        emb_view.add_field(name="/get_players_in_vacation", value="Gibt alle Spieler die gerade im Urlaub sind zurück.",
                          inline=False)
        emb_view.add_field(name="/add_tax",
                          value="(Parm: @member, amount) - Record tax payment for player.", inline=False)
        emb_view.add_field(name="/fetch_all", value="Show tax status for all players.",
                          inline=False)
        emb_view.add_field(name="/tax", value="(Parm: @member) - Show tax status for specific player.",
                          inline=False)
        return emb_view

    @staticmethod
    def get_character_cmd_help():
        emb_view = nextcord.Embed(title="Charakterbezogene Commands", description="Slightly Unbotable", color=0xf00000)
        emb_view.add_field(name="/add_character_information",
                          value="(Parm: name, klasse, spec, rolle) - Verlinkt Spieler mit Main Charakter", inline=False)
        return emb_view

    @staticmethod
    def get_trial_cmd_help():
        emb_view = nextcord.Embed(title="Trialbezogene Commands", description="Slightly Unbotable", color=0xf00000)
        emb_view.add_field(name="/showTrails", value="Gibt Liste mit allen aktiven Trials zurück", inline=False)
        emb_view.add_field(name="/makeTrail", value="Gibt Spieler Trial Status", inline=False)
        return emb_view

    @staticmethod
    def get_message_cmd_help():
        emb_view = nextcord.Embed(title="Informationsbezogene Commands", description="Slightly Unbotable",
                                 color=0xf00000)
        emb_view.add_field(name="/gildentab", value="Gibt Gildentabelle zurück", inline=False)
        emb_view.add_field(name="/wowaudit", value="Gibt wowaudit zurück", inline=False)
        emb_view.add_field(name="/progress", value="Gibt Progressseite zurück", inline=False)
        return emb_view

    @staticmethod
    def get_fun_cmd_help():
        emb_view = nextcord.Embed(title="Inspirierende Commands", description="Slightly Unbotable", color=0xf00000)
        emb_view.add_field(name="/hurensohn", value="Get a random inspiring quote.", inline=False)
        emb_view.add_field(name="/ja", value="Get a random inspiring quote.", inline=False)
        emb_view.add_field(name="/nein", value="Get a random inspiring quote.", inline=False)
        emb_view.add_field(name="/robinsmutter", value="Get a random inspiring quote.", inline=False)
        emb_view.add_field(name="/whiteknight", value="Get a random inspiring quote.", inline=False)
        emb_view.add_field(name="/motherjokes", value="Random Motherjoke.", inline=False)
        return emb_view

    @staticmethod
    def get_reminder_cmd_help():
        emb_view = nextcord.Embed(title="Reminderbezogene Commands", description="Slightly Unbotable", color=0xf00000)
        emb_view.add_field(name="/start_tax_reminder", value="Start daily tax payment reminder.", inline=False)
        emb_view.add_field(name="/stop_tax_reminder", value="Stop tax payment reminder.", inline=False)
        return emb_view
