import datetime

class Fonctions:
    def debutJourneeByTimecode(timecode: int) -> int:
        dt = datetime.datetime.fromtimestamp(timecode / 1000.0)
        # Définir le début de la journée à 7h00
        day_start = dt.replace(hour=7, minute=0, second=0, microsecond=0)

        # Si l'heure actuelle est avant 7h00, définir le début de la journée sur le jour précédent
        if dt.hour < 7:
            day_start = day_start - datetime.timedelta(days=1)

        # Convertir le résultat en timecode
        result = int(day_start.timestamp() * 1000)

        return result
    
    def timeSinceBeginnigSaison(saisonTimeStamp: int, nowTimeStamp : int) -> int:

        # convert in datetime objects
        actualTime = datetime.datetime.fromtimestamp(nowTimeStamp / 1000)
        seasonStartedOn = datetime.datetime.fromtimestamp(saisonTimeStamp / 1000)

        # time between
        delta = actualTime - seasonStartedOn
        numberOfDays = delta.days

        return numberOfDays
