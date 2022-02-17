# bot.py
import os
from posixpath import split
import random
from Stones import SixteenStones
from Instance import Instance, Player
import discord
from dotenv import load_dotenv

load_dotenv()

file=open("token.tkn","r")
TOKEN=file.readline()
print("Token from \{token.tkn\}: "+TOKEN)
file.close()
#TOKEN = os.getenv(token)

client = discord.Client()

instances={}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#@client.event
#async def on_member_join(member):
#    await member.create_dm()
#    await member.dm_channel.send(
#        f'Hi {member.name}, welcome to my Discord server!'
#    )

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#
#    brooklyn_99_quotes = [
#        ('I\'m the human form of the 💯 emoji.'),
#        ('Bingpot!'),
#        ( 'Cool. Cool cool cool cool cool cool cool, '
#            'no doubt no doubt no doubt no doubt.'
#        ),
#    ]
#
#    if message.content == '99!':
#        response = random.choice(brooklyn_99_quotes)
#        await message.channel.send(response)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        player1=Player(message.author.id,message.author.name)
        outputString="**An unexpected error has occurred.**\nPlease make sure that the command syntax is correct."
        splitMessage=message.content.strip().split(" ")

        if len(splitMessage)==2:
            targetUser= await client.fetch_user(int(splitMessage[1][3:-1]))
            player2=Player(targetUser.id,targetUser.name)

            if player2==None:
                outputString="**Error:** user not found."
            elif player1.id==player2.id:
                outputString="**Error:** You cannot play against yourself."
            elif player1.id in instances:
                outputString="**Error:** ["+player1.username+"] is already in an instance."
            elif player2.id in instances:
                outputString="**Error:** ["+player2.username+"] is already in an instance."
            else:
                instance=Instance(player1,player2)
                instances[player1.id]=instance
                instances[player2.id]=instance

                outputString=instance.outputString
        else:
            outputString="**Input error:** Ping the user who you want to play against."

        #game = SixteenStones()
        #outputString =('Turn: '+str(game.getTurn()) + '\n')
        #currentBoard = game.getBoard()
        #for i in range(len(currentBoard)):
        #    for j in range(currentBoard[i]):
        #        outputString+='O '
        #    outputString+='\n'
        await message.channel.send(outputString)

    elif message.content.startswith('!take'):
        print("This should be configured to take in arguments.  String should contain '!take', not have only '!take'.")

        await message.channel.send("**'!take'** command received without any arguments.\nSorry, but this command is still in the works.")


client.run(TOKEN)
