



from models.AttacksAndBombs import MemberABInfos
from models.User import User
from settings.Connexion import Connexion
from settings.MembersBombsAndAttacksInfos import MembersBombsAndAttacksInfos
from settings.SetUserGuild import SetUserGuild


user: User = Connexion.getConnexion()

dict_for_traduce_memberId_to_name: dict = SetUserGuild.dict_UserId_To_DisplayName(user)

membersData: list[MemberABInfos] = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_last_days(user, days=1)

# membersData = list(filter(lambda x:(x.activity.bomb_left > 0 or x.activity.attacks_left > 0), membersData))


message: str = "```Bilan des attaques et bombes ratés hier : \n\n"
for datum in sorted(membersData, key=lambda x: (x.activity.attacks_left, x.activity.bomb_left)):
    message += datum.displayInfoToString(dict_for_traduce_memberId_to_name) + "\n\n"
message += "```"

print(message)