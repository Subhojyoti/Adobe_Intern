'''
Created on Mar 29, 2018

@author: subhomuk
'''

import math
import random
import numpy
import fileinput
import sets
from scipy.io.matlab.mio5_utils import scipy
from cmath import isnan
import sys,traceback


class MetaLowRankBandit(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

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

    def User_Nature(self):

        #ROUND ROBIN
        #return self.t%self.users

        #UNIFORM SAMPLING
        return random.randint(0,self.users-1)

    def rewards(self, user, choice):
        # Noise Free
        #return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0
    
    def upperBound(self, numPlays):
        
        #return 0.0
        alpha = 2.0
        psi = 2.0
        if numPlays == 0:
            return self.MAX
        
        return math.sqrt(alpha * (math.log((psi * self.numRounds)/(self.t)) / (numPlays)))
    
    
    #Read Environment
    def readenv(self, readfile):
        data = []
        #filename = "env/env1/AP" + str(p) + ".txt"
        filename = readfile
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
        print self.bestAction
        
        take =sets.Set(self.bestAction)
        sum1 = []
        for col in take:
            count = 0
            for col1 in range(0,len(self.bestAction)):
                if col == self.bestAction[col1]:
                    count = count + 1
        
            
            sum1.append(count)
        
        print take, sum1
    
    def select_Col(self):
        
        #print self.user_nature,self.action
        #print self.user_nature, self.action
        self.theReward = self.rewards(self.user_nature, self.action)
        self.R.append(self.theReward)
        
        self.arm_reward[self.user_nature][self.action] = self.arm_reward[self.user_nature][self.action] + self.theReward
        self.numPlays[self.user_nature][self.action] += 1
        #self.numPlaysPhase[self.user_nature][self.action] += 1
        self.payoffSums[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action] + self.theReward
         
        self.estR[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action]/self.numPlays[self.user_nature][self.action]
        #self.ucbs[self.user_nature][self.action] = self.estR[self.user_nature][self.action] + self.upperBound(self.user_nature, self.action)
                      
        #self.estR[user][self.action] = theReward
            
        self.cumulativeReward += self.theReward
        self.bestActionCumulativeReward += self.theReward if self.action == self.bestAction[self.user_nature] else self.rewards(self.user_nature,self.bestAction[self.user_nature])
        #print self.bestAction[user],self.action
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            
        self.actionRegret.append(self.regret)
        self.t = self.t + 1
    
    
    def metaBanditEXP3(self):
        
        self.bestActionSet = []
        
        for bandit in range(0,self.rank):
            
            for col in range(0,self.numActions):
                
                self.prob[bandit][col]=(1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)

        
        #print self.prob
        #print self.prob
        '''
        num=random.uniform(0,1)
        if num <= self.gamma:
            ind = sorted(range(0,len(self.prob[0])), key=lambda col: self.prob[0][col], reverse = True)
            self.bestActionSet.append(ind[0])  
            ind = sorted(range(0,len(self.prob[1])), key=lambda col: self.prob[1][col], reverse = True)
            if ind[0] not in self.bestActionSet:
                self.bestActionSet.append(ind[0])  
            else:
                self.bestActionSet.append(ind[1])  
        else:
            self.bestActionSet = []
            while True:
                action = random.randint(0,self.numActions-1)
                if action not in self.bestActionSet:
                    self.bestActionSet.append(action)
                if len(self.bestActionSet) >= self.rank:
                    break
            
        ''' 
          
        sortedProb = list(numpy.sort(self.prob[0]))
            
        num=random.uniform(0,1)
        cum = 0.0
        for b in range(0,self.numActions):
            cum = cum + sortedProb[b]
            if num <= cum:
    
                for c in range(0,self.numActions):
                    if sortedProb[b] == self.prob[bandit][c]:
                                
                        action = c
                        if action not in (self.bestActionSet): 
                                    
                            self.bestActionSet.append(action)  
                            self.prob[1][action] = 0  
                                
                            break
                break   
        
        sortedProb = list(numpy.sort(self.prob[1]))
        
        while True:   
            num=random.uniform(0,1)
            cum = 0.0
            for b in range(0,self.numActions):
                cum = cum + sortedProb[b]
                if num <= cum:
        
                    for c in range(0,self.numActions):
                        if sortedProb[b] == self.prob[bandit][c]:
                                    
                            action = c    
                                
                            if action not in (self.bestActionSet): 
                                        
                                self.bestActionSet.append(action)  
                                        
                                    
                                break
                    break   
                    
                    
            if len(self.bestActionSet) >= self.rank:
                break
              
            
            #if len(self.bestActionSet) >= self.explore:
            #    break
    
        #print self.bestActionSet
        
    def changeWeight(self):
        '''
        print self.R
        print self.a
        print self.bestActionSet
        '''
        for d in range(0,self.rank):
            if self.a[d] == self.bestActionSet[0]:
                
                #print self.R[d],self.a[d]
                r1 = self.R[d]
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r1/self.prob[0][self.a[d]]
                for col in range(0,self.numActions):
                    self.weights[0][col] = self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions)
                
            #if self.a[0] = self.a[1]:
            elif self.a[d] == self.bestActionSet[1]:
                r2 = max(self.R) - self.R[d]
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r2/self.prob[1][self.a[d]]
                for col in range(0,self.numActions):
                    self.weights[1][col] = self.weights[1][col]*math.exp(self.gamma*xj[col]/self.numActions)
            
            '''
            else:
                
                #r2 = max(self.R) - self.R[d]
                r2 = self.R[d]
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r2/self.prob[0][self.a[d]]
                for col in range(0,self.numActions):
                    self.weights[0][col] = self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions)
                
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r2/self.prob[1][self.a[d]]
                for col in range(0,self.numActions):
                    self.weights[1][col] = self.weights[1][col]*math.exp(self.gamma*xj[col]/self.numActions)
            '''
        if isnan(sum(self.prob[0])) == True:
            print self.R
            print self.a
            print self.bestActionSet
            
            sys.exit(0)
        
    
    
    def MetaLowRankBandit(self, users, numActions, rank, readfile):

        # Set the environment
        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users
        self.rank = rank
        
        self.gamma = 0.9
        
        self.explore = pow(self.rank,3)
        
        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.theta = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.colReward = [0.0 for i in range(0,self.numActions)]
        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 4000000
        # numRounds = 250000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]
        self.bestSet = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        for user in range(self.users):
            for col in range(self.numActions):
                #theta[i]=random.gauss((self.payoffSums[i]/(self.numPlays[i]+1)) ,(1.0/(self.numPlays[i]+1)))
                self.theta[user][col]=random.betavariate((self.payoffSums[user][col]+1.0),(self.numPlays[user][col]-self.payoffSums[user][col]+1.0))
        

        # Read the environment
        self.readenv(readfile)
        
        print self.means
        print self.bestAction

        self.weights = [[1.0 for i in range(0, self.numActions)] for j in range (0,self.rank)]
        self.prob = [[(1.0/self.numActions) for i in range(0, self.numActions)] for j in range (0,self.rank)]
        self.cumulativeColReward = [0.0 for i in range(0, self.numActions)]

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0
        
        self.bestActionSet = []
        while True:
            action = random.randint(0,self.numActions-1)
            if action not in self.bestActionSet:
                self.bestActionSet.append(action)
            if len(self.bestActionSet) >= self.rank:
                break
            
        print self.bestActionSet
        
        count = 0
        self.R = []
        self.a = []
        while True:

            self.user_nature = self.User_Nature()
            
            for col in range(0,self.numActions):
                if col in self.bestActionSet:
                    self.ucbs[self.user_nature][col] = self.estR[self.user_nature][col] + self.upperBound(self.numPlays[self.user_nature][col])
                    
                    
            max_val = self.MIN
            max_index = -1
            for col in range(0,self.numActions):
                if col in self.bestActionSet:
                    if max_val < self.ucbs[self.user_nature][col]:
                        max_val = self.ucbs[self.user_nature][col]
                        max_index = col
                        
            self.action = max_index
                    
            #self.action=max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
            self.a.append(self.action)
            
            self.select_Col()
            
            count = count + 1
            
            if count >= self.rank:
                self.changeWeight()
                self.metaBanditEXP3()
                count = 0
                self.R = []
                self.a = []
            # print t
            
            
            
            if self.t % 1000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", best: " + str(self.bestAction[user]) , ", regret:", str(self.regret)
                print self.bestActionSet
                print self.prob
                #print self.colReward
                
            if self.t >= self.numRounds:
                break



        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open('NewExpt/expt14/testRegretCustomEXP30RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 1024
    actions = 16
    rank = 2
    readfile = "env/env1/AP19.txt"

    # turn = 0
    for turn in range(0,1):
        
        obj = MetaLowRankBandit()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.MetaLowRankBandit(users, actions, rank, readfile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open('NewExpt/expt14/testCustomEXP30RR1.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
