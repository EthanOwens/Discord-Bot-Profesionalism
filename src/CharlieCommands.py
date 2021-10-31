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

cur.execute("ALTER TABLE player_table ADD level INT DEFAULT 0 AFTER exp")

#Bot commandsd must start with @bot.command and async, similarly to the events
#typing >help in a discord server with this bot will bring up a help list of all commands
# ctx (context) is a discord specific parameter that is required for all discord commands. It will refer to data about the user that ran the command

@bot.command(help = "Manually insert row of data by command line: mention, starting balance. ")
async def manualInsert(ctx, user: discord.User, arg1):
    cur.execute(f'INSERT INTO player_data VALUES ("{user.id}", "{user.name}", "{ctx.guild}", {arg1}, {0})')
    con.commit()
    print(f'Tuple inserted into player_data: ({user.id}, {user.name}, {ctx.guild}, {arg1}, {0})')

@bot.command(help = "Returns the balance of mentioned user")
async def bal(ctx, user: discord.User):
    cur.execute(f'SELECT balance FROM player_data WHERE id = "{user.id}"')
    await ctx.channel.send(f'{user.name}, your balance is {cur.fetchone()[0]}')

@bot.command()
async def level(ctx, user:discord.User):
    cur.execute(f'Select level FROM player_table WHERE id = "{user.id}"')
    #add an embed here to return the data with their icon and level

@bot.command(help = "Returns all rows to terminal")
async def printRows(ctx):
    cur.execute("SELECT * FROM player_data")
    await ctx.channel.send("Printing player data to terminal")
    for row in cur:
        print(row)

@bot.command()
async def printID(ctx, user: discord.User):
    cur.execute(f'SELECT id FROM player_data WHERE id = "{user.id}"')
    print(cur.fetchone()[0])

bot.run(TOKEN)