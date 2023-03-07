from jsonFiles.reals.json import JsonAPI
from models.Urls import Urls
from models.Member import Member
from models.Guild import Guild

import requests

from models.User import User

class SetUserGuild:

    def getGuild(user: User) -> Guild:

        Json_Player_2: dict = JsonAPI.json_player_2()

        getInfos = requests.post(url = Urls.urlApi(user), json = Json_Player_2)
        infos: dict = getInfos.json()

        guild: dict = infos["eventResult"]["eventResponseData"]["player"]["guild"]

        id: str = guild["guildId"]
        name: str = guild["name"]

        # init listMembers
        listMembers: list[Member] = []

        # set listMembers
        members = guild["members"]
        for member in members:
            try:
                isClashOn = member["guildChallengeOptIn"]
            except:
                isClashOn = False
            listMembers.append(Member(member["userId"], member["displayName"], isClashOn))
        
        return Guild(id, name, listMembers)
    
    def dict_UserId_To_DisplayName(user: User) -> dict:

        guildDic: dict = {}
        players: list[Member] = SetUserGuild.getGuild(user).members

        for player in players:
            guildDic[player.userId] = player.displayName
        
        return guildDic