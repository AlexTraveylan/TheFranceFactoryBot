from models.Member import Member

class Guild:

    def __init__(self, id: int, name: str , members: Member):
        self.id = id
        self.name = name
        self.members = members
    
    