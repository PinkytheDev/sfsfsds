import discord
import youtube_dl
import requests
import random
import asyncio
import time
import aiohttp
import json
import os
from discord import Game
from discord.ext import commands

client = commands.Bot(command_prefix='.m')
client.remove_command('help')
os.chdir(r'/sfsfsds/Protect.py')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

@client.event
async def on_ready():
    await client.change_presence(game=Game(name='MagicNoob | .m'))
    print('The bot is connected')
    print('Discord Application is being online')
    print('Connected on Application ' + client.user.name)


@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{}: {}'.format(author, content))
    await client.process_commands(message)


@client.event
async def on_member_join(member):
    roles = discord.utils.get(member.server.roles, name='Members')
    await client.add_roles(member, role)
    await client.say(
        "Hey! Server Owner. But if you don't have **Members** role. Then, I prefer you to add it to make this function work.")
    await client.process_commands(message)
    
@client.event
async def on_member_join(member):
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, member)
	
	with open('users.json', 'w') as f:
		json.dump(users, f)
	await client.process_commands(message)
	
@client.event
async def on_message(message):
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, message.author)
	await add_experience(users, message.author, 5)
	await level_up(users, message.author, message.channel)
	
	with open('users.json', 'w') as f:
		json.dump(users, f)
		
async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experience'] = 0
		users[user.id]['level'] = 0
		
async def add_experience(users, user, exp):
	users[user.id]['experience'] += exp
	
async def level_up(users, user, channel):
	experience = users[user.id]['experience']
	lvl_start = users[user.id]['level']
	lvl_end = int(experience ** (1/4))
	
	if lvl_start < lvl_end:
		await client.send_messsage(channel, "{} has leveled up to {}".format(user.mention, lvl_end))
		users[user.id]['level'] = lvl_end
		await client.process_commands(message)
	
		
@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    print('Deleted Message > {}: {}'.format(author, content))
    await client.process_commands(message)


@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji ,reaction.message.content))
    await client.process_commands(message)


@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has removed {} from the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
    await client.process_commands(message)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video queued.')

@client.command()
async def infobot():
    await client.say('Name: MagicNoob')
    await client.say('Role: Supreme')
    await client.say('Owner: Join My Minecraft Server or Mr Noob Pink')
    await client.say('Main Server: MagicNoob')


@client.command()
@commands.has_permissions(administrator=True)
async def say(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Deleted Message(s)')


@client.command(name='8ball',
                description="Answers yes/no",
                brief="Answers from the beyond. Do .m8ball for more info",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'No',
        'This question is shit',
        'Fuck U',
        'Yes',
        'Hmmm???',
        'I dont think so!',
        'You Know What BYE!',
        'I dont know',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


# Math Addition #

@client.command()
async def add(left: int, right: int):
    """Adds Two Numbers"""
    await client.say(left + right)


# Math Subtraction #

@client.command()
async def subtract(left: int, right: int):
    """Subtracts Two Numbers."""
    await client.say(left - right)


# Math Multiplication #

@client.command()
async def multiply(left: int, right: int):
    """Multiplies Numbers."""
    await client.say(left * right)


# Math Division #

@client.command()
async def divide(left: int, right: int):
    """Divides Numbers!"""
    try:
        await client.say(left // right)
    except ZeroDivisionError:
        await client.say("Numbers can't be divided by ZERO")


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.green()
    )
    embed.set_author(name='Help')
    embed.add_field(name='infobot', value='Gives bot information', inline=False)
    embed.add_field(name='8ball', value='Gives 8ball Messages', inline=False)
    embed.add_field(name='join', value='Makes the bot join the voice channel where you are in', inline=False)
    embed.add_field(name='leave', value='Makes the bot leave the voice channel', inline=False)
    embed.add_field(name='play', value='Plays an Audio. Usage: .mplay (Youtube Video Url)', inline=False)
    embed.add_field(name='pause', value='Pauses the Audio', inline=False)
    embed.add_field(name='stop', value='Stops the Audio', inline=False)
    embed.add_field(name='resume', value='Resumes the Audio', inline=False)
    embed.add_field(name='queue', value='Queues an Audio. Usage: .mqueue (Youtube Url)', inline=False)
    embed.add_field(name='add', value='Adds 2 numbers', inline=False)
    embed.add_field(name='subtract', value='Subtracts 2 numbers', inline=False)
    embed.add_field(name='multiply', value='Multiplies 2 numbers', inline=False)
    embed.add_field(name='divide', value='Divides 2 numbers', inline=False)
    embed.add_field(name='say', value='Repeats what you have said after .msay', inline=False)
    embed.add_field(name='clear', value='Clears Messages', inline=False)
    embed.add_field(name='Prefix', value='= .m', inline=False)

    await client.send_message(author, embed=embed)


client.run(str(os.environ.get('BOT_TOKEN')))
