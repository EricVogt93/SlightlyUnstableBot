import discord


class HelpHandler:

    def getHelpTextOfficer(self):
        embView = discord.Embed(title="Bob the mover - Hilfe", description="Eric ist der Beste!", color=0xffffff)
        embView.add_field(name="!addFlasks",
                          value="Offi only - Added Flask für angegeben Spieler. (Parm: member, flaskanzahl)",
                          inline=False)
        embView.add_field(name="!kickTrial", value="Offi only - Kickt Spieler. (Parm: member, reason [mit ""])",
                          inline=False)
        embView.add_field(name="!addGamer", value="Offi only - Fügt Spieler zur Datenbank hinzu. (Parm: member)",
                          inline=False)
        embView.add_field(name="!addVac", value="Offi only - Startet Spieler - Urlaub. (Parm: member)", inline=False)
        embView.add_field(name="!delVac", value="Offi only - Beendet Spieler - Urlaub. (Parm: member)", inline=False)
        embView.add_field(name="!getVacGamers", value="Offi only - Gibt alle Spieler zurück die im Urlaub sind.",
                          inline=False)
        embView.add_field(name="!createAppl",
                          value="Offi only - Zeigt Bewerbungsmessage. (Parm: url, datum [dd.MM.yy], Zeit [hh:mm])",
                          inline=False)
        embView.add_field(name="!fetchGamers", value="Offi only - Gibt Flaskcount aller Spieler zurück.", inline=False)
        embView.add_field(name="!mLead", value="Offi only - Moved Offis zu Offiziersstube.", inline=False)
        embView.add_field(name="!mRaid", value="Offi only - Moved Offis zum Raidchannel.", inline=False)
        embView.add_field(name="!startThread", value="Offi only - Startet die Notifications", inline=False)
        embView.add_field(name="!stopThread", value="Offi only - Stoppt die Notifications", inline=False)
        embView.add_field(name="!ashen", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!flasks", value="Gibt eingezahlte FLask - Anzahl zurück.", inline=False)
        embView.add_field(name="!gildentab", value="Gibt wowaudit Gildentabelle zurück.", inline=False)
        embView.add_field(name="!nein", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!hurensohn", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!progress", value="Gibt Progress - Seite zurück.", inline=False)
        embView.add_field(name="!wowaudit", value="Gibt wowaudit Anmeldeseite zurück.", inline=False)
        embView.add_field(name="!trialList", value="Offi only - Gibt die aktuelle Trialliste zurück.")
        embView.add_field(name="!overduegamers",
                          value="Offi only - Gibt eine Liste aller Leute zurück, die mit den Flask hinten sind.")
        return embView

    def getHelpText(self):
        embView = discord.Embed(title="Bob the mover - Hilfe", description="Eric ist der Beste!", color=0xffffff)
        embView.add_field(name="!ashen", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!flasks", value="Gibt eingezahlte FLask - Anzahl zurück.", inline=False)
        embView.add_field(name="!gildentab", value="Gibt wowaudit Gildentabelle zurück.", inline=False)
        embView.add_field(name="!nein", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!hurensohn", value="Get a random inspirational quote", inline=False)
        embView.add_field(name="!progress", value="Gibt Progress - Seite zurück.", inline=False)
        embView.add_field(name="!wowaudit", value="Gibt wowaudit Anmeldeseite zurück.", inline=False)
        return embView
