import discord
import os
from dotenv import load_dotenv
import random
import sqlite3

con = sqlite3.connect('charlie.db')
cur = con.cursor()

if(not cur.execute('SELECT name FROM sqlite_master WHERE type = \'table\' AND name = \'{player_data}\'')):
    cur.execute('CREATE TABLE player_data (id varchar(50), name varchar(50), guild varchar(50), balance int, exp int, level int)') #create table
    con.commit()
    print("Table created")
else:
    print("Table player_data already exists")

#loads in our Token from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(intents = intents)

#Discord events must be started with @client.event
#Discord event commands and events are couruntine functions and must start with async
#on_ready() runs on bot startup (aka when you run this file)
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Charlie is connected to {guild.name}')
        for member in guild.members:
            cur.execute(f'SELECT id FROM player_data WHERE id = "{member.id}" AND guild = "{guild}"')
            data = cur.fetchall()
            if(len(data) == 0):
                #add new member to the database with starting balance of 50
                print(f'Adding {member.name} to player_data')
                cur.execute(f'INSERT INTO player_data VALUES ("{member.id}", "{member.name}", "{guild}", 50, 0)')
            else:
                print(f'{member.name} already in database')
    con.commit()

@client.event
async def on_guild_join(guild):
    for member in guild.members:
        print(f'Member: {member}')

#on_message will check every message sent and trigger when a condition is met
@client.event
async def on_message(message):
    if message.content.lower() == "How are you Charlie?".lower():
        #sending messages require you to include "await" to wait for the bot to be done with any existing processes before running your code
        await message.channel.send("I'm a happy dino!")

    if(not message.author.bot):
        cur.execute(f'SELECT exp, level FROM player_data WHERE id = "{message.author.id}"')
        row = cur.fetchone()
        exp_gain = 15 + len(message.content.replace(" ", ""))
        new_exp = int(row[0]) + exp_gain
        cur_level = row[1]
        if(new_exp/500 >= cur_level):
            new_level = int(new_exp/500) + 1
            bal_increase = random.randint(15, 100)

            cur.execute(f'UPDATE player_data SET level = {new_level} WHERE id = "{message.author.id}"')
            con.commit()
            cur.execute(f'UPDATE player_data SET balance = {bal_increase} WHERE id = "{message.author.id}"')
            cur.commit()
            await message.channel.send(f'You leveled up! Your new level is {new_level}\n You also found a little bundle of money! You are now {bal_increase} richer.')

        cur.execute(f'UPDATE player_data SET exp = {new_exp} WHERE id = "{message.author.id}"')
        con.commit()

#running the bot using our unique bot Token
client.run(TOKEN)