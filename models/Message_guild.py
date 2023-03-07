

class Message_guild:

    def __init__(self, displayName, content, timestamp, seq):
        self.displayName = displayName
        self.content = content
        self.timestamp = timestamp
        self.seq = seq
    
    def __str__(self):
        return f"Message_guild : [seq: {self.seq}, timestamp: {self.timestamp}, content: {self.displayName}, seq: {self.content}]"