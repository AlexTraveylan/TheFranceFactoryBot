import discord
from discord.ext import commands
from models.AttacksAndBombs import MemberABInfos
from models.User import User
from settings.MembersBombsAndAttacksInfos import MembersBombsAndAttacksInfos
from settings.SetUserGuild import SetUserGuild

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
    
@bot.command("cd")
async def cd(ctx):
    '''EasterEgg pour mezzerine le relou
    TO DO : S'il abuse, ajouter un avertissement, suivi d'un ban.
    '''
    ctx.send(f"Haha t'es trop drole {ctx.author.name} !! (non ...)")

@bot.command("ab_detail")
async def ab_detail(ctx):
    ''' Display the remining attacks or bombs for the current day, with members details
    input
    -----
        None
    output
    -----
        remining bombs and attacks on discord
    '''

    user: User = Connexion.getConnexion()

    dict_for_traduce_memberId_to_name = SetUserGuild.dict_UserId_To_DisplayName(user)

    membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

    message = "```Bilan des attaques et des bombes restantes : \n\n"
    for datum in sorted(membersData, key=lambda x: (x.activity.attacks_left, x.activity.bomb_left)):
        message += datum.displayInfoToString(dict_for_traduce_memberId_to_name) + "\n\n"
    message += "```"

    await ctx.send(message)

@bot.command("ab")
async def ab(ctx):
    '''Display on discord the remining bombs and attacks. No members names.
    '''

    user: User = Connexion.getConnexion()

    membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

    remaningBombs: int = sum([x.activity.bomb_left for x in membersData])
    remaningAttacks: int = sum([x.activity.attacks_left for x in membersData])

    await ctx.send(f"```Attaques restantes : {remaningAttacks} \nBombes restantes : {remaningBombs}\n```")

@bot.command("a")
async def a(ctx):
    '''Display on discord the remining attacks and list of members with attacks
    '''
    user: User = Connexion.getConnexion()

    dict_for_traduce_memberId_to_name = SetUserGuild.dict_UserId_To_DisplayName(user)

    membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

    remaningAttacks: int = sum([x.activity.attacks_left for x in membersData])
    listMembersWithRemaningAttacks: MemberABInfos = filter(lambda x:x.activity.attacks_left > 0, membersData)

    message = f"```{remaningAttacks} attaques restantes: \n\n"
    for member in sorted(listMembersWithRemaningAttacks,key=lambda x: x.activity.attacks_left):
        name = dict_for_traduce_memberId_to_name[member.userId]
        space = " " * (14 - len(name))
        message += f"{name}{space} {member.activity.attacks_left}\n"
    message += "```"
    await ctx.send(message)


@bot.command("b")
async def b(ctx):
    '''Display on discord the remining bombs and list of members with bomb
    '''
    user: User = Connexion.getConnexion()

    dict_for_traduce_memberId_to_name = SetUserGuild.dict_UserId_To_DisplayName(user)

    membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_today(user)

    remaningBombs: int = sum([x.activity.bomb_left for x in membersData])
    listMembersWithRemaningAttacks: MemberABInfos = filter(lambda x:x.activity.bomb_left == 1, membersData)

    message = f"```{remaningBombs} bombes restantes: \n\n"
    for member in listMembersWithRemaningAttacks:
        name = dict_for_traduce_memberId_to_name[member.userId]
        message += f"{name}\n"
    message += "```"
    await ctx.send(message)


@bot.command("ab_week")
async def ab_week(ctx):

    user: User = Connexion.getConnexion()

    dict_for_traduce_memberId_to_name = SetUserGuild.dict_UserId_To_DisplayName(user)

    membersData: MemberABInfos = MembersBombsAndAttacksInfos.Remaning_attacks_and_bombs_for_saison(user)

    message = "```Bilan des attaques et bombes ratés sur une semaine : \n\n"
    for datum in sorted(membersData, key=lambda x: (x.activity.attacks_left, x.activity.bomb_left)):
        message += datum.displayInfoToString(dict_for_traduce_memberId_to_name) + "\n\n"
    message += "```"

    await ctx.send(message)


bot.run(BOT_KEY)


