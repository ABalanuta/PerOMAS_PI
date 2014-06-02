#!/usr/bin/env python
""" Multiple Linear Regression Model used 
to predict thermostat vantilation levels based
on the user interaction with the system """

__author__ = "Artur Balanuta"
__version__ = "1.0.0"
__email__ = "artur.balanuta [at] tecnico.ulisboa.pt"

from numpy import array,linalg, ones,vstack

class LinRegNumpy():

    def __init__(self):

        self.y = []
        self.X = []

    #Add Training Values
    def train(self,X,y):
        self.X.append(X)
        self.y.append(y)

    def dump(self):
        print "X:", self.X
        print "y:", self.y
        if self.coefs.any():
            print "eq:", self.coefs.T

    def calculate(self):
        
        X = vstack([array(self.X).T,ones(len(self.X))]).T
        self.coefs = linalg.lstsq(X,self.y)[0]
        self.coefs = self.coefs.reshape(self.coefs.shape[0],-1)

    def predict(self,Z):

        if len(Z) !=( len(self.coefs) - 1):
            raise Exception("Invalid number of Parameters")

        r = 0.0
        for i in range(0, len(Z)):
            r = r + Z[i]*self.coefs[i]
        r = r + self.coefs[-1]
        return r

if __name__ == '__main__':

    lr = LinRegNumpy()
    #lr.train([[1, 2, 3]], [1])
    lr.train([30, 80, 24, 96], -3)

    lr.calculate()
    lr.dump()

    print lr.predict([26, 70, 5, 99])
    
    #print '\n', lr.predict([[1, 2, 3]])