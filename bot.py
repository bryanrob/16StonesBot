# bot.py
from asyncio.windows_events import NULL
import atexit
import os
from posixpath import split
import random
from unittest import result
from Stones import SixteenStones
from Instance import Instance, Player
import discord
from dotenv import load_dotenv
from Database import DB

prefix="!"

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
db=DB()

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

    if message.content.startswith(prefix):
        outputString="**Error: unknown command.**\nPlease make sure your syntax is correct and try again."

        if message.content.startswith(prefix+'play'):
            #print(message.content) #Debugging
            player1=Player(message.author.id,message.author.name)
            
            splitMessage=message.content.strip().split(" ")

            if len(splitMessage)==2:
                userFound,targetUser=await getUserInMessage(message.content)

                if userFound:
                    player2=Player(targetUser.id,targetUser.name)
                    if player1.id==player2.id:
                        outputString="**Error:** You cannot play against yourself."
                    elif player2.id==client.user.id:
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
                    outputString=targetUser
            else:
                outputString="**Input error:** Ping the user who you want to play against.\nExample:/n> !play @exampleUser"

        elif message.content.startswith(prefix+'take'):
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

        elif message.content.startswith(prefix+'quit'):
            found,instance=removeInstance(message.author.id)

            if found:
                if instance.players[0].id==message.author.id:
                    outputString="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!"
                elif instance.players[1].id==message.author.id:
                    outputString="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!"
            else:
                outputString=instance

        elif message.content.startswith(prefix+'help'):
            outputString="__**The Rules of Sixteen Stones**__\nThe game starts with a new board that contains sixteen stones.  Each player takes turns taking stones from the board.  This will continue until there is only 1 stone left on the board; at which point, **the player that takes the last stone __loses__**.  In other words, it does not matter how many stones you have- make sure you do **__not__** take the last stone!\nThe rules for taking stones from the board are as follows:\n> The turn player must take at least one stone to complete their turn.\n> A player can take as many stones from a single row as they want during their turn.\n> Players cannot add stones to the board.\n\n__**In-Chat Commands**__\nTo play the game against someone, simply enter:\n```!play @<user>```\t**<user>** will be the player you play against.\nIf you are playing, you can take stones using:\n```!take <row> <stones>```\tTakes the amount of **<stones>** from your selected **<row>**.\nIf you want to quit an instance, enter:\n```!quit```\nGood luck, and have fun!"
                    
        elif message.content.startswith(prefix+'fu'):
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
                    outputString+="ヾ(ﾟдﾟ)ﾉ゛\n```\t\t\t\t\tBut we just started!```"

                outputString+="**\n"
                if instance.players[0].id==message.author.id:
                    outputString+="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!"
                elif instance.players[1].id==message.author.id:
                    outputString+="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!"
            else:
                outputString=instance
        elif message.content.startswith(prefix+"clearInstances"):
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
        elif message.content.startswith(prefix+"clearInstance"):
            if message.author.guild_permissions.administrator:
                splitMessage=message.content.strip().split(" ")
                if len(splitMessage)==2:
                    userFound,user=await getUserInMessage(message.content)
                    #print(user)
                    if userFound:
                        success,instance=removeInstance(user.id)
                        if success:
                            outputString="Removed instance between <@"+str(instance.players[0].id)+"> and <@"+str(instance.players[1].id)+">."
                        else:
                            outputString="**Error:** Specified user is not in an instance."
                    else:
                        outputString=user
                else:
                    outputString="**Input error:** Ping the user in the instance you want to delete.\nExample:\n```!clearInstance @<user>```"
            else:
                outputString="**Error:** You are not a server administrator."

        elif message.content.startswith(prefix+"leaderbord"):
            splitMessage=message.content.strip().split(" ")
            if len(splitMessage)==2:
                if splitMessage[1][0].lower()=='w':
                    rows=db.getOrderByWins(message.guild.id)

                    outputString+="> **__Leaderbord by Wins__**\n"
                    #
                    #Enter addition to output string here.
                    #
                elif splitMessage[1][0].lower()=='l':
                    rows=db.getOrderByLosses(message.guild.id)

                    outputString+="> **__Leaderbord by Losses__**\n"
                    #
                    #Enter addition to output string here.
                    #
                elif splitMessage[1][0].lower()=='r':
                    rows=db.getOrderByWinLossRatio(message.guild.id)

                    outputString+="> **__Leaderbord by Win/Loss Ratio__**\n"
                    #
                    #Enter addition to output string here.
                    #
                else:
                    outputString="**Input error:** Please specify which leaderbord you want to view:\n```"+prefix+"leaderbord <arg>```> W = Wins\n> L = Losses\n> R = Win/Loss Ratio"
            else:
                outputString="**Input error:** Invalid amount of arguments passed.\nPlease make sure that your syntax is correct."
        await message.channel.send(outputString)
#End of on_message()

#removeInstance(id:int) : Boolean, Instance OR String;
#Deletes an instance populated by the player with the specified {id}.
#Returns True and the Instance object that was just deleted from the
#dictionary if the {id} is present in an instance.  Otherwise, returns
#False and a string containing a default error message.
def removeInstance(id):
    if id in instances:
        instance=instances[id]
        del instances[instance.players[0].id]
        del instances[instance.players[1].id]
        return True,instance
    return False,"**Error:** You are not in an active instance, <@"+str(id)+">."
            
#getUserInMessage(message:String) : Boolean, discord.User OR String;
#Obtains the user who's specified within the message containing only
#the command and the mention of the user.  If the message does NOT
#meet the above criteria, then the function will return False and
#a String default error message.  Otherwise, it will attempt to get
#the user data from Discord.  If the user was not found, the function
#will return False and a default error message stating that the user
#wasn't found.  If the user was found, then it will return True and
#the discord.User object of the specified user.
async def getUserInMessage(message):
    splitMessage=message.strip().split(" ")
    #print(splitMessage[1][3:-1]) #debugging...
    if len(splitMessage)==2:
        userFound=False
        try:
            try:
                result= await client.fetch_user(int(splitMessage[1][3:-1]))
            except:
                #print("Mobile input detected.") #debugging...
                result= await client.fetch_user(int(splitMessage[1][2:-1]))
            userFound=True
        except:
            result="**Error:** user not found."
        finally:
            return userFound,result
    else:
        return False,"**Syntax Error:** Enter only the command and its user argument."
client.run(TOKEN)

import atexit
@atexit.register
def terminate():
    db.close()
