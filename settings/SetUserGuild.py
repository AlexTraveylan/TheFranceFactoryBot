from jsonFiles.reals.json import JsonAPI
from models.Urls import Urls
from models.Member import Member
from models.Guild import Guild

import requests

from models.User import User

class SetUserGuild:

    def setUserGuild(user: User) -> Guild:

        Json_Player_2 = JsonAPI.json_player_2()

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
    
    def dict_UserId_To_DisplayName(user: User) -> dict:

        guildDic: dict = {}
        players: list[Member] = SetUserGuild.setUserGuild(user).members

        for player in players:
            guildDic[player.userId] = player.displayName
        
        return guildDic