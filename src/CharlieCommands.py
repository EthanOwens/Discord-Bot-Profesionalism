import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3

con = sqlite3.connect('charlie.db')
cur = con.cursor()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=">") #set command keyfigure to >



#Bot commandsd must start with @bot.command and async, similarly to the events
#typing >help in a discord server with this bot will bring up a help list of all commands
@bot.command(help = "Returns the id of the user")
# ctx (context) is a discord specific parameter that is required for all discord commands. It will refer to data about the user that ran the command
async def userID(ctx, user: discord.User):
    await ctx.channel.send(f'User Id: {user.id}')

@bot.command(help = "Manually insert row of data by command line: mention, starting balance. ")
async def manualInsert(ctx, user: discord.User, arg1):
    cur.execute(f'INSERT INTO player_data VALUES ("{user.id}", "{user.name}", "{ctx.guild}", {arg1}, {0})')
    con.commit()
    print(f'Tuple inserted into player_data: ({user.id}, {user.name}, {ctx.guild}, {arg1}, {0})')
    cur.close()

@bot.command(help = "Returns balance of user")
async def bal(ctx):
    cur.execute(f'SELECT balance FROM player_data WHERE id = "{ctx.author.id}"')
    await ctx.channel.send(f'Your balance is {cur.fetchone()[0]}')

@bot.command(help = "Returns guild name")
async def guild(ctx):
    await ctx.channel.send(f'Guild: {ctx.guild}')

bot.run(TOKEN)