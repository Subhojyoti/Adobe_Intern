'''
Created on Mar 6, 2018

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

    def User_Nature(self):

        #ROUND ROBIN
        return self.t%self.users

        #UNIFORM SAMPLING
        #return random.randint(0,self.users-1)
    
    def remArms(self):
        count=0
        for i in range(0,self.numActions):
            if self.B[i]!=-1:
                count=count+1
        return count
    
    def remExplore(self):
        count=0
        for i in range(0,self.users):
            for j in range(0,self.numActions):
                
                if self.expl[j]!=-1:
                    if self.estR[i][j] == 0.0:
                        count=count+1
                        break
        return count
    
    def rewards(self, user, choice):
        # Noise Free
        return self.means[user][choice]

        # Noisy
        # return random.gauss(self.means[user][choice],0.25)
        # return sum(numpy.random.binomial(1, self.means[user][choice], 1)) / 1.0

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

    def upperBound(self, numPlays):
        
        return 0.0
        #return math.sqrt(2.0 * math.log(self.numRounds) / (numPlays))
    
    def choose_Col(self,user):
        
        chooseCol = 0
        while True:
            
            if self.remExplore() > 0:
                if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
                    return chooseCol
                #elif self.remArms() <=self.rank:
                #    return self.bestColumns[0]
                else:
                    chooseCol = chooseCol + 1
            else:
                self.write_file(self.t,self.estR,'_R_')
                return 0
                #return chooseCol
            #elif sum(self.B) + sum(self.expl) > -1 * self.numActions:
            #    return 0
            #print "h"
    
    def choose_Col1(self,user):
        
        chooseCol = 0
        while True:
            
            if self.remExplore() > 0:
                chooseCol = random.randint(0,self.numActions-1)
                if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
                    return chooseCol
                #elif self.remArms() <=self.rank:
                #    return self.bestColumns[0]
                #else:
                    #chooseCol = chooseCol + 1
            else:
                self.write_file(self.t,self.estR,'_R_')
                return 0
                #return chooseCol
            #elif sum(self.B) + sum(self.expl) > -1 * self.numActions:
            #    return 0
            #print "h"
    
    def explore_full_Col(self,user):
        
        chooseCol = 0
        while True:
            #chooseCol = random.randint(0,self.numActions - 1)
            #chooseCol = (self.remExplore())%self.numActions
            #if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1 and chooseCol not in self.bestColumns:
            #    return chooseCol 
            #print chooseCol
            #and self.estR[user][chooseCol]==0.0
            if self.B[chooseCol] != -1 and self.expl[chooseCol]!=-1:
                return chooseCol
            elif self.remArms() <=self.rank:
                return self.bestColumns[0]
            else:
                chooseCol = chooseCol + 1
                #return chooseCol
            #elif sum(self.B) + sum(self.expl) > -1 * self.numActions:
            #    return 0
            #print "h"
    
    
    
    def write_file(self,t,mat,name):
        
        f = open('Test/test' + str(name) + 'GLB.txt_'+str(t), 'w')
        for r in range(len(mat)):
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in mat[r]])))
        f.close()
    
    
    def colElim(self):
        
        print self.expl
        self.Col = [0 for i in range(0,self.numActions)]
        for col in range(0,self.numActions):
               
            
            rowbest = 0
            colbest = 0
            
            max_val = self.MIN
            for i in range(0,self.users):
                if self.B[col]!=-1 and self.estR[i][col] > max_val and self.estR[i][col]!= -1.0 and self.estR[i][col]!= 0.0:
                    max_val = self.estR[i][col]
                    rowbest = i
            
            max_val = self.MIN
            for i in range(0,self.numActions):
                if self.B[col]!=-1 and self.estR[rowbest][i] > max_val and self.estR[rowbest][i]!= -1.0 and self.estR[rowbest][i]!= 0.0:
                    max_val = self.estR[rowbest][i] 
                    colbest = i
            
            #rowbest = max(range(0,self.users), key=lambda j: self.estR[j][col])
            #colbest = max(range(0,self.numActions), key=lambda j: self.estR[rowbest][j])
            #print self.t,self.estR[rowbest][col],self.estR[rowbest][colbest]
            
            #best = max(range(0,self.numActions), key=lambda j: self.estR[user][j])
            #for row in range(0,self.users):
            
            #if self.B[col]!=-1 and self.estR[rowbest][col]!=0.0 and self.estR[rowbest][colbest]!=0.0 and self.estR[rowbest][col] > self.estR[rowbest][colbest] and self.estR[rowbest][col]!= self.estR[rowbest][colbest]:                 
            #    self.Col[col] = self.Col[col] + 1
            
            if self.B[col]!=-1 and self.estR[rowbest][col]!=0.0 and self.estR[rowbest][colbest]!=0.0 and self.estR[rowbest][col] < self.estR[rowbest][colbest] and self.estR[rowbest][col]!= self.estR[rowbest][colbest]:
                       
                print self.t,self.estR[rowbest][col],self.estR[rowbest][colbest] 
                self.Col[col] = self.Col[col] - 1
            
            '''
            for b in range(0,self.numActions): 
                    
                if self.estR[rowbest][col]!=0.0 and self.estR[rowbest][b]!=0.0 and self.estR[rowbest][col] > self.estR[rowbest][b]:
                            
                        Col[col] = Col[col] + 1
            '''                
        
        #self.bestColumns = Col
        print self.Col
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        for i in range(0,self.numActions):
            
            if self.Col[i] < 0 and self.B[i]!=-1:
                print "remove: "+str(i)
                self.B[i] = -1
                
                for u in range(0,self.users):
                    self.estR[u][i] = -1.0
    
    #Equivalence class
    
    def get_max_equiV(self,colTake,c):
        
        
        equival = self.MIN
        equicol = 0
        equirow = 0
        
        for row in range(self.take[c],self.take[c+1]):
            for col in range(0,self.numActions):
                
                if self.equiV[row][colTake] == self.equiV[row][col] and self.equiV[row][colTake] == -2 and self.equiV[row][col]==-2 and colTake != col:
                    
                    if self.estR[row][col] > equival:
                        equival = self.estR[row][col]
                        equicol = col
                        equirow = row
                
                
        return equicol,equirow,equival
    
    
    def colElim1(self):
        
        print self.expl
        self.Col = [0 for i in range(0,self.numActions)]
        #c=0
        for col in range(0,self.numActions):
            
            
            for c in range(0,len(self.take)-1):
                
                equicol,equirow,equival = self.get_max_equiV(col, c)
                count = 0
                for row in range(self.take[c],self.take[c+1]):
            
                    #print row,col
                    #if self.B[col]!=-1 and self.estR[row][col]!= -1.0 and self.estR[row][col]!= 0.0 and self.equiV[row][col]== -2:
                        
                    if self.B[col]!=-1 and self.estR[row][col]!= -1.0 and self.estR[row][col]!= 0.0 and self.equiV[row][col]== -2 and self.estR[row][col] < self.estR[equirow][equicol]:
                        print self.estR[row][col], self.estR[equirow][equicol], count
                        #print equicol, equival,equirow, row, col, self.estR[row][col]
                        count = count + 1
            
            
            #c=c+1
            
            
            
                if count >= self.explore:        
                    #print self.t,self.estR[rowbest][col],self.estR[rowbest][colbest] 
                    self.Col[col] = self.Col[col] - 1
            
                         
        
        #self.bestColumns = Col
        print self.Col
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        for i in range(0,self.numActions):
            
            if self.Col[i] < 0 and self.B[i]!=-1:
                print "remove: "+str(i)
                self.B[i] = -1
                
                for u in range(0,self.users):
                    self.estR[u][i] = -1.0
    
    
    
    
    
    def explore_func(self):
        
        self.expl
        count = 0
        for col in range(0,self.numActions):
            
            if self.expl[col] == -1:
                
                count = count + 1
        
        if count >= self.numActions:
            return False
        
        return True                    
                         
    
    def GLBUCB(self, users, numActions, rank):

        # Set the environment

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
        
        self.equiV = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        
        #self.upbs = [0] * self.numActions
        # self.numRounds = 3000000
        self.numRounds = 2000
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]
        self.bestAction = [0 for i in range(0,self.users)]

        self.Col = [0 for i in range(0,self.numActions)]


        self.means = [[0.0 for i in range(0, self.numActions)] for j in range (0,self.users)]

        self.readenv(6)
        #print self.means,self.bestAction

        # t = numActions
        
        #self.explore = self.rank
        self.explore = int(math.ceil(math.sqrt(self.users)))
        print "Explore: " + str(self.explore)
        #self.explore = 1
        
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
        
        self.bestColumns = [0 for i in range(0,self.rank)]
        
        self.take = [0,8,16,24,32,40,48,56,63]
        
        self.countCol = 0
        self.countRow = 0
        
        #print self.estR
        #self.write_file(self.t)
        
        self.action = self.choose_Col(0)
        #self.action = 0
        print self.action
        while True:


            user = self.User_Nature()
            
            if self.remArms() > self.rank:
                #Explore
                
                #if self.explore_func() == True:
                if self.remExplore() > 0:
                    
                    print self.expl, self.countRow
                    if self.countRow < self.explore:
                        #action = self.remArmsRow(user)
                        #action = chooseCol
                        self.countRow = self.countRow + 1
    
                    else:
    
                        #self.colElim(self.countRow,self.countCol)
                        #print self.estR
                        #for col in self.bestColumns:
                        #self.colElim2(self.action)
                        #self.colElim()
                        #self.write_file(self.t)
                        
                        self.expl[self.action] = -1 
                        self.action = self.choose_Col(user)
                        print self.action
                        #self.countCol = self.countCol + 1
                        self.countRow = 1
                        
                    
                else:
                    self.write_file(self.t,self.estR,'_R_')
                    self.colElim1()    
                    self.expl = [0 for i in range(0,self.numActions)]
                    for i in range(0,self.numActions):
                        if self.B[i] == -1:
                            self.expl[i] = -1
                    self.write_file(self.t,self.equiV,'_V_')
                    self.equiV = [[0 for i in range(0, self.numActions)] for j in range (0,self.users)]
                    
                    #self.explore = self.explore + 1
            else:
                
                #Explore best d columns fully
                if self.remExplore() > 0:
                    
                    for col in range(0,self.numActions):
                        if self.expl[col] != -1 and self.estR[user][col]== 0.0:
                            self.action = col
                    
                    #print self.B
                    
                else:
                    #Exploit
                    self.action = max(range(0,self.numActions), key=lambda col: self.estR[user][col])
                    '''
                    max_val = self.MIN
                    for col in range(0,self.numActions):
                        if self.B[col]!=-1 and self.estR[user][col] > max_val:
                            max_val = self.estR[user][col]
                            self.action = col
                    '''
            
            #print user, self.action
            self.equiV[user][self.action] = -2
            theReward = self.rewards(user, self.action)
            #print theReward
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

            if self.t % 10 == 0:
                print "At time: " + str(self.t), ", action: " +str(self.action), ", regret:", str(regret)

            if self.t >= self.numRounds:
                break

        #print self.estR
        
        #self.write_file(self.t)
        
        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        f = open('NewExpt/expt4/testRegretGLBUCB0RR2.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, self.action, self.t


if __name__ == "__main__":

    wrong = 0
    user = 64
    action = 10
    rank = 2

    #turn = 0
    for turn in range(1):
        obj = GLBUCB()
        random.seed(turn + action)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep = obj.GLBUCB(user, action, rank)
        #if obj.check(bestSet) == False:
            # print bestSet
        #    wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\twrong: " + str(wrong) + "\tarms: " + str(action) + "\tbarm: " + str(arm) + "\tReward: " + str(cumulativeReward) + "\tbestCumReward: " + str(bestActionCumulativeReward) + "\tregret: " + str(regret)
        f = open('NewExpt/expt4/testGLBUCB0RR2.txt', 'a')
        f.writelines("arms: %d\tbArms: %d\ttimestep: %d\tregret: %d\tcumulativeReward: %.2f\tbestCumulativeReward: %.2f\n" % (action, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
        #j = j + 1

