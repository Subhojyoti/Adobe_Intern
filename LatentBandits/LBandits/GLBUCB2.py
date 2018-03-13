'''
Created on Mar 2, 2018

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
    
    def colElim(self):
        #print "elim: " + str(row) + " , " +str(col) 
        
        for col in range(1,self.numActions):
            row = max(range(0,self.users), key=lambda r: self.estR[r][col])
                
            if self.B[col]!=-1 and self.estR[row][self.best] - self.upperBound(0.0) >= self.estR[row][col] + self.upperBound(0.0):
                print "remove: " + str(col)
                print "best: " + str(self.best)
                for j in range(0,self.users):
                    self.estR[j][col] = -1.0
                
                self.B[col] = -1
            
            elif self.B[col]!=-1 and self.estR[row][self.best] + self.upperBound(0.0) < self.estR[row][col] - self.upperBound(0.0):
                
                print "remove: " + str(self.best)
                print "best: " + str(col)
                for j in range(0,self.users):
                    self.estR[j][self.best] = -1.0
                
                self.B[self.best] = -1
                self.best = col
            
        #else:
        #    print "remove: " + str(self.best)
        #    self.best = self.col
            
        

    def GLBUCB(self, users, numActions, rank):

        # Set the environment

        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.d = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.B = [0 for i in range(0,self.numActions)]

        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 500
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]




        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.readenv(4)
        print self.means,self.bestAction

        # t = numActions

        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        self.countCol = 0
        self.countRow = 0
        self.colDone = 0
        self.count = 0
        self.best = 0
        
        while True:

            user = self.User_Nature()

            if self.countCol < self.d:
                
                
                if self.countRow < self.users:

                    action = self.countCol
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

            if self.t > (self.users*self.d):

                self.t = self.t - 1
                self.estR[user][action] = 0.0
                break

        self.countCol = self.d
        self.countRow = 0
        
        print self.estR
        
        while True:


            user = self.User_Nature()

            if self.countCol < self.numActions:
                #Explore

                if self.countRow < self.d:
                    #action = self.remArmsRow(user)
                    action = self.countCol
                    self.countRow = self.countRow + 1

                else:

                    #self.colElim(self.countRow,self.countCol)
                    #print self.estR

                    action = self.countCol
                    self.countCol = self.countCol + 1
                    self.countRow = 1

            else:
                #print self.estR
                #Elimination
                if self.remArms() > 1:
                    self.colElim()
                #Exploit
                action = max(range(0,self.numActions), key=lambda j: self.estR[user][j])


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

            #print t

            if self.t % 10 == 0:
                print self.t, action

            if self.t >= self.numRounds:
                break

        print self.estR

        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        f = open('NewExpt/expt3/testRegretGLBUCB0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, action, self.t


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

