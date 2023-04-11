import datetime
import random
import discord
from discord.ext import commands, tasks
from DataSheets.GoogleSheet import GoogleSheet
from action.PushMessage import pushMessage
from exportedFunctions import ExportedFuntions
from settings.Connexion import Connexion
from settings.GuildChatSettings import GuildChat
from settings.SetClash import SetClash
from settings.SetUserGuild import SetUserGuild
from settings.followClash import FollowClash

from varEnviron.environ import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "!" , intents=intents)
utc_plus_1 = datetime.timezone(datetime.timedelta(hours=1))
guildChat = GuildChat()

@bot.event
async def on_ready():
    ''' Here its lauch the loop task updateChatGuildOnGeneral.
    The timer cant be changed during the execution.
    '''
    print("Bot event ready")

    # Initialisation du seq de guildchat au lancement du bot
    user = Connexion.getConnexion()
    guildChat.setInitSeq(user)

    # Lancement des Threads
    updateChatGuildOnGeneral.start()
    # infoClashAuto.start()
    Goodmorning.start()
    checkAB.start()

@tasks.loop(minutes=2.0)
async def updateChatGuildOnGeneral():
    ''' Go to guildChat and see if news messages are here, then write them on discord.
    It don't write messages from MAINUSER for dodge infinite boucle. 
    '''
    channel = bot.get_channel(MAIN_DISCORD_CHAT)
    user = Connexion.getConnexion()

    messages = guildChat.recupGuildChatMessages(user)

    if messages:
        for message in messages:
            # Si cela ne fonctionne pas, utiliser guild.chatChat.setInitseq(user) mais pas opti
            guildChat.initSeq += 1
            if message.displayName != MAINUSER_DISPLAYNAME:
                await channel.send(f"`{message.displayName} a dit : {message.content}`")

@bot.event
async def on_message(ctx: discord.Message):
    ''' If someone write a message on discord main channel, then write it on the game, on guildChat.
    It don't write messages on others channels and if the bot write the message.
    '''
    if ctx.channel.id == MAIN_DISCORD_CHAT and ctx.author != bot.user:
        user = Connexion.getConnexion()
        guild = SetUserGuild.getGuild(user)
        pushMessage.messageGuildPush(f"{ctx.author} : {ctx.content}", user, guild)

@tasks.loop(hours=2.0)
async def infoClashAuto():
    ctx = bot.get_channel(CLASH_GUILD_DISCORD_CHAT)
    try:
        user = Connexion.getConnexion()
        print("Connexion reussie")

        clashInfo = SetClash.recupClashInfo(user)
        print("Infos du clash récupérées")

        clash = FollowClash.dropClash(user, clashInfo)
        print("Objets du clash mis en liste")
        
        await ctx.send(GoogleSheet.writeInSheetForGetClashDatas(clash))
    
    except:
        print("Pas d'infos sur le clash")
    
@tasks.loop(time=datetime.time(hour=5, minute=55, tzinfo=utc_plus_1))
async def checkAB():
    channel_officier = bot.get_channel(OFFICIER_DISCORD_CHAT)
    channel_main = bot.get_channel(MAIN_DISCORD_CHAT)

    message_officier = ExportedFuntions.exported_ab_details()
    message_main = ExportedFuntions.exported_ab()

    await channel_officier.send(message_officier)
    await channel_main.send(message_main)

@tasks.loop(time=datetime.time(hour=7, tzinfo=utc_plus_1))
async def Goodmorning():
    user = Connexion.getConnexion()
    guild = SetUserGuild.getGuild(user)
    messages_possibles = ["Salut la guilde", "Bonjour tous le monde", "Chef, tu nages bien", "Yo les gens", "Bonjour les gens"]

    pushMessage.messageGuildPush(messages_possibles[random.randint(0, len(messages_possibles))], user, guild)


bot.run(BOT_KEY)
