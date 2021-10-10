import discord
import os
from dotenv import load_dotenv

#loads in our Token from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Basic python function
def contains(arr, item):
    for i in range(len(arr)):
        if arr[i].lower() == item:
            return True

#Discord events must be started with @client.event
#Discord event commands and events are couruntine functions and must start with async
#on_ready() runs on bot startup (aka when you run this file)
@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Charlie is connected to {guild.name}')


#on_message will check every message sent and trigger when a condition is met
@client.event
async def on_message(message):
    if message.content.lower() == "How are you Charlie?".lower():
        #sending messages require you to include "await" to wait for the bot to be done with any existing processes before running your code
        await message.channel.send("I'm a happy dino!")

#running the bot using our unique bot Token
client.run(TOKEN)