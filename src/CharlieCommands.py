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
# ctx (context) is a discord specific parameter that is required for all discord commands. It will refer to data about the user that ran the command

@bot.command(help = "Manually insert row of data by command line: mention, starting balance. ")
async def manualInsert(ctx, user: discord.User, arg1):
    cur.execute(f'INSERT INTO player_data VALUES ("{user.id}", "{user.name}", "{ctx.guild}", {arg1}, 0, 1)')
    con.commit()
    print(f'Tuple inserted into player_data: ({user.id}, {user.name}, {ctx.guild}, {arg1}, 0, 1)')

@bot.command(help = "Returns the balance of mentioned user")
async def bal(ctx, user: discord.User):
    cur.execute(f'SELECT balance FROM player_data WHERE id = "{user.id}"')
    await ctx.channel.send(f'{user.name}, your balance is {cur.fetchone()[0]}')

@bot.command(help = "Shows general data on a user")
async def profile(ctx, user: discord.User):
    cur.execute(f'SELECT balance, exp, level FROM player_data WHERE id = "{user.id}"')
    #add an embed here to return the data with their icon and level
    row = cur.fetchone()
    pfp = user.avatar_url
    profile = discord.Embed(title = f'{user.name}\'s profile', description = f'Balance: {row[0]}\n'
                                                                             f'Current Experience: {row[1]}\n '
                                                                             f'Level: {row[2]}')
    profile.set_thumbnail(url=(pfp))
    await ctx.channel.send(embed = profile)

@bot.command(help = "Pay user x amount")
async def pay(ctx, user: discord.User, amount):
    cur.execute(f'SELECT balance FROM rat_bank.users WHERE user_id = {ctx.author.id}')
    payer_bal = int(cur.fetchone()[0])

    if(payer_bal > amount):
        cur.execute(f'UPDATE rat_bank.users SET balance = ({amount} + balance) WHERE user_id = "{user.id}"')
        cur.execute(f'UPDATE rat_bank.users SET balance = (balance - {amount}) WHERE user_id = "{ctx.author.id}"')
        con.commit()
        await ctx.channel.send(f'{user.name}, you have been payed {amount} by {ctx.author.id}')
    else:
        await ctx.channel.send(f'{ctx.author.name}, you have insufficient funds')

@bot.command(help = "Returns all rows to terminal")
async def printRows(ctx):
    cur.execute("SELECT * FROM player_data")
    await ctx.channel.send("Printing player data to terminal")
    for row in cur:
        print(row)

bot.run(TOKEN)