
from models.AttacksAndBombs import MemberABInfos
from models.User import User
from settings.Connexion import Connexion
from settings.MembersBombsAndAttacksInfos import MembersBombsAndAttacksInfos
from settings.SetUserGuild import SetUserGuild


class ExportedFuntions:

    def exported_ab_details() -> str:
        user: User = Connexion.getConnexion()

        dict_for_traduce_memberId_to_name = SetUserGuild.dict_UserId_To_DisplayName(user)

        membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

        message = "```Bilan des attaques et des bombes restantes : \n\n"
        for datum in sorted(membersData, key=lambda x: (x.activity.attacks_left, x.activity.bomb_left)):
            message += datum.displayInfoToString(dict_for_traduce_memberId_to_name) + "\n\n"
        message += "```"

        return message
    
    def exported_ab() -> str:

        user: User = Connexion.getConnexion()

        membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

        remaningBombs: int = sum([x.activity.bomb_left for x in membersData])
        remaningAttacks: int = sum([x.activity.attacks_left for x in membersData])

        return f"```Attaques restantes : {remaningAttacks} \nBombes restantes : {remaningBombs}\n```"