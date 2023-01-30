

class PowerClash:

    def __init__(self, id_member, id_guild, powers, scores, isKilled, endBonus):
        self.id_member = id_member
        self.id_guild = id_guild
        self.endBonus = endBonus
        self.powers = powers
        self.scores = scores
        self.isKilled = isKilled
    
    def toString(self):
        msg = f"Power clash Display : Guild : {self.id_guild}  id : {self.id_member} bonus : {self.endBonus}\n"
        for i in range(3):
            msg+= f"  - Team n°{i} killed ? {self.isKilled[i]}: power {self.powers[i]} score {self.scores[i][0] + self.scores[i][1]}\n"     
        return msg