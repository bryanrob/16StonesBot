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

    outputString="**An unexpected error has occurred.**\nPlease make sure that the command syntax is correct."

    if message.content.startswith('!play'):
        player1=Player(message.author.id,message.author.name)
        
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
        user=Player(message.author.id,message.author.name)
        #outputString="**'!take'** command received without any arguments.\nSorry, but this command is still in the works."
        if message.author.id in instances:
            instance=instances[message.author.id]
            splitMessage=message.content.strip().split(" ")
            
            if len(splitMessage)!=3:
                outputString="**Input error:** Command syntax is incorrect."
            else:
                isValid=False
                row,num=0,0
                makeMove=False
                try:
                    row=int(splitMessage[1])
                    num=int(splitMessage[2])

                    makeMove=True
                except:
                    outputString="**Input error:** The command arguments can only be integers."
                finally:
                    if makeMove:
                        instance.move(user,row,num)

                        outputString=instance.outputString
            if instance.game.getBoardSum()==1:
                del instances[instance.players[0].id]
                del instances[instance.players[1].id]
        else:
            outputString="**Error:** You are not in any existing instance.\nYou can create one using the **!play** command."
        #print("This should be configured to take in arguments.  String should contain '!take', not have only '!take'.")

        await message.channel.send(outputString)

    elif message.content.startswith('!quit'):
        if message.author.id in instances:
            instance=instances[message.author.id]
            
            if instance.players[0].id==message.author.id:
                outputString="Player 1 ["+instance.players[0].username+"] admits defeat."
            elif instance.players[1].id==message.author.id:
                outputString="Player 2 ["+instance.players[1].username+"] admits defeat."
            del instances[instance.players[0].id]
            del instances[instance.players[1].id]
        else:
            outputString="**Error:** You are not in an active instance."

        await message.channel.send(outputString)
            
client.run(TOKEN)
