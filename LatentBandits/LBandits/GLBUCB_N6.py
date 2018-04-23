'''
Created on Mar 23, 2018

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
        if self.numPlays[user][col] == 0:
            #print self.MAX
            return self.MAX
        
        #print math.sqrt(math.log((self.psi*self.numRounds*self.epsilon*self.epsilon))/(8.0*self.numPlays[user][col]))
    
        return math.sqrt(math.log((self.psi*self.numRounds*self.epsilon*self.epsilon))/(4.0*self.numPlays[user][col]))
    
    #Choose Column in Round Robin Fashion
                
    def choose_Col_RR1(self, user):
     
        for col in range(0,self.numActions):
            
            if self.B[col] != -1 and self.expl[col] != -1 and col in self.bestCol[user]:
                
                #print col, self.expl, self.B

                return col
    
    def choose_Col_RR2(self, user):
        
        for col in range(0,self.numActions):
            
            #if self.B[col] != -1 and self.expl[user][col] < 1 and col in self.bestCol[user]:
            if self.B[col] != -1 and col in self.bestCol[user] and len(self.bestCol[user]) > 0:
            
                #if self.numPlaysPhase[user][col] >= self.nm:
                #    self.bestCol[user].remove(col)
                return col
                    

        #max_index = max(range(0,self.numActions), key=lambda col1: self.estR[user][col1])
        #return max_index
            
    
    #Write a file with a matrix
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'GLB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.5f" % i for i in mat[r]])))
        f.close()
    
    
    #Find best Columns
    
    def find_best_cols(self):
        
        take = []
        for col in range(0,self.numActions):
            
            max_index = max(range(0,self.users), key=lambda user: self.ucbs[user][col]) 
            take.append(self.estR[max_index][col])
            
            
        ind = sorted(range(0,len(take)), key=lambda col: take[col], reverse = True)
        
        print take, ind
        
        self.bestCol = [[] for j in range (0,self.users)]
        self.expl = [[] for j in range (0,self.users)]
        
        for user in range(0,self.users):
            
            for  col in range(0,self.rank):
                self.bestCol[user].append(ind[col])
            #self.bestCol[user].append(ind[1])
            
            if self.remArms() > self.rank:
                while True:
                    #print "hh4"
                    index = random.randint(0,self.numActions-1)
                    if index not in self.bestCol[user] and self.B[index]!=-1:
                        self.bestCol[user].append(index)
                    if len(self.bestCol[user]) >= self.explore or len(self.bestCol[user])==self.remArms():
                        break
                
        
        
        for c in range(0,len(self.equiValence)-1):   
            
            take = self.bestCol[self.equiValence[c]]
                    
            for user in range(self.equiValence[c],self.equiValence[c+1]):
                self.bestCol[user] = sorted(take)
                self.expl[user] = sorted(take)
        
        print self.bestCol
    
    def find_best_cols1(self):
        
        take = [0 for i in range(0,self.numActions)]
           
        for user in range(0,self.users):   
            
            max_val = self.MIN
            max_index = -1
            
            for col in range(0,self.numActions):
                
                if col in self.bestCol[user]:
                    
                    if max_val < self.ucbs[user][col]:
                        
                        max_val = self.ucbs[user][col]
                        max_index = col
                    
                    
            #max_index = max(range(0,self.numActions), key=lambda col: self.ucbs[user][col]) 
            take[max_index] += 1
                           
        ind = sorted(range(0,len(take)), key=lambda col: take[col], reverse = True)
        
        print take
        print ind
        print sum(take)
        
        #self.bestCol = [[] for j in range (0,self.users)]
        self.expl = [[] for j in range (0,self.users)]
        
        for user in range(0,self.users):
            
            for  col in range(0,self.rank):
                self.bestCol[user][col] = ind[col]
            #self.bestCol[user].append(ind[1])
            '''
            if self.remArms() > self.rank:
                while True:
                    #print "hh4"
                    index = random.randint(0,self.numActions-1)
                    if index not in self.bestCol[user] and self.B[index]!=-1:
                        self.bestCol[user].append(index)
                    if len(self.bestCol[user]) >= self.explore or len(self.bestCol[user])==self.remArms():
                        break
            '''
        print self.bestCol
        
        
     
    #Eliminate Column   
    
    def colElim(self):
        
        
        for c in range(0,len(self.equiValence)-1):
            
            count_colrow = 0
            while True:
                #print "hh1"
                for col in range(0,self.numActions):
                #Compare against other column max row by row in the same equivalence class
                    #coladd = []
                    
                    count = 0
                    colrow = 0
                    for row in range(self.equiValence[c],self.equiValence[c+1]):  
                        
                        count_colrow = count_colrow + 1
                        if self.B[col]!=-1 and self.numPlays[row][col]!= 0.0:
                            
                            colrow = colrow + 1
                            index = max(range(0,self.numActions), key=lambda col1: self.estR[row][col1])
                            
                            #print self.estR[row][col] + self.upperBound(row, col), self.estR[row][index] - self.upperBound(row, index), row, col, count
                                
                            
                            if self.estR[row][col] + self.upperBound(row, col) < self.estR[row][index] - self.upperBound(row, index):
                            
                                #print self.estR[row][col] + self.upperBound(row, col), self.estR[row][index] - self.upperBound(row, col), row, col, count
                                #print self.estR[row][col], self.max_take[row][col1], count
                                
                                count = count + 1
                                #print self.estR[row][col], self.estR[row][index], row, col, count
                                #print count
            
                    
                    #if count >= self.explore:  
                    if self.B[col]!=-1 and count >= self.rank and self.remArms() > self.rank:     
                        
                        
                        self.B[col] = -1
                        print "remove: "+str(col)+ ". Remaining columns: " + str(self.B)
                        
                                
                        for u in range(0,self.users):
                            self.estR[u][col] = self.MIN
                            self.ucbs[u][col] = self.MIN
                            self.B1[u][col] = -1
                        
                    count = 0   
                    #self.calc_max()
                    count_colrow = 0
                
                if count_colrow >= self.numActions*self.users or self.remArms() >= self.rank:
                    break        
                    #self.Col[col] = self.Col[col] - 1
                    #coladd.append(col)
                        
                
        #self.write_file(self.t, self.max_take, '_MAX_')            
                           
    
    
    def select_Col(self):
        
        #print self.user_nature,self.action
        #print self.user_nature, self.action
        theReward = self.rewards(self.user_nature, self.action)
        self.arm_reward[self.user_nature][self.action] = self.arm_reward[self.user_nature][self.action] + theReward
        self.numPlays[self.user_nature][self.action] += 1
        self.numPlaysPhase[self.user_nature][self.action] += 1
        self.payoffSums[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action] + theReward
         
        self.estR[self.user_nature][self.action] = self.payoffSums[self.user_nature][self.action]/self.numPlays[self.user_nature][self.action]
        self.ucbs[self.user_nature][self.action] = self.estR[self.user_nature][self.action] + self.upperBound(self.user_nature, self.action)
                        
        #self.estR[user][self.action] = theReward
            
        self.cumulativeReward += theReward
        self.bestActionCumulativeReward += theReward if self.action == self.bestAction[self.user_nature] else self.rewards(self.user_nature,self.bestAction[self.user_nature])
        #print self.bestAction[user],self.action
        self.regret = self.bestActionCumulativeReward - self.cumulativeReward
            
        self.actionRegret.append(self.regret)
        self.t = self.t + 1
    
    
    def GLBUCB(self, users, numActions, rank, readfile):

        # Set the environment and initialize

        self.MAX = 99999.0
        self.MIN = -99999.0
        self.numActions = numActions
        self.users = users

        self.rank = rank

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlays = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.numPlaysPhase = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        #self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.estR = [[-0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.ucbs = [[self.MAX for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        self.B = [0 for i in range(0,self.numActions)]
        self.B1 = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        
        #self.max_take = [[self.MIN for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        self.numRounds = 4000000
        
        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]

        #self.Col = [0 for i in range(0,self.numActions)]


        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        # Read the environment
        self.readenv(readfile)
        
        #self.explore = int(1.0*math.ceil(math.sqrt(self.users)))
        #self.explore = 2*self.rank
        
        self.explore = pow(self.rank,3)
        
        print "Explore Factor: " + str(self.explore)
        
        
        self.cumulativeReward = 0
        self.bestActionCumulativeReward = 0
        self.regret = 0

        self.actionRegret = []
        self.t = 0
        
        self.equiValence = []
        sum1 = 0
        for i in range(0,int(self.users/self.rank)+1):
            
            self.equiValence.append(sum1)
            #sum1 = sum1 + int(self.users/self.explore)
            sum1 = sum1 + self.rank
        
        
        
        print "Equivalence class: " + str(self.equiValence)
        
        
        self.countCol = 0
        
        #initialize phase
        self.m = 0
        
        self.psi = (self.numRounds/(self.explore*self.numActions*self.numActions))
        #self.psi = 1.0
        self.epsilon = 1.0
        
        self.M = int(math.floor(0.5 * (math.log((self.numRounds/math.e))/math.log(1+1.0))))
        
        #self.bestCol = [[4,5,6,7] for user in range(0,self.users)]
        
        
        
        #Initialize the best columns randomly
        self.bestCol = [[] for j in range (0,self.users)]
        self.expl = [[] for j in range (0,self.users)]
        
        for user in range(0,self.users):
            
            
            if self.remArms() > self.rank:
                while True:
                    #print "hh4"
                    index = random.randint(0,self.numActions-1)
                    if index not in self.bestCol[user] and self.B[index]!=-1:
                        self.bestCol[user].append(index)
                    if len(self.bestCol[user]) >= self.explore or len(self.bestCol[user])==self.remArms():
                        break
                
        
        
        for c in range(0,len(self.equiValence)-1):   
            
            take = self.bestCol[self.equiValence[c]]
                    
            for user in range(self.equiValence[c],self.equiValence[c+1]):
                self.bestCol[user] = sorted(take)
                self.expl[user] = sorted(take)
        
        print self.bestCol
        
        
        self.nm = int(math.ceil((1.0*math.log(self.psi*self.numRounds*self.epsilon*self.epsilon)/(self.epsilon))))
        #self.nm = int(1.0)
        #self.n0 = 5
        #self.n1 = 5
        #self.Nm = self.users*(len(self.bestCol[0]))*self.nm
        self.Nm = self.users*self.explore*self.nm
        #self.Nm =  self.rank*self.users*self.nm + self.Nmx 
        #self.Nm =  0.0 + self.Nmx 
        print self.Nm, self.nm
        
        while True:

            #User gives row
            
            #print "hh2", str(self.t), str(self.Nm)
            if self.remArms() > self.rank:
                
                
                #Exploit 1st half
                #print "hh"
                if self.t < self.Nm:
                #if self.t < self.Nm:
                    
                    self.user_nature = self.User_Nature()
                    for col1 in range(0,self.numActions):
                        if col1 in self.bestCol[self.user_nature]:
                            self.ucbs[self.user_nature][col1] = self.estR[self.user_nature][col1]+ self.upperBound(self.user_nature, col1)
                    
                    
                    max_val = self.MIN
                    max_index = -1
                    for col in range(0,self.numActions):
                        if col in self.bestCol[self.user_nature]:
                            if max_val < self.ucbs[self.user_nature][col]:
                                max_val = self.ucbs[self.user_nature][col]
                                max_index = col
                    self.action = max_index
                    #self.action = max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col] )
                    self.select_Col()
                
                else:
                    print self.bestCol
                    #self.write_file(self.t, self.estR, '_R_')
                    #self.write_file(self.t, self.numPlays, '_NM_')
                    if self.remArms() > self.rank:
                        self.colElim()
                        self.find_best_cols1()
                    
                    self.epsilon = self.epsilon*0.5
                    
                    self.nm = int(math.ceil((1.0*math.log(self.psi*self.numRounds*self.epsilon*self.epsilon)/(self.epsilon))))
                    #self.nm = int(1.0)
                    #self.Nmx = self.t + self.explore*self.n0*self.remArms()
                    #self.Nm = self.t + self.rank*self.explore*(len(self.equiValence)-1)*self.nm
                    #self.Nmx = self.t + self.users*(len(self.bestCol[0])+1)*self.n0
                    #self.n1 = self.n1 + self.n0
                    self.Nm =  self.t + self.explore*self.users*self.nm 
                    #self.Nm =  self.Nmx + 0.0
                    #print "\n\nPhase: " + str(self.m) + '\t Nmx: ' + str(self.Nmx) + '\t Nm: ' + str(self.Nm)
                    #print "\n\nPhase: " + str(self.m) + '\t Nm: ' + str(self.Nm) + '\t Nmx: ' +str(self.Nmx) + '\t nm: ' +str(self.nm)
                    print "\n\nPhase: " + str(self.m) + '\t Nm: ' + str(self.Nm) + '\t nm: ' +str(self.nm)
                    
                             
                    self.m = self.m + 1
            else:
                
                
                for col1 in range(0,self.numActions):
                    self.ucbs[self.user_nature][col1] = self.estR[self.user_nature][col1]+ self.upperBound(self.user_nature, col1)
                
                self.user_nature = self.User_Nature()
                self.action = max(range(0,self.numActions), key=lambda col: self.ucbs[self.user_nature][col] )
                self.select_Col()
                #print self.action, self.bestAction[user]
            
            

            #print t

            if self.t % 5000 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", best: " + str(self.bestAction[self.user_nature]) , ", regret:", str(self.regret)

            if self.t >= self.numRounds:
                break
        
        #self.write_file(self.t, self.estR, '_R_')
        
        #write regret to file
        f = open('NewExpt/expt13/testRegretGLBUCB0RR2.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return self.cumulativeReward, self.bestActionCumulativeReward, self.regret, self.action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 1024
    action = 16
    rank = 3
    readfile = "env/env1/AP20.txt"

    for turn in range(0,1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank, readfile)
        #if obj.check(bestSet) == False:
            # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(action) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open('NewExpt/expt13/testGLBUCB0RR2.txt', 'a')
        f.writelines("arms: %d\t bArms: %d\t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        


