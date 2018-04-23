'''
Created on Apr 5, 2018

@author: subhomuk
'''



import math
import random
import numpy
import fileinput
import sets


# from random import betavariate
# from scipy.special import btdtri


class CustomTS(object):
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
                
    
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'UCB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in mat[r]])))
        f.close()
    
    
    def CustomTS(self, users, numActions, readfile, writefile):

        # Set the environment

        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.theta = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        
        
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
            
            #Explore all columns fully
            
            for col in range(0,self.numActions):
                #print random.betavariate(success[i]+1,failure[i]+1)
                self.theta[user][col]=random.betavariate((self.payoffSums[user][col]+1.0),(self.numPlays[user][col]-self.payoffSums[user][col]+1.0))
                    
            
            self.action=max(range(0,self.numActions), key=lambda col: self.theta[user][col])
            
            self.select_Col(user, self.action)
            self.a.append(self.action)
            
            for col in range(0,self.numActions):
                #print random.betavariate(success[i]+1,failure[i]+1)
                self.theta[user][col]=random.betavariate((self.payoffSums[user][col]+1.0),(self.numPlays[user][col]-self.payoffSums[user][col]+1.0))
                    
            
            self.action=max(range(0,self.numActions), key=lambda col: self.theta[user][col])
            
            self.select_Col(user, self.action)
            self.a.append(self.action)
            
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



        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open(writefile + 'testRegretCustomTS0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 4096
    actions = 128
    readfile = "env/env2/AP5.txt"
    writefile = "NewExpt1/expt5/"
    
    for turn in range(0,1):
        obj = CustomTS()
        random.seed(turn + actions + 5)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.CustomTS(users,actions,readfile,writefile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(writefile + 'testCustomTS0RR1.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        
