import os
import discord
from dotenv import load_dotenv
from replit import db
from on_message import *
from on_reaction import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await on_message_detected(client, message)


@client.event
async def on_raw_reaction_add(payload):
    await on_reaction_added(client, payload)


@client.event
async def on_raw_reaction_remove(payload):
    await on_reaction_removed(client, payload)


client.run(TOKEN)
