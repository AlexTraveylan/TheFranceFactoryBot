from models import User


class Urls:

    def urlConnect(user: User):
        return f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{user.userID}"

    def urlApi(user: User):
        return f"https://api-live.thor.snowprintstudios.com/player/player2/userId/{user.userID}/sessionId/{user.sessionID}"

    def urlChannel(user: User):
        return f"https://channel-live.thor.snowprintstudios.com/events/lp/userId/{user.userID}/sessionId/{user.sessionID}"