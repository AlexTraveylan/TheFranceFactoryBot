import discord
from discord.ext import commands, tasks
from DataSheets.GoogleSheet import GoogleSheet
from action.PushMessage import pushMessage
from settings.Connexion import Connexion
from settings.GuildChatSettings import GuildChat
from settings.SetClash import SetClash
from settings.SetUserGuild import SetUserGuild
from settings.followClash import FollowClash

from varEnviron.environ import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "!" , intents=intents)

@bot.event
async def on_ready():
    ''' Here its lauch the loop task updateChatGuildOnGeneral.
    The timer cant be changed during the execution.
    '''
    print("Bot event ready")
    updateChatGuildOnGeneral.start()
    infoClashAuto.start()

@tasks.loop(minutes=2.0)
async def updateChatGuildOnGeneral():
    ''' Go to guildChat and see if news messages are here, then write them on discord.
    It don't write messages from MAINUSER for dodge infinite boucle. 
    '''
    print("on update")
    channel = bot.get_channel(MAIN_DISCORD_CHAT)
    user = Connexion.getConnexion()
    messages = GuildChat.recupGuildChatMessages(user)

    if messages:
        for message in messages:
            if message.displayName != MAINUSER_DISPLAYNAME:
                await channel.send(f"`{message.displayName} a dit : {message.content}`")

@bot.event
async def on_message(ctx):
    ''' If someone write a message on discord main channel, then write it on the game, on guildChat.
    It don't write messages on others channels and if the bot write the message.
    '''
    if ctx.channel.id == MAIN_DISCORD_CHAT and ctx.author != bot.user:
        user = Connexion.getConnexion()
        guild = SetUserGuild.setUserGuild(user)
        pushMessage.messageGuildPush(f"{ctx.author} : {ctx.content}", user, guild)

@tasks.loop(hours=2.0)
async def infoClashAuto():
    print("on info")
    ctx = bot.get_channel(732284378918682675)
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

bot.run(BOT_KEY)
