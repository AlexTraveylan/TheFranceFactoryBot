

class CLashStatut:

    def __init__(self, userID, numAttempts, accumulatedScore, fortification, spectator: bool = False):
        self.userID = userID
        self.numAttempts = numAttempts
        self.accumulatedScore = accumulatedScore
        self.fortification = fortification
        self.spectator = spectator
    
    def __str__(self):
        if self.spectator:
            return f"{self.userID} est spectateur"
        else:
            if self.numAttempts != 7:
                return f"{7 - self.numAttempts} attaques restantes // {self.userID} // Score actuel : {self.accumulatedScore}"
            else:
                return f"{self.userID} // Score final : {self.accumulatedScore}"
