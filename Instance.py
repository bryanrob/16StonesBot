#Instance.py
#Created: 2 / 8 / 2022 (MM/DD/YYYY)
#Author: Robert B.
#Summary:
#The definition of an Instance: includes control logic for ensuring that the turn player is the only one who can
#change the state of the game.  Also defines the Player class, which simplifies how the system keeps track of each
#users' information in memory.

from Stones import SixteenStones
import random

class Instance:
	#The definition of an Instance.
	#Instances have 3 essential properties:
	#	1) The game itself.
	#	2) The players playing the game.
	#	3) A string output for each action.
	#
	#When initialized, an Instance must have 2 players (defined by thier Username & ID).
	#After an action has been performed through any of its functions (including its initializer), the 'outputString'
	#will be updated.  This value must be retreived after every action to show the game status.
	
	#Initializer
	def __init__(this,guildId,player1,player2):
		this.game=SixteenStones()
		this.players=[player1,player2]
		this.graphicsBoard=[]
		this.guild=guildId
		
		this.outputString="The game between [<@"+str(this.players[0].id)+">] and [<@"+str(this.players[1].id)+">] has begun!\n"
		this.outputString+=this.initializeBoardGraphics()
	#end function __init__(self,Player,Player)

	#Internal Function(s)

	def initializeBoardGraphics(this):
		returnThis=""
		returnThis+="> Turn: "+str(this.game.getTurn())+", Player "+str(this.game.getTurnPlayer())+" [<@"+str(this.players[this.game.getTurnPlayer()-1].id)+">], go.\n"

		stones=[":rock:",":new_moon:",":mountain:",":mountain_snow:",":moyai:"]
		rowLabels=[":one:",":two:",":three:",":four:",":five:"]
		rows=this.game.getBoard()

		for i in range(len(rows)):
			temp=[rowLabels[i]]
			for j in range(rows[i]):
				num=random.randint(0,99)
				if num>94:
					#print("Moyai generated!")
					temp.append(stones[len(stones)-1])
				else:
					temp.append(random.choice(stones[0:len(stones)-1]))
			this.graphicsBoard.append(temp)

		#tmp,moyaiFound,moyaiCounter=this.configureBoardGraphics()
		#returnThis+=tmp
		returnThis+=this.configureBoardGraphics()

		return returnThis.strip()

	def configureBoardGraphics(this):
		returnThis=""
		#moyaiFound=False
		#moyaiCounter=0

		board=this.game.getBoard()

		for i in range(len(board)):
			if board[i]<len(this.graphicsBoard[i]):
				this.graphicsBoard[i]=this.graphicsBoard[i][0:(board[i]+1)]

		for i in range(len(this.graphicsBoard)):
			for j in range(len(this.graphicsBoard[i])):
				returnThis+=this.graphicsBoard[i][j]
			returnThis+="\n"

		return returnThis#,moyaiFound,moyaiCounter

	#self.generateBoardGraphics(self):
	#Creates the graphical output of the board.  Is called in other Instance functions to update the 'outputString' value.
	def generateBoardGraphics(this):
		returnThis=""
		moyaiCounter=0
		moyaiFound=False

		for i in range(len(this.game.getBoard())):
			row=this.graphicsBoard[i][this.game.getBoard()[i]+1:len(this.graphicsBoard[i])]
			#print(row)
			if ':moyai:' in row:
				#print("Moyai found!")
				moyaiFound=True
				for stone in row:
					if stone==':moyai:':
						moyaiCounter+=1
		if moyaiFound:
			returnThis+=":moyai:\n"
		
		if this.game.getBoardSum()!=1:
			returnThis+="> Turn: "+str(this.game.getTurn())+", Player "+str(this.game.getTurnPlayer())+" [<@"+str(this.players[this.game.getTurnPlayer()-1].id)+">], go.\n" 

		#stones=["o","O","0"]
		#
		#rows=len(this.game.getBoard())
		#
		#for i in range(rows):
		#	returnThis+=str(i+1)+") "
		#	for j in range(this.game.getBoard()[i]):
		#		returnThis+=random.choice(stones)+" "
		#	returnThis+="\n"
		
		tmp=this.configureBoardGraphics()
		returnThis+=tmp

		return returnThis.strip(),moyaiFound,moyaiCounter
	#end function generateBoardGraphics(self)

	#Public Function(s)

	#move(self,Player,int,int)
	#Much like the move function in the SixteenStones class, the move function of Instance attempts to make a
	#play for a user.  There are a few checks that occur here, such as the state of the game (finished or ongoing),
	#as well as which player in this instance is allowed to make a play.
	#
	#'player' refers to the player attempting to make a play.  'row' is the selected row that the player is choosing,
	#whereas 'num' is the amount of stones that they are attempting to take from the selected 'row'.
	def move(this,player,row,num):
		this.outputString=""
		
		turnPlayer=this.game.getTurnPlayer()-1

		if player.id!=this.players[turnPlayer].id:
			this.outputString+="It is not your turn, <@"+str(player.id)+">."
		else:	
			result,resultMessage=this.game.move(row-1,num)	#The row input is supposed to be the index of the gameBoard
															#value in this game.  The player is expected to input a value
															#offset from the index by 1, thus the correction is made here.
			
			if this.game.getBoardSum()==1:
				output,moyaiFound,moyaiCounter=this.generateBoardGraphics()

				this.outputString="> **Game over!**\n> [<@"+str(this.players[turnPlayer].id)+">] wins!\n"

				for row in this.graphicsBoard:
					if ":moyai:" in row:
						this.outputString+="https://cdn.discordapp.com/attachments/331316693941092362/957274958940221461/sadmoyai.mp4\n"

				this.outputString+=output

				return moyaiFound,moyaiCounter
			else:			
				if result:
					this.outputString,moyaiFound,moyaiCounter=this.generateBoardGraphics()
					return moyaiFound,moyaiCounter
				else:
					this.outputString=resultMessage
		return False,0
	#end function move(self,Player,int,int)

	def hasPlayer(this,playerID):
		if playerID==this.player1.id or playerID==this.player2.id:
			return True
		else:
			return False
	#end function hasPlayer(int)
#END CLASS: Instance

class Player:
	#The definition of Player:
	#A player is composed of both the int userID and string username of a Discord user.  This exists to simplify how
	#an Instance stores the values of a player.

	#Initializer
	def __init__(this,id,username):
		this.id=id
		this.username=username
	#end __init__(self,int,string)

#END CLASS: Player

#EVERYTHING BELOW THIS LINE IS ONLY USED TO TEST THE CODE ABOVE.
#---------------------------------------------------------------

def main():
	print("Terst.\n")
	player1=Player(0,"xXplayer1Xx")
	player2=Player(1,"Player_2")
	
	runningInstance=Instance(player1,player2)
	
	print(runningInstance.outputString)
	
	move=[5,1]
	print(player1.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player1,move[0],move[1])
	print(runningInstance.outputString)
	
	move=[5,1]
	print(player1.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player1,move[0],move[1])
	print(runningInstance.outputString)
	
	move=[5,1]
	print(player2.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player2,move[0],move[1])
	print(runningInstance.outputString)
	
	move=[2,4]
	print(player2.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player2,move[0],move[1])
	print(runningInstance.outputString)
	
	runningInstance.move(player1,4,2)
	runningInstance.move(player2,1,6)
	
	print("\n...Some inputs later...\n")
	
	move=[2,-1]
	print(player1.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player1,move[0],move[1])
	print(runningInstance.outputString)
	
	move=[3,3]
	print(player1.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player1,move[0],move[1])
	print(runningInstance.outputString)
	
	move=[3,2]
	print(player1.username+": move "+str(move[0])+" "+str(move[1]))
	runningInstance.move(player1,move[0],move[1])
	print(runningInstance.outputString)
	
if __name__=="__main__":
	main()