
class Clash:
    def __init__(self, saison: str , opponentGuildID: str, idClash: str, team: str) -> None:
        self.saison: str = saison
        self.opponentGuildID: str = opponentGuildID
        self.idClash: str = idClash
        self.team: str = team

    def __str__(self) -> str:
        return f"ObjClash :[saison:{self.saison}, oponentGuildID:{self.opponentGuildID}, idClash:{self.idClash}, team:{self.team}]"
