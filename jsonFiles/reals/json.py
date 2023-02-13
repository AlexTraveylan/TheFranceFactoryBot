
import time
from models.Versions import Versions

class JsonAPI:

    def json_message(message, guild):
        return {
                "builtInMultiConfigVersion": Versions.builtInMultiConfigVersion,
                "installId": Versions.installId,
                "playerEvent": {
                    "createdOn": str(int(time.time()*1000)),
                    "gameConfigVersion": Versions.gameConfigVersion,
                    "multiConfigVersion": Versions.multiConfigVersion,
                    "playerEventData": {
                        "guildId": guild.id,
                        "message": message
                    },
                    "playerEventType": "SEND_GUILD_CHAT_MESSAGE_2",
                    "universeVersion": Versions.universeVersion
                }
            }
    
    def json_player_2():
        return {
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
    
    def json_get_guild(guildId):
        return {
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