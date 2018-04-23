'''
Created on Apr 21, 2018

@author: Subhojyoti
'''

'''
Created on Apr 20, 2018

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
from math import gamma


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
        print "PredSet: " + str(set1)
        if len(set1) < len(testset) or len(set1) > len(testset):
            return False
        for i in range(0,len(set1)):
            # if set[i]!=testset[i] or set1[i]!=testset[i]:
            if set1[i] != testset[i]:
                return False
        return True

    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)

    def rewards(self, user, choice):
        # Noise Free
        #return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0
    
    
    
    
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
        
        print take
        print sum1
        #sys.exit(0)
    
    #Selecting action and environment interaction
    def select_Col(self, user_nature, action):
        
        theReward = self.rewards(user_nature, action)
        self.R.append(theReward)
        
        self.arm_reward[user_nature][action] = self.arm_reward[user_nature][action] + theReward
        self.numPlays[user_nature][action] += 1
        #self.numPlaysPhase[self.user_nature][self.action] += 1
        self.payoffSums[user_nature][action] = self.payoffSums[user_nature][action] + theReward
         
        self.estR[user_nature][action] = self.payoffSums[user_nature][action]/self.numPlays[user_nature][action]
        
        
            
        self.cumulativeReward += theReward
        self.bestActionCumulativeReward += theReward if action == self.bestAction[user_nature] else self.rewards(user_nature,self.bestAction[user_nature])
        #print self.bestAction[user],self.action
        self.setBestAction.add(self.bestAction[user_nature])
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            
        
        
    
    #Implementation of column Bandits
    def metaBanditEXP3(self):
        
        self.bestActionSet = []
        self.bestActionSetUnique = []
        
        #for bandit in range(0,self.rank):
        #self.gamma = 1/math.sqrt(self.t)
        #self.gamma = 0.1
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        
        #print self.gamma
        
        for bandit in range(0,self.rank):
            
            max_weight = max(self.weights[bandit])
            for col in range(0,self.numActions):
                self.prob[bandit][col] = math.exp(self.weights[bandit][col] - max_weight)
            
            
            sum1 = sum(self.prob[bandit])
            for col in range(0,self.numActions):
                    
                #if col not in self.bestActionSet:
                #self.prob[bandit][col]=(1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)
                self.prob[bandit][col]=(1.0-self.gamma)*(self.prob[bandit][col]/(sum1)) + (self.gamma/self.numActions)
                
                #else:
                #    self.prob[bandit][col] = 0.0
            
            #Sampling from probability distribution
            sortedProb = list(numpy.sort(self.prob[bandit]))
            action1 = 0
            num = random.uniform(0,1)
            cum = 0.0
            for b in range(0,self.numActions):
                cum = cum + sortedProb[b]
                if num <= cum:
        
                    for c in range(0,self.numActions):
                        if sortedProb[b] == self.prob[bandit][c]:
                        
                            action1 = c
                            self.bestActionSet.append(action1) 
                            
                            break
                    break   
        
            
            #Check error/NAN
            if isnan(sum(self.prob[bandit])) == True:
                print self.R
                print self.a
                print self.bestActionSet
                print self.prob
                print self.weights
            
                sys.exit(0)
            
            
        self.bestActionSetUnique = self.bestActionSet
        
        
        #If action not unique choose another action unoform randomly from rest of the actions and 
        #mark it so that reward is not updated
        if len(sets.Set(self.bestActionSet)) < self.rank:
            
            for bandit in range(1,self.rank):
                
                if self.bestActionSet[bandit] == self.bestActionSet[bandit-1]:
                    while True:
                        
                        action = random.randint(0,self.numActions-1)
                        if action not in self.bestActionSet:
                            self.bestActionSet[bandit] = action 
                            break
        
        
        #print "p: " + str(self.prob)
        #print "bA: " + str(self.bestActionSet)
        
    
    
    
    #Update weights of the Column Bandits
    def updateWeight(self, user):
        
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        
        
        #print self.bestActionSetUnique, self.bestActionSet
        
        r1 = self.R[0]
        if self.bestActionSetUnique[0]!=self.bestActionSetUnique[1]:
            r2 = max(self.R) - r1
        else:
            r2 = 0
        #r2 = self.R[1]
        
        xj = [0.0 for col in range(0,self.numActions)]
        xj[self.a[0]] = (r1/(self.user_bandit_prob[user][2]*self.prob[0][self.a[0]]))
        #xj[self.a[0]] = (r1/(self.prob[0][self.a[0]]*self.prob[0][self.a[1]]))
        
        
        #max_val = max(self.weights[0])
        
        
        for col in range(0,self.numActions):
            self.weights[0][col] = self.weights[0][col] + (self.gamma*xj[col]/self.numActions)
            
            
            
         
        xj = [0.0 for col in range(0,self.numActions)]
        xj[self.a[1]] = (r2/(self.user_bandit_prob[user][2]*self.prob[1][self.a[1]]))
        #xj[self.a[1]] = (r2/(self.prob[1][self.a[0]] * self.prob[1][self.a[1]]))
        for col in range(0,self.numActions):
            #self.weights[0][col] = min(self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions),2.8e+290)
            #self.weights[1][col] = self.weights[1][col]*math.exp((self.gamma*xj[col]/self.numActions) - max(self.weights[1]))
            self.weights[1][col] = self.weights[1][col] + (self.gamma*xj[col]/self.numActions)
            
            
            
    
    
    
    def MetaLowRankBandit(self, users, numActions, rank, readfile, writefile, filename):

        # Set the environment
        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users
        self.rank = rank
        
        
        self.setBestAction = sets.Set()
        #self.explore = pow(self.rank,3)
        
        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.theta = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        self.numRounds = 2000000
        # numRounds = 250000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]
        
        
        
        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        # Read the environment
        self.readenv(readfile)
        
        print self.means
        print self.bestAction
        
        self.t = 0
        #self.gamma = 1/math.sqrt(self.t+1)
        #self.gamma = 0.01
        self.gamma = math.sqrt((self.numActions*math.log(self.numActions))/self.numRounds)
        #self.eta = math.sqrt(1.0/(self.t + 1))
        
        self.weights = [[1.0 for i in range(0, self.numActions)] for j in range (0,self.rank)]
        self.prob = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.rank)]
        
        for bandit in range(0,self.rank):
            for col in range(0,self.numActions):
                self.prob[bandit][col] = (1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)
        
        
        #self.cumulativeColReward = [0.0 for i in range(0, self.numActions)]

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0

        self.actionRegret = []
        #self.epsilon = 1.0/(math.sqrt(math.log(self.t + 2.0)))
        #self.epsilon = 0.1
        
        self.bestActionSet = []
        self.bestActionSetUnique = []
        while True:
            action = random.randint(0,self.numActions-1)
            if action not in self.bestActionSet:
                self.bestActionSet.append(action)
            if len(self.bestActionSet) >= self.rank:
                break
        
        self.bestActionSet = sorted(self.bestActionSet)   
        self.bestActionSetUnique = self.bestActionSet
        print self.bestActionSet
        
        count = 0
        self.R = []
        self.a = []
        
        
        
        #User meta actions for each user
        self.meta_action = 3
        self.gamma_meta = math.sqrt((self.meta_action*math.log(self.meta_action))/self.numRounds)
        self.user_bandit_prob = [[0.0 for col in range(self.meta_action)] for user in range(0,self.users)]
        self.user_bandit_weight = [[1.0 for col in range(self.meta_action)] for user in range(0,self.users)]
        
        for bandit in range(0,self.users):
            for col in range(0,self.meta_action):
                self.user_bandit_prob[bandit][col] = (1.0 - self.gamma_meta)*(self.user_bandit_weight[bandit][col]/(sum(self.user_bandit_weight[bandit]))) + (self.gamma_meta/self.meta_action)
        
        
        
        
        
        while True:
            
            
            self.user_nature = self.User_Nature()
            
            
            #Sample from user EXP3 distribution to choose between meta actions
            max_weight = max(self.user_bandit_weight[self.user_nature])
            for col in range(0,self.meta_action):
                self.user_bandit_prob[self.user_nature][col] = math.exp(self.user_bandit_weight[self.user_nature][col] - max_weight)
            
            
            
            sum1 = sum(self.user_bandit_prob[self.user_nature])
            for col in range(0,self.meta_action):
                self.user_bandit_prob[self.user_nature][col] = (1.0 - self.gamma_meta)*(self.user_bandit_prob[self.user_nature][col]/(sum1)) + (self.gamma_meta/self.meta_action)
            
            
            
            sortedProb = list(numpy.sort(self.user_bandit_prob[self.user_nature]))
            self.meta_action_taken = -1
            num = random.uniform(0,1)
            cum = 0.0
            for b in range(0,self.meta_action):
                cum = cum + sortedProb[b]
                #print num,cum
                if num <= cum:
        
                    for c in range(0,self.meta_action):
                        if sortedProb[b] == self.user_bandit_prob[self.user_nature][c]:
                        
                            self.meta_action_taken = c
                            
                            break
                    break   
        
            
            
            
            #print self.meta_action_taken, sortedProb, num, sum(sortedProb)
            
            
            if self.meta_action_taken == 2:
                self.R = []
                self.a = []
                
                for count in range(0,self.rank):
                    self.select_Col(self.user_nature, self.bestActionSet[count])
                    self.a.append(self.bestActionSet[count])
                    self.aS = sets.Set(self.a)
                    
                  
                xj = [0.0 for col in range(0,self.meta_action)]
                xj[self.meta_action_taken] = (sum(self.R)/(self.user_bandit_prob[self.user_nature][self.meta_action_taken]))
                    
                    
                for col in range(0,self.meta_action):
                            
                    self.user_bandit_weight[self.user_nature][col] += (self.gamma_meta*xj[col]/self.meta_action)
                           
                    
                
                self.updateWeight(self.user_nature)
                
                #print self.t, self.bestActionSet, self.a, self.meta_action_taken, self.regret, self.user_nature, self.bestAction[self.user_nature]
                
                self.metaBanditEXP3()
                   
                #count = 0
                self.R = []
                self.a = []
                
            else:
                self.R = []
                self.a = []
                
                for count in range(0,self.rank):
                    
                    
                    #print self.action
                    
                    self.select_Col(self.user_nature, self.bestActionSet[self.meta_action_taken])
                    self.a.append(self.bestActionSet[self.meta_action_taken])
                    self.aS = sets.Set(self.a)
                    
                    #count = count + 1
                
                    
                xj = [0.0 for col in range(0,self.meta_action)]
                xj[self.meta_action_taken] = (sum(self.R)/(self.user_bandit_prob[self.user_nature][self.meta_action_taken]))
                        
                for col in range(0,self.meta_action):
                            
                    self.user_bandit_weight[self.user_nature][col] = self.user_bandit_weight[self.user_nature][col] + (self.gamma_meta*xj[col]/self.meta_action)
                            
                #print self.t, self.bestActionSet, self.a, self.meta_action_taken, self.regret, self.user_nature, self.bestAction[self.user_nature]
                   
                #self.metaBanditEXP3()
                
                #count = 0
                self.R = []
                self.a = []
            
                
            
            
            
            self.actionRegret.append(self.regret)
            self.t = self.t + 1
            
            if self.t % 1000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.aS), ", best: " + str(self.setBestAction) , ", regret:", str(self.regret)
                
                print self.bestActionSet
                print self.prob[0][self.bestActionSet[0]], self.prob[0][self.bestActionSet[1]]
                print self.prob[1][self.bestActionSet[0]], self.prob[1][self.bestActionSet[1]]
                print self.user_bandit_prob[self.user_nature], self.gamma_meta/self.meta_action, sum(self.user_bandit_prob[self.user_nature])
                #print self.prob
                #print sum(self.prob[0]),sum(self.prob[1])
                '''
                print self.weights
                #print self.colReward
                '''
            if self.t >= self.numRounds:
                break


        self.action = self.bestActionSet
        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward
        self.bestSet = [0 for i in range(0, self.users)]
        for user in range(0,self.users):
            #print self.estR[user]
            self.bestSet[user] = max(range(0,self.numActions), key=lambda col: self.numPlays[user][col])
        
        f = open(writefile + 'testRegret' + str(filename), 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 100
    actions = 16
    rank = 2
    readfile = "env/env2/AP6.txt"
    writefile = "NewExpt1/expt6/"
    filename = 'NewMetaEXP0RR2.txt'

    # turn = 0
    for turn in range(0,1):
        
        obj = MetaLowRankBandit()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.MetaLowRankBandit(users, actions, rank, readfile, writefile, filename)
        
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(sets.Set(bestSet)) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(str(writefile) + 'test' + str(filename), 'a')
        f.writelines("arms: %d \t bArms: %s \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, str(sets.Set(bestSet)), timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1

