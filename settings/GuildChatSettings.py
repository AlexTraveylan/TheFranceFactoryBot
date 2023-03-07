import requests
from DataSheets.GoogleSheet import GoogleSheet
from models.Message_guild import Message_guild
from models.Urls import Urls
from models.User import User

from varEnviron.Versions import Versions


class GuildChat:

    def __init__(self) -> None:
        self.initSeq: int = 0
    
    def jsonForGetGuildChat(seq : int):
        return {
                "channels": [
                    {
                        "name": "guildchat",
                        "seq": (seq - 1)
                    }
                ],
                "gameConfigVersion": Versions.gameConfigVersion,
                "multiConfigVersion": Versions.multiConfigVersion
            }
    
    def setInitSeq(self, user: User) -> None:
        ''' Go to api for return last seq on guild chat
        '''

        json = GuildChat.jsonForGetGuildChat(0)
        try:
            messages = requests.post(url = Urls.urlChannel(user), json = json).json()["events"]["guildchat"]
        except:
            raise ValueError("Echec dans la recupération des messages")
        
        self.initSeq = int(messages[-1]["seq"]) + 1 
        

    def recupGuildChatMessages(self, user):
        ''' A function who recup news messages from ChatGuild.
        Execute self.setInitSeq first
        Using GoogleSheet as bdd for recup last seq of messages recupered

        return
        ------
            Messages : list[Message_guild]
            or None.

        '''
        newMessages = []
        # Execute self.setInitSeq first
        seq = self.initSeq

        # Here with seq-1, we are sure to recup at least 1 message, and dont have slow bug.
        jsonForGetGuildChat = GuildChat.jsonForGetGuildChat(seq - 1)

        try:
            messages = requests.post(url = Urls.urlChannel(user), json = jsonForGetGuildChat).json()["events"]["guildchat"]
            # messages should contain an array with messages, with at least 1 message (cause seq - 1)

            if len(messages) > 1:
                messages = messages[1:]

                for message in messages:
                    newMessages.append(Message_guild(
                        message["sourceUser"]["displayName"],
                        message["content"],
                        message["timestamp"],
                        message["seq"]
                        ))
                
                GoogleSheet.updateLastSeqFromGuildChat(newMessages[-1].seq)

                return newMessages
            else:
                print("Pas de nouveaux messages")

        except:
            print("Erreur pour recuperer les messages")
