'''
Created on Mar 13, 2018

@author: subhomuk
'''


import math
import random
import numpy
import fileinput
from _ast import Num
import sets
from numpy.matlib import rand

class CreateEnvironment(object):
    '''
    classdocs
    '''


    def __init__(self,filename):
        '''
        Constructor
        '''
        self.filename = filename


    def readenv(self):
        data=[]
        #filename="env/env1/AP8.txt"
        for line in fileinput.input([self.filename]):

            try:
                line1 = [line.split(", ") or line.split("\n") ]
                #print numpy.shape(line1)
                #print line1
                take=[]
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                #print take
                data.append(take)
            except ValueError,e:
                print e
        #print data
        self.means=(data[0])
        self.variance=(data[1])
    
    def permute_col(self):
        
        
        #Permute best col
        choose_index = []
        while True:
            index = random.randint(0,self.numActions-1)
            if index not in choose_index and index not in self.bestCol:
                choose_index.append(index)
            
            if len(choose_index) >= self.rank:
                break
        
        print choose_index
        m=0
        for col in choose_index:
            temp = []
            for user in range(0,self.users):
                temp.append(self.means[user][m])
                self.means[user][m] = self.means[user][col]
                self.means[user][col] = temp[user]
            m = m + 1
    
    def permute_col1(self):
        
        
        #Permute best col
        choose_index = []
        while True:
            index = random.randint(0,self.numActions-1)
            if index not in choose_index and index not in self.bestCol:
                choose_index.append(index)
            
            if len(choose_index) >= self.rank:
                break
        
        print choose_index
        m=0
        for col in choose_index:
            #temp = []
            for user in range(0,self.users):
                temp = self.means[user][m]
                self.means[user][m] = self.means[user][col]
                self.means[user][col] = temp
            m = m + 1
        
    
    def create(self, rank, users, numActions, gap):
    
        #Set the environment

        self.numActions = numActions
        self.users = users
        self.rank = rank
        self.gap = gap

        '''
        self.means =[]
        self.variance=[]
        self.readenv()
        '''

        self.means =[[0.0 for i in range(self.numActions)] for j in range(0,self.users)]
        self.variance=[[0.0 for i in range(self.numActions)] for j in range(0,self.users)]
        
        '''
        for i in range(0,self.rank):
            self.means[i][self.numActions - i -1] = 1.0
        '''
        
        self.U = [[0.0 for i in range(self.rank)] for j in range(0,self.users)]
        self.V = [[0.0 for i in range(self.rank)] for j in range(0,self.numActions)]
        
        
        #self.V = [[1,0],[0,1],[0.5,0.0],[0.0,0.5]]
        #self.U = [[1,0],[0,1],[0.5,0.0],[0.0,0.5]]
        take = [0.0,0.5,1.0]
        '''
        self.U[0] = [1,0]
        self.U[1] = [0,1]
        
        self.V[0] = [1,0]
        self.V[1] = [0,1]
        '''
        for i in range(0,rank):
            self.U[i][i] = 1
            self.V[i][i] = 1
        
        for i in range(rank,self.users):
            
            ##index = random.randint(0,rank - 1)
            #X = [0.0 for j in range(0,self.users)]
            #X[index] = 1.0
            #val = random.uniform(self.gap, 1.0)
            #val = take[random.randint(0,len(take)-1)]
            #print val, index
            #val = 0.5
            #self.U[i]= numpy.ndarray.tolist(numpy.dot(val,X))
            
            #X = [0.0 for j in range(0,self.numActions)]
            #X[index] = 1.0
            #val = random.uniform(0.0, 1.0)
            #val = 1.0
            #index = random.randint(0,rank - 1)
            #X = [0.0 for j in range(0,self.users)]
            #X[index] = 1.0
            #val = random.uniform(self.gap, 1.0)
            #self.V[i]= numpy.ndarray.tolist(numpy.dot(val,X))
           
            #index = random.randint(0,self.rank - 1)
            #val = random.randint(0,self.rank-1)
            #val = i%rank
            
            take = random.uniform(0,1)
            if take > 0.5:
                val = 1
            else:
                val = 0
                
            self.U[i][val] = gap
            
        
        for i in range(rank,self.numActions):
            
            #val = i%rank
            take = random.uniform(0,1)
            if take > 0.5:
                val = 1
            else:
                val = 0
            self.V[i][val] = gap
        
        
        print self.U
        print self.V
        
        self.R = numpy.dot(self.U,numpy.transpose(self.V))    
        
        for i in range(0,self.users):
            for j in range(0,self.numActions):
                self.means[i][j] = self.R[i][j]    
        
        
        
        print self.means
        #print self.variance
        
        
        self.bestCol = []
        for user in range(0,self.users):
             
            index = max(range(0,self.numActions), key=lambda col: self.means[user][col])
            self.bestCol.append(index) 
        
        print self.bestCol
        
        self.permute_col1()
          
        self.bestCol = []
        for user in range(0,self.users):
             
            index = max(range(0,self.numActions), key=lambda col: self.means[user][col])
            self.bestCol.append(index) 
        
        print self.bestCol
        
        take =sets.Set(self.bestCol)
        sum1 = []
        for col in take:
            count = 0
            for col1 in range(0,len(self.bestCol)):
                if col == self.bestCol[col1]:
                    count = count + 1
        
            
            sum1.append(count)
        
        print take, sum1
        
        f = open(self.filename, 'w')
        for j in range(0,self.users):
            #print sum(self.means[j])
            f.writelines("%s\n" % (', '.join(["%.5f" % i for i in self.means[j]])))
            #f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.variance])))
        f.close()
        
        

if __name__ == "__main__":
        
        users = 16
        numActions = 16
        rank = 2
        gap = 0.5
        filename = 'env/env1/AP27.txt'
        
        random.seed(numActions+users+rank+3)
        
        obj=CreateEnvironment(filename)
        obj.create(rank, users, numActions, gap)

                