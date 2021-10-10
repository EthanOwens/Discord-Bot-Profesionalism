import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=">") #set command keyfigure to >

def toID(mention):
    return str(mention).replace('@', '').replace('>', '').replace('<', '').replace('!', '')  # strips a mention down to the id

#Bot commandsd must start with @bot.command and async, similarly to the events
#typing >help in a discord server with this bot will bring up a help list of all commands
@bot.command(help = "Returns the id of the user")
# ctx (context) is a discord specific parameter that is required for all discord commands. It will refer to data about the user that ran the command
async def userID(ctx, arg):
    arg = toID(arg)
    await ctx.channel.send(f'User Id: {arg}')

bot.run(TOKEN)