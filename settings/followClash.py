from jsonFiles.reals.json import JsonAPI
from models.ClashStatut import CLashStatut
from settings.SetClash import SetClash
from varEnviron.environ import *
from varEnviron.Versions import *
from models.Urls import Urls
from models.Result_clash import Result_clash
from settings.SetOtherGuild import SetGuild
from settings.SetUserGuild import SetUserGuild

import requests


class FollowClash:


    def dropClash(user, clashInfo):

        json_GcID = {
                "channels": [
                    {
                        "name": clashInfo.idClash,
                        "seq": 0
                    }
                ],
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion
            }

        ennemyGuild = SetGuild.recupGuild(clashInfo.opponentGuildID, user)
        dictForTraduce_UserId_in_DisplayName = {}
        for member in ennemyGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName
        
        ourGuild = SetUserGuild.getGuild(user)
        for member in ourGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName
        
        
        messages = requests.post(Urls.urlChannel(user), json=json_GcID).json()
        

        results = []
        datas = messages["events"][clashInfo.idClash]


        for data in datas:
            if data["type"] == "GUILD_CHALLENGE_ENCOUNTER_ENDED_EVENT":
                enemyUserId = dictForTraduce_UserId_in_DisplayName[data["data"]["enemyUserId"]]
                defensiveFortification = data["data"]["defensiveFortification"]
                try:
                    defensiveFortificationDamage = data["data"]["defensiveFortificationDamage"]
                except:
                    defensiveFortificationDamage = 0
                try:
                    damage = data["data"]["damage"]
                except:
                    damage = 0
                try:
                    currentHp = data["data"]["currentHp"]
                except:
                    currentHp = 0
                userId = data["data"]["user"]["displayName"]
                seq = data["seq"]
                results.append(Result_clash(userId, enemyUserId, damage, currentHp, defensiveFortification, defensiveFortificationDamage, seq))
        
        return results
    
    def displayRemainingAttacks(user, clashInfo, team) -> list[CLashStatut]:

        ennemyGuild = SetGuild.recupGuild(clashInfo.opponentGuildID, user)
        dictForTraduce_UserId_in_DisplayName = {}
        for member in ennemyGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName
        
        ourGuild = SetUserGuild.getGuild(user)
        for member in ourGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName
        
        getInfos = requests.post(url = Urls.urlApi(user), json = JsonAPI.json_player_2())
        infos = getInfos.json()

        liveEvents = infos["eventResult"]["eventResponseData"]["player"]["hero"]["liveEvents"]["liveEvents"]

        i=0
        for event in liveEvents:
            try:
                if event["type"] == "GuildChallenge":break
            except:
                pass
            i+=1
        
        guild = liveEvents[i]["config"]["liveEventGameModes"]["guildChallenge"][team]

        datas = guild["teamMembers"]

        result = []
        for data in datas:
            userId = dictForTraduce_UserId_in_DisplayName[data["userId"]]
            try:
                numAttempts = data["numAttempts"]
            except:
                numAttempts = 0
            try:
                accumulatedScore = data["accumulatedScore"]
            except:
                accumulatedScore = 0
            try:
                fortification = data["fortification"]
            except:
                fortification = 0
            try:
                spectator = data["spectator"]
            except:
                spectator = False
            result.append(CLashStatut(userId, numAttempts, accumulatedScore, fortification, spectator))
        
        return result
            
            

        



#    eventResult
#        eventResponseData
#            player
#                hero
#                    liveEvents
#                        liveEvents[9] 10eme     
#                            type GuildChallenge
#                            started bool true ou false
#                            config
#                                liveEventGameModes
#                                    guildChallenge
#                                        team1
# "teamMembers"


# userId
# numAttempts ?
# accumulatedScore ?
# fortification ?
# spectator true or null




        
        
        
        
