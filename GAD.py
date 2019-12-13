'''
GAD - a simple program that plays a famous game against humans
Copyright 2019 Eugenio Menegatti
myindievg@gmail.com

	 This file is part of GAD.
	 The file COPYING describes the terms under which GAD is distributed.

   GAD is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   GAD is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with GAD.  If not, see <http://www.gnu.org/licenses/>.
 '''
 
import AI as mai
import IOUtils as mioutils
import copy
import Tree as mtree

DATA_GRID_W = 8
DATA_GRID_H = 8

o = '_'		# empty
B = 'B' 	# black
W = 'W' 	# white
N = 'N'		# compuer plays alone
NL = '\n'	# newline
MOVES_FIRST = W

# Inizia sempre il NERO (B)
#COMPUTER_COLOR = W
#HUMAN_COLOR = B
EMPTY = o

MAX_DEPTH = 2

startingBoard = [ 
		[o, o, o, o, o, o, o, o],
		[o, o, o, o, o, o, o, o],
		[o, o, o, o, o, o, o, o],
		[o, o, o, W, B, o, o, o],
		[o, o, o, B, W, o, o, o],
		[o, o, o, o, o, o, o, o],
		[o, o, o, o, o, o, o, o],
		[o, o, o, o, o, o, o, o]
	]

class GAD:

	player = B
	ai = None

	#computerMove = { "x": -1 , "y": -1 }
	#computerMove = ( -1, -1 )
	#possibleMoves = []

	currentBoard = None

	def __init__(self):
		self.currentBoard = startingBoard
		self.ai = mai.AI(self)
		self.movesOutFile = None
		self.predictionsOutFile = None

	def saveMove(self, board, x, y, heuristic):
		if self.movesOutFile is None:
			self.movesOutFile = open("moves.txt","a+")
		mioutils.writeMoveToFile(board, x, y, heuristic, self.movesOutFile)
	
	def savePrediction(self, heuristic, prediction):
		if self.predictionsOutFile is None:
			self.predictionsOutFile = open("predictions.txt","a+")
		mioutils.writePredictionToFile(heuristic, prediction, self.predictionsOutFile)

	def getStartingBoard(self):
		return startingBoard

	def getOpponentColor(self):
		if self.player == N:
			return B
		if self.player == W:
			return B
		else:
			return W

	def getAllPossibleNextMovesFromBoardForPlayer(self, board, player):
		'''
		Return all the possible legal moves from the input board.
		Can be improved by searching only the checkers near the pieces instead of all the checkers in the board
		(Let's do it in the next version)
		'''
		possibleMoves = [] #https://stackoverflow.com/questions/1400608/how-to-empty-a-list-in-python
		copyBoard = copy.deepcopy(board)
		possibleMoves.append( (-1, -1, copyBoard, player) ) # root for the tree: the current board before moving
		for y, row in enumerate(copyBoard):
			for x, _ in enumerate(row):
				isValid, nextBoard = self.isPossibleMove(copyBoard, x, y, player)
				if isValid:
					possibleMoves.append( (x, y, nextBoard, player) )
		return possibleMoves

	def isPossibleMove(self, board, x, y, player):
		'''
			Player wants to put a piece in x, y:
			Is it a legal move?
		'''
		isValid = False
		#startingBoard = copy.deepcopy(board)
		startingBoard = board
		nextBoard = copy.deepcopy(board)
		if (startingBoard[y][x] == o):
			isLocallyValid, nextBoard = self.esisteCamminoVerticaleSu(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True

			isLocallyValid, nextBoard = self.esisteCamminoVerticaleGiu(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True

			isLocallyValid, nextBoard = self.esisteCamminoOrizzontaleDestra(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True

			isLocallyValid, nextBoard = self.esisteCamminoOrizzontaleSinistra(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True
			
			isLocallyValid, nextBoard = self.esisteCamminoDiagonaleQuadrante1(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True
			
			isLocallyValid, nextBoard = self.esisteCamminoDiagonaleQuadrante2(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True
			
			isLocallyValid, nextBoard = self.esisteCamminoDiagonaleQuadrante3(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True

			isLocallyValid, nextBoard = self.esisteCamminoDiagonaleQuadrante4(startingBoard, nextBoard, x, y, player)
			if isLocallyValid: isValid = True
			
			if isValid: return True, nextBoard
			else: return False, startingBoard
		else:
			return False, startingBoard

	def esisteCamminoVerticaleSu(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if y > 1:
			workingBoard[y][x] = player
			y -= 1
			if y > 0 and board[y][x] == opponent:
				while y > 0 and board[y][x] == opponent:
					workingBoard[y][x] = player
					y -= 1

				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard

	def esisteCamminoVerticaleGiu(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if y < DATA_GRID_H - 2:
			workingBoard[y][x] = player
			y += 1
			if y < DATA_GRID_H - 1 and board[y][x] == opponent:
				while y < DATA_GRID_H - 1 and board[y][x] == opponent:
					workingBoard[y][x] = player
					y += 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard

	def esisteCamminoOrizzontaleDestra(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x < DATA_GRID_W - 2:
			workingBoard[y][x] = player
			x += 1
			if x < DATA_GRID_W - 1 and board[y][x] == opponent:
				while x < DATA_GRID_W - 1 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x += 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard

	def esisteCamminoOrizzontaleSinistra(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x > 1:
			workingBoard[y][x] = player
			x -= 1
			if x > 0 and board[y][x] == opponent:
				while x > 0 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x -= 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard

	def esisteCamminoDiagonaleQuadrante1(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x < DATA_GRID_W - 2 and y > 1:
			workingBoard[y][x] = player
			x += 1
			y -= 1
			if x < DATA_GRID_W - 1 and y > 0 and board[y][x] == opponent:
				while x < DATA_GRID_W - 1 and y > 0 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x += 1
					y -= 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard
	
	def esisteCamminoDiagonaleQuadrante2(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x > 1 and y > 1:
			workingBoard[y][x] = player
			x -= 1
			y -= 1
			if x > 0 and y > 0 and board[y][x] == opponent:
				while x > 0 and y > 0 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x -= 1
					y -= 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard

	def esisteCamminoDiagonaleQuadrante3(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x > 1 and y < DATA_GRID_H - 2:
			workingBoard[y][x] = player
			x -= 1
			y += 1
			if x > 0 and y < DATA_GRID_H - 1 and board[y][x] == opponent:
				while x > 0 and y < DATA_GRID_H - 1 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x -= 1
					y += 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard
	
	def esisteCamminoDiagonaleQuadrante4(self, board, nextBoard, x, y, player):
		workingBoard = copy.deepcopy(nextBoard)
		opponent = self.ai.invertPlayer(player)
		if x < DATA_GRID_W - 2 and y < DATA_GRID_H - 2:
			workingBoard[y][x] = player
			x += 1
			y += 1
			if x < DATA_GRID_W - 1 and y < DATA_GRID_H - 1 and board[y][x] == opponent:
				while x < DATA_GRID_W - 1 and y < DATA_GRID_H - 1 and board[y][x] == opponent:
					workingBoard[y][x] = player
					x += 1
					y += 1
				if board[y][x] == player:
					return True, workingBoard
				else:
					return False, nextBoard
			else:
					return False, nextBoard
		else:
			return False, nextBoard


	def dumpCurrentBoard(self):
		mioutils.dumpBoard(self.currentBoard)

	def getMoveCoordsFromHumanInput(self, coords):
		x = ord( coords[0].lower() ) - 96 - 1
		y = int(coords[1]) - 1
		return x, y

	def isBoardFull(self, board):
		for row in board:
			for checker in row:
				if checker == EMPTY:
					return False
		return True

	def humanMove(self):
		playerPass = False
		quit = False

		possibleMoves = self.getAllPossibleNextMovesFromBoardForPlayer(self.currentBoard, self.player)
		if not possibleMoves:
			playerPass = True
			return quit, playerPass
		
		while True:
			coords = input("Enter your move or Q to quit (format: <letter><number>, e.g.: C4): ")
			if len(coords) < 2:
				if coords == 'q' or coords == 'Q':
					quit = True
					break
			else:
				x, y = self.getMoveCoordsFromHumanInput(coords)
				#print("coords = ", x, y)
				isValid = False
				if x >= 0 and x <= 7 and y >=0 and y <= 7:
					isValid, nextBoard = self.isPossibleMove(self.currentBoard, x, y, self.player)
					if isValid:
						self.currentBoard = nextBoard
					
				if not isValid:
					print("The move is invalid")
				else:
					break

		return quit, playerPass

	def computerMove(self):
		moved = True
		#print("Opponent color = ", self.getOpponentColor())
		nextBoard, x, y, heuristic, prediction = self.ai.calcMove( self.currentBoard, self.getOpponentColor() )
		if nextBoard is not None:
			self.currentBoard = nextBoard
			#mioutils.dumpBoard(nextBoard)
		else:
			moved = False
			print("No available move")
		return moved, x, y, heuristic, prediction

	def noPlayerMove(self):
		moved = True
		nextBoard, x, y, heuristic, prediction = self.ai.randomMove( self.currentBoard, W )
		if nextBoard is not None:
			self.currentBoard = nextBoard
		else:
			moved = False
		return moved, x, y, heuristic, prediction
	
	def playerChooseColor(self):
		print("Player chooses color.")
		if MOVES_FIRST == W:
			print("WHITE moves first.")
		if MOVES_FIRST == B:
			print("BLACK moves first.")	
		print()
		print("Enter W for white, B for black or Q to quit.")
		print("Enter N to let computer play alone.")
		
		quit = False
		while True:
			#print("Type C or W here to see copyright and licensing notes or select player's color.")
			color = input("Player color? ")
			if len(color) >= 1 and (color[0].lower() == 'w' or color[0].lower() == 'b' or color[0].lower() == 'n'):
				break
			if len(color) >= 1:
				if color[0].lower() == 'q':
					quit = True
					break
				if color[0].lower() == 'd':
					self.printWarrenty()
				if color[0].lower() == 'c':
					self.printCopying()
		c = color[0].lower()
		if c == 'w':
			self.player = W
		if c == 'b':
			self.player = B
		if c == 'n':
			self.player = N
		return quit

	def getCheckersCount(self, board):
		blackCount = 0
		whiteCount = 0
		for row in board:
			for checker in row:
				if checker == B:
					blackCount += 1
				if checker == W:
					whiteCount += 1
		return blackCount, whiteCount

	def closeFiles(self):
		if self.movesOutFile is not None:
			self.movesOutFile.close()
		if self.predictionsOutFile is not None:
			self.predictionsOutFile.close()
		
	def printCopying(self):
		print('''The file COPYING describes the terms under which GAD is distributed.
			GAD is free software: you can redistribute it and/or modify
		it under the terms of the GNU General Public License as published by
		the Free Software Foundation, either version 3 of the License, or
		(at your option) any later version.
			GAD is distributed in the hope that it will be useful,
		but WITHOUT ANY WARRANTY; without even the implied warranty of
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
		GNU General Public License for more details.
			You should have received a copy of the GNU General Public License
		along with GAD.  If not, see <http://www.gnu.org/licenses/>.''')

	def printWarrenty(self):
		print('''Disclaimer of Warranty.
			THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
		APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
		HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
		OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
		THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
		PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
		IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
		ALL NECESSARY SERVICING, REPAIR OR CORRECTION.''')
		print('''Limitation of Liability.
			IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
		WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
		THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
		GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
		USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
		DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
		PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
		EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
		SUCH DAMAGES.''')