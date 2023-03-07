


from action.PushMessage import pushMessage
from settings.Connexion import Connexion
from settings.SetUserGuild import SetUserGuild


user = Connexion.getConnexion()

guild = SetUserGuild.getGuild(user)

message = "(bot) J'avais pas encore une fonction pour parler sur le chat de clash avec mon bot, si vous voyez ce message, c'est que maintenant si."

pushMessage.messageClashPush(message, user, guild)