
class User:

    def __init__(self, userID, sessionID=""):
        self.userID = userID
        self.sessionID = sessionID
    
    def __str__(self) -> str:
        return f"User : [userId: {self.userID}, sessionID: {self.sessionID}]"