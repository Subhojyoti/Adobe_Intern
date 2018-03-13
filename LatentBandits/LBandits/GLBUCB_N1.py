'''
Created on Oct 6, 2015

@author: Subhojyoti
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

        # ROUND ROBIN
        return self.t % self.users

        # UNIFORM SAMPLING
        # return random.randint(0,self.users-1)

    def reconstruct(self, col):

        array_estR = numpy.array(self.estR)
        
        theta_hat = numpy.dot(numpy.linalg.inv(numpy.dot(numpy.transpose(array_estR[0:self.d,0:self.d]) , array_estR[0:self.d,0:self.d])), array_estR[0:self.d,col] )

        
        M_hat =  numpy.dot(array_estR[:, 0:self.d], theta_hat)

        print theta_hat, M_hat

        for i in range(0,self.users):
            #self.estR[i][self.d] = numpy.dot(array_estR[i,0:self.d],theta_hat)
            self.estR[i][col] = M_hat[i]  

    def rewards(self, user, choice):
        # Noise Free
        # return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0

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
        for i in range(0, self.users):
            self.means[i] = (data[i])
            self.bestAction[i] = max(range(self.numActions), key=lambda j: self.means[i][j])

        # self.variance = (data[1])

        # print self.means
        # print self.variance

    def upperBound(self, numPlays):

        return math.sqrt(2.0 * math.log(self.numRounds) / (numPlays))

    def GLBUCB(self, users, numActions, rank):

        # Set the environment

        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.d = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.checkR = [0 for i in range(0, self.numActions)]

        # self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 15000
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.bestAction = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]

        self.readenv(1)
        print self.means, self.bestAction

        # t = numActions

        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        
        self.countCol = [0 for i in range(0,self.numActions)]
        self.countRow = 0
        self.selectCol = [random.randint(0,self.numActions-1) for i in range(0,self.d)]
        
        self.epsilon = 1.0
        
        self.alpha = 0.5
        self.psi = 1.0
        self.nm = math.ceil(self.alpha*math.log(self.psi*self.numRounds*self.epsilon)/(self.epsilon))
        self.Nm = self.t + int(2.0*(self.numActions+self.users)*self.nm*self.d)
        print "nm: " + str(self.nm) + " Nm: " + str(self.Nm) + str(self.countCol)
        self.s = 0
        
        #Initialization
        '''
        while True:

            user = self.User_Nature()

            if self.countCol < self.d:

                if self.countRow < self.users*self.nm:

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

                self.estR[user][action] = self.payoffSums[user][action]/self.numPlays[user][action]

                cumulativeReward += theReward
                bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])



                regret = bestActionCumulativeReward - cumulativeReward

                self.actionRegret.append(regret)

                self.t = self.t + 1

            if self.t > (self.users * self.d * self.nm):
                self.t = self.t - 1
                break
        
        self.countCol = 0
        self.countRow = 0
        
        self.epsilon = 1.0
        self.alpha = 1.0
        
        self.psi = self.numRounds
        self.nm = math.ceil(self.alpha*math.log(self.psi*self.numRounds*self.epsilon)/(self.epsilon))
        self.Nm = self.t + int(2.0*self.numActions*self.nm*self.d)
        print "nm: " + str(self.nm) + " Nm: " + str(self.Nm)
        '''
        while True:

            user = self.User_Nature()

            if self.countCol[self.selectCol[self.s]] < self.users*self.nm:
                # Explore

                if self.countRow < self.d*self.nm:
                    # action = self.remArmsRow(user)
                    action = self.selectCol[self.s]
                    self.countRow = self.countRow + 1

                else:

                    self.reconstruct(self.countCol)
                    print self.estR
                    
                    self.s = self.s + 1
                    action = self.selectCol[self.s]
                    self.countRow = 1

            else:
                # Exploit
                action = max(range(0, self.numActions), key=lambda j: self.estR[user][j])

            theReward = self.rewards(user, action)

            self.arm_reward[user][action] = self.arm_reward[user][action] + theReward
            self.numPlays[user][action] += 1
            self.payoffSums[user][action] += theReward

            self.estR[user][action] = self.payoffSums[user][action]/self.numPlays[user][action]

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])

            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)

            self.t = self.t + 1
            
            if self.t>= self.Nm:
                
                self.epsilon = self.epsilon*0.5
                self.countCol = [0 for i in range(0,self.numActions)]
                self.countRow = 0
                self.selectCol = [random.randint(0,self.numActions-1) for i in range(0,self.d)]
                
                self.s = 0
                self.nm = math.ceil(self.alpha*math.log(self.psi*self.numRounds*self.epsilon)/(self.epsilon))
                self.Nm = self.t + int(2.0*self.numActions*self.nm*self.d)
                
                print "nm: " + str(self.nm) + " Nm: " + str(self.Nm)

            # print t

            if self.t % 100 == 0:
                print self.t, regret

            if self.t >= self.numRounds:
                break

        print self.estR

        # action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        f = open('NewExpt/expt3/testRegretGLBUCBN0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 20
    action = 3
    rank = 2

    # turn = 0
    for turn in range(1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank)
        # if obj.check(bestSet) == False:
        # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\twrong: " + str(wrong) + "\tarms: " + str(action) + "\tbarm: " + str(
            arm) + "\tReward: " + str(cumulativeReward) + "\tbestCumReward: " + str(
            bestActionCumulativeReward) + "\tregret: " + str(regret)
        f = open('NewExpt/expt3/testGLBUCBN0RR1.txt', 'a')
        f.writelines(
            "arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (
            action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        # j = j + 1

