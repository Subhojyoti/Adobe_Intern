'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput


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

    '''
    def check(self, set1):
        testset = [2, 1, 0, 2]
        print set1
        if len(set1) < len(testset) or len(set1) > len(testset):
            return False
        for i in range(len(set1)):
            # if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i] != testset[i]:
                return False
        return True
    '''


    def remArmsCol(self,user):


        #for i in range(0,self.users):
        for j in range(0,self.d):
            if self.estR[user][j] == self.MAX:
                #self.flag = True
                self.countCol = self.countCol + 1
                return j
        #self.flag = False

    def remArmsRow(self,user):


        #for i in range(0,self.users):
        for j in range(self.d,self.numActions):

            print self.countRow
            if self.estR[user][j] == self.MAX:
                #self.flag = True
                self.countRow = self.countRow + 1
                return j


    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)

    def reconstruct(self,col):

        array_estR = numpy.array(self.estR)
        #theta_hat = numpy.dot(numpy.linalg.inv(numpy.dot(numpy.transpose(array_estR[:,0:self.d]),array_estR[:,0:self.d])),numpy.transpose(array_estR[0:self.d,col]) )
        theta_hat = numpy.dot(numpy.linalg.inv(numpy.dot(numpy.transpose(array_estR[:,0:self.d]) , array_estR[:,0:self.d])), array_estR[0:self.d,col] )
        #numpy.invert
        #*array_estR[0:self.d,col]
        #print theta_hat,numpy.shape(theta_hat),numpy.shape(array_estR[:,col])
        #print numpy.dot(theta_hat,array_estR[0:self.d,col])
        #y = numpy.array(array_estR[0:self.d])

        #print array_estR[0:self.d, col], array_estR[:,0:self.d]

        #theta_hat = numpy.linalg.lstsq(array_estR[0:self.d,0:self.d], numpy.transpose(array_estR[0:self.d, col]),rcond=None )[0]

        M_hat =  numpy.dot((array_estR[:, 0:self.d]),theta_hat)

        print theta_hat,M_hat

        for i in range(0,self.users):
            #self.estR[i][self.d] = numpy.dot(array_estR[i,0:self.d],theta_hat)
            self.estR[i][self.d] = M_hat[i]





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

        return math.sqrt(2.0 * math.log(self.numRounds) / (numPlays))

    def GLBUCB(self, users, numActions, rank):

        # Set the environment

        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.d = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.checkR = [0 for i in range(0,self.numActions)]

        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 500
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]




        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.readenv(0)
        print self.means,self.bestAction

        # t = numActions

        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        self.countCol = 0
        self.countRow = 0
        self.colDone = self.d

        #self.flag = True
        '''
        for i in range(0,self.users):
            for j in range(0,self.numActions):
                theReward = self.rewards(i,j)
                # self.numPlays[i]=self.numPlays[i]+1

                action = j
                user = i
                self.arm_reward[user][action] = self.arm_reward[user][action] + theReward
                self.numPlays[user][action] += 1
                self.payoffSums[user][action] += theReward

                cumulativeReward += theReward
                bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])
                regret = bestActionCumulativeReward - cumulativeReward

                self.actionRegret.append(regret)
                self.t = self.t + 1
        '''
        while True:



            # upbs = [self.upperBound(t, self.numPlays[i]) for i in range(self.numActions)]
            # print "upbs"
            # print upbs
            # print ucbs
            # getting the maximum of the ucbs

            user = self.User_Nature()
            #print user
            action=0



            if self.countCol < (self.users * self.d):
                action = self.remArmsCol(user)

            elif self.countRow < self.d and self.colDone < self.numActions:
                action = self.remArmsRow(user)
                #break
            elif self.countRow >= self.d and self.countCol >= (self.users*self.d):
                #print "h"
                self.reconstruct(self.colDone)
                print self.estR
                self.colDone = self.colDone + 1
                self.countRow = 0
                #break
            #action = max(range(0,self.numActions), key=lambda j: self.ucbs[user][j])
            else:
                action = max(range(0,self.numActions), key=lambda j: self.estR[user][j])

            #print user,action
            #print self.ucbs
            # action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(user, action)

            self.arm_reward[user][action] = self.arm_reward[user][action] + theReward
            self.numPlays[user][action] += 1
            self.payoffSums[user][action] += theReward

            self.estR[user][action] = theReward

            #print self.estR

            # f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            # f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))

            # yield action, theReward, ucbs

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)



            self.t = self.t + 1

            #print t

            if self.t % 1 == 0:
                print self.t

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
    user = 3
    action = 3
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

