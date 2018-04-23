'''
Created on Apr 17, 2018

@author: subhomuk
'''

import math
import random
import numpy
import fileinput
import sets


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
    
    
    #Generate Rewards
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
        
        print take, sum1
    
    
    def klucbGauss(self, x, d, sig2=1., precision=0.):
        """klUCB index computation for Gaussian distributions.
    
        Note that it does not require any search.
        """
        return x + math.sqrt(2*sig2*d)

    def klucbBern(self, x, d, precision=1e-6):
        """klUCB index computation for Bernoulli distributions."""
        upperbound = min(1., self.klucbGauss(x, d))
        #upperbound = min(1.,klucbPoisson(x,d)) # also safe, and better ?
        return self.klucb(x, d, self.klBern, upperbound, precision)


    def klBern(self, x, y):
        """Kullback-Leibler divergence for Bernoulli distributions."""
        
        eps = 1e-15
        x = min(max(x, eps), 1-eps)
        y = min(max(y, eps), 1-eps)
        return x*math.log(x/y) + (1-x)*math.log((1-x)/(1-y))
    
    def klucb(self, x, d, div, upperbound, lowerbound=-float('inf'), precision=1e-6):
        """
        The generic klUCB index computation.
    
        Input args.: x, d, div, upperbound, lowerbound=-float('inf'), precision=1e-6,
        where div is the KL divergence to be used.
        """
        l = max(x, lowerbound)
        #upperbound = self.klucbGauss(x, d, precision)
        u = upperbound
        while u-l>precision:
            m = (l+u)/2
            
            if div(x, m)>d:
                u = m
            else:
                l = m
        return (l+u)/2
    
    
    
    def computeIndex(self, user, arm, t):
        
        self.c=0.0
        #d = 2.51
        #print self.numPlays[user][arm]
        if self.numPlays[user][arm] == 0:
            return float('+infinity')
            #return self.MAX
        else:
            #self.cumReward[arm] / self.nbDraws[arm], self.c * log(self.t) / self.nbDraws[arm], 1e-4
            #return self.klucbBern((self.payoffSums[arm] / self.numPlays[arm]), (self.c * math.log(t)) / self.numPlays[arm], 1e-4) 
            
            return self.klucbBern((self.estR[user][arm]), (math.log(t+2)+self.c * math.log(math.log(t+2))) / self.numPlays[user][arm], 1e-4) 
    
    
    
    def select_Col(self, user_nature, action):
        
        theReward = self.rewards(user_nature, action)
        self.R.append(theReward)
        
        self.arm_reward[user_nature][action] = self.arm_reward[user_nature][action] + theReward
        self.numPlays[user_nature][action] += 1
        
        self.payoffSums[user_nature][action] = self.payoffSums[user_nature][action] + theReward
         
        self.estR[user_nature][action] = self.payoffSums[user_nature][action]/self.numPlays[user_nature][action]
          
        self.cumulativeReward += theReward
        self.bestActionCumulativeReward += theReward if action == self.bestAction[user_nature] else self.rewards(user_nature,self.bestAction[user_nature])
        #print self.bestAction[user],self.action
        self.setBestAction.add(self.bestAction[user_nature])
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
                
    
    
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'UCB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in mat[r]])))
        f.close()
    
    
    def CustomUCB(self, users, numActions, rank, readfile, writefile):

        # Set the environment

        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users
        self.rank = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.lcbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        
        
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

        # t = numActions

        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0

        self.actionRegret = []
        self.t = 0
        
        self.R = []
        self.a = []
        self.setBestAction = sets.Set()
        
        while True:
            user = self.User_Nature()
            
            for d in range(0,self.rank):
                
                '''
                for arm in range(0,self.numActions):
                    self.ucbs[user][arm] = self.computeIndex(user,arm,self.t)
                ''' 
                
                self.action = max(range(0,self.numActions), key=lambda j: self.ucbs[user][j])
                self.select_Col(user, self.action)
                self.a.append(self.action)
                
                self.ucbs[user][self.action] = self.computeIndex(user,self.action,self.t)
            
            #print self.a
            
            self.aS = sets.Set(self.a)
            
            self.actionRegret.append(self.regret)
            
            self.t = self.t + 1
            self.R = []
            self.a = []

            # print t
            '''
            if self.t== self.users*self.numActions:
                self.write_file(self.t,self.estR,'_R_')
            '''
            if self.t % 5000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.aS), ", best: " + str(self.setBestAction) , ", regret:", str(self.regret)
            
            if self.t >= self.numRounds:
                break
        
        

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open(writefile + 'testRegretCustomKLUCB0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 2048
    actions = 64
    rank = 2
    
    readfile = "env/env2/AP2.txt"
    writefile = "NewExpt1/expt2/"
    
    for turn in range(0,1):
        obj = CustomUCB()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.CustomUCB(users,actions,rank,readfile,writefile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(writefile + 'testCustomKLUCB0RR1.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        

