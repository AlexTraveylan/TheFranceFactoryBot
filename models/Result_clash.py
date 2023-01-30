
class Result_clash:

    def __init__(self, userID, ennemyID, damage, currentHp, defensiveFortification, defensiveFortificationDamage, seq):
        self.userID=userID
        self.ennemyID=ennemyID
        self.damage=damage
        self.currentHp=currentHp
        self.defensiveFortification=defensiveFortification
        self.defensiveFortificationDamage=defensiveFortificationDamage
        self.seq=seq

    def toString(self):
        return f"{self.seq} : {self.userID} deal {self.damage} ({self.currentHp} left) to {self.ennemyID} and dammage {self.defensiveFortificationDamage} to defense({self.defensiveFortification} left)"

    def toArray(self):
        return [self.userID, self.ennemyID, self.damage, self.currentHp, self.defensiveFortification, self.defensiveFortificationDamage, self.seq]
