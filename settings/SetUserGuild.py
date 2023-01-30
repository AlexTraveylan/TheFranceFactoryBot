from models.Versions import Versions
from models.Urls import Urls
from models.Member import Member
from models.Guild import Guild

import time
import requests

class SetUserGuild:

    def setUserGuild(user):

        Json_Player_2 = {
            "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
            "installId": Versions.installId,
            "playerEvent": {
                "createdOn": str(int(time.time()*1000)),
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion,
                "playerEventData": {},
                "playerEventType": "GET_PLAYER_2",
                "universeVersion": Versions.universeVersion
            }
        }

        getInfos = requests.post(url = Urls.urlApi(user), json = Json_Player_2)
        infos = getInfos.json()

        guild = infos["eventResult"]["eventResponseData"]["player"]["guild"]

        id = guild["guildId"]
        name = guild["name"]
        listMembers = []


        members = guild["members"]
        for member in members:
            try:
                isClasOn = member["guildChallengeOptIn"]
            except:
                isClasOn = False
            listMembers.append(Member(member["userId"], member["displayName"], isClasOn))
        
        return Guild(id, name, listMembers)