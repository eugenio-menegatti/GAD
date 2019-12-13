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

import IOUtils as mioutils

def getIDGenerator():
    idSeed = 0
    while True:
        yield idSeed
        idSeed += 1


idGen = getIDGenerator()

class Node:

    def __init__(self):
        self.id = next(idGen)
        self.children = []
        self.x = -1
        self.y = -1
        self.player = None
        self.eval = None
        self.prediction = None
        self.board = None
        self.parent = None

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def isLeaf(self):
        if not self.children:
            return True
        else:
            return False

    def dump(self):
        print("id = " + str(self.id), end = ' ')
        print("eval = " + str(self.eval), end = ' ')
        if self.isLeaf():
            print("isLeaf", end = '')
        print("\n")

    def dumpVerboseInfo(self):
        print("id = " + str(self.id))
        print("eval = " + str(self.eval))
        print("children: ")
        for node in self.children:
            print(str(node.id) + " ")
        if self.isLeaf():
            print("nessuno")
        print("\n")

    def dumpBoard(self):
        mioutils.dumpBoard(self.board)

# ------------------------------------------------------------------------------------------------

class Tree:

    root = None

    def subtreeAsList(self, fromNode):
        r = []
        return self.subtreeAsList_Impl(fromNode, r)

    def subtreeAsList_Impl(self, fromNode, r):
        if ( not fromNode.isLeaf() ):
            for node in fromNode.children:
                self.subtreeAsList_Impl(node, r)
        else:
            r.append(node.alpha)
        return r

    def dump(self):
        self.dumpImpl(self.root)

    def dumpImpl(self, node):
        node.dump()
        for n in node.children:
            self.dumpImpl(n)

    def DFS(self, func):
        self.DFS_Impl(self.root, func)

    def DFS_Impl(self, currentNode, func):
        node = self.root
        for node in currentNode.children:
            if not node.isLeaf():
                self.DFS_Impl(node, func)
            func(node)

    def visitByLevel(self):
        level = 0
        nodesByLevel = []
        node = self.root
        self.visitByLevelImpl(node, level, nodesByLevel)
        return nodesByLevel

    def visitByLevelImpl(self, node, level, nodesByLevel):
        if node is not None:
            if len(nodesByLevel) <= level:
                nodesByLevel.append([])

        if not node.isLeaf():
            for child in node.children:
                self.visitByLevelImpl(child, level + 1, nodesByLevel)
        nodesByLevel[level].append(node)


    def dumpByLevel(self):
        nodesByLevel = self.visitByLevel()
        for level, nodeListForLevel in enumerate(nodesByLevel):
            for node in nodeListForLevel:
                print("Level: ", level, "; node_id = ", node.id, "; x = ", node.x, "; y = ", node.y, "; player = ", node.player)
                print("Board:")
                node.dumpBoard()

    def getLeaves(self):
        nodesByLevel = self.visitByLevel()
        leavesList = nodesByLevel[len(nodesByLevel) - 1]
        return leavesList