from models.Guild import Guild
from models.Versions import Versions
from models.Urls import Urls
from models.Member import Member
import time
import requests

class SetGuild:

    def recupGuild(guildId, user):

        json_View_Guild = {
            "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
            "installId": Versions.installId,
            "playerEvent": {
                "createdOn": str(int(time.time()*1000)),
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion,
                "playerEventData": {
                    "guildId": guildId
                },
                "playerEventType": "VIEW_GUILD_2",
                "universeVersion": Versions.universeVersion
            }
        }

        getInfos = requests.post(url = Urls.urlApi(user), json = json_View_Guild)
        infos = getInfos.json()

        name = infos["eventResult"]["eventResponseData"]["guild"]["name"]
        id = infos["eventResult"]["eventResponseData"]["guild"]["guildId"]
        getMembers = infos["eventResult"]["eventResponseData"]["guild"]["members"]

        members = []
        for member in getMembers:
            try:
                isClashOn = member["guildChallengeOptIn"]
            except:
                isClashOn = False
            members.append(Member(member["userId"], member["displayName"], isClashOn))

        return Guild(id,name,members)


