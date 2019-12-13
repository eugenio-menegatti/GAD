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
import GAD as mGAD
import IOUtils as mioutils


def loadBoard_FromCPP(fIN):
	playerColor = None
	firstLine = fIN.readline()
	#print("Player color from file: [", firstLine, "]")
	if "B" in firstLine or "b" in firstLine:
		playerColor = mGAD.B
	if "W" in firstLine or "w" in firstLine:
		playerColor = mGAD.W

	return playerColor, mioutils.readBoardFromFile(fIN)

def saveBoard_ToCPP(board, x, y, fOUT):
	fOUT.write( str(x) + " " + str(y) + str('\n') )
	mioutils.writeBoardToFile(board, fOUT)

def aiMove():
	data_path = "C:\\Users\\darth_000\\Desktop\\workspaces\\python\\GadLearner\\"
	board_InFileName = "boardIN.txt"
	board_OutFileName = "boardOUT.txt"

	fIN = open(data_path + board_InFileName,"r")
	fOUT = open(data_path + board_OutFileName,"w+")
	
	gad = mGAD.GAD()
	gad.ai.init(mai.ALGORITHMIC)
	
	gad.player, gad.currentBoard = loadBoard_FromCPP(fIN)
	#gad.player = mGAD.B
	print("Player color is: ", gad.player)
	print("Input board is:")
	mioutils.dumpBoard(gad.currentBoard)
	
	computerMoved, x, y, _, _ = gad.computerMove()
	if not computerMoved:
		x = -1
		y = -1
		print("Computer passed")
	else:
		print("Computer moved in x=", x, " y=", y)
	print("Output board is")
	mioutils.dumpBoard(gad.currentBoard)

	saveBoard_ToCPP(gad.currentBoard, x, y, fOUT)
	fIN.close
	fOUT.close

if __name__== "__main__":
	aiMove()
