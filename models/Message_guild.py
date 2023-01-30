

class Message_guild:

    def __init__(self, displayName, content, timestamp, seq):
        self.displayName=displayName
        self.content=content
        self.timestamp=timestamp
        self.seq=seq
    
    def toString(self):
        return f"{self.seq} ({self.timestamp}) // {self.displayName} : {self.content}"