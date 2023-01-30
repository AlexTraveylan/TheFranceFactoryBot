from models.Versions import Versions
from models.Urls import Urls

import time
import requests

class pushMessage:

    def messageGuildPush(message, user, guild):

        json_message = {
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

        requests.post(url=Urls.urlApi(user), json=json_message)