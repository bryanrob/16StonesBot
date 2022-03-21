# bot.py
from asyncio.windows_events import NULL
import os
from posixpath import split
import random
from Stones import SixteenStones
from Instance import Instance, Player
import discord
from dotenv import load_dotenv

load_dotenv()

file=open("token.tkn","r")
TOKEN=NULL
tokens=[]
while(True):
    line=file.readline()
    if not line:
        break
    line=line.strip()
    tokens.append(line)

if len(tokens)==0:
    print("Error: token.tkn file is empty.\nPlease save your Discord bot tokens into the file.")
elif len(tokens)==1:
    TOKEN=tokens[0]
else:
    print("Multiple tokens found.  Please select which one you are using:")
    for i in range(len(tokens)):
        print(str(i+1)+") "+tokens[i])
    invalidSelection=True
    while invalidSelection:
        response=input()
        if response.lower()=="exit":
            print("Program terminated.")
            exit(0)
        try:
            selection=int(response)
            if selection>0 and selection<=len(tokens):
                TOKEN=tokens[selection-1]
                invalidSelection=False
            else:
                print("Invalid selection.  Please enter only the number corresponding with the listed token above.")
        except:
            print("Input error: enter only an integer value.")

#TOKEN=file.readline()
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
    sendOutput=False
    if message.author == client.user:
        return

    outputString="**An unexpected error has occurred.**\nPlease make sure that the command syntax is correct."

    if message.content.startswith('!'):
        #sendOutput=True
        outputString="**Error: unknown command.**\nPlease make sure your syntax is correct and try again."

        if message.content.startswith('!play'):
            #print(message.content)
            player1=Player(message.author.id,message.author.name)
            
            splitMessage=message.content.strip().split(" ")

            if len(splitMessage)==2:
                #print("Player 1 id: "+str(message.author.id)+"\nPlayer 2 id: "+splitMessage[1][3:-1])
                userFound=False
                targetUser=0
                try:
                    try:
                        targetUser= await client.fetch_user(int(splitMessage[1][3:-1]))
                    except:
                        print("Mobile input detected.")
                        targetUser= await client.fetch_user(int(splitMessage[1][2:-1]))
                    userFound=True
                    player2=Player(targetUser.id,targetUser.name)
                except:
                    outputString="**Error:** user not found."
                

                if userFound:
                    if player1.id==player2.id:
                        outputString="**Error:** You cannot play against yourself."
                    elif player2==client.user.id:
                        outputString="**Error:** I cannot play Sixteen Stones against you."
                    elif player1.id in instances:
                        outputString="**Error:** ["+player1.username+"] is already in an instance."
                    elif player2.id in instances:
                        outputString="**Error:** ["+player2.username+"] is already in an instance."
                    else:
                        instance=Instance(message.guild.id,player1,player2)
                        instances[player1.id]=instance
                        instances[player2.id]=instance

                        outputString=instance.outputString
            else:
                outputString="**Input error:** Ping the user who you want to play against.\nExample:/n> !play @exampleUser"

        elif message.content.startswith('!take'):
            user=Player(message.author.id,message.author.name)
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
                outputString="**Error:** You are not in any existing instance, <@"+str(message.author.id)+">.\nYou can create one using the **!play** command."

        elif message.content.startswith('!quit'):
            found,instance=removeInstance(message.author.id)

            if found:
                if instance.players[0].id==message.author.id:
                    outputString="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!"
                elif instance.players[1].id==message.author.id:
                    outputString="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!"
            else:
                outputString=instance

        elif message.content.startswith('!help'):
            outputString="__**The Rules of Sixteen Stones**__\nThe game starts with a new board that contains sixteen stones.  Each player takes turns taking stones from the board.  This will continue until there is only 1 stone left on the board; at which point, **the player that takes the last stone __loses__**.  In other words, it does not matter how many stones you have- make sure you do **__not__** take the last stone!\nThe rules for taking stones from the board are as follows:\n> The turn player must take at least one stone to complete their turn.\n> A player can take as many stones from a single row as they want during their turn.\n> Players cannot add stones to the board.\n\n__**In-Chat Commands**__\nTo play the game against someone, simply enter:\n```!play @<user>```\t**<user>** will be the player you play against.\nIf you are playing, you can take stones using:\n```!take <row> <stones>```\tTakes the amount of **<stones>** from your selected **<row>**.\nIf you want to quit an instance, enter:\n```!quit```\nGood luck, and have fun!"
                    
        elif message.content.startswith('!fu'):
            found,instance=removeInstance(message.author.id)

            if found:
                outputString="**> (ノಠ益ಠ)ノ彡┻━┻ "

                stones=" ﾟ.*・｡ﾟ"
                boardSum=instance.game.getBoardSum()
                if len(stones)<boardSum:
                    n=len(stones)
                else:
                    n=boardSum
                for i in range(n):
                    outputString+=stones[i]

                if instance.game.getTurn()<=2:
                    outputString+="ヾ(ﾟдﾟ)ﾉ゛\n```\t\t\tBut we just started!```"

                outputString+="**\n"
                if instance.players[0].id==message.author.id:
                    outputString+="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!"
                elif instance.players[1].id==message.author.id:
                    outputString+="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!"
            else:
                outputString=instance
        elif message.content.startswith("!clearInstances"):
            if message.author.guild_permissions.administrator:
                messageGuild=message.guild.id
                outputString="**yeet**\n```All guild instances removed.```"
                toDelete=[]

                for instance in instances:
                    if messageGuild==instances[instance].guild:
                        if instances[instance].players[0].id not in toDelete:
                            toDelete.append(instances[instance].players[0].id)
                        if instances[instance].players[1].id not in toDelete:
                            toDelete.append(instances[instance].players[1].id)
                if len(toDelete)==0:
                    outputString="**Error:** No running instances found."
                else:
                    for i in toDelete:
                        del instances[i]
            else:
                outputString="**Error:** You are not a server administrator."
        await message.channel.send(outputString)
#End of on_message()


def removeInstance(id):
    if id in instances:
        instance=instances[id]
        del instances[instance.players[0].id]
        del instances[instance.players[1].id]
        return True,instance
    return False,"**Error:** You are not in an active instance, <@"+str(id)+">."
            
client.run(TOKEN)
