import requests
from DataSheets.GoogleSheet import GoogleSheet
from models.Message_guild import Message_guild
from models.Urls import Urls

from models.Versions import Versions


class GuildChat:

    def recupGuildChatMessages(user):
        ''' A function who recup news messages from ChatGuild.
        Using GoogleSheet as bdd for recup last seq of messages recupered

        return
        ------
            Messages : list[Message_guild]
            or None.

        '''
        newMessages = []
        seq = GoogleSheet.recupLastSeqFromGuildChat()

        # Here with seq-1, we are sure to recup at least 1 message, and dont have slow bug.
        jsonForGetGuildChat = {
                        "channels": [
                            {
                                "name": "guildchat",
                                "seq": (seq - 1)
                            }
                        ],
                        "gameConfigVersion": Versions.gameConfigVersion,
                        "multiConfigVersion": Versions.multiConfigVersion
                            }
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
