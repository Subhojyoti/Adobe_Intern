'''
Created on Mar 20, 2018

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
        #return self.t%self.users

        #UNIFORM SAMPLING
        return random.randint(0,self.users-1)
    
    #Calculate Remaining Arms
    def remArms(self):
        count=0
        for i in range(0,self.numActions):
            if self.B[i]!=-1:
                count=count+1
        return count
    
    def remArmsUser(self,user):
        count=0
        for i in range(0,self.numActions):
            if self.B1[user][i]!=-1:
                count=count+1
        return count
    
    
    def remTotalArmsUser(self):
        count=0
        for user in range(0,self.users):
            for col in range(0,self.numActions):
                if self.B1[user][col]!=-1:
                    count=count+1
        return count
    
    def fullExplore(self):
        
        count=0
        for i in range(0,self.users):
            for j in range(0,self.numActions):
                
                if self.expl[j]!=-1:
                    if self.estR[i][j] == self.MIN:
                        count=count+1
                        break
        return count
    
    #Calculate whether the column has been explored
    def remExplore(self):
        count=0
        #for i in range(0,self.users):
        for j in range(0,self.numActions):
                
            if self.expl[j]!=-1:
                    #if self.estR[i][j] == self.MIN:
                count=count+1
                        #break
        return count
    
    
    #Generate Rewards
    def rewards(self, user, choice):
        # Noise Free
        #return self.means[user][choice]

        # Noisy
        #return random.gauss(self.means[user][choice],0.25)
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
    
    def upperBound(self, user, col):
        
        # Noise Free
        #return 0.0
        
        # Noisy
        return math.sqrt(math.log((self.psi*self.numRounds*self.epsilon*self.epsilon))/(4.0*self.numPlays[user][col]))
    
    
    
    
    #Choose Column in Round Robin Fashion
                
    def choose_Col_RR1(self, user):
        
        for col in range(0,self.numActions):
            
            if self.B[col] != -1 and self.expl[col] != -1:
                
                #print col, self.expl, self.B

                return col
        
        
            
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
                
    
    
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'GLB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.5f" % i for i in mat[r]])))
        f.close()
    
    
    #Find best Columns
    def find_best_cols(self):
        
        self.bestCol = []
        #print "old best col: " + str(self.bestCol) 
        take = [0 for col in range(0,self.numActions)]
        '''
        for user in range(0,self.users):
            print self.B1[user]
        '''         
        for col in range(0,self.numActions):
            sum1 = 0
            for user in range(0,self.users):
                #print col, user, sum1, self.B1[user][col]
                sum1 =sum1 + self.B1[user][col]
                        
            take[col] = sum1
                        
                            
        print take               
        for i in range(0,self.explore):
            #for col in range(0,self.numActions):
            index = max(range(0,self.numActions), key=lambda col1: take[col1])
            if index not in self.bestCol:
                self.bestCol.append(index)
                take[index] = self.MIN
        
        
        '''
        self.bestCol = []
        for col in self.bestCol1:
            self.bestCol.append(col)
        '''
        print "new best col: " + str(self.bestCol) 
    
    
           
    #Calculate the max of each equivalent class
    def calc_max(self):
        
        #self.write_file(self.t, self.estR, '_R_')
        self.max_take = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        #self.write_file(self.t, self.estR, '_estR_')
        
        
        for c in range(0,len(self.equiValence)-1):   
            
               
            for row in range(self.equiValence[c],self.equiValence[c+1]):
                    
                max_val = self.MIN
                for col in range(0,self.numActions):
                    
                    #print self.estR[row][col], row, col, max_val
                    #if self.B[col]!= -1 and self.estR[row][col]!= self.MIN and self.estR[row][col] > max_val:
                    if self.B[col]!= -1 and self.estR[row][col]!= self.MIN and self.estR[row][col] > max_val:
                    
                        #print max_val
                        max_val = self.estR[row][col]
                    
                
                #for row in range(self.equiValence[c],self.equiValence[c+1]):
                #print row
                for col1 in range(0,self.numActions):
                    
                    self.max_take[row][col1] = max_val
                    
        
        #self.write_file(self.t, self.max_take, '_MAX_')
     
    #Eliminate Column   
    
    def colElim(self):
        
        
        #print self.expl      
        #self.write_file(self.t, self.max_take, '_MAX_')
        #self.write_file(self.t, self.estR, '_estR_')
        #self.write_file(self.t, self.estR, '_estR_')
        #compare_col = 8
        self.calc_max()
        for c in range(0,len(self.equiValence)-1):
            
            count_colrow = 0
            while True:
                #self.Col = [0 for i in range(0,self.numActions)]
                #print count_col
                
                
                for col in range(0,self.numActions):
                #Compare against other column max row by row in the same equivalence class
                    #coladd = []
                    
                    count = 0
                    colrow = 0
                    for row in range(self.equiValence[c],self.equiValence[c+1]):  
                        
                        count_colrow = count_colrow + 1
                        if self.B[col]!=-1 and self.estR[row][col]!= self.MIN:
                            
                            colrow = colrow + 1
                            if self.estR[row][col] + self.upperBound(row, col) < self.max_take[row][col] - self.upperBound(row, col):
                            
                            #print self.estR[row][col], self.max_take[row][col], row, col, count
                            #print self.estR[row][col], self.max_take[row][col1], count
                                
                                count = count + 1
                            
            
                    
                    #if count >= self.explore:  
                    if count >= colrow:     
                        
                        if self.remArms() > self.rank:
                            self.B[col] = -1
                            print "remove: "+str(col)+ ". Remaining columns: " + str(self.B)
                        
                                
                            for u in range(0,self.users):
                                self.estR[u][col] = self.MIN
                                self.B1[u][col] = -1
                        
                        count = 0   
                        self.calc_max()
                        count_colrow = 0
                
                if count_colrow >= self.numActions*self.n0*self.explore or self.remArms() >= self.rank:
                    break        
                    #self.Col[col] = self.Col[col] - 1
                    #coladd.append(col)
                        
                
        #self.write_file(self.t, self.max_take, '_MAX_')            
    
    def colElim1(self):
        
        #self.bestCol = []
        for user in range(0,self.users):
            
            #max_index = max(range(0,self.numActions), key=lambda col: self.estR[user][col])
            max_index = -1
            max_val = self.MIN
            for col in range(0,self.numActions):
                
                if self.estR[user][col] != self.MIN and self.B1[user][col]!= -1 and self.estR[user][col] > max_val:
                    
                    max_val = self.estR[user][col]
                    max_index = col
                
            
            
            if self.remArmsUser(user) > 1:
                
                for col in range(0,self.numActions):
                
                    if col!=max_index and self.estR[user][col]!= self.MIN and self.B[col]!= -1 and self.B1[user][col]!= -1 and self.estR[user][col]+ self.upperBound(user, col) < self.estR[user][max_index] - self.upperBound(user, max_index):
                        
                         
                        self.B1[user][col] = -1
            
                
            
            else:   
                max_index = max(range(0,self.numActions), key=lambda col: self.B1[user][col])
                #if max_index not in self.bestCol and len(self.bestCol) <= self.rank :
                if max_index not in self.bestCol :
                    self.bestCol.append(max_index)  
                    
            print "User: " + str(user) + str(self.B1[user])   
    
    def colElim2(self):
        
        #self.bestCol = []
        for col in self.bestCol:
        
            
            count = 0
            sum1 = 0.0
            for user in range(0,self.users):
                
                if self.estR[user][col] != self.MIN and self.B1[user][col]!= -1 and self.B[col]!=-1:
                    
                    sum1 = sum1 + self.estR[user][col]
                    count = count + 1
                    
            
            for col1 in range(self.numActions):
                
                if col1 not in self.bestCol and self.B[col1]!=-1 and self.estR[user][col] + self.upperBound(user, col) < (sum1/count) - self.upperBound(user, col):
                         
                    if self.remArms() > self.rank:
                        self.B[col] = -1
                        print "remove: "+str(col)+ ". Remaining columns: " + str(self.B)
                        
                                
                        for u in range(0,self.users):
                            self.estR[u][col] = self.MIN
                            self.B1[u][col] = -1
                           
    
    
    def GLBUCB(self, users, numActions, rank, readfile):

        # Set the environment and initialize

        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users

        self.rank = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[self.MIN for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        self.B = [0 for i in range(0,self.numActions)]
        self.B1 = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        self.max_take = [[self.MIN for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.numRounds = 2000000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]

        self.Col = [0 for i in range(0,self.numActions)]


        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        # Read the environment
        self.readenv(readfile)
        
        #self.explore = int(1.0*math.ceil(math.sqrt(self.users)))
        self.explore = self.rank
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
            #sum1 = sum1 + int(self.users/self.explore)
            sum1 = sum1 + self.explore
        
        
        
        print "Equivalence class: " + str(self.equiValence)
        
        
        self.countCol = 0
        
        
        #print self.estR
        #self.write_file(self.t)
        
        
        
        #initialize phase
        self.m = 0
        
        self.psi = self.numRounds
        #self.psi = 1.0
        self.epsilon = 1.0
        
        self.M = int(math.floor(0.5 * (math.log((self.numRounds/math.e))/math.log(1+1.0))))
        self.nm = int(math.ceil((1.0*math.log(self.psi*self.numRounds*self.epsilon*self.epsilon)/(self.epsilon))))
        #self.nm = int(1.0)
        
        self.n0 = math.ceil(math.log(self.numRounds))
        
        self.Nmx = self.explore*self.n0*self.remArms()
        self.Nm = self.Nmx + self.nm*self.remArms()
        
        print self.Nm, self.nm, self.n0
        self.action = 0
        #self.expl[self.action] = -1 
        self.countRow = 0
        #cal_phase = 0
        #self.find_best_cols()
        
        self.flag = True
        self.bestCol = []
        '''
        self.selectCol = []
        '''
        #for i in range(0,self.explore):
        while True:
            col = random.randint(0,self.numActions-1)
            if col not in self.bestCol:
                self.bestCol.append(col)
            if len(self.bestCol) >= self.explore:
                break
            #self.selectCol.append(col)
        
        print self.bestCol
        while True:

            #User gives row
            self.user_nature = self.User_Nature()
            
            if self.remArms() > self.rank:
                
                
                #Exploit 1st half
                if self.t < self.Nm and self.t < self.Nmx:
                #Explore the column if not explored
                    
                    if self.remExplore() > 0:
                        if self.countRow < self.explore:
                            
                            
                            self.countRow = self.countRow + 1
            
                        else:
                            
                            
                            self.action = self.choose_Col_RR1(self.user_nature)
                            self.expl[self.action] = -1 
                            self.countRow = 1
                    else:
                        
                        self.expl = [0 for i in range(0,self.numActions)]
                        for i in range(0,self.numActions):
                            if self.B[i] == -1:
                                self.expl[i] = -1
                        
                        
                        self.action = self.choose_Col_RR1(self.user_nature)
                        #self.expl[self.action] = 
                        
                    #print self.action
                
                #if self.t <= self.Nm:   
                elif self.t <= self.Nm and self.t >= self.Nmx:
                    
                    for col in range(0,self.numActions):
                        if self.B1[self.user_nature][col] == -1 :
                            self.ucbs[self.user_nature][col] = self.MIN
                        if self.numPlays[self.user_nature][col] != 0 and self.B1[self.user_nature][col] != -1 and self.B[col]!=-1:
                            self.ucbs[self.user_nature][col] = self.estR[self.user_nature][col] + self.upperBound(self.user_nature,col)
                    
                    #while True:
                        #self.action = max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
                    self.action = max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
                    
                    
                    
                    
                    
                else:
                    
                    
                    self.colElim()
                    
                    self.expl = [0 for i in range(0,self.numActions)]
                    for i in range(0,self.numActions):
                        if self.B[i] == -1:
                            self.expl[i] = -1
                    
                    self.colElim1()    
                    self.find_best_cols()
                    #self.colElim2()
                    
                    self.epsilon = self.epsilon*0.5
                    
                    self.nm = int(math.ceil((1.0*math.log(self.psi*self.numRounds*self.epsilon*self.epsilon)/(self.epsilon))))
                    #self.nm = int(1.0)
                    self.Nmx = self.t + self.explore*self.n0*self.remArms()
                    self.Nm = self.Nmx + self.nm*self.remArms()
                    
                    print "\n\nPhase: " + str(self.m) + '\t Nmx: ' + str(self.Nmx) + '\t Nm: ' + str(self.Nm)
                    
                                      
                    self.m = self.m + 1
            else:
                
                #Explore best d columns fully
                
                if self.fullExplore() > 0:
                #if self.remArms() > 0:
                    
                    self.bestCol = []
                    for col in range(0,self.numActions):
                        
                        if self.B[col] != -1:
                            
                            self.bestCol.append(col)
                    
                    for col in range(0,self.numActions):
                        if self.estR[self.user_nature][col]== self.MIN and col in self.bestCol:
                            self.action = col
                            break
                            #print user, self.action
                            #theReward = self.rewards(user, self.action)
                            #self.estR[user][self.action] = theReward
                    
                #Exploit
                else:
                    self.action = max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col])
                    #print self.action, self.bestAction[user]
            
            #Calculate Regret
            #print self.user_nature,self.action
            
            theReward = self.rewards(self.user_nature, self.action)
            self.arm_reward[self.user_nature][self.action] = self.arm_reward[self.user_nature][self.action] + theReward
            self.numPlays[self.user_nature][self.action] += 1
            self.payoffSums[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action] + theReward

            self.estR[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action]/self.numPlays[self.user_nature][self.action]
            self.ucbs[self.user_nature][self.action] = self.estR[self.user_nature][self.action] + self.upperBound(self.user_nature, self.action)
            
            #self.estR[user][self.action] = theReward

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if self.action == self.bestAction[self.user_nature] else self.rewards(self.user_nature,self.bestAction[self.user_nature])
            #print self.bestAction[user],self.action
            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)
            self.t = self.t + 1

            #print t

            if self.t % 10000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", best: " + str(self.bestAction[self.user_nature]) , ", regret:", str(regret)

            if self.t >= self.numRounds:
                break
        
        self.write_file(self.t, self.estR, '_R_')
        
        #write regret to file
        f = open('NewExpt/expt9/testRegretGLBUCB0RR2.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 16
    action = 16
    rank = 2
    readfile = "env/env1/AP13.txt"

    for turn in range(0,1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank, readfile)
        #if obj.check(bestSet) == False:
            # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(action) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open('NewExpt/expt9/testGLBUCB0RR2.txt', 'a')
        f.writelines("arms: %d\t bArms: %d\t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        


