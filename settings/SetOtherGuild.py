from jsonFiles.reals.json import JsonAPI
from models.Guild import Guild
from varEnviron.Versions import Versions
from models.Urls import Urls
from models.Member import Member
import time
import requests

class SetGuild:

    def recupGuild(guildId, user) -> Guild:

        json_View_Guild = JsonAPI.json_get_guild(guildId)

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

        return Guild(id, name, members)


