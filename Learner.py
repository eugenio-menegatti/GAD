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


# https://medium.com/@parthvadhadiya424/hello-world-program-with-scikit-learn-a869beb55deb
# https://github.com/parthvadhadiya/hello-world-program-in-Scikit-Learn/blob/master/Hello_Wold.ipynb
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn import neighbors
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import main as mmain
import GAD as mGAD
import IOUtils as mioutils
import os


#import scipy

def helloWorld():
    
    X = np.random.random((10,5))
    #shape of X
    print("x.shape(samples, features): ", X.shape)
    print("Dump:", X)
    y = np.array(['M','F','M','M','M','F','M','F','M','F'])
    #shape of y
    print("y.shape(samples, _)", y.shape)
    print("Dump:", y)

    # split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    # init
    svc = SVC(kernel='linear')
    knn = neighbors.KNeighborsClassifier(n_neighbors=4)
    gnb = GaussianNB()
    pca = PCA(n_components=0.95)
    k_means = KMeans(n_clusters=4, random_state=0)

    # train
    svc.fit(X_train, y_train)
    knn.fit(X_train, y_train)
    gnb.fit(X_train, y_train)
    k_means.fit(X_train)
    pca_model = pca.fit_transform(X_train)

    #predict
    pred = svc.predict(X_test)
    print(pred)
    pred = knn.predict(X_test)
    print(pred)
    pred = gnb.predict(X_test)
    print(pred)
    pred = k_means.predict(X_test)
    print(pred)

MOVES_FILE_NAME = "moves.txt"

class Learner:
    
    learnFunc = None
    
    def __init__(self):
        self.movesInFile = None
    
    def readMoves(self):
        if self.movesInFile is None:
            self.movesInFile = open(MOVES_FILE_NAME, "r")
        moves = mioutils.readMovesFromFile(self.movesInFile)
        return moves
    
    def loadSamples(self):
        return self.readMoves()

    def isTrainFileValid(self):
        if os.stat(MOVES_FILE_NAME).st_size > 0:
            return True
        else:
            return False

    def train(self):
        #return
        if not self.isTrainFileValid():
            return

        # Which algorithm showd we use?
        self.svc = SVC(kernel='linear') # Useful for dividing data into two planes
        self.knn = neighbors.KNeighborsClassifier(n_neighbors=5) # For finding the class of the prediction
        self.gnb = GaussianNB()  # For continuous values with gaussian distribution
        self.lgr = LogisticRegression() # For binary decisions
        self.rfc = RandomForestClassifier(n_estimators=10000, max_depth=2, random_state=0) # A tree classifier
        
        self.lnr = linear_model.LinearRegression() # OK! Predict a continuous variable 
        self.rgr = linear_model.Ridge(alpha = 5)
        self.lss = linear_model.Lasso(alpha = 0.1)

        self.learnFunc = self.lnr

        samples = self.loadSamples()
        X_train = self.getTrainSamples(samples)
        y_train = self.getTrainLabels(samples)
        #print("11111111111111111111111111111111111111111111")
        #print(X_train)
        #print("22222222222222222222222222222222222222222222")
        #print(y_train)
        self.learnFunc.fit(X_train, y_train)

    def getTrainSamples(self, samples):
        X_train = []
        for sample in samples:
            #print("sample:")
            #print(sample)
            line = sample[0:64] + sample[64:66]
            #print("line")
            #print(line)
            X_train.append(line)
        return X_train

    def getTrainLabels(self, samples):
        y_train = []
        for sample in samples:
            label = sample[66]
            y_train.append(label)
        return y_train

    def predict(self, X):
        y = self.learnFunc.predict(X)
        prediction = y[0]
        #print("Prediction: ", prediction)
        return prediction

    def calcPredictionsOnTree(self, movesTree):
        '''
        Calculate the precition values on the first level of the tree
        (not on all the tree)
        '''
        for move in movesTree.root.children:
            X = genSample(movesTree.root.board, move.x, move.y)
            X = np.array(X).reshape(1, -1)
            move.prediction = self.predict(X)

# ---------------------------------------------------------------------------  

def genFeaturesFromBoard(board):
    X = []
    for row in board:
        for checker in row:
            if checker == mGAD.EMPTY:
                X.append(0)
            if checker == mGAD.B:
                X.append(1)
            if checker == mGAD.W:
                X.append(2)
    return X

def genSample(board, x, y):
    X = genFeaturesFromBoard(board)
    X.append(x)
    X.append(y)
    return X
#---------------------------------

def main():
    #scipy.test('full')
    mmain.main()

if __name__== "__main__":
    #helloWorld()
	main()
