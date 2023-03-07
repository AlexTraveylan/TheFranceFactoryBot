

import requests
from functions.functions import Fonctions
from jsonFiles.reals.json import JsonAPI
from models.AttacksAndBombs import Activity, MemberABInfos
from models.Urls import Urls
from models.User import User
from settings.SetUserGuild import SetUserGuild


class MembersBombsAndAttacksInfos:

    def Remaning_attacks_and_bombs_for_today(user: User) -> list[MemberABInfos]:

        guild = SetUserGuild.getGuild(user)

        membersData: list[MemberABInfos] = []
        for member in guild.members:
            membersData.append(MemberABInfos(member.userId, Activity()))
        
        play_2_response = requests.post(url = Urls.urlApi(user), json = JsonAPI.json_player_2()).json()

        player = play_2_response['eventResult']['eventResponseData']['player']
        actualTimecode = player['timestamp']

        guild = player['guild']['guildBossGameMode']

        guildActivities = player['guild']['guildActivities']

        for act in guildActivities:
            if act['createdOn'] > Fonctions.debutJourneeByTimecode(actualTimecode):
                if act['type'] == 'GUILD_BOSS_BOMB':
                    for datum in membersData:
                        if act['userId'] == datum.userId:
                            datum.activity.bomb_left -= 1
                else:
                    for datum in membersData:
                        if act['userId'] == datum.userId:
                            datum.activity.attacks_left -= 1
        
        return membersData

    def Remaning_attacks_and_bombs_for_saison(user: User) -> list[MemberABInfos]:

            guild = SetUserGuild.getGuild(user)
            
            play_2_response = requests.post(url = Urls.urlApi(user), json = JsonAPI.json_player_2()).json()

            player = play_2_response['eventResult']['eventResponseData']['player']
            actualTimecode = player['timestamp']
            # beginSaisonTimeCode = player['guild']['guildBossGameMode']['season']['seasonStartedOn']

            guildActivities = player['guild']['guildActivities']


            membersData: list[MemberABInfos] = []
            for member in guild.members:
                membersData.append(MemberABInfos(member.userId, Activity(7, 14)))

            for act in guildActivities:
                if act['createdOn'] < Fonctions.debutJourneeByTimecode(actualTimecode):
                    if act['type'] == 'GUILD_BOSS_BOMB':
                        for datum in membersData:
                            if act['userId'] == datum.userId:
                                datum.activity.bomb_left -= 1
                    else:
                        for datum in membersData:
                            if act['userId'] == datum.userId:
                                datum.activity.attacks_left -= 1
            
            return membersData

