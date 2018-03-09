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


class CustomUCB(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    #Check output set with best set of actions
    def check(self, set1):
        testset = self.bestAction
        print "BestSet: " + str(testset)
        print "TestSet: " + str(set1)
        if len(set1) < len(testset) or len(set1) > len(testset):
            return False
        for i in range(0,len(set1)):
            # if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i] != testset[i]:
                return False
        return True

    #Nature selects User
    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)
    
    #Calculate whether column is explored
    def colExplore(self, colTake):
        count=0
        for i in range(0,self.users):
            if self.expl[colTake]!=-1:
                if self.estR[i][colTake] == 0.0:
                    count=count+1
                    break
        return count
    
    #Calculate whether the column has been explored
    def remExplore(self):
        count=0
        for i in range(0,self.users):
            for j in range(0,self.numActions):
                
                if self.expl[j]!=-1:
                    if self.estR[i][j] == 0.0:
                        count=count+1
                        break
        return count
    
    
    #Generate Rewards
    def rewards(self, user, choice):
        # Noise Free
        return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        # return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0
    
    
    #Read Environment
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
    
    #Calculate Upper Bound
    def upperBound(self, numPlays):
        
        return 0.0
        #return math.sqrt(2.0 * math.log(self.numRounds) / (numPlays))
    
    #Choose Column in Round Robin Fashion
    def choose_Col_RR(self,user):
        
        chooseCol = 0
        while True:
            
            if self.remExplore() > 0:
                if self.expl[chooseCol]!=-1:
                    return chooseCol
                else:
                    chooseCol = chooseCol + 1
            else:
                #self.write_file(self.t,self.estR,'_R_')
                return 0
                
    
    #Choose Column Randomly
    def choose_Col_Random(self,user):
        
        chooseCol = 0
        while True:
            
            if self.remExplore() > 0:
                chooseCol = random.randint(0,self.numActions-1)
                if self.expl[chooseCol]!=-1:
                    return chooseCol
            else:
                #self.write_file(self.t,self.estR,'_R_')
                return 0
                
    
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'UCB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in mat[r]])))
        f.close()
    
    
    def CustomUCB(self, users, numActions):

        # Set the environment

        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 2000
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]
        self.bestSet = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.readenv(6)
        print self.means
        print self.bestAction

        # t = numActions

        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0
        
        self.expl = [0 for i in range(0,self.numActions)]

        
        while True:
            user = self.User_Nature()
            
            #Explore all columns fully
            if(self.remExplore() > 0):
                
                self.action = self.choose_Col_RR(user)
                if self.colExplore(self.action) <= 0:
                    
                    self.expl[self.action] = -1
                    self.action = self.choose_Col_RR(user)
                #else:
                    
                
            else:
                #Exploit
                
                for i in range(0,self.numActions):
                    #if self.estR[user][i] != self.MAX:
                    self.estR[user][i] = (self.payoffSums[user][i] / self.numPlays[user][i]) + self.upperBound(self.numPlays[user][i])

                
                self.action = max(range(0,self.numActions), key=lambda j: self.estR[user][j])

                
            #print user,action
            #print self.estR
            # action = max(range(self.numActions), key=lambda i: ucbs[i])
            theReward = self.rewards(user, self.action)

            self.arm_reward[user][self.action] = self.arm_reward[user][self.action] + theReward
            self.numPlays[user][self.action] += 1
            self.payoffSums[user][self.action] += theReward
            
            self.estR[user][self.action] = (self.payoffSums[user][self.action] / self.numPlays[user][self.action]) + self.upperBound(self.numPlays[user][self.action])
            
            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if self.action == self.bestAction[user] else self.rewards(user,self.bestAction[user])
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)
            
            self.t = self.t + 1

            # print t
            if self.t== self.users*self.numActions:
                self.write_file(self.t,self.estR,'_R_')

            if self.t % 100 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", regret:", str(regret)

            if self.t >= self.numRounds:
                break



        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open('NewExpt/expt4/testRegretCustomUCB0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 64
    actions = 10

    
    for turn in range(0,100):
        obj = CustomUCB()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.CustomUCB(users,actions)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open('NewExpt/expt4/testCustomUCB0RR1.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        
