from models.Member import Member

class Guild:

    def __init__(self, id: int, name: str , members: list[Member]):
        self.id: int = id
        self.name: str = name
        self.members: list[Member] = members
    
    def __str__(self) -> str:
        return f"Guild : [id: {self.id}, name: {self.name}, members: {[(str(x) for x in self.members)]}"