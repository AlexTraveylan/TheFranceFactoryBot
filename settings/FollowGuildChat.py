from models.User import User
from varEnviron.Versions import Versions
from models.Urls import Urls
from models.Message_guild import Message_guild

import requests

class FollowGuildChat:

    def messagesGuildChat(user: User):

        json_guild_chat = {
                "channels": [
                    {
                "name": "guildchat",
                "seq": 0
                    }
                ],
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion
            }
        
        datas = requests.post(url = Urls.urlChannel(user), json=json_guild_chat).json()
        
        messages=[]
        for data in datas["events"]["guildchat"]:
            displayName = data["sourceUser"]["displayName"]
            content = data["content"]
            seq = data["seq"]
            timestamp = data["timestamp"]
            messages.append(Message_guild(displayName, content, timestamp, seq))
        
        return messages


