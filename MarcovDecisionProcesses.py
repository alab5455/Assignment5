#Name: Ali Abu AlSaud
#Date: 10/7/2015
#Assignemnt 5: Searching for a solution using Markov Decision Processes

#Importing the array library, that is going to be used later
from array import*

#Maze class that will store each maze in a dictionary format
class maze():
	
	#Constructor
	def __init__(Maze):
		Maze.dictionary = {}
	
	#Method to add vertex to the dictionary, in my situation, to add a row number from the maze
	def addVertex(Maze, value):
		newDictionary = {value:[]}
		Maze.dictionary.update(newDictionary)
	
	#Method to add punch of numbers inside the row, which is in my case the numbers in each colomn on that specific row
	def addEdge(Maze, row, element):
		if Maze.dictionary.has_key(row):
			Maze.dictionary.get(row).append(element)
		else:
			print "The row cannot be found."
			
	#Method that will return the content of the position that you entered (row, colomn)
	def location(Maze, row, Position):
		my_array = array('i', [])
		for elements in Maze.dictionary.get(8-row):
			my_array.append(int(format(elements)))
		return my_array[Position-1]

gamma = 0.9
epsilon = input("Enter the value of epsilon that you want to use, the value should be small (typically Less than 1) : ") #The user get to choose the value of epsilon
Reward = 0
Utility = 0
changeRequired = epsilon * ( (1 - gamma) / gamma )
Maze = maze()

#Reading the data from the files to the mazes variables:
with open('World1MDP.txt') as world:
	for i in range(8):
		Maze.addVertex(i)
		for j in range(10):
			element = int(world.readline(1))
			if element == 5:
				element = element * 10
				world.readline(1)
			Maze.addEdge(i, element)
			world.readline(1)

#Storing all the rewards of all the positions on the maze
reward = [[0 for x in range(10)] for x in range(8)]
for i in range(8):
	for j in range(10):
		if Maze.location(i+1,j+1) == 1:
			reward[i][j] = -1
		elif Maze.location(i+1,j+1) == 3:
			reward[i][j] = -2
		elif Maze.location(i+1, j+1) == 4:
			reward[i][j] = 5
		elif Maze.location(i+1, j+1) == 50:
			reward[i][j] = 50
		elif Maze.location(i+1, j+1) == 2:
			reward[i][j] = -50
		else:
			reward[i][j] = 0

#A two-domensional array that is going to store the utility of each position in the maze
utility = [[0 for x in range(10)] for x in range(8)]
for i in range(8):
	for j in range(10):
		utility[i][j] = 0

#A two-dimensional array that is going to be used in order to determine whether the change in the utility is small enough to quit or not
smallEnough = [[0 for x in range(10)] for x in range(8)]
for i in range(8):
	for j in range(10):
		smallEnough[i][j] = 0


#A function that re-evaluate a specific position
def evaluate(Row, Column):
	Reward = reward[Row-1][Column-1]
	currentUtility = utility[Row-1][Column-1]
	
	if Row == 8:
		utilityUp = currentUtility
	else:
		utilityUp = utility[Row][Column-1]	
	if Column == 10:
		utilityRight = currentUtility
	else:
		utilityRight = utility[Row-1][Column]	
	if Column == 1:
		utilityLeft = currentUtility
	else:
		utilityLeft = utility[Row-1][Column-2]
	
	#Moving up:
	moveUp = 0.8 * utilityUp + 0.1 * utilityRight + 0.1 * utilityLeft
	#Moving right:
	moveRight = 0.8 * utilityRight + 0.1 * utilityLeft + 0.1 * utilityUp
	#Moving Left:
	moveLeft = 0.8 * utilityLeft + 0.1 * utilityUp + 0.1 * utilityRight
	
	utility[Row-1][Column-1] = Reward + ( gamma * max(moveUp, moveRight, moveLeft))
	change = abs(currentUtility - utility[Row-1][Column-1])
	return change

#A loop that makes the program evaluate the positions until the change in utility becomes small enough
for n in range(100):
	for i in range(8):
		for j in range(10):
			if smallEnough[7-i][9-j] == 0:
				change = evaluate(8-i,10-j)
				#print change
				if change < changeRequired:
					smallEnough[7-i][9-j] = 1

#The function that actually solve the maze using Markov Decision Processes
def MarkovDP(Row, Column, Reward, Utility):
	#Initialize the values of the possible next moves
	if Row == 8:
		utilityUp = utility[Row-1][Column-1]
		rewardUp = reward[Row-1][Column-1]
	else:
		utilityUp = utility[Row][Column-1]	
		rewardUp = reward[Row][Column-1]
	if Column == 10:
		utilityRight = utility[Row-1][Column-1]
		rewardRight = reward[Row-1][Column-1]
	else:
		utilityRight = utility[Row-1][Column]	
		rewardRight = reward[Row-1][Column]
	if Column == 1:
		utilityLeft = utility[Row-1][Column-1]
		rewardLeft = reward[Row-1][Column-1]
	else:
		utilityLeft = utility[Row-1][Column-2]
		rewardLeft = reward[Row-1][Column-2]
		
	#An exit road of the recutsion function
	if Maze.location(Row, Column) == 50:
		print("Reward of the path = {}"). format(Reward)
		print("Utility of the path = {}"). format(Utility)
		return
	else:
		#Now, we search for the maximum utility among all the possible moves (Up, Right, and Left)
		if utilityRight >= utilityUp and utilityRight >= utilityLeft:
			Column = Column + 1
			Utility = Utility + utilityRight
			Reward = Reward + rewardRight
			print("Move to ({}, {})"). format(Row, Column)
			MarkovDP(Row,Column,Reward,Utility)
		elif utilityUp >= utilityRight and utilityUp >= utilityLeft:
			Row = Row + 1
			Utility = Utility + utilityUp
			Reward = Reward + rewardUp
			print("Move to ({}, {})"). format(Row, Column)
			MarkovDP(Row,Column,Reward,Utility)
		elif utilityLeft >= utilityUp and utilityLeft >= utilityRight:
			Column = Column - 1
			Utility = Utility + utilityLeft
			Reward = Reward + rewardLeft
			print("Move to ({}, {})"). format(Row, Column)
			MarkovDP(Row,Column,Reward,Utility)

#Calling the MarkovDP Function
MarkovDP(1,1,Reward,Utility)
