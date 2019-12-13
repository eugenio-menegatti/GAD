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
import copy
import time

# --------------------------------------------------------------------------------	

def getOutputFromMoveCoords(x, y):
	output = str(chr(x + 1 + 96).upper())
	output += str(y + 1)
	return output

def checkGameOver(gad):
	if gad.isBoardFull( gad.currentBoard ):
		return True
	else:
		return False

def main():
	print("GAD start")
	print()
	print("GAD Copyright 2019 Eugenio Menegatti")
	print("This program comes with ABSOLUTELY NO WARRANTY; type D at the color selection prompt for details.")
	print("This is free software, and you are welcome to redistribute it")
	print("under certain conditions; type C at the color selection prompt for details.")
	print("-----")
	print()
	gad = mGAD.GAD()
	gad.ai.init(mai.DEFAULT_AI_TYPE)

	quit = gad.playerChooseColor()
	if not quit:
		startTime = time.time()
		print()
		gameOver = False
		playerPassed = False
		starting = True
		prevBoard = copy.deepcopy(gad.currentBoard)
		while not quit and not gameOver:
			if starting:
				starting = False
				if gad.player.upper() == mGAD.MOVES_FIRST:
					mioutils.outputBoard( gad.currentBoard )
					print("Player is: ", gad.player)
					quit, playerPassed = gad.humanMove()
					if not playerPassed:
						# da correggere saveMove(prevBoard, x, y, heuristic)
						pass
			else:
				if gad.player == mGAD.N:
					print()
					print("Player is: W")
					print("Computer is moving for player, please wait")
					print()
					computerMoved, x, y, heuristic, prediction = gad.noPlayerMove()
					if computerMoved:
						#gad.saveMove(prevBoard, x, y, heuristic)
						prevBoard = copy.deepcopy(gad.currentBoard)
					playerPassed = not computerMoved
				else:
					mioutils.outputBoard( gad.currentBoard )
					print("Player is: ", gad.player)
					quit, playerPassed = gad.humanMove()
			if not quit:
				mioutils.outputBoard( gad.currentBoard )
				print("Computer is thinking, please wait.")
				print()
				computerMoved, x, y, heuristic, prediction = gad.computerMove()
				if computerMoved:
					print("Computer moves in ", getOutputFromMoveCoords(x, y), " with heuristic gain = ", heuristic, " and prediction = ", prediction)
					#No perche' salvo l'albero in AI gad.saveMove(prevBoard, x, y, heuristic)
					if gad.ai.aiType == mai.LEARNING:
						gad.savePrediction(heuristic, prediction)
					prevBoard = copy.deepcopy(gad.currentBoard)
				if playerPassed and not computerMoved:
					gameOver = True
				if not gameOver:
					gameOver = checkGameOver(gad)

		if gameOver:
			endTime = time.time()
			elapsedTime = endTime - startTime
			print("Game over")
			print()
			print("Final board:")
			mioutils.outputBoard( gad.currentBoard )
			print()
			blackCount, whiteCount = gad.getCheckersCount(gad.currentBoard)
			if blackCount > whiteCount:
				if gad.player == mGAD.B:
					print("Player wins")
				else:
					print("Computer wins")
			if whiteCount > blackCount:
				if gad.player == mGAD.W:
					print("Player wins")
				else:
					print("Computer wins")
			if blackCount == whiteCount:
				print("Game draw")
			print("White count = %d. Black Count = %d" %(whiteCount, blackCount))
			print("Game time: %.1f seconds" %(elapsedTime))
	
	gad.closeFiles()
	print()
	print("GAD end")



if __name__== "__main__":
	main()
 