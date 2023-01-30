import discord
from discord.ext import commands

from varEnviron.environ import *

from settings.Connexion import Connexion
from settings.SetClash import SetClash
from settings.followClash import FollowClash

from DataSheets.GoogleSheet import GoogleSheet


intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "!" , intents=intents)


@bot.event
async def on_ready():
    print("Bot command ready")



@bot.command("buildClash")
async def buildClash(ctx):
    ''' This command recup ennemy power on clash and display them on googleSheet
    Then GoogleSheet give the targetsx to members. 
    '''
    try:
        user = Connexion.getConnexion()
        await ctx.send("`Connexion réussie`")

        clashInfo = SetClash.recupClashInfo(user)
        await ctx.send("`Infos du clash récupérées`")

        ennemiesPowers = SetClash.recupPowers(user, clashInfo)
        await ctx.send("`Recupération des puissances ennemies reussie`")

        GoogleSheet.writeInSheetForSetClash(ennemiesPowers)
        await ctx.send("`Build réussi et données envoyées avec succes dans le google sheet !`")

    except:
        await ctx.send("`Une ou plusieurs erreurs se sont produites`")

@bot.command("fClash")
async def fClash(ctx):
    '''This command recup datas from clash and send them to googleSheet to be analysed
    TO DO : Use a timer here instead of command.
    TO DO 2 : Distinct ennemies from allies.
    TO DO 3 : Datas includes defenseSucces.
    '''
    try:
        user = Connexion.getConnexion()
        print("Connexion reussie")


        clashInfo = SetClash.recupClashInfo(user)
        print("Infos du clash récupérées")

        clash = FollowClash.dropClash(user, clashInfo)
        print("Objets du clash mis en liste")
        
        await ctx.send(GoogleSheet.writeInSheetForGetClashDatas(clash))
    
    except:
        await ctx.send("`Une ou plusieurs erreurs se sont produites`")

@bot.command("infoClash")
async def infoClash(ctx, number):
    if number == "1" or number == "2":
        team = f"team{number}"
        print(f"Recherche lancé pour la {team}")

        user = Connexion.getConnexion()
        print("Connexion reussie")

        clashinfo = SetClash.recupClashInfo(user)
        print("Infos du clash récupérées")

        results = FollowClash.displayRemainingAttacks(user, clashinfo, team)
        print("liste des infos sur le statut du clash récupérée")

        results = sorted(results, key=lambda x: x.accumulatedScore)
        reponse = "```"
        for result in results:
            reponse += result.toString() + "\n\n"
        reponse += "```"

        await ctx.send(reponse)
    

bot.run(BOT_KEY)


