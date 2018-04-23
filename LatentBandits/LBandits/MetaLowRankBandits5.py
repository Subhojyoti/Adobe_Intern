'''
Created on Apr 3, 2018

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
    
    def upperBound1(self, numPlays):
        
        #return 0.0
        
        if numPlays == 0:
            return self.MAX
        else:
            return math.sqrt((1.0 * math.log(self.numRounds)) / (numPlays))
    
    
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
    
    def select_Col(self, user_nature, action):
        
        
        
        theReward = self.rewards(user_nature, action)
        self.R.append(theReward)
        
        self.arm_reward[user_nature][action] = self.arm_reward[user_nature][action] + theReward
        self.numPlays[user_nature][action] += 1
        #self.numPlaysPhase[self.user_nature][self.action] += 1
        self.payoffSums[user_nature][action] = self.payoffSums[user_nature][action] + theReward
         
        self.estR[user_nature][action] = self.payoffSums[user_nature][action]/self.numPlays[user_nature][action]
        self.ucbs[user_nature][action] = self.estR[user_nature][action] + self.upperBound(self.numPlays[user_nature][action])
        self.lcbs[user_nature][action] = self.estR[user_nature][action] - self.upperBound(self.numPlays[user_nature][action])
                      
        #self.estR[user][self.action] = theReward
            
        self.cumulativeReward += theReward
        self.bestActionCumulativeReward += theReward if action == self.bestAction[user_nature] else self.rewards(user_nature,self.bestAction[user_nature])
        #print self.bestAction[user],self.action
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            
        self.actionRegret.append(self.regret)
        self.t = self.t + 1
    
    
    def metaBanditEXP3(self):
        
        self.bestActionSet = []
        
        #for bandit in range(0,self.rank):
        #self.gamma = 1/math.sqrt(self.t)
        #self.gamma = 0.1
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        
        #print self.gamma
        
        for bandit in range(0,self.rank):
            for col in range(0,self.numActions):
                    
                #if col not in self.bestActionSet:
                self.prob[bandit][col]=(1.0-self.gamma)*(self.weights[bandit][col]/(sum(self.weights[bandit]))) + (self.gamma/self.numActions)
                #else:
                #    self.prob[bandit][col] = 0.0
            
            
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
                            
                            if action1 not in (self.bestActionSet): 
                                        
                                self.bestActionSet.append(action1)  
                                #Set the prob of that action to 0 so that it is not chosen by others
                                
                                for bandit1 in range(0,self.rank):
                                    if action1 in self.bestActionSet and bandit != bandit1:
                                        #self.prob[bandit1][action1] = 0  
                                        self.weights[bandit1][action1] = 0
                                        
                                        sum1 = sum(self.weights[bandit1])
                                
                                        for col1 in range(0,self.numActions):
                                            self.weights[bandit1][col1] = self.weights[bandit1][col1]/sum1
                                    
                                break
                    break   
        
        
        
        #    break
        #print "p: " + str(self.prob)
        #print "bA: " + str(self.bestActionSet)
        if isnan(sum(self.prob[bandit])) == True:
            print self.R
            print self.a
            print self.bestActionSet
            print self.prob
            print self.weights
            
            sys.exit(0)
    
    
    
    
    def updateWeight(self):
        
        self.gamma = math.sqrt(self.numActions*math.log(self.numActions)/self.numRounds)
        #self.eta = math.sqrt(2.0/(self.t + 1))
        #self.eta = 1.0
        
        r1 = self.R[0]
        r2 = max(self.R) - r1
        #r2 = self.R[1]
        
        xj = [0.0 for col in range(0,self.numActions)]
        xj[self.a[0]] = (r1/self.prob[0][self.a[0]])
        
        #max_val = max(self.weights[0])
        
        
        for col in range(0,self.numActions):
            #self.weights[0][col] = min(self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions),2.8e+290)
            self.weights[0][col] = self.weights[0][col]*math.exp((self.gamma*xj[col]/self.numActions))
            #self.weights[0][col] = self.weights[0][col]*min(1.0, (self.gamma*xj[col]/self.numActions))
        
        #max_val = max(self.weights[1])
           
        xj = [0.0 for col in range(0,self.numActions)]
        xj[self.a[1]] = (r2/self.prob[1][self.a[1]])
        for col in range(0,self.numActions):
            #self.weights[0][col] = min(self.weights[0][col]*math.exp(self.gamma*xj[col]/self.numActions),2.8e+290)
            self.weights[1][col] = self.weights[1][col]*math.exp((self.gamma*xj[col]/self.numActions))
            #self.weights[1][col] = self.weights[1][col]*min(1.0, (self.gamma*xj[col]/self.numActions))   
        
    
    
    
    
    def MetaLowRankBandit(self, users, numActions, rank, readfile, writefile):

        # Set the environment
        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users
        self.rank = rank
        
        
        
        #self.explore = pow(self.rank,3)
        
        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.theta = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.ucbs = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.lcbs = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        #self.colReward = [0.0 for i in range(0,self.numActions)]
        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 4000000
        # numRounds = 250000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]
        self.bestSet = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        # Read the environment
        self.readenv(readfile)
        
        print self.means
        print self.bestAction
        
        self.t = 0
        #self.gamma = 1/math.sqrt(self.t+1)
        #self.gamma = 0.01
        self.gamma = math.sqrt((self.numActions*math.log(self.numActions))/self.numRounds)
        self.eta = math.sqrt(1.0/(self.t + 1))
        
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
        
        self.bestActionSet = sorted(self.bestActionSet)   
        print self.bestActionSet
        
        count = 0
        self.R = []
        self.a = []
        
        self.explore = pow(self.rank, 3)
        self.actionSet = [[0 for col in range(0,self.explore)] for user in range(0,self.users)]
        
        for user in range(0,self.users):
            
            take = sorted(random.sample(range(0,self.numActions), self.explore))
            for col in range(0,self.explore):
                self.actionSet[user][col] = take[col]
                
            print self.actionSet[user]
            
        while True:

            self.user_nature = self.User_Nature()
            #self.action = random.choice(self.bestActionSet)
            setTake = sets.Set(self.bestActionSet)
            setTake.update(self.actionSet[self.user_nature])
            
            #for col in (self.bestActionSet or self.actionSet[self.user_nature]):
            for col in setTake:
                #print self.user_nature, col
                self.ucbs[self.user_nature][col] = self.estR[self.user_nature][col] + self.upperBound1(self.numPlays[self.user_nature][col])
                self.lcbs[self.user_nature][col] = self.estR[self.user_nature][col] - self.upperBound1(self.numPlays[self.user_nature][col])
                    
            #print self.ucbs[self.user_nature], self.numPlays[self.user_nature]     
            max_val = self.MIN
            max_index = -1
            for col in range(0,self.numActions):
            #for col in setTake:
                #if col in (self.bestActionSet or self.actionSet[self.user_nature]):
                if col in setTake:
                    if max_val < self.ucbs[self.user_nature][col]:
                        max_val = self.ucbs[self.user_nature][col]
                        max_index = col
                        
            self.action = max_index
            
            
            min_val = self.MAX
            min_index = -1
            for col in range(0,self.numActions):
            #for col in setTake:
                #if col in (self.bestActionSet or self.actionSet[self.user_nature]):
                if col in setTake:
                    if min_val > self.lcbs[self.user_nature][col]:
                        min_val = self.lcbs[self.user_nature][col]
                        min_index = col
                        
            self.action1 = min_index
            
            #print self.action, self.action1
            #self.action=max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
            
            #if self.lcbs[self.user_nature][self.action] > self.ucbs[self.user_nature][self.action1] or self.lcbs[self.user_nature][self.action1] > self.ucbs[self.user_nature][self.action]:
            if self.lcbs[self.user_nature][self.bestActionSet[0]] < self.ucbs[self.user_nature][self.bestActionSet[1]] and self.lcbs[self.user_nature][self.bestActionSet[1]] < self.ucbs[self.user_nature][self.bestActionSet[0]]:
            
                
                self.select_Col(self.user_nature, self.bestActionSet[0])
                self.a.append(self.bestActionSet[0])
                #self.aS = sets.Set(self.a)
                
                count = count + 1
                
                self.select_Col(self.user_nature, self.bestActionSet[1])
                self.a.append(self.bestActionSet[1])
                
                
                self.aS = sets.Set(self.a)  
                count = count + 1
            else:
                self.select_Col(self.user_nature, self.action)
                self.a.append(self.action)
                #self.aS = sets.Set(self.a)
                
                count = count + 1
                
                self.select_Col(self.user_nature, self.action)
                self.a.append(self.action)
                
                self.aS = sets.Set(self.a)
                count = count + 1
            
            #if len(self.aS) >= self.rank:
            if count >= self.rank:
                #print len(self.aS), self.aS
                #print self.a, self.R
                #self.aS = sorted(self.aS)
                #if len(self.aS) >= self.rank and (self.lcbs[self.user_nature][self.action] > self.ucbs[self.user_nature][self.action1] or self.lcbs[self.user_nature][self.action1] > self.ucbs[self.user_nature][self.action]):
                if len(self.aS) >= self.rank:
                    #if self.lcbs[self.user_nature][self.bestActionSet[0]] < self.ucbs[self.user_nature][self.bestActionSet[1]] and self.lcbs[self.user_nature][self.bestActionSet[1]] < self.ucbs[self.user_nature][self.bestActionSet[0]]:
                    
                    self.updateWeight()
                        
                self.metaBanditEXP3()
                count = 0
                self.R = []
                self.a = []
                
                #self.aS = sets.Set()
            # print t
            
            
            
            if self.t % 1000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.aS), ", best: " + str(self.bestAction[self.user_nature]) , ", regret:", str(self.regret)
                
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

        f = open(writefile + 'testRegretMetaEXP0RR6.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 1024
    actions = 64
    rank = 2
    readfile = "env/env1/AP22.txt"
    writefile = "NewExpt/expt17/"

    # turn = 0
    for turn in range(0,1):
        
        obj = MetaLowRankBandit()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.MetaLowRankBandit(users, actions, rank, readfile, writefile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(writefile +'testMetaEXP0RR6.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1

