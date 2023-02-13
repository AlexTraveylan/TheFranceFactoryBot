
class Activity:

    def __init__(self, bomb_left: int = 1, attacks_left: int = 2) -> None:
        self.bomb_left = bomb_left
        self.attacks_left = attacks_left

class MemberABInfos:

    def __init__(self, userId: str, activity: Activity) -> None:
        self.userId = userId
        self.activity = activity

    def useBomb(self):
        self.activity.bomb_left -= 1
    
    def useAttack(self):
        self.activity.attacks_left -= 1
    
    def displayInfoToString(self, dict_for_traduce_userId_to_name: dict):
        name = dict_for_traduce_userId_to_name[self.userId]
        return f"{name} : \nBomb: {self.activity.bomb_left} | Attacks: {self.activity.attacks_left}"

