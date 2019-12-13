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
 
# coding: latin-1
import IOUtils as mioutils
import Tree as mtree
import GAD as mGAD
from random import randrange
import Learner as mlearner

LEARNING = 1
ALGORITHMIC = 2
DEFAULT_AI_TYPE = 3

AI_TYPE = LEARNING



POS_INFINITE = float("inf")
NEG_INFINITE = float("-inf")

H = [
	[ 120, -20, 20,  5, 5,  20, -20, 120 ],
	[ -20, -40, -5, -5, -5, -5, -40, -20 ],
	[  20,  -5, 15,  3,  3, 15,  -5,  20 ],
	[   5,  -5,  3,  3,  3,  3,  -5,   5 ],
	[   5,  -5,  3,  3,  3,  3,  -5,   5 ],
	[  20,  -5, 15,  3,  3, 15,  -5,  20 ],
	[ -20, -40, -5, -5, -5, -5, -40, -20 ],
	[ 120, -20, 20,  5, 5,  20, -20, 120 ]
]

def doNothing(node):
	pass

class AI:

	PLAYER_MIN = 1
	PLAYER_MAX = 2

	
	Htest = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, POS_INFINITE, 5, -10, 7, 5, NEG_INFINITE, -7, -5 ]

	heuristicMethod = None

	owner = None
	learner = None

	def __init__(self, revdiscs):
		self.setHeuristic(self.heuristic_Optimum)
		self.owner = revdiscs
		self.aiType = AI_TYPE

	def init(self, newAiType):
		if newAiType == DEFAULT_AI_TYPE:
			self.aiType = AI_TYPE
		else:
			self.aiType = newAiType
		if self.aiType == LEARNING:
			print("AI type set to LEARNING")
			print("Please wait while training...")
			self.learner = mlearner.Learner()
			self.learner.train()
			print("Done")
		if self.aiType == ALGORITHMIC:
			print("AI type set to ALGORITHMIC")

	def heuristic_TestFunc(self, node):
		return self.Htest[node.id]

	def heuristic_Zero(self, node):
		return 0

	def heuristic_Optimum(self, node):
		hSum = 0
		for y, row in enumerate(H):
			for x, h in enumerate(row):
				if node.board[y][x] != mGAD.EMPTY:
					hSum += h
		return hSum

	def setHeuristic(self, heuristicFunc):
		self.heuristicMethod = heuristicFunc

	def heuristic(self, node):
		if self.heuristicMethod is not None:
			h = self.heuristicMethod(node)
			return h
		else:
			return NEG_INFINITE

	def min(self, x, y):
		if (x < y): return x
		else: return y

	def max(self, x, y):
		if (x > y): return x
		else: return y

	def miniMax(self, player, depth, root):
		'''
		Mimimax algorithm on Wikipedia.it ( https://it.wikipedia.org/wiki/minimax )

		function miniMax(nodo, profondita)
			SE nodo e' un nodo terminale OPPURE profondita = 0
				return il valore euristico del nodo
			SE l'avversario deve giocare
				alpha := +INFINITO
				PER OGNI figlio di nodo
					alpha := min(alpha, miniMax(figlio, profondita-1))
			ALTRIMENTI dobbiamo giocare noi
				alpha := -INFINITO
				PER OGNI figlio di nodo
					alpha := max(α, miniMax(figlio, profondita-1))
			return alpha
		'''

		if root.isLeaf() or depth == 0:
			eval = self.heuristic(root)
			root.eval = eval
			return eval
		
		if player == self.PLAYER_MIN:
			minEval = POS_INFINITE
			for node in root.children:
				eval = self.miniMax(self.PLAYER_MAX, depth - 1, node)
				minEval = self.min(eval, minEval)
				node.eval = eval
			return minEval

		if player == self.PLAYER_MAX:
			maxEval = NEG_INFINITE
			for node in root.children:
				eval = self.miniMax(self.PLAYER_MIN, depth - 1, node)
				maxEval = self.max(eval, maxEval)
				node.eval = eval
			return maxEval

		
	def alphaBetaPrune(self, player, board, alpha, beta, depth, evaluate):
		pass

	def calcMiniMaxOnTree(self, tree):
		treeRoot = tree.root
		self.miniMax(self.PLAYER_MAX, mGAD.MAX_DEPTH, treeRoot)
		return treeRoot

	def calcMove(self, fromBoard, playerColor):
		if self.aiType == LEARNING:
			return self.calcMove_Intelligent(fromBoard, playerColor)
		if self.aiType == ALGORITHMIC:
			return self.calcMove_Algorithmic(fromBoard, playerColor)
		
	def calcMove_Intelligent(self, fromBoard, playerColor):
		movesTree = self.genMovesTree(  mGAD.MAX_DEPTH, fromBoard, playerColor )
		self.calcMiniMaxOnTree(movesTree)
		self.learner.calcPredictionsOnTree(movesTree)
		bestMove = self.findBestPredictedMove(movesTree)
		if bestMove is not None:
			#print("Algorithmic heuristic = ", bestMove.eval, " Predicted heuristic = ", bestMove.prediction)
			return bestMove.board, bestMove.x, bestMove.y, bestMove.eval, bestMove.prediction
		else:
			return None, -1, -1, NEG_INFINITE, -1

	def calcMove_Algorithmic(self, fromBoard, playerColor):
		movesTree = self.genMovesTree( mGAD.MAX_DEPTH, fromBoard, playerColor )
		#movesTree.dumpByLevel()	# Shows the boards
		#movesTree.dump()			# Shows the evals

		self.calcMiniMaxOnTree(movesTree)
		for leaf in movesTree.getLeaves():
			if leaf.parent is not None:
				self.owner.saveMove(leaf.parent.board, leaf.x, leaf.y, leaf.eval)

		#movesTree.dump()
		bestMove = self.findBestMove(movesTree)
		if bestMove is not None:
			#print("Algorithmic heuristic = ", bestMove.eval, " Predicted heuristic = ", bestMove.prediction)
			return bestMove.board, bestMove.x, bestMove.y, bestMove.eval, None
		else:
			return None, -1, -1, NEG_INFINITE, -1

	def randomMove(self, fromBoard, playerColor):
		movesTree = self.genMovesTree( 1, fromBoard, playerColor )
		self.calcMiniMaxOnTree(movesTree)
		movesList = movesTree.root.children
		if len(movesList) > 0:
			aMove = movesList[ randrange(len(movesList)) ]
			return aMove.board, aMove.x, aMove.y, aMove.eval, aMove.prediction
		else:
			return None, -1, -1, NEG_INFINITE, -1

	def findBestPredictedMove(self, tree):
		treeRoot = tree.root
		max = NEG_INFINITE
		bestMove = None
		for move in treeRoot.children:
			if move.prediction > max:
				max = move.prediction
				bestMove = move
		return bestMove

	def findBestMove(self, tree):
		treeRoot = tree.root
		max = NEG_INFINITE
		bestMove = None
		for move in treeRoot.children:
			if move.eval > max:
				max = move.eval
				bestMove = move
		return bestMove

	def genSubtreeFromMoves(self, moves):
		'''
		Returns the root of the subtree
		'''
		root = mtree.Node()
		root.x, root.y, root.board, root.player = moves[0]

		for move in moves[1:]:
			node = mtree.Node()
			node.x, node.y, node.board, node.player = move
			root.addChild(node)
		
		return root

	def linkSubtree(self, linkToNode, subTree):
		linkToNode.children = subTree.root.children

	def invertPlayer(self, player):
		if player == mGAD.W:
			return mGAD.B
		else:
			return mGAD.W

	def genMovesTree(self, depth, board, player):
		'''
		Returns a tree of all the possible legal moves from the input board for
		the specified depth.
		The root of the returned tree is the input board. The children are the possible moves
		from that situation on.
		'''
		if depth <= 0: return None
		possibleMoves = self.owner.getAllPossibleNextMovesFromBoardForPlayer( board, player )
		# qui gestire possibleMoves is None
		movesSubTreeRoot = self.genSubtreeFromMoves( possibleMoves )
		for node in movesSubTreeRoot.children:
			#dumpPairedBoards( movesSubTreeRoot.board, node.board )
			nextSubtree = self.genMovesTree( depth - 1, node.board, self.invertPlayer(player) )
			if nextSubtree is not None:
				self.linkSubtree( node, nextSubtree )
		movesTree = mtree.Tree()
		movesTree.root = movesSubTreeRoot
		return movesTree


	def genDemoTree(self):
		'''
		Returns a test tree found on the wikipedia page about minimax
		'''
		tree = mtree.Tree()
		
		tree.root = mtree.Node()
		
		node1 = mtree.Node()
		node2 = mtree.Node()
		node3 = mtree.Node()
		node4 = mtree.Node()
		node5 = mtree.Node()
		node6 = mtree.Node()
		node7 = mtree.Node()
		node8 = mtree.Node()
		node9 = mtree.Node()
		node10 = mtree.Node()
		node11 = mtree.Node()
		node12 = mtree.Node()
		node13 = mtree.Node()
		node14 = mtree.Node()
		node15 = mtree.Node()
		node16 = mtree.Node()
		node17 = mtree.Node()
		node18 = mtree.Node()
		node19 = mtree.Node()
		node20 = mtree.Node()
		node21 = mtree.Node()

		tree.root.addChild( node1 )
		tree.root.addChild( node2 )
		
		node1.addChild( node3 )
		node1.addChild( node4 )
		
		node2.addChild( node5 )
		node2.addChild( node6 )

		node3.addChild( node7 )
		node3.addChild( node8 )

		node4.addChild( node9 )

		node5.addChild( node10 )
		node5.addChild( node11 )

		node6.addChild( node12 )
		
		node7.addChild( node13 )
		node7.addChild( node14 )

		node8.addChild( node15 )

		node9.addChild( node16 )

		node10.addChild( node17 )
		node10.addChild( node18 )

		node11.addChild( node19 )

		node12.addChild( node20 )
		node12.addChild( node21 )
		
		return tree


