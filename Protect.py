import discord
import requests
import random
import asyncio
import time
import aiohttp
import json
import os
from discord import Game
from discord.ext import commands

client = commands.Bot(command_prefix='.p')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=Game(name='Protecting Accounts | .p'))
    print('Connected on ' + client.user.name)

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)

@client.command(pass_context=True)
async def report(ctx, target: discord.User):
    client.send_message(target, 'You have been reported')
    client.say('Reported')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )



    await client.send_message(channel, embed=embed)

client.run(str(os.environ.get('BOT_TOKEN')))
