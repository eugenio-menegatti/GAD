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

import Learner as mlearner
from ast import literal_eval

def dumpBoard(board):
	'''
	print( board[0:8] )
	print( board[8:16] )
	print( board[16:24] )
	print( board[24:32] )
	print( board[32:40] )
	print( board[40:48] )
	print( board[48:56] )
	print( board[56:64] )
	'''
	print( board[0] )
	print( board[1] )
	print( board[2] )
	print( board[3] )
	print( board[4] )
	print( board[5] )
	print( board[6] )
	print( board[7] )
	print()

def outputBoard(board):
	print( "   A  B  C  D  E  F  G  H ")
	for i in range(8):
		print( i + 1, " ", end = '')
		[ print(checker, ' ', end = '') for checker in board[i] ]
		print()
	print()
	print()

def dumpPairedBoards(board1, board2):
	print( board1[0], board2[0] )
	print( board1[1], board2[1] )
	print( board1[2], board2[2] )
	print( board1[3], board2[3] )
	print( board1[4], board2[4] )
	print( board1[5], board2[5] )
	print( board1[6], board2[6] )
	print( board1[7], board2[7] )
	print()

def writeBoardToFile(board, file):
	file.write( str(board[0]) + str('\n') )
	file.write( str(board[1]) + str('\n') )
	file.write( str(board[2]) + str('\n') )
	file.write( str(board[3]) + str('\n') )
	file.write( str(board[4]) + str('\n') )
	file.write( str(board[5]) + str('\n') )
	file.write( str(board[6]) + str('\n') )
	file.write( str(board[7]) + str('\n') )

def readBoardFromFile(file):
	board = [list(literal_eval(line)) for line in file]
	#print("Read board:")
	# print(board)
	return board

def writeMoveToFile(board, x, y, heuristic, file):
	sample = mlearner.genSample(board, x, y)
	sample.append(heuristic)
	file.write( str(sample) + str('\n') )

def writePredictionToFile(heuristic, prediction, file):
	file.write( str(heuristic) + " " + str(prediction) + str('\n') )

def readMovesFromFile(file):
	moves = [list(literal_eval(line)) for line in file]
	return moves
