#SixteenStones.py
#Created: 5 / 12/ 2021 (MM/DD/YYYY)
#Author: Robert B.
#Summary:
#The base game logic of Sixteen Stones: an interactive strategic multiplayer turn-based game.  Each player must take at least one stone from one of the five rows on the board, which homes sixteen individual stones total.  Players can take as many stones from a single row in their turn, but they must take at least one.  The player that takes the last stone loses, and becomes branded as the biggest dork the world has ever given birth to.
class SixteenStones:
	board=[0,0,0,0,0]
	boolBoard=[] 
	#[[true,true,true,true,true,true],
	#[false,false,true,true,true,true],
	#[false,false,false,true,true,true],
	#[false,false,false,false,true,true],
	#[false,false,false,false,false,true]]
	turn=0
	turnPlayer=[2,1]
	boardSum=0
	
	#Constructor:
	def __init__(self):
		self.board=[6,4,3,2,1]
		self.turn=1
		self.turnPlayer=[2,1]
		
		self.cfgBoolBoard()
		self.cfgBoardSum()
	#end function __init__(self)
	
	#Getter(s):
	def getBoard(self):
		return self.board
	def getBoolBoard(self):
		return self.boolBoard
	def getTurn(self):
		return self.turn
	def getTurnPlayer(self):
		return self.turnPlayer[self.turn%2]
	def getBoardSum(self):
		return self.boardSum
	#end of Getter(s).
	
	#Return Function(s)
	def move(self,row,stones):
		returnThisBool,returnThisStr = False,'Unexpected error.'
		
		if row>=5 or row<0:
			returnThisBool,returnThisStr=False,'Row does not exist.'
		else:
			if stones==0:
				returnThisBool,returnThisStr=False,'Player must take at least 1 stone.'
			elif stones<0:
				returnThisBool,returnThisStr=False,'Negative stones do not exist!'
			elif stones>self.board[row]:
				returnThisBool,returnThisStr=False,'Not enough stones exist in the row.'
			else:
				tempBoard=[]
				for i in range(len(self.board)):
					tempBoard.append(self.board[i])
				
				tempBoard[row]-=stones
				val=0
				for i in range(len(tempBoard)):
					val+=tempBoard[i]
				
				if val<1:
					returnThisBool,returnThisStr=False,'Must leave at least one stone on the board.'
				else:
					self.board=tempBoard
					self.cfgBoardSum()
					self.cfgBoolBoard()
					if self.boardSum>1:
						self.turn+=1
					returnThisBool,returnThisStr=True,'Success!'
		
		return returnThisBool,returnThisStr
	#end function move(self,row,stones)
	#end of Return Function(s)
	
	#Void Function(s):
	def cfgBoolBoard(self):
		self.boolBoard=[]
		for i in range(len(self.board)):
			temp=[]
			tempInt=self.board[i]
			for j in range(6):
				if tempInt>0:
					temp.append(True)
				else:	
					temp.append(False)
				tempInt-=1
			self.boolBoard.append(temp)
	#end function cfgBoolBoard(self)
		
	def cfgBoardSum(self):
		self.boardSum=0
		for i in range(len(self.board)):
			self.boardSum+=self.board[i]
	#end function cfgBoardSum(self)
	#end of Void Function(s)
#end class SixteenStones
#Everything below is only used to test the class.
def main():
	game=SixteenStones()

	while game.getBoardSum()>1:
		outputString=('Turn: '+str(game.getTurn())+'\n')
		currentBoard=game.getBoard()
		for i in range(len(currentBoard)):
			for j in range(currentBoard[i]):
				outputString+='O '
			outputString+='\n'
			
		print(outputString)
		
		waitForInput=True
		while waitForInput:
			inputArr=inputIntArr("Enter 2 integer values separated by a space(\" \"): ")
			
			inputArr[0]-=1
			if len(inputArr)==2:
				cBool,cStr=game.move(inputArr[0],inputArr[1])
				
				if cBool:
					waitForInput=False
				else:
					print('Error: '+cStr)
			else:
				print("Input error: Must enter only 2 values.")
		print()
	
	outputString=('Turn: '+str(game.getTurn())+'\n')
	currentBoard=game.getBoard()
	for i in range(len(currentBoard)):
		for j in range(currentBoard[i]):
			outputString+='O '
		outputString+='\n'
		
	print(outputString)
	
	print('Player '+str(game.getTurnPlayer())+' has won!')
	
	#print('Returned values: '+str(x)+' & '+str(y))
	
def inputIntArr(query):
	keepGoing=True
	returnThis=[]
	while keepGoing:
		returnThis=[]
		response=input(query)
		
		rSplit=response.split(' ')
		try:
			for i in range(len(rSplit)):
				returnThis.append(int(rSplit[i]))
			keepGoing=False
		except:
			print("Input error: Enter only integer values separated by a single space (\" \").")
		
	return returnThis

if __name__=="__main__":
	main()