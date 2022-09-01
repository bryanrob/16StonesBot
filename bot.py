# bot.py
import atexit
import os
import sys
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
TOKEN=None
tokens=file.readlines()
file.close()

if len(tokens)==0:
    sys.exit("\nSTARTUP ERROR: \"token.tkn\" file is empty.\nPlease save your Discord bot tokens into the file.")
else:
    for i in range(len(tokens)):
        tokens[i]=tokens[i].strip()
    if len(tokens)==1:
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
                sys.exit(0)
            try:
                selection=int(response)
                if selection>0 and selection<=len(tokens):
                    TOKEN=tokens[selection-1]
                    invalidSelection=False
                else:
                    print("Invalid selection.  Please enter only the number corresponding with the listed token above.")
            except:
                print("Input error: enter only an integer value.")

print("Connecting with TOKEN: "+TOKEN)

client = discord.Client()
db=DB()

print("Creating instances library...")
instances={}
print("Instance library initialized!")

print("Logging into Discord...")
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
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
        #end: if(prefix+"play")
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
                            moyaiFound,moyaiCounter=instance.move(user,row,num)

                            if moyaiFound:
                                db.addMoyai(message.author.id,message.guild.id,moyaiCounter)

                            outputString=instance.outputString
                if instance.game.getBoardSum()==1:
                    looser=instance.game.getTurn()%2
                    if looser==0:
                        winrar=1
                    else:
                        winrar=0
                    #db.addWin(instance.players[winrar].id,message.guild.id)
                    #db.addLoss(instance.players[looser].id,message.guild.id)

                   

                    #distributeWinLoss(instance,message.guild.id)

                    w_user=await client.fetch_user(instance.players[winrar].id)
                    l_user=await client.fetch_user(instance.players[looser].id)

                    outputString+="\n"+distributeWinLossAndOutput(w_user,l_user,message.guild.id)

                    del instances[instance.players[0].id]
                    del instances[instance.players[1].id]
            else:
                outputString="**Error:** You are not in any existing instance, <@"+str(message.author.id)+">.\nYou can create one using the **!play** command."
        #end: if(prefix+"take <arg>")
        elif message.content==prefix+'quit':
            outputString=""
            found,instance=removeInstance(message.author.id)

            if found:
                if instance.players[0].id==message.author.id:
                    #db.addLoss(instance.players[0].id,message.guild.id)
                    #db.addWin(instance.players[1].id,message.guild.id)
                    outputString+="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!\n"
                    
                    w_user=await client.fetch_user(instance.players[1].id)
                    l_user=await client.fetch_user(instance.players[0].id)

                    outputString+=distributeWinLossAndOutput(w_user,l_user,message.guild.id)

                elif instance.players[1].id==message.author.id:
                    #db.addLoss(instance.players[1].id,message.guild.id)
                    #db.addWin(instance.players[0].id,message.guild.id)
                    outputString+="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!\n"
                    
                    w_user=await client.fetch_user(instance.players[0].id)
                    l_user=await client.fetch_user(instance.players[1].id)

                    outputString+="\n"+distributeWinLossAndOutput(w_user,l_user,message.guild.id)

            else:
                outputString=instance
        #end: if(prefix+"quit")
        elif message.content==prefix+'help':
            outputString="__**The Rules of Sixteen Stones**__\nThe game starts with a new board that contains sixteen stones.  Each player takes turns taking stones from the board.  This will continue until there is only 1 stone left on the board; at which point, **the player that takes the last stone __loses__**.  In other words, it does not matter how many stones you have- make sure you do **__not__** take the last stone!\nThe rules for taking stones from the board are as follows:\n> The turn player must take at least one stone to complete their turn.\n> A player can take as many stones from a single row as they want during their turn.\n> Players cannot add stones to the board.\n\n__**In-Chat Commands**__\nTo play the game against someone, simply enter:\n```!play @<user>```\t**<user>** will be the player you play against.\nIf you are playing, you can take stones using:\n```!take <row> <stones>```\tTakes the amount of **<stones>** from your selected **<row>**.\nIf you want to quit an instance, enter:\n```!quit```To view the leaderboards, use:```!leaderboard <arg>```Keep in mind, however, that **your played games will __NOT__ be tracked on the leaderboard until you complete your leaderboard registration!**\nYou can do this by using the `!register` command.\nYou can also remove your leaderboard data at anytime using the `!unregister` command, or `!unregister-from-all` to erase all of your registries from the database under this bot's control.\n\nGood luck, and have fun!"
        #end: if(prefix+"help")
        elif message.content==prefix+'help-admin':
            if message.author.guild_permissions.administrator:
                outputString="__**Administrator Commands**__\nAdministrators can use these commands in order to moderate the activities of SixteenStones within their server:\n```!clearInstance @<user>```Deletes the instance with the pinged <user>.  Wins/Losses are not affected by this command.```!clearInstances```Deletes all instances running on your server.  Wins/Losses are not affected by this command.```!unregister-user```Unregisters the pinged user from your server's leaderboard.  Their Wins and Losses will be erased from your server's database completely, so if the user registers again, their data will reset to the default starter values.\nIf you need to erase all leaderboard records from your server, you can use ```!unregister-server```"
            else:
                outputString="**Error:** you do not have sufficient server permissions to access this command."
        #end: if(prefix+"help-admin")
        elif message.content==prefix+'fu':
            found,instance=removeInstance(message.author.id)

            if found:
                outputString="> ** (ノಠ益ಠ)ノ彡┻━┻ "

                stones=" ﾟ.*・｡ﾟ"
                boardSum=instance.game.getBoardSum()
                if len(stones)<boardSum:
                    n=len(stones)
                else:
                    n=boardSum
                for i in range(n):
                    outputString+=stones[i]
                outputString+="ヾ(ﾟдﾟ)ﾉ゛**"
                if instance.game.getTurn()<=2:
                    outputString+="```\t\t\t\t\tBut we just started!```"
                else:
                    outputString+="\n"
                outputString+="\n"
                if instance.players[0].id==message.author.id:
                    #db.addLoss(instance.players[0].id,message.guild.id)
                    #db.addWin(instance.players[1].id,message.guild.id)
                    outputString+="Player 1 [<@"+str(instance.players[0].id)+">] admits defeat.\nPlayer 2 [<@"+str(instance.players[1].id)+">] wins!\n"
                    w_user=await client.fetch_user(instance.players[1].id)
                    l_user=await client.fetch_user(instance.players[0].id)

                    outputString+=distributeWinLossAndOutput(w_user,l_user,message.guild.id)
                elif instance.players[1].id==message.author.id:
                    #db.addLoss(instance.players[1].id,message.guild.id)
                    #db.addWin(instance.players[0].id,message.guild.id)
                    outputString+="Player 2 [<@"+str(instance.players[1].id)+">] admits defeat.\nPlayer 1 [<@"+str(instance.players[0].id)+">] wins!\n"
                    w_user=await client.fetch_user(instance.players[0].id)
                    l_user=await client.fetch_user(instance.players[1].id)

                    outputString+=distributeWinLossAndOutput(w_user,l_user,message.guild.id)
            else:
                outputString=instance
            #end: if(prefix+"fu")
        elif message.content==prefix+"clearInstances":
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
        #end: if(prefix+"clearInstances")
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
        #end: if(prefix+"clearInstance <arg>")
        elif message.content.startswith(prefix+"leaderboard"):
            outputString=""
            splitMessage=message.content.strip().split(" ")
            if len(splitMessage)==2:
                if splitMessage[1][0].lower()=='w':
                    rows=db.getOrderByWins(message.guild.id)

                    outputString+="> **__Leaderbord by Wins__**\n"
                    outputString="```{:^4s}|{:^25s}|{:^6s}|{:^6s}|{:^9s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^6s}+{hf:-^6s}+{hf:-^9s}\n".format("Pos.","User","Wins","Losses","W/L Ratio",hf="")
                    for i in range(len(rows)):
                        outputString+="{:>4d}|".format(i+1)
                        user=await client.fetch_user(rows[i][0])
                        outputString+="{:^25s}|{:^6d}|{:^6d}|{:^9.2f}\n".format(user.display_name,rows[i][2],rows[i][3],rows[i][4])
                    outputString+="```"

                    #outputString+=await generateLeaderboardData(rows)
                    
                elif splitMessage[1][0].lower()=='l':
                    rows=db.getOrderByLosses(message.guild.id)

                    outputString+="> **__Leaderbord by Losses__**\n"
                    outputString="```{:^4s}|{:^25s}|{:^6s}|{:^6s}|{:^9s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^6s}+{hf:-^6s}+{hf:-^9s}\n".format("Pos.","User","Losses","Wins","W/L Ratio",hf="")
                    for i in range(len(rows)):
                        outputString+="{:>4d}|".format(i+1)
                        user=await client.fetch_user(rows[i][0])
                        outputString+="{:^25s}|{:^6d}|{:^6d}|{:^9.2f}\n".format(user.display_name,rows[i][3],rows[i][2],rows[i][4])
                    outputString+="```"
                    
                    #outputString+=await generateLeaderboardData(rows)
                    
                elif splitMessage[1][0].lower()=='r':
                    rows=db.getOrderByWinLossRatio(message.guild.id)

                    outputString+="> **__Leaderbord by Win/Loss Ratio__**\n"
                    
                    outputString="```{:^4s}|{:^25s}|{:^9s}|{:^6s}|{:^6s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^9s}+{hf:-^6s}+{hf:-^6s}\n".format("Pos.","User","W/L Ratio","Wins","Losses",hf="")
                    for i in range(len(rows)):
                        outputString+="{:>4d}|".format(i+1)
                        user=await client.fetch_user(rows[i][0])
                        outputString+="{:^25s}|{:^9.2f}|{:^6d}|{:^6d}\n".format(user.display_name,rows[i][4],rows[i][2],rows[i][3])
                    outputString+="```"

                    #outputString+=await generateLeaderboardData(rows)

                elif splitMessage[1][0].lower()=='m':
                    rows=db.getOrderByMoyai(message.guild.id)

                    outputString+="> **__Leaderbord :moyai:__**\n"

                    outputString+="```{:^4s}|{:^25s}|{:^5s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^5s}\n".format("Pos.","User","Moyai",hf="")
                    for i in range(len(rows)):
                        outputString+="{:>4d}|".format(i+1)
                        user=await client.fetch_user(rows[i][0])
                        outputString+="{:^25s}|{:^5d}\n".format(user.display_name,rows[i][5])
                    outputString+="```"

                else:
                    outputString="**Input error:** Please specify which leaderbord you want to view:\n```"+prefix+"leaderbord <arg>```Replace **<arg>** with any of the following:\n> **W** = Wins\n> **L** = Losses\n> **R** = Win/Loss Ratio\n> **M** = :moyai:"
            else:
                outputString="**Input error:** Invalid amount of arguments passed.\nPlease specify which leaderbord you want to view:\n```"+prefix+"leaderbord <arg>```Replace **<arg>** with any of the following:\n> **W** = Wins\n> **L** = Losses\n> **R** = Win/Loss Ratio\n> **M** = :moyai:"
        #end: if(prefix+"leaderboard <arg>")
        elif message.content.startswith(prefix+"register"):
            result=db.addNewUser(message.author.id,message.guild.id)
            if result:
                outputString=f"<@{message.author.id}>, you have been successfully registered to this server's leaderboard database."
            else:
                outputString=f"<@{message.author.id}>, you are already registered in this server's leaderboard database."
        #end: if(prefix+"register")
        elif message.content==prefix+"unregister":
            result=db.removeUser(message.author.id,message.guild.id)
            if result:
                outputString=f"<@{message.author.id}>, you have been successfully removed this server's leaderboard database."
            else:
                outputString=f"<@{message.author.id}>, you are not in this server's leaderboard database.  If you would like to join the database, use the `!register` command."
        #end: if (prefix+"unregister")
        elif message.content==prefix+"unregister-from-all":
            result=db.removeAllofUser(message.author.id)

            if result:
                outputString=f"<@{message.author.id}>, you have been unregistered from all server databases monitored by this bot."
            else:
                outputString=f"<@{message.author.id}>, your user data was not detected in our database."
        #end: if(prefix+"unregister-from-all")
        elif message.content.startswith(prefix+"unregister-user"):
            if message.author.guild_permissions.administrator:
                userFound,user=await getUserInMessage(message.content)

                if userFound:
                    result=db.removeUser(user.id,message.guild.id)

                    if result:
                        outputString=f"Removed {user.display_name} from this server's database."
                    else:
                        outputString=f"{user.display_name} is not in this server's database."
                else:
                    outputString="**Error:** user not found."
            else:
                outputString="**Error:** you do not have sufficient server permissions to use this command."
        #end: if(prefix+"unregister-user <arg>")
        elif message.content==prefix+"unregister-server":
            if message.author.guild_permissions.administrator:
                result=db.removeAllInServer(message.guild.id)

                if result:
                    outputString="All leaderboard records in this server have been successfully erased!"
                else:
                    outputString="**Error:** No leaderboard records for this server were found."
            else:
                outputString="**Error:** you do not have sufficient server permissions to use this command."
        #end: if(prefix+"unregister-server")
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

async def generateLeaderboardData(data):
    outputString="```{:^4s}|{:^25s}|{:^6s}|{:^6s}|{:^9s}|{:^5s}\n{hf:-^4s}+{hf:-^25s}+{hf:-^6s}+{hf:-^6s}+{hf:-^9s}+{hf:-^5s}\n".format("Pos.","User","Wins","Losses","W/L Ratio","Moyai",hf="")
    for i in range(len(data)):
        outputString+="{:>4d}|".format(i+1)
        user=await client.fetch_user(data[i][0])
        outputString+="{:^25s}|{:^6d}|{:^6d}|{:^9.2f}|{:^5d}\n".format(user.display_name,data[i][2],data[i][3],data[i][4],data[i][5])
    outputString+="```"
    return outputString

def distributeWinLoss(instance,guildid):
    looser=instance.game.getTurn()%2
    if looser==0:
        winrar=1
    else:
        winrar=0
    db.addWin(instance.players[winrar].id,guildid)
    db.addLoss(instance.players[looser].id,guildid)

def distributeWinLossAndOutput(winrar,looser,guildid):
    returnThis=""

    winrarRowExists,wdata=db.getRowById(winrar.id,guildid)
    looserRowExists,ldata=db.getRowById(looser.id,guildid)

    if winrarRowExists:
        db.addWin(winrar.id,guildid)
        #returnThis+=f"**{winrar.display_name}:** Wins: {wdata[2]} (+1), Losses: {wdata[3]} (+0), Ratio: {wdata[4]}\n"
        winrarRowExists,wdata=db.getRowById(winrar.id,guildid)
        returnThis+="**{:s}:** Wins: {:d} (+1), Losses: {:d} (+0), Ratio: {:.2f}.\n".format(winrar.display_name,wdata[2],wdata[3],wdata[4])
    else:
        #returnThis+=f"**{winrar.display_name}:** __Results not saved__.  You must `!register` to this server's leaderboard in order to save future results.\n"
        returnThis+="**{:s}:** __Results not saved__.  You must `!register` to this server's leaderboard in order to save future results.\n".format(winrar.display_name)
    if looserRowExists:
        db.addLoss(looser.id,guildid)
        looserRowExists,ldata=db.getRowById(looser.id,guildid)
        #returnThis+=f"**{looser.display_name}:** Wins: {ldata[2]} (+0), Losses: {ldata[3]} (+1), Ratio: {ldata[4]}"
        returnThis+="**{:s}:** Wins: {:d} (+0), Losses: {:d} (+1), Ratio: {:.2f}.\n".format(looser.display_name,ldata[2],ldata[3],ldata[4])
    else:
        #returnThis+=f"**{looser.display_name}:** __Results not saved__.  You must `!register` to this server's leaderboard in order to save future results."
        returnThis+="**{:s}:** __Results not saved__.  You must `!register` to this server's leaderboard in order to save future results.\n".format(looser.display_name)
    return returnThis


client.run(TOKEN)

import atexit
@atexit.register
def terminate():
    db.close()
