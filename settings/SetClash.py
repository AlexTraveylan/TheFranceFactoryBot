
#    eventResult
#        eventResponseData
#            player
#                hero
#                    sharedEvents
#                        sharedEvents []
#                            tournamentId (nume ro du clash enformat dguilchallencge_149)
#                            guildChallengeId
#                            guildChallenge
#                                teamId (team1ou2)
#                                opponentGuildId

from models.Versions import Versions
from models.Urls import Urls
from models.Clash import Clash
from models.PowerClash import PowerClash
from settings.SetOtherGuild import SetGuild

import time
import requests
import re


class SetClash:

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

    
    def recupClashInfo(user):

        getInfos = requests.post(url = Urls.urlApi(user), json = SetClash.Json_Player_2)
        infos = getInfos.json()

        events = infos["eventResult"]["eventResponseData"]["player"]["guild"]["sharedEvents"]["sharedEvents"]
        event = events[-1]
        saison = re.sub("[a-zA-Z]+_" , "" , event["tournamentId"])
        idClash = event["guildChallengeId"]
        opponentGuildID = event["guildChallenge"]["opponentGuildId"]
        teamID = event["guildChallenge"]["teamId"]

        return Clash(saison,opponentGuildID, idClash, teamID)
    
# Find team ("team1" or "team2") in object Clash returned by recupClashInfo just over there
# Option : Reversed = True for data from MainUser guild.
    def recupPowers(user , clashInfo, reversed = False):

        if clashInfo.team == "team1" and not reversed:
            team = "team2"
        else:
            team = "team1"
        
        print(team)

        # TO DO : MAKE a method makeDitionnary(guildId) who return the dict
        ennemyGuild = SetGuild.recupGuild(clashInfo.opponentGuildID, user)
        dictForTraduce_UserId_in_DisplayName = {}
        for member in ennemyGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName


        getInfos = requests.post(url = Urls.urlApi(user), json = SetClash.Json_Player_2)
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

        powersclash = []

        id_guild = guild["guildId"]

        bouts =  guild["bouts"]
        for bout in bouts:
            try:
                userId = dictForTraduce_UserId_in_DisplayName[bout["opponent"]["userId"]]
            except:
                userId = "inconnu"
            bonus = bout["boutBonus"]
            powers = []
            scores = []
            isKilled = []
            encounters = bout["encounters"]
            for encounter in encounters:
                powers.append(encounter["duelPower"])
                scores.append((encounter["duelBonus"], encounter["duelDamageScore"]))
                try:
                    encounter["mostDamageEntry"]["userId"]
                    isKilled.append(True)
                except:
                    isKilled.append(False)

            powersclash.append(PowerClash(userId, id_guild, powers, scores, isKilled, bonus))
        
        return powersclash
    
    def recupAlliesPowers(user , clashInfo, reversed=False):

        if clashInfo.team == "team1" and not reversed:
            team = "team1"
        else:
            team = "team2"

        getInfos = requests.post(url = Urls.urlApi(user), json = SetClash.Json_Player_2)
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

        powersclash = []

        id_guild = guild["guildId"]

        # TO DO : MAKE a method makeDitionnary(guildId) who return the dict
        allyGuild = SetGuild.recupGuild(id_guild, user)
        dictForTraduce_UserId_in_DisplayName = {}
        for member in allyGuild.members:
            dictForTraduce_UserId_in_DisplayName[member.userId] = member.displayName

        bouts =  guild["bouts"]
        for bout in bouts:
            try:
                userId = dictForTraduce_UserId_in_DisplayName[bout["opponent"]["userId"]]
            except:
                userId = "inconnu"
            bonus = bout["boutBonus"]
            powers = []
            scores = []
            isKilled = []
            encounters = bout["encounters"]
            for encounter in encounters:
                powers.append(encounter["duelPower"])
                scores.append((encounter["duelBonus"], encounter["duelDamageScore"]))
                try:
                    encounter["mostDamageEntry"]["userId"]
                    isKilled.append(True)
                except:
                    isKilled.append(False)

            powersclash.append(PowerClash(userId, id_guild, powers, scores, isKilled, bonus))
        
        return powersclash






# lines 27121

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
#                                            guildId
#                                            teamName
#                                            bouts[]*nbjoueurs
#                                                opponent
#                                                    userId
#                                                    boutPower
#                                                encounters[*3]
#                                                    duelPower
#                                                    duelBonus
#                                                    duelDamageScore
#                                                boutBonus

        