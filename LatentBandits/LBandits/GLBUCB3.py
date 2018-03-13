'''
Created on Mar 5, 2018

@author: subhomuk
'''


import math
import random
import numpy
import fileinput
from __builtin__ import str


# from random import betavariate
# from scipy.special import btdtri


class GLBUCB(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)
    
    def remArms(self):
        count=0
        for i in range(0,self.numActions):
            if self.B[i]!=-1:
                count=count+1
        return count
    
    def rewards(self, user, choice):
        # Noise Free
        return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        # return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0

    def readenv(self, p):
        data = []
        filename = "env/env1/AP" + str(p) + ".txt"
        for line in fileinput.input([filename]):

            try:
                line1 = [line.split(", ") or line.split("\n")]
                # print numpy.shape(line1)
                # print line1
                take = []
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                # print take
                data.append(take)
            except ValueError, e:
                print e
        # print data
        for i in range(0,self.users):

            self.means[i] = (data[i])
            self.bestAction[i] = max(range(self.numActions), key=lambda j: self.means[i][j])

        #self.variance = (data[1])


        # print self.means
        # print self.variance

    def upperBound(self, numPlays):
        
        return 0.0
        #return math.sqrt(2.0 * math.log(self.numRounds) / (numPlays))
    
    def choose_Col(self):
        
        while True:
            chooseCol = random.randint(0,self.numActions - 1)
            if self.B[chooseCol] != -1 and chooseCol not in self.bestColumns:
                return chooseCol 
            if self.remArms() <=self.rank:
                return self.bestColumns[0]
    
    def colElim(self,take):
        #print "elim: " + str(row) + " , " +str(col) 
        
        for col in self.bestColumns:
            rowbest = max(range(0,self.users), key=lambda r: self.estR[r][col])
            
            for row in (0,self.users):
                
                
                if self.B[col]!=-1 and self.estR[rowbest][col] - self.upperBound(0.0) >= self.estR[row][take] + self.upperBound(0.0):
                    
                    print self.estR[rowbest][col],self.estR[row][take]
                    print "remove: " + str(take)
                    print "best: " + str(col)
                    
                    for j in range(0,self.users):
                        self.estR[j][take] = -1.0
                
                    self.B[take] = -1
                    print self.B
                    return
            
                elif self.B[col]!=-1 and self.estR[rowbest][col] + self.upperBound(0.0) < self.estR[row][take] - self.upperBound(0.0):
                    
                    print self.estR[rowbest][col],self.estR[row][take]
                    print "remove: " + str(col)
                    print "best: " + str(take)
                    for j in range(0,self.users):
                        self.estR[j][col] = -1.0
                
                    self.B[col] = -1
                    for j in range(0,self.rank):
                        if self.bestColumns[j] == col:
                            self.bestColumns[j] = take
                            
                    print self.B
                    return
        #else:
        #    print "remove: " + str(self.best)
        #    self.best = self.col
            
    
    def colElim1(self,take,col):
        #print "elim: " + str(row) + " , " +str(col) 
        
        print self.estR
        #take_best = []
        #for col in self.bestColumns:
        rowbest = (max(range(0,self.users), key=lambda r: self.estR[r][col]))
        #take_best.append(self.estR[rowbest][col])
            
        best = self.estR[rowbest][col]
        
        count = 0 
        for row in (0,self.rank):
            
            print best,self.estR[row][take]
            if best - self.upperBound(0.0) >= self.estR[row][take] + self.upperBound(0.0):
                
                
                count = count + 1
            
                if count >= self.rank:
                    #print self.estR[rowbest][col],self.estR[rowtake][take]
                    print "remove1: " + str(take)
                    print "best: " + str(col)
                        
                    for j in range(0,self.users):
                        self.estR[j][take] = -1.0
                    
                    self.B[take] = -1
                    print self.B
                #return
            
            elif best + self.upperBound(0.0) < self.estR[row][take] - self.upperBound(0.0):
                
                count = count + 1
                
                if count >= self.rank:
                    #print self.estR[rowbest][col],self.estR[rowtake][take]
                    print "remove2: " + str(col)
                    print "best: " + str(take)
                    for j in range(0,self.users):
                        self.estR[j][col] = -1.0
                    
                    self.B[col] = -1
                    for j in range(0,self.rank):
                        if self.bestColumns[j] == col:
                            self.bestColumns[j] = take
                                
                    print self.B
                    #return
        #else:
        #    print "remove: " + str(self.best)
        #    self.best = self.col
            
        
    def colElim2(self,take):
        #print "elim: " + str(row) + " , " +str(col) 
        
        print self.estR
        #take_best = []
        #for col in self.bestColumns:
        count_col = 0
        for col in self.bestColumns:
            rowbest = (max(range(0,self.users), key=lambda r: self.estR[r][col]))
        #take_best.append(self.estR[rowbest][col])
            
            best = self.estR[rowbest][col]
        
            count = 0 
            for row in (0,self.rank+self.explore):
            
                print best,self.estR[row][take]
                if best - self.upperBound(0.0) >= self.estR[row][take] + self.upperBound(0.0):
                
                
                    count = count + 1
                    
                    if count >= self.rank:
                    #print self.estR[rowbest][col],self.estR[rowtake][take]
                        count_col = count_col + 1
                        if count_col >= self.rank+self.explore:
                            
                            print "remove1: " + str(take)
                            print "best: " + str(col)
                            
                            for j in range(0,self.users):
                                self.estR[j][take] = -1.0
                        
                            self.B[take] = -1
                            print self.B
                            #return
                            
                        
                elif best + self.upperBound(0.0) < self.estR[row][take] - self.upperBound(0.0):
                
                    count = count + 1
                    
                    if count >= self.rank+self.explore:
                        #print self.estR[rowbest][col],self.estR[rowtake][take]
                        count_col = count_col + 1
                        if count_col >= self.rank:
                            
                            print "remove2: " + str(col)
                            print "best: " + str(take)
                            for j in range(0,self.users):
                                self.estR[j][col] = -1.0
                        
                                self.B[col] = -1
                            for j in range(0,self.rank):
                                if self.bestColumns[j] == col:
                                    self.bestColumns[j] = take
                                    
                            print self.B
                            #return
                            
        
            
        #else:
        #    print "remove: " + str(self.best)
        #    self.best = self.col
            
        
        

    def GLBUCB(self, users, numActions, rank):

        # Set the environment

        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.rank = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.B = [0 for i in range(0,self.numActions)]

        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 100
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]




        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.readenv(5)
        #print self.means,self.bestAction

        # t = numActions
        
        self.explore = 0
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        self.countCol = 0
        self.countRow = 0
        self.colDone = 0
        self.count = 0
        self.best = 0
        
        #select random d-columns
        
        self.bestColumns = [0 for i in range(0,self.rank)]
        for c in range(0,self.rank):
            
            self.bestColumns[c] = random.randint(0,self.numActions - 1)
        
        print "Best Columns: " + str(self.bestColumns)
        while True:

            user = self.User_Nature()

            if self.countCol < self.rank:
                
                
                if self.countRow < self.users:

                    action = self.bestColumns[self.countCol]
                    self.countRow = self.countRow + 1



                else:
                    self.countRow = 1
                    self.countCol = self.countCol + 1
                    action = self.countCol

                theReward = self.rewards(user, action)

                self.arm_reward[user][action] = self.arm_reward[user][action] + theReward
                self.numPlays[user][action] += 1
                self.payoffSums[user][action] += theReward

                self.estR[user][action] = theReward

                cumulativeReward += theReward
                bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])

                regret = bestActionCumulativeReward - cumulativeReward



                self.actionRegret.append(regret)

                self.t = self.t + 1

            if self.t > (self.users*self.rank):

                self.t = self.t - 1
                self.estR[user][action] = 0.0
                break

        self.countCol = 0
        self.countRow = 0
        
        print self.estR
        
        self.action = self.choose_Col()
        print self.action
        while True:


            user = self.User_Nature()

            if self.remArms() > self.rank:
                #Explore
                
                if self.countRow < self.rank+self.explore:
                    #action = self.remArmsRow(user)
                    #action = chooseCol
                    self.countRow = self.countRow + 1

                else:

                    #self.colElim(self.countRow,self.countCol)
                    #print self.estR
                    #for col in self.bestColumns:
                    self.colElim2(self.action)
                        
                    
                    self.action = self.choose_Col()
                    print self.action
                    #self.countCol = self.countCol + 1
                    self.countRow = 1

            else:
                #print self.estR
                #Elimination
                #if self.remArms() > self.rank:
                #    self.colElim()
                #Exploit
                self.action = max(range(0,self.numActions), key=lambda j: self.estR[user][j])


            theReward = self.rewards(user, self.action)
            #print theReward
            self.arm_reward[user][self.action] = self.arm_reward[user][self.action] + theReward
            self.numPlays[user][self.action] += 1
            self.payoffSums[user][self.action] += theReward

            self.estR[user][self.action] = theReward

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if self.action == self.bestAction[user] else self.rewards(user,self.bestAction[user])
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)



            self.t = self.t + 1

            #print t

            if self.t % 10 == 0:
                print self.t, self.action

            if self.t >= self.numRounds:
                break

        print self.estR

        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        f = open('NewExpt/expt3/testRegretGLBUCB0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 20
    action = 10
    rank = 2

    #turn = 0
    for turn in range(1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank)
        #if obj.check(bestSet) == False:
            # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\twrong: " + str(wrong) + "\tarms: " + str(action) + "\tbarm: " + str(arm) + "\tReward: " + str(cumulativeReward) + "\tbestCumReward: " + str(bestActionCumulativeReward) + "\tregret: " + str(regret)
        f = open('NewExpt/expt3/testGLBUCB0RR1.txt', 'a')
        f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        #j = j + 1

