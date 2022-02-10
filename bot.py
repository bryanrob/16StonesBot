# bot.py
import os
import random
from Stones import SixteenStones
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        ('I\'m the human form of the 💯 emoji.'),
        ('Bingpot!'),
        ( 'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    game = [ (os.system('python Stones.py')
    ) ]

    if message.content == '!play':
        game = SixteenStones()
        outputString('Turn: '+str(game.getturn()) + '\n')
        currentBoard = game.getBoard()
        for i in range(len(currentBoard)):
            for j in range(currentBoard[i]):
                outputString+='O '
            outputString+='\n'
        await message.channel.send(OutputString)
client.run(TOKEN)
