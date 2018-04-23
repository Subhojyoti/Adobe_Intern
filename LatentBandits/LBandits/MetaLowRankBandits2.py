'''
Created on Mar 30, 2018

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
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)

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
        else:
            return math.sqrt(alpha * (math.log((psi * self.numRounds)/(self.t+1)) / (numPlays)))
    
    
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
        
        
        
        self.theReward = self.rewards(self.user_nature, self.action)
        self.R.append(self.theReward)
        
        self.arm_reward[self.user_nature][self.action] = self.arm_reward[self.user_nature][self.action] + self.theReward
        self.numPlays[self.user_nature][self.action] += 1
        #self.numPlaysPhase[self.user_nature][self.action] += 1
        self.payoffSums[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action] + self.theReward
         
        self.estR[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action]/self.numPlays[self.user_nature][self.action]
        self.ucbs[self.user_nature][self.action] = self.estR[self.user_nature][self.action] + self.upperBound(self.numPlays[self.user_nature][self.action])
                      
        #self.estR[user][self.action] = theReward
            
        self.cumulativeReward += self.theReward
        self.bestActionCumulativeReward += self.theReward if self.action == self.bestAction[self.user_nature] else self.rewards(self.user_nature,self.bestAction[self.user_nature])
        #print self.bestAction[user],self.action
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            
        self.actionRegret.append(self.regret)
        self.t = self.t + 1
    
    
    def metaBanditEXP3(self):
        
        self.bestActionSet = []
        
        #for bandit in range(0,self.rank):
        #self.gamma = 1/math.sqrt(self.t)
        #self.gamma = 0.01
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        #print self.gamma
        
        for col in range(0,self.numActions):
                
            self.prob[0][col]=(1.0-self.gamma)*(self.weights[0][col]/(sum(self.weights[0]))) + (self.gamma/self.numActions)

        
        
        sortedProb = list(numpy.sort(self.prob[0]))
        action1 = 0
        num=random.uniform(0,1)
        cum = 0.0
        for b in range(0,self.numActions):
            cum = cum + sortedProb[b]
            if num <= cum:
    
                for c in range(0,self.numActions):
                    if sortedProb[b] == self.prob[0][c]:
                    
                        action1 = c
                        
                        if action1 not in (self.bestActionSet): 
                                    
                            self.bestActionSet.append(action1)  
                            self.prob[1][action1] = 0  
                            
                                
                            break
                break   
        
        
        for col in range(0,self.numActions):
            if col!= action1: 
                self.prob[1][col]=(1.0-self.gamma)*(self.weights[1][col]/(sum(self.weights[1]))) + (self.gamma/self.numActions)

        
        sortedProb = list(numpy.sort(self.prob[1]))
        
        num=random.uniform(0,1)
        cum = 0.0
        for b in range(0,self.numActions):
            cum = cum + sortedProb[b]
            if num <= cum:
    
                for c in range(0,self.numActions):
                    if sortedProb[b] == self.prob[1][c]:
                    
                        action1 = c
                        
                        if action1 not in (self.bestActionSet): 
                                    
                            self.bestActionSet.append(action1)  
                                
                            break
                break   
            
            #    break
        #print "p: " + str(self.prob)
        #print "t: " + str(self.bestActionSet)
        
    def metaBanditEXP3_1(self):
        
        self.bestActionSet = []
        
        #for bandit in range(0,self.rank):
        #self.gamma = 1/math.sqrt(self.t)
        #self.gamma = 0.01
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        #print self.gamma
        
        for bandit in range(0,self.rank):
            for col in range(0,self.numActions):
                    
                self.prob[bandit][col]=(1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)
    
            
            
            sortedProb = list(numpy.sort(self.prob[bandit]))
            action1 = 0
            num=random.uniform(0,1)
            cum = 0.0
            for b in range(0,self.numActions):
                cum = cum + sortedProb[b]
                if num <= cum:
        
                    for c in range(0,self.numActions):
                        if sortedProb[b] == self.prob[bandit][c]:
                        
                            action1 = c
                            
                            if action1 not in (self.bestActionSet): 
                                        
                                self.bestActionSet.append(action1)  
                                #Set the prob of that action to 0 so that it is not chosen by others
                                for bandit1 in range(0,self.rank):
                                    if bandit!= bandit1:
                                        self.prob[bandit1][action1] = 0  
                                
                                    
                                break
                    break   
        
        
        '''
        for col in range(0,self.numActions):
            if col!= action1: 
                self.prob[1][col]=(1.0-self.gamma)*(self.weights[1][col]/(sum(self.weights[1]))) + (self.gamma/self.numActions)

        
        sortedProb = list(numpy.sort(self.prob[1]))
        
        num=random.uniform(0,1)
        cum = 0.0
        for b in range(0,self.numActions):
            cum = cum + sortedProb[b]
            if num <= cum:
    
                for c in range(0,self.numActions):
                    if sortedProb[b] == self.prob[1][c]:
                    
                        action1 = c
                        
                        if action1 not in (self.bestActionSet): 
                                    
                            self.bestActionSet.append(action1)  
                                
                            break
                break   
        '''    
            #    break
        #print "p: " + str(self.prob)
        #print "t: " + str(self.bestActionSet)
    
    def changeWeight(self):
        '''
        print "R: " + str(self.R)
        print "A: " + str(self.a)
        print self.bestActionSet
        #2.8e+290
        ''' 
        R1 = sorted(range(0,len(self.R)), key=lambda col: self.R[col], reverse = True)
        
        
        for d in range(0,self.rank):
            if self.a[d] == self.bestActionSet[0]:
                
                #print self.R[d],self.a[d]
                r1 = self.R[R1[0]]
                #r2 = self.R[d]
                #r1 = max(self.R)
                
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r1/self.prob[0][self.a[d]]
                for col in range(0,self.numActions):
                    #self.weights[0][col] = min(self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions),2.8e+290)
                    self.weights[0][col] = self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions)
                
                '''
                sum1 = sum(self.weights[0]) 
                
                for col in range(0,self.numActions):
                    self.weights[0][col] = self.weights[0][col]/sum1
                '''
            #if self.a[0] = self.a[1]:
            elif self.a[d] == self.bestActionSet[1]:
                #min_index = max(range(0,self.rank), key=lambda col: self.R[col])
                
                #r2 = max(self.R) - self.R[min_index]
                #r2 = self.R[min_index]
                r2 = sum(self.R) - self.R[R1[0]]
                #r2 = self.R[R1[0]] - self.R[R1[1]]
                xj = [0.0 for col in range(0,self.numActions)]
                xj[self.a[d]] = r2/self.prob[1][self.a[d]]
                for col in range(0,self.numActions):
                    #self.weights[1][col] = min(self.weights[1][col]*math.exp(self.gamma*xj[col]/self.numActions),2.8e+290)
                    self.weights[1][col] = self.weights[1][col]*math.exp(self.gamma*xj[col]/self.numActions)
                
                '''
                sum1 = sum(self.weights[1]) 
                
                for col in range(0,self.numActions):
                    self.weights[1][col] = self.weights[1][col]/sum1
                '''
        
        if isnan(sum(self.prob[0])) == True:
            print self.R
            print self.a
            print self.bestActionSet
            print self.prob
            print self.weights
            
            sys.exit(0)
            
        #print self.bestActionSet
    
    
    def MetaLowRankBandit(self, users, numActions, rank, readfile, writefile):

        # Set the environment
        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users
        self.rank = rank
        
        
        
        self.explore = pow(self.rank,3)
        
        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.theta = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.ucbs = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.colReward = [0.0 for i in range(0,self.numActions)]
        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 4000000
        # numRounds = 250000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]
        self.bestSet = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        '''
        for user in range(self.users):
            for col in range(self.numActions):
                #theta[i]=random.gauss((self.payoffSums[i]/(self.numPlays[i]+1)) ,(1.0/(self.numPlays[i]+1)))
                self.theta[user][col]=random.betavariate((self.payoffSums[user][col]+1.0),(self.numPlays[user][col]-self.payoffSums[user][col]+1.0))
        '''

        # Read the environment
        self.readenv(readfile)
        
        print self.means
        print self.bestAction
        
        self.t = 0
        #self.gamma = 1/math.sqrt(self.t+1)
        #self.gamma = 0.01
        self.gamma = math.sqrt((self.numActions*math.log(self.numActions))/self.numRounds)
        
        self.weights = [[1.0 for i in range(0, self.numActions)] for j in range (0,self.rank)]
        self.prob = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.rank)]
        
        for bandit in range(0,self.rank):
            for col in range(0,self.numActions):
                self.prob[bandit][col] = (1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)

        
        #self.cumulativeColReward = [0.0 for i in range(0, self.numActions)]

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0

        self.actionRegret = []
        
        
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
            #self.action = random.choice(self.bestActionSet)
            
            for col in range(0,self.numActions):
                if col in self.bestActionSet:
                    self.ucbs[self.user_nature][col] = self.estR[self.user_nature][col] + self.upperBound(self.numPlays[self.user_nature][col])
                    
            #print self.ucbs[self.user_nature], self.numPlays[self.user_nature]     
            max_val = self.MIN
            max_index = -1
            for col in range(0,self.numActions):
                if col in self.bestActionSet:
                    if max_val < self.ucbs[self.user_nature][col]:
                        max_val = self.ucbs[self.user_nature][col]
                        max_index = col
                        
            self.action = max_index
            
            
            #self.action=max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
            
            self.select_Col()
            self.a.append(self.action)
            
        
            count = count + 1
            
            if count >= self.rank:
                self.changeWeight()
                while True:
                    self.metaBanditEXP3_1()
                    if len(self.bestActionSet) >= self.rank:
                        break
                    
                count = 0
                self.R = []
                self.a = []
            # print t
            
            
            
            if self.t % 1000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", best: " + str(self.bestAction[self.user_nature]) , ", regret:", str(self.regret)
                
                print self.bestActionSet
                #print self.prob
                #print sum(self.prob[0]),sum(self.prob[1])
                '''
                print self.weights
                #print self.colReward
                '''
            if self.t >= self.numRounds:
                break



        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open(writefile + 'testRegretMetaEXP0RR4.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 1024
    actions = 64
    rank = 2
    readfile = "env/env1/AP23.txt"
    writefile = "NewExpt/expt16/"

    # turn = 0
    for turn in range(0,1):
        
        obj = MetaLowRankBandit()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.MetaLowRankBandit(users, actions, rank, readfile, writefile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(writefile +'testMetaEXP0RR4.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
