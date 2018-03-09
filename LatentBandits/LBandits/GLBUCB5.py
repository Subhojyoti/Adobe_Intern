'''
Created on Mar 7, 2018

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
    
    #Nature selects User
    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)
    
    #Calculate Remaining Arms
    def remArms(self):
        count=0
        for i in range(0,self.numActions):
            if self.B[i]!=-1:
                count=count+1
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
                if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
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
                if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
                    return chooseCol
            else:
                #self.write_file(self.t,self.estR,'_R_')
                return 0
                
    
    #Fully explore the selected Column
    def explore_full_Col(self,user):
        
        chooseCol = 0
        while True:
            
            if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
                return chooseCol
            elif self.remArms() <=self.rank:
                return self.bestColumns[0]
            else:
                chooseCol = chooseCol + 1
                
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'GLB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in mat[r]])))
        f.close()
    
    
    #Calculate the max of each equivalent class
    def calc_max(self):
        
        
        self.max_take = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        #self.write_file(self.t, self.estR, '_estR_')
        
        for col in range(0,self.numActions):
            
            for c in range(0,len(self.equiValence)-1):
                
                max_val = self.MIN
                for row in range(self.equiValence[c],self.equiValence[c+1]):
                    
                    if self.estR[row][col]!= 0 and self.estR[row][col]!= -1 and self.estR[row][col] > max_val:
                        
                        max_val = self.estR[row][col]
                    
                
                for row in range(self.equiValence[c],self.equiValence[c+1]):
                    #print row
                    self.max_take[row][col] = max_val
                    
        
        #self.write_file(self.t, self.max_take, '_MAX_')
     
    #Eliminate Column   
    def colElim1(self):
        
        
        print self.expl      
        #self.write_file(self.t, self.max_take, '_MAX_')
        #self.write_file(self.t, self.estR, '_estR_')
        #self.write_file(self.t, self.estR, '_estR_')
        self.calc_max()
        for c in range(0,len(self.equiValence)-1):
            
            
            self.Col = [0 for i in range(0,self.numActions)]
            for col in range(0,self.numActions):
                
                #Calculate the number of columns you need to compare with
                compare_col = 0
                for col2 in range(0,self.numActions):
                    if col!= col2 and self.max_take[self.equiValence[c]][col2]!=self.MIN:
                        compare_col = compare_col + 1
                
                #Compare against other column max row by row in the same equivalence class
                coladd = []
                for col1 in range(0,self.numActions):
                    count = 0
                    
                    for row in range(self.equiValence[c],self.equiValence[c+1]):
                        
                        
                        if col!= col1 and self.max_take[row][col1]!=self.MIN:
                            
                            if self.B[col]!=-1 and self.B[col1]!=-1 and self.estR[row][col]!= 0  and self.estR[row][col]!= -1 and self.estR[row][col] < self.max_take[row][col1]:
                            
                                #print self.estR[row][col], self.max_take[row][col1], count, row, col, col1
                                #print self.estR[row][col], self.max_take[row][col1], count
                                
                                count = count + 1
            
            
                    
                    if count >= self.explore - 1:        
                        self.Col[col] = self.Col[col] - 1
                        coladd.append(col1)
                        
                    
                if self.remArms() > self.rank and compare_col > 0 and self.Col[col] <= -1.0*compare_col and self.B[col]!=-1:
                    
                    print "remove: "+str(col), " by comparing against " + str(compare_col) , "column(s): " +str(coladd)
                    self.B[col] = -1
                            
                    for u in range(0,self.users):
                        self.estR[u][col] = -1.0
                        
                    self.calc_max()
                        
    
    
    def GLBUCB(self, users, numActions, rank):

        # Set the environment and initialize

        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users

        self.rank = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.B = [0 for i in range(0,self.numActions)]
        self.max_take = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.numRounds = 2000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]

        self.Col = [0 for i in range(0,self.numActions)]


        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        # Read the environment
        self.readenv(6)
        
        self.explore = int(1.0*math.ceil(math.sqrt(self.users)))
        print "Explore Factor: " + str(self.explore)
        
        
        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        self.countCol = 0
        self.countRow = 0
        self.colDone = 0
        self.count = 0
        self.best = 0
        
        self.expl = [0 for i in range(0,self.numActions)]
        #select random d-columns
        
        #self.bestColumns = [0 for i in range(0,self.rank)]
        
        
        self.equiValence = []
        sum1 = 0
        for i in range(0,int(self.users/self.explore)+1):
            
            self.equiValence.append(sum1)
            sum1 = sum1 + int(self.users/self.explore)
        
        
        print "Equivalence class: " + str(self.equiValence)
        
        
        self.countCol = 0
        self.countRow = 0
        
        #print self.estR
        #self.write_file(self.t)
        
        self.action = self.choose_Col_RR(0)
        
        #initialize phase
        m = 0
        while True:

            #User gives row
            user = self.User_Nature()
            
            if self.remArms() > self.rank:
                #Explore
                
                #Explore the column if not explored
                if self.remExplore() > 0:
                    
                    #print self.expl, self.countRow
                    if self.countRow < self.explore:
                        
                        self.countRow = self.countRow + 1
    
                    else:
    
                        
                        self.expl[self.action] = -1 
                        self.action = self.choose_Col_RR(user)
                        self.countRow = 1
                        
                    
                else:
                    #self.write_file(self.t,self.estR,'_R_')
                    print "Phase: " + str(m) + " explored " + str(self.remArms()) + " columns " + str(self.explore) + " times"
                    self.colElim1()    
                    self.expl = [0 for i in range(0,self.numActions)]
                    for i in range(0,self.numActions):
                        if self.B[i] == -1:
                            self.expl[i] = -1
                    
                    m = m + 1
            else:
                
                #Explore best d columns fully
                self.bestCol = []
                
                for col in range(0,self.numActions):
                    
                    if self.B[col] != -1:
                        
                        self.bestCol.append(col)
                
                
                if self.remExplore() > 0:
                    
                    for col in range(0,self.numActions):
                        if self.expl[col] != -1 and self.estR[user][col]== 0.0:
                            self.action = col
                    
                else:
                    #print "Fully explored " + str(self.remArms()) + " best columns " + str(self.bestCol)
                    #Exploit
                    self.action = max(range(0,self.numActions), key=lambda col: self.estR[user][col])
                    
            
            #Calculate Regret
            theReward = self.rewards(user, self.action)
            self.arm_reward[user][self.action] = self.arm_reward[user][self.action] + theReward
            self.numPlays[user][self.action] += 1
            self.payoffSums[user][self.action] += theReward

            self.estR[user][self.action] = theReward

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if self.action == self.bestAction[user] else self.rewards(user,self.bestAction[user])
            #print self.bestAction[user],self.action
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)
            self.t = self.t + 1

            #print t

            if self.t % 100 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", regret:", str(regret)

            if self.t >= self.numRounds:
                break

        #write regret to file
        f = open('NewExpt/expt4/testRegretGLBUCB0RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 64
    action = 10
    rank = 2

    for turn in range(0,1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank)
        #if obj.check(bestSet) == False:
            # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(action) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open('NewExpt/expt4/testGLBUCB0RR1.txt', 'a')
        f.writelines("arms: %d\t bArms: %d\t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        

