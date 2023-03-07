
class Member:

    def __init__(self, userId: str, displayName: str, isClashOn: bool):
        self.userId: str = userId
        self.displayName: str = displayName
        self.isClashOn: bool = isClashOn
    
    def __str__(self) -> str:
        return f"Member: [userId: {self.userId}, displayName: {self.displayName}, isClashOn: {self.isClashOn}]"