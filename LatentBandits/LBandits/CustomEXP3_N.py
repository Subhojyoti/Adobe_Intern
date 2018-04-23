'''
Created on Oct 6, 2015

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput
import sets


class CustomEXP3(object):
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
            
    
    def CustomEXP3(self, users, numActions, readfile, writefile):

        # Set the environment
        self.MAX = 99999.0
        self.numActions = numActions
        self.users = users

        self.payoffSums = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.numPlays = [[1 for i in range(0, self.numActions)] for j in range(0, self.users)]

        self.numRounds = 4000000
        # numRounds = 250000

        self.arm_reward = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.bestAction = [0 for i in range(0, self.users)]

        self.means = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]

        self.bestSet = [0 for i in range(0, self.users)]

        # Read the environment
        self.readenv(readfile)
        
        print self.means, self.bestAction

        self.weights = [[1.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.prob = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]
        self.cumulativeLoss = [[0.0 for i in range(0, self.numActions)] for j in range(0, self.users)]

        cumulativeReward = 0
        bestActionCumulativeReward = 0

        self.actionRegret = []
        self.t = 0

        self.eta = 1.0 / math.sqrt(self.t+1.0)

        while True:

            user = self.User_Nature()

            for i in range(0,self.numActions):
                # self.prob[i]=(1-self.eta)*(self.weights[i]/sum(self.weights))+(self.eta/self.numActions)
                self.eta = 1.0 / math.sqrt(self.t+1.0)
                self.prob[user][i] = math.exp(-1.0 * self.eta * self.cumulativeLoss[user][i])

            sum_prob = sum(self.prob[user])

            for i in range(0, self.numActions):
                self.prob[user][i] = math.exp(-1.0 * self.eta * self.cumulativeLoss[user][i]) / (sum_prob)

            # print sortedProbAction

            num = random.uniform(0, 1)
            cum = 0.0
            sortedProb = list(numpy.sort(self.prob[user]))

            for b in range(0, self.numActions):
                cum = cum + sortedProb[b]
                if num <= cum:

                    for c in range(0, self.numActions):
                        if sortedProb[b] == self.prob[user][c]:
                            action = c
                            break
                    break

            theReward = self.rewards(user,action)
            # print theReward,action

            self.arm_reward[user][action] = self.arm_reward[user][action] + theReward
            self.numPlays[user][action] += 1
            self.payoffSums[user][action] += theReward

            # f1.writelines("ucbs: (%s)" % (', '.join(["%.8f" % ucb for ucb in ucbs])))
            # f1.writelines("\tupbs: (%s)\n" %( ', '.join(["%.8f" % upb for upb in upbs])))

            # yield action, theReward, ucbs

            cumulativeReward += theReward
            bestActionCumulativeReward += theReward if action == self.bestAction[user] else self.rewards(user,self.bestAction[user])

            regret = bestActionCumulativeReward - cumulativeReward

            self.actionRegret.append(regret)



            loss = [0.0] * self.numActions

            for i in range(0,self.numActions):

                if i == action:
                    loss[i] = (1.0 - theReward) / self.prob[user][i]
                    self.cumulativeLoss[user][i] += loss[i]

                # self.weights[i]=self.weights[i]*math.exp(self.eta*loss[i]/self.numActions)

            # print "t: "+str(t) + " action: "+str(action)

            self.t = self.t + 1

            # print t

            if self.t % 1000 == 0:
                print "At time: " + str(self.t), ", action: " +str(action), ", best: " + str(self.bestAction[user]) , ", regret:", str(regret)

            if self.t >= self.numRounds:
                break



        #action = max(range(self.numActions), key=lambda i: self.arm_reward[i])
        # print self.arm_reward

        for user in range(0,self.users):
            self.bestSet[user] = max(range(0,self.numActions), key=lambda i: self.numPlays[user][i])

        f = open(writefile + 'testRegretCustomEXP30RR1.txt', 'a')
        for r in range(len(self.actionRegret)):
            f.write(str(self.actionRegret[r]) + "\n")
        f.close()

        return cumulativeReward, bestActionCumulativeReward, regret, action, self.t, self.bestSet


if __name__ == "__main__":

    wrong = 0
    users = 1024
    actions = 64
    readfile = "env/env1/AP23.txt"
    writefile = "NewExpt/expt16/"
    
    # turn = 0
    for turn in range(0,1):
        obj = CustomEXP3()
        random.seed(turn + actions)
        cumulativeReward, bestActionCumulativeReward, regret, arm, timestep, bestSet = obj.CustomEXP3(users,actions,readfile,writefile)
        if obj.check(bestSet) == False:
            # print bestSet
            wrong = wrong + 1
        print "turn: " + str(turn + 1) + "\t wrong: " + str(wrong) + "\t arms: " + str(actions) + "\t barm: " + str(arm) + "\t Reward: " + str(cumulativeReward) + "\t bestCumReward: " + str(bestActionCumulativeReward) + "\t regret: " + str(regret)
        f = open(writefile + 'testCustomEXP30RR1.txt', 'a')
        f.writelines("arms: %d \t bArms: %d \t timestep: %d\t regret: %d \t cumulativeReward: %.2f \t bestCumulativeReward: %.2f \n" % (actions, arm, timestep, regret, cumulativeReward, bestActionCumulativeReward))
        f.close()

        turn = turn + 1
