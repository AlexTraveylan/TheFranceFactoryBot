from discord import Guild, User
from jsonFiles.reals.json import JsonAPI
from models.Urls import Urls
import requests

class pushMessage:

    def messageGuildPush(message: str, user: User, guild: Guild) -> None:
        ''' This function post a message, on guild chat
        inputs :
        ------
            message (str) : the message to send
            user (User) : the user who will speak on channel
            guild (Guild) : the guild where the user is
        output :
        ------
            void : The message will be on the game.

        REFACTORED AND TESTED WITH SUCCES : 13/02/2023
        '''

        json_message = JsonAPI.json_message(message, guild)

        requests.post(url=Urls.urlApi(user), json=json_message)